#!/usr/bin/env python3
"""Branchless Stack Removal

This module / script deletes AWS stacks that have no corresponding branch on
GitHub anymore. It is expected that AWS stacks have a tag called `branch`.

Example:
    Running this is as simple as:

        $ python3 remove_branchless_stacks.py my-github-repo

    It'll assume the AWS region is `eu-central-1` it can be set via the
    optional CLI parameter `--region`


Attributes:
    _PROTECTED_STACKS (tuple): This iterable of branch-names will never be
    deleted. Change these to branches you'll make sure to keep, e.g. `master`
    or `production`.
"""
from typing import Dict, Set

import argparse
import os

import boto3
import github


_PROTECTED_STACKS = (
    "alasco-app-staging-staging",
    "alasco-app-production-production",
    "alasco-app-production-demo",
)
_PROTECTED_BRANCHES = ("staging", "master", "demo")


def _create_repo_client(repo: str) -> github.Repository.Repository:
    """ Create GitHub client for given repository """
    token = os.getenv("GITHUB_TOKEN")
    client = github.Github(token)
    return client.get_repo(repo)


def _get_cloudformation_stacks(region: str) -> Dict[str, str]:
    """
    Get a Dictionary of Cloudformation stacks (branch -> stackname)

    It is assumed that your AWS credentials are already set up!
    """
    cf_client = boto3.client("cloudformation", region_name=region)
    res_describe_stacks = cf_client.describe_stacks()

    stacks_aws = dict()

    # Collect only stacks which are tagged with a branch
    for stack in res_describe_stacks["Stacks"]:
        for tag in stack["Tags"]:
            if tag["Key"] == "branch":
                stacks_aws[tag["Value"]] = stack["StackName"]
                break

    return stacks_aws


def _clean_s3_bucket(stacks: Set[str], region: str):
    """ Empty S3 buckets, else stack deletes fail """
    cf_client = boto3.client("cloudformation", region_name=region)
    s3_client = boto3.client("s3")

    for stack_name in stacks:
        stack_desc = cf_client.describe_stacks(StackName=stack_name)["Stacks"][0][
            "Outputs"
        ]
        stack_outputs = {item["OutputKey"]: item["OutputValue"] for item in stack_desc}
        s3_bucket_name = stack_outputs["PrivateAssetsBucketDomainName"].replace(
            ".s3.amazonaws.com", ""
        )

        paginator = s3_client.get_paginator("list_object_versions")
        response_iterator = paginator.paginate(Bucket=s3_bucket_name)
        try:
            for response in response_iterator:
                versions = response.get("Versions", [])
                versions.extend(response.get("DeleteMarkers", []))
                for version in versions:
                    s3_client.delete_object(
                        Bucket=s3_bucket_name,
                        Key=version["Key"],
                        VersionId=version["VersionId"],
                    )
        except s3_client.exceptions.NoSuchBucket:
            print(f"Bucket '{s3_bucket_name}' not found, continuing to stack delete.")


def _delete_stacks(stacks: Set[str], region: str):
    cf_client = boto3.client("cloudformation", region_name=region)

    for stack_name in stacks:
        try:
            cf_client.delete_stack(StackName=stack_name)
        except Exception:  # pylint: disable=broad-except
            print(f"Failed to delete stack for branch '{stack_name}':")
            raise


def remove_branchless_stacks(repo: str, region: str):
    """
    Find Cloudformation Stacks without a branch on GitHub and delete those
    """
    stacks = _get_cloudformation_stacks(region)

    repo = _create_repo_client(repo)
    branches = set(branch.name for branch in repo.get_branches())

    stacks_to_delete = set()
    for branch, stack_name in stacks.items():
        if (
            branch in branches
            or branch in _PROTECTED_BRANCHES
            or stack_name in _PROTECTED_STACKS
        ):
            continue
        stacks_to_delete.add(stack_name)

    if not stacks_to_delete:
        print("Found no stacks to be deleted")
        return

    print("Deleting stacks:")
    for stack in stacks_to_delete:
        print("  - {}".format(stack))

    _clean_s3_bucket(stacks_to_delete, region)
    _delete_stacks(stacks_to_delete, region)


def main():
    """ Remove AWS Stacks without an GitHub branch """
    parser = argparse.ArgumentParser(
        description="Remove Cloudformation stacks without branch"
    )
    parser.add_argument("repo", type=str, help="GitHub repo to check")
    parser.add_argument(
        "--region", type=str, help="AWS region name", default="eu-central-1"
    )

    args = parser.parse_args()

    remove_branchless_stacks(args.repo, args.region)


if __name__ == "__main__":
    main()
