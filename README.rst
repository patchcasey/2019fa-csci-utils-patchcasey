========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
        |
        | |codeclimate|
    * - package
      - | |commits-since|

.. |travis| image:: https://api.travis-ci.org/csci-e-29/2019fa-csci-utils-patchcasey.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/csci-e-29/2019fa-csci-utils-patchcasey

.. |codeclimate| image:: https://codeclimate.com/github/csci-e-29/2019fa-csci-utils-patchcasey/badges/gpa.svg
   :target: https://codeclimate.com/github/csci-e-29/2019fa-csci-utils-patchcasey
   :alt: CodeClimate Quality Status

.. |commits-since| image:: https://img.shields.io/github/commits-since/csci-e-29/2019fa-csci-utils-patchcasey/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/csci-e-29/2019fa-csci-utils-patchcasey/compare/v0.0.0...master



.. end-badges

Utils problemset

Installation
============

::

    pip install csci-utils

You can also install the in-development version with::

    pip install https://github.com/csci-e-29/2019fa-csci-utils-patchcasey/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import csci_utils
    csci_utils.longest()


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
