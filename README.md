[![CircleCI](https://circleci.com/gh/alasco-tech/alasco-tools/tree/master.svg?style=svg)](https://circleci.com/gh/alasco-tech/alasco-tools/tree/master)

# alasco-tools
Useful scripts and other Reusuable things

## Scripts

### Clean Up CF
A regular circleci job that deletes all stacks we no longer have branches on
github for.


## Contributing

Thanks for your interest in contributing! There are many ways to get involved; just check any open issues for specific tasks or create your own!

### Checking out
Easiest start is probably to create a virtual environment for the alasco-tools.
(It is assumed that you've python (>3.6) and virtual environments set up on your
computer)

```python
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

    [Install pre-commit](https://pre-commit.com/#install)
    Navigate to the project root and run `pre-commit install`


If you want to set it up manually, install black via `pip install black`.


## License

See the [LICENSE](./LICENSE) file. In short: we use the (MIT)[https://choosealicense.com/licenses/mit/] license.
