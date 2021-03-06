# Contributing to napari

We welcome your contributions! Please see the provided steps below and never hesitate to contact us.

If you are a new user, we recommend checking out the detailed [Github Guides](https://guides.github.com).

## Setting up a development installation

In order to make changes to `napari`, you will need to [fork](https://guides.github.com/activities/forking/#fork) the
[repository](https://github.com/napari/napari).

If you are not familiar with `git`, we recommend reading up on [this guide](https://guides.github.com/introduction/git-handbook/#basic-git).

Clone the forked repository to your local machine and change directories:
```sh
$ git clone https://github.com/your-username/napari.git
$ cd napari
```

Set the `upstream` remote to the base `napari` repository:
```sh
$ git remote add upstream https://github.com/napari/napari.git
```

Install the required dependencies:
```sh
$ pip install -r requirements.txt
```

Make the development version available globally:
```sh
$ pip install -e .
```

We use
[`pre-commit`](https://pre-commit.com) to run [`black`](https://github.com/psf/black) formatting and [`flake8`](https://github.com/PyCQA/flake8) linting automatically prior to each commit.  Please install it in your environment as follows:
```sh
$ pre-commit install
```
Upon committing, your code will be formatted according to our [`black` configuration](../pyproject.toml),
which includes the settings `skip-string-normalization = true` and `max-line-length = 79`.
To learn more, see [`black`'s documentation](https://black.readthedocs.io/en/stable/).

Code will also be linted to enforce the stylistic and logistical rules specified in our [`flake8` configuration](../setup.cfg), which currently ignores [E203](https://lintlyci.github.io/Flake8Rules/rules/E203.html), [E501](https://lintlyci.github.io/Flake8Rules/rules/E501.html), [W503](https://lintlyci.github.io/Flake8Rules/rules/W503.html) and [C901](https://lintlyci.github.io/Flake8Rules/rules/C901.html).  For information on any specific flake8 error code, see the [Flake8 Rules](https://lintlyci.github.io/Flake8Rules/).  You may also wish to refer to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).

If you wish to tell the linter to ignore a specific line use the `# noqa` comment along with the specific error code (e.g. `import sys  # noqa: E402`) but please do not ignore errors lightly.

## Building the icons

Our icon build process starts with a base set of `svg` formatted icons stored in `napari/resources/icons/svg`. If you want to add a new icon to the app, make the icon in whatever program you like and add it to that folder.

Then run the following command

```sh
python -m napari.resources.build_icons
```

This creates separate folders in `napari/resources/icons` with full colored icon sets for each of our themes.

If you want to change one of the existing icons, modify the version in `napari/resources/icons/svg` and run the commands above.

Icons are typically used inside of one of our `stylesheet.qss` files, with the `{{ folder }}` variable used to expand the current theme name.

```css
QtDeleteButton {
   image: url(":/icons/{{ folder }}/delete.svg");
}
```

### Creating and testing themes

A theme is a set of colors used throughout napari.  See, for example, the
builtin themes in `napari/utils/theme.py`.  To make a new theme, create a new
`dict` in `palettes` with the same keys as one of the existing themes, and
replace the values with your new colors.  To test out the theme, use the
`theme_sample.py` file from the command line as follows:

```sh
python -m napari._qt.theme_sample
```
*note*: you may specify a theme with one additional argument on the command line:
```sh
python -m napari._qt.theme_sample dark
```
(providing no arguments will show all themes in `theme.py`)

## Making changes

Create a new feature branch:
```sh
$ git checkout master -b your-branch-name
```

`git` will automatically detect changes to a repository.
You can view them with:
```sh
$ git status
```

Add and commit your changed files:
```sh
$ git add my-file-or-directory
$ git commit -m "my message"
```
## Running Tests

To run our test suite locally, install test requirements and run pytest as follows:

```sh
pip install -r requirements/test.txt
pytest
```

## Writing Tests

Writing tests for new code is a critical part of keeping napari maintainable as
it grows. Tests are written in files whose names
begin with `test_*` and which are contained in one of the `_tests` directories.

There are a couple things to keep in mind when writing a test where a `Qt` event
loop or a `napari.Viewer` is required.  The important thing is that any widgets
you create during testing are cleaned up at the end of each test:

1. If you need a `QApplication` to be running for your test, you can use the
   [`qtbot`](https://pytest-qt.readthedocs.io/en/latest/reference.html#pytestqt.qtbot.QtBot) fixture from `pytest-qt`

    > note: fixtures in pytest can be a little mysterious, since it's not always
    > clear where they are coming from.  In this case, using a pytest-qt fixture
    > looks like this:

    ```python
    # just by putting `qtbot` in the list of arguments
    # pytest-qt will start up an event loop for you
    def test_something(qtbot):
        ...
    ```

   `qtbot` provides a convenient
   [`addWidget`](https://pytest-qt.readthedocs.io/en/latest/reference.html#pytestqt.qtbot.QtBot.addWidget)
   method that will ensure that the widget gets closed at the end of the test.
   It *also* provides a whole bunch of other
   convenient methods for interacting with your GUI tests (clicking, waiting
   signals, etc...).  See the [`qtbot` docs](https://pytest-qt.readthedocs.io/en/latest/reference.html#pytestqt.qtbot.QtBot) for details.

    ```python
    # the qtbot provides convenience methods like addWidget
    def test_something_else(qtbot):
        widget = QWidget()
        qtbot.addWidget(widget)  # tell qtbot to clean this widget later
        ...
    ```

2. When writing a test that requires a `napari.Viewer` object, we provide our
   own convenient fixture called `viewer_factory` that will take care of
   creating a viewer and cleaning up at the end of the test.  When using this
   function, it is **not** necessary to use a `qtbot` fixture, nor should you do
   any additional cleanup (such as using `qtbot.addWidget` or calling
   `viewer.close()`) at the end of the test.  Duplicate cleanup may cause an
   error.  Use the factory as follows:

    ```python
    # the viewer_factory fixture is defined in napari/conftest.py
    def test_something_with_a_viewer(viewer_factory):
        # viewer factory takes any keyword arguments that napari.Viewer() takes
        view, viewer = viewer_factory()
        # note, `view` here is just a pointer to viewer.window.qt_viewer

        # do stuff with the viewer, no qtbot or viewer.close() methods needed.
        ...
    ```

> If you're curious to see the actual `viewer_factory` fixture definition, it's in `napari/conftest.py`

### Help us make sure it's you

Each commit you make must have a [GitHub-registered email](https://github.com/settings/emails)
as the `author`. You can read more [here](https://help.github.com/en/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address).

To set it, use `git config --global user.email your-address@example.com`.

## Keeping your branches up-to-date

Switch to the `master` branch:
```sh
$ git checkout master
```

Fetch changes and update `master`:
```sh
$ git pull upstream master --tags
```

This is shorthand for:
```sh
$ git fetch upstream master --tags
$ git merge upstream/master
```

Update your other branches:
```sh
$ git checkout your-branch-name
$ git merge master
```

## Sharing your changes

Update your remote branch:
```sh
$ git push -u origin your-branch-name
```

You can then make a [pull-request](https://guides.github.com/activities/forking/#making-a-pull-request) to `napari`'s `master` branch.

## Building the docs

From the project root:
```sh
$ make docs
```

The docs will be built at `docs/build/html`.

Most web browsers will allow you to preview HTML pages.
Try entering `file:///absolute/path/to/napari/docs/build/html/index.html` in your address bar.

## Code of conduct

`napari` has a [Code of Conduct](CODE_OF_CONDUCT.md) that should be honored by everyone who participates in the `napari` community.

## Questions, comments, and feedback

If you have questions, comments, suggestions for improvement, or any other inquiries
regarding the project, feel free to open an [issue](https://github.com/napari/napari/issues).

Issues and pull-requests are written in [Markdown](https://guides.github.com/features/mastering-markdown/#what). You can find a comprehensive guide [here](https://guides.github.com/features/mastering-markdown/#syntax).
