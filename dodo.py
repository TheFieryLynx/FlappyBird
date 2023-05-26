def task_html_ru():
    """Make HTML RU documentation."""
    return {
        'actions': ["make -C docs/ -e SPHINXOPTS=\"-D language='ru'\" html"],
    }


def task_html_en():
    """Make HTML EN documentation."""
    return {
        'actions': ["make -C docs/ -e SPHINXOPTS=\"-D language='en'\" html"],
    }


def task_check_style():
    """Make codestyle check."""
    return {'actions': ["""
                flake8
                pydocstyle
                """],
            'verbosity': 2,
            }


def task_format():
    """Format all .py files."""
    return {'actions': ["""
                autopep8 --in-place --aggressive FlappyBird/__main__.py
                autopep8 --in-place --aggressive dodo.py
                autopep8 --in-place --aggressive FlappyBird/settings.py
                autopep8 --ignore=E402 --in-place --aggressive tests/*
                """],
            'verbosity': 2,
            }


def task_play():
    """Run game."""
    return {
        'actions': ["python3 FlappyBird/__main__.py"],
    }


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
        'actions': ['git clean -xdf'],
    }


def task_build():
    """Build wheel."""
    return {
        'actions': ['pyproject-build -w'],
    }


def task_tests():
    """Test the app."""
    return {
        'actions': ['coverage run -m unittest discover -s "tests" -v && coverage html'],
        'verbosity': 2
    }
