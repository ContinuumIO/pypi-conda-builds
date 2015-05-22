Type of build error
===================

## 1. **missing build dependency**

This occurs when a build dependency has not been stated in `meta.yaml` in the recipes. Example log:
```
Removing old build directory
Removing old work directory
BUILD START: hacking-0.9.6-py27_0
Fetching package metadata: ........
Solving package specifications: .+ /home/hargup/anaconda/envs/_build/bin/python setup.py install
Traceback (most recent call last):
  File "setup.py", line 30, in <module>
.
. <lines removed for brevity>
.
  File "/home/hargup/anaconda/envs/_build/lib/python2.7/site-packages/setuptools-16.0-py2.7.egg/setuptools/package_index.py", line 283, in process_url
RuntimeError: Setuptools downloading is disabled in conda build. Be sure to add all dependencies in the meta.yaml  url=https://pypi.python.org/simple/pbr/r

The following NEW packages will be INSTALLED:

    openssl:    1.0.1k-1    
    pip:        6.1.1-py27_0
.
. <lines removed for brevity>
.
Package: hacking-0.9.6-py27_0
source tree in: /home/hargup/anaconda/conda-bld/work/hacking-0.9.6
Command failed: /bin/bash -x -e /home/hargup/210fs/pypi-conda-builds/recipes/hacking/build.sh
```


## 2. **test failure: missing dependency**

This occurs when a test dependency has not been stated in `meta.yaml` in the recipes. Example log:
```
Removing old build directory
Removing old work directory
BUILD START: django-appconf-1.0.1-py27_0
.
. <lines removed for brevity>
.
BUILD END: django-appconf-1.0.1-py27_0
TEST START: django-appconf-1.0.1-py27_0
Fetching package metadata: ........
Solving package specifications: .===== testing package: django-appconf-1.0.1-py27_0 =====
import: u'appconf'
Traceback (most recent call last):
  File "/home/hargup/anaconda/conda-bld/test-tmp_dir/run_test.py", line 25, in <module>
    import appconf
  File "build/bdist.linux-x86_64/egg/appconf/__init__.py", line 2, in <module>
  File "build/bdist.linux-x86_64/egg/appconf/base.py", line 5, in <module>
ImportError: No module named django.core.exceptions
.
. <lines removed for brevity>
.
TESTS FAILED: django-appconf-1.0.1-py27_0
```

## 3. **No packages found in current linux-64 channels**

Example logs:
```
Removing old build directory
Removing old work directory
BUILD START: paste-2.0.2-py27_0
Fetching package metadata: ........
Error: No packages found in current linux-64 channels matching: flup
```
```
Removing old build directory
Removing old work directory
BUILD START: warlock-1.1.0-py27_0
Fetching package metadata: ........
Error: No packages found in current linux-64 channels matching: jsonpatch >=0.10,<2
```

It might mean that package or one of its dependency is platform dependent and is
not available on `linux-64`. This can also occur when a error occurs in building
one of more dependencies of a package.

**NOTE:** our initial aim is to build no-arch packages, so system dependent
packages are out of scope


## 4. **invalid syntax**

Example log:
```
Removing old build directory
Removing old work directory
BUILD START: astroid-1.3.6-py27_0
.
. <lines removed for brevity>
.
Compiling /home/hargup/anaconda/envs/_build/lib/python2.7/site-packages/astroid/tests/testdata/python3/data/module2.py ...
  File "/home/hargup/anaconda/envs/_build/lib/python2.7/site-packages/astroid/tests/testdata/python3/data/module2.py", line 100
    print('bonjour', file=stream)
                         ^
SyntaxError: invalid syntax
.
. <lines removed for brevity>
.
Command failed: /home/hargup/anaconda/envs/_build/bin/python -Wi /home/hargup/anaconda/envs/_build/lib/python2.7/compileall.py -q -x port_v3 /home/hargup/anaconda/envs/_build/lib/python2.7/site-packages
```

A likely reason: trying to build python 3 package on python 2


## 5. **unclassified**

Either we don't what's wrong or the error is too rare to have a different
category for itself.

A few of the know reasons are:

* Missing non python dependency: swig, lapack etc.
* package trying to write in `/opt` or `/etc`
