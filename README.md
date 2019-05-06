[![CircleCI](https://circleci.com/gh/alasco-tech/alasco-tools/tree/master.svg?style=svg)](https://circleci.com/gh/alasco-tech/alasco-tools/tree/master)

# alasco-tools
Useful scripts and other Reusuable things

## Scripts

### Clean Up CF
A regular circleci job that deletes all stacks we no longer have branches on
github for.

#### Usage

It's assumed that the AWS credentials are set up in a way that [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) can find
them. For example by setting the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
environment variables. REMINDER: Never share your AWS credentials with anybody!

The [github access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) needs to be set in the environment variable
`GITHUB_TOKEN`.

```bash
remove_branchless_stacks.py $repository
```

#### How it works
The script gets all branches from the given repository and compares them to
stacks on AWS Cloudformation. Those stacks are assumed to have a tag with the
key `branch` which is the relation to the branch name on Github.

All stacks that have no branch (anymore) will be deleted! Attached S3 buckets
will be truncated first - otherwise the stack-deletion fails.


## Contributing

Thanks for your interest in contributing! There are many ways to get involved; just check any open issues for specific tasks or create your own!

### Checking out
Easiest start is probably to create a virtual environment for the alasco-tools.
(It is assumed that you've python (>3.6) and virtual environments set up on your
computer)

```bash
python3 -m venv alasco-tools
mkdir alasco-tools/src/
cd alasco-tools/src/
git@github.com:alasco-tech/alasco-tools.git
```

For each script/tool there should be a single folder, e.g. `clean_up_cf/`. If
specific dependencies are necessary there'll be a `requirements.txt` file that
can easily be installed via `pip install -r requirements.txt`.

To not overwrite your system python dependencies / libraries, make sure to first
activate your virtual environment! `source alasco-tools/bin/activate`

You can find more information on how to use virtual environments all over the
internet and of course the [official python documentation](https://docs.python.org/3/tutorial/venv.html).


### Code Style

We use black as a code formatting tool for Python code to ensure checked in code
is nicely formatted. If your code is not formatted properly, CircleCI will fail to build.

There is a pre-commit hook that invokes black upon every commit. To install the pre commit, do the following:

1. [Install pre-commit](https://pre-commit.com/#install)
2. Navigate to the project root and run `pre-commit install`


If you want to set it up manually, install black via `pip install black`.


## License

See the [LICENSE](./LICENSE) file. In short: we use the [MIT](https://choosealicense.com/licenses/mit/) license.
