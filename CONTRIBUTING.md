# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/SSJenny90/django-content-license/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

### Write Documentation

Django Content License could always use more documentation, whether as part of the
official Django Content License docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/SSJenny90/django-content-license/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

>[!Note]
> This package uses Poetry for dependency management and packaging. If you are unfamiliar with Poetry, please see the [Poetry documentation](https://python-poetry.org/docs/) and install the package before continuing.

Ready to contribute? Here's how to set up `django-content-license` for local development.

1. Fork the `django-content-license` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/django-content-license.git

3. Install dev environment using poetry and activate it:

    $ poetry install
    $ poetry shell

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Write tests for any code changes where applicable.

> [!Note]
> This package provides some helpful utility scripts via the `invoke` package that help with code quality and testing. Invoke is installed with the dev dependencies, so you should be able to run the following commands from the root of the project when you are in the virtual environment. To see what commands are available to you, run:

    $ invoke --list

6. When you're done making changes, check that your changes pass all code quality checks.

    $ invoke check

7. Now make sure all tests are passing, including testing other Python versions with tox

    $ invoke test

8. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

9.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. Pull requests that modify functionality should include tests and udpated documentation.
2. Make sure that all tests pass for all supported Python versions.
