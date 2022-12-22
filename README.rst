===========
NeuroHub
===========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - Documentation
      - |docs|
    * - Code
      - | |made-with-python| |code-style| |imports|
        | |pre-commit| |built-with|
    * - Tests
      - | |github-actions| |code-quality|
    * - Packaging
      - | |version|

.. |docs| image:: https://readthedocs.org/projects/neurohub/badge/?style=flat
    :target: https://neurohub.readthedocs.io
    :alt: Documentation Status

.. |made-with-python| image:: https://img.shields.io/badge/Made%20with%20Python-v3.9-blue.svg?style=flat
    :target: https://www.python.org/
    :alt: Made with Python

.. |code-style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style

.. |imports| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: Imports

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://pre-commit.com/
    :alt: Pre-commit

.. |built-with| image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
    :target: https://github.com/cookiecutter/cookiecutter-django/
    :alt: Built with cookiecutter-django

.. |code-quality| image:: https://app.codacy.com/project/badge/Grade/b31cb38534da448b9833b0ac2e1f4327
    :target: https://www.codacy.com/gh/GalKepler/neurohub/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=GalKepler/neurohub&amp;utm_campaign=Badge_Grade
    :alt: Code quality

.. |github-actions| image:: https://github.com/GalKepler/neurohub/actions/workflows/ci.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/GalKepler/neurohub/actions

.. |version| image:: https://badge.fury.io/py/neurohub.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/neurohub





A python package aimed at making neuroimaging studies easier to analyse.


* Free software: MIT license
* Documentation: https://neurohub.readthedocs.io.


Settings
========

Moved to settings_.

Basic Commands
==============

Setting Up Your Users
---------------------

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

    .. code-block:: shell

        python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
-----------

Running type checks with mypy:

.. code-block:: shell

    mypy neurohub

Test coverage
-------------

To run the tests, check your test coverage, and generate an HTML coverage report:

.. code-block:: shell

    coverage run -m pytest
    coverage html
    open htmlcov/index.html

Running tests with pytest
-------------------------

.. code-block:: shell

    pytest

Live reloading and Sass CSS compilation
---------------------------------------

Moved to `Live reloading and SASS compilation <https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading>`_.

Deployment
==========

The following details how to deploy this application.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html
