from __future__ import print_function
from os.path import isdir
import argparse
import subprocess
import yaml
import shlex
from compile_report import compile_report
from conda.install import rm_rf

log_dir = "./logs/"
recipes_dir = "./recipes/"

# anaconda_packages = set(yaml.load(open('anaconda.yaml', 'r')))
# greylist_packages = set(yaml.load(open('greylist.yaml', 'r')))
# packages = yaml.load(open('packages.yaml', 'r'))
# recipes = yaml.load(open('recipes.yaml', 'r'))
# build = yaml.load(open('build.yaml', 'r'))
# pipbuild = yaml.load(open('pipbuild.yaml', 'r'))


def create_recipe(package, recipes):
    log_file_name = log_dir + "%s_recipe.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in recipes.keys():
        recipes[package] = dict()

    msg = "Creating Conda recipe for %s\n" % (package)
    print(msg)

    # Remove the old recipe
    if isdir(recipes_dir + package):
        rm_rf(recipes_dir + package)

    cmd = "conda skeleton pypi %s --output-dir %s" \
        " --recursive --no-prompt --all-extras --noarch-python"
    cmd = cmd % (package, recipes_dir)
    err = subprocess.call(shlex.split(cmd), stdout=log_file,
                          stderr=subprocess.STDOUT)

    if err is 0:
        msg = "Succesfully created conda recipe for %s\n" % (package)
        recipes[package]['recipe_available'] = True
    else:
        msg = "Failed to create conda recipe for %s\n" % (package)
        recipes[package]['recipe_available'] = False
        print(msg)
    log_file.close()


def build_recipe(package, build):
    log_file_name = log_dir + "%s_build.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in build.keys():
        build[package] = dict()

    msg = "Building Conda recipe for %s\n" % (package)
    print(msg)

    cmd = "conda build %s" % (recipes_dir + package)
    err = subprocess.call(shlex.split(cmd), stdout=log_file,
                          stderr=subprocess.STDOUT)

    if err is 0:
        msg = "Succesfully build conda package for %s\n" % (package)
        build[package]['build_successful'] = True
    else:
        msg = "Failed to build conda package for %s\n" % (package)
        build[package]['build_successful'] = False
    print(msg)
    log_file.close()


def pipbuild(package, pipbuild):
    log_file_name = log_dir + "%s_pipbuild.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in pipbuild.keys():
        pipbuild[package] = dict()

    msg = "Creating Conda recipe for %s using pipbuild\n" % (package)
    print(msg)

    cmd = "conda pipbuild %s" % (package)
    err = subprocess.call(shlex.split(cmd), stdout=log_file,
                          stderr=subprocess.STDOUT)

    if err is 0:
        msg = "Succesfully created conda package for %s\n" % (package)
        pipbuild[package]['build_successful'] = True
    else:
        msg = "Failed to create conda package for %s\n" % (package)
        pipbuild[package]['build_successful'] = False
    print(msg)
    log_file.close()


def save_data():
    yaml.dump(recipes, open('recipes.yaml', 'w'))
    yaml.dump(build, open('build.yaml', 'w'))
    yaml.dump(pipbuild, open('pipbuild.yaml', 'w'))


def reorganise_old_format(packages_old, packages, recipes, build):
    for package in packages_old:
        package_available = False
        availablility_type = None
        if package['anaconda']:
            package_available = True
            availablility_type = "Anaconda"
        elif package['build']:
            package_available = True
            availablility_type = "conda-build"

        packages[package['name']] = {'package_available': package_available,
                                     'availablility_type': availablility_type}

        recipes[package['name']] = {'recipe_available': package['recipe']}
        build[package['name']] = {'build_successful': package['build']}

# all_packages = set(packages.keys())
# packages_to_build = all_packages - anaconda_packages - greylist_packages
