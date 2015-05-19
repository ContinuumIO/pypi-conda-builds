# Build noarch conda packages from PyPI


## Background:

Conda is a cross platform package manager created by Continuum Analytics. It
was initially created for the needs of python scientific community, later it was
made python agnostic and can be used for general purposes. Python already has a
repository of python packages as PyPI (Python Packaging Index) which can be
installed with the program called “pip”. pip works well if the package is
written purely in python but often, especially scientific packages, uses C and
Fortran in backend and it is hard to install them. The problem is especially
very hard for windows users, though developers generally don’t use windows,
windows is the platform where most of the users reside. Conda essentially solves
the packaging problem by installing binaries in a user’s system.

To create a conda package we need to specify a “recipe” to conda-build. We also
have a tool called conda-skeleton to automatically conda recipes from packages
repositories like PyPI, CPAN, CRAN, the former two are for Perl and R language.


## Problem:

We need to automatically noarch build conda packages from PyPI. System
independent python packages are called noarch packages.

A detailed approach to the problem can be found out at
https://docs.google.com/document/d/1eQ0SqlSyGPjt-82_yE21AbyBItUBpLReFN_w5Vwleu4

I'm also maintain an intern-dairy at https://github.com/hargup/intern-dairy


### Sub Targets


- [ ] Build top 10 packages
- [ ] Build top 20 packages
- [ ] Build top 50 packages
- [ ] Build top 200 packages
- [ ] Build top 1000 packages
- [ ] Build top 5000 packages
- [ ] Build all packages
