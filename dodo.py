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
                autopep8 --in-place --aggressive --aggressive main.py
                autopep8 --in-place --aggressive --aggressive dodo.py
                autopep8 --in-place --aggressive --aggressive settings.py
                """],
            'verbosity': 2,
            }


def task_play():
    """Run game."""
    return {
        'actions': ["python3 main.py"],
    }


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
        'actions': ['git clean -xdf'],
    }
