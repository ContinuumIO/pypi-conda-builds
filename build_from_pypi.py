from __future__ import print_function
from os.path import isdir
import argparse
import subprocess
import yaml
import shlex
from conda.install import rm_rf

parser = argparse.ArgumentParser()
parser.add_argument("-n",
                    help="Number of packages",
                    type=int)
parser.add_argument("--start-over",
                    help="Remove all the current information and packages",
                    action="store_true")
parser.add_argument("--recipe",
                    help="Creates recipes for the specified packages",
                    action="store_true")
parser.add_argument("--build",
                    help="Build packages for the available recipes",
                    action="store_true")
parser.add_argument("--pipbuild",
                    help="pipuild packages",
                    action="store_true")
# parser.add_argument("--all",
#                     help="Apply process at all the packages including the ones"
#                          " those passed",
#                     action="store_true")
parser.add_argument("--packages",
                    help="List of names of packags to create",
                    nargs="+",
                    action="store")
args = parser.parse_args()

log_dir = "./logs/"
recipes_dir = "./recipes/"

all_packages = yaml.load(open('sorted_packages.yaml', 'r'))
anaconda_packages = set(yaml.load(open('anaconda.yaml', 'r')))
greylist_packages = set(yaml.load(open('greylist.yaml', 'r')))
packages_data = yaml.load(open('packages_data.yaml', 'r'))
recipes_data = yaml.load(open('recipes_data.yaml', 'r'))
build_data = yaml.load(open('build_data.yaml', 'r'))
pipbuild_data = yaml.load(open('pipbuild_data.yaml', 'r'))


def create_recipe(package, recipes_data):
    log_file_name = log_dir + "%s_recipe.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in recipes_data.keys():
        recipes_data[package] = dict()

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
        recipes_data[package]['recipe_available'] = True
    else:
        msg = "Failed to create conda recipe for %s\n" % (package)
        recipes_data[package]['recipe_available'] = False
        print(msg)
    log_file.close()


def build_recipe(package, build_data, packages_data):
    log_file_name = log_dir + "%s_build_data.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in build_data.keys():
        build_data[package] = dict()

    msg = "Building Conda recipe for %s\n" % (package)
    print(msg)

    cmd = "conda build_data %s" % (recipes_dir + package)
    err = subprocess.call(shlex.split(cmd), stdout=log_file,
                          stderr=subprocess.STDOUT)

    if err is 0:
        msg = "Succesfully build_data conda package for %s\n" % (package)
        build_data[package]['build_successful'] = True
    else:
        msg = "Failed to build_data conda package for %s\n" % (package)
        build_data[package]['build_successful'] = False
        packages_data[package]['package_available'] = True
        packages_data[package]['availability_type'] = 'conda-build'
    print(msg)
    log_file.close()


def pipbuild(package, pipbuild_data, packages_data):
    log_file_name = log_dir + "%s_pipbuild_data.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in pipbuild_data.keys():
        pipbuild_data[package] = dict()

    msg = "Creating Conda recipe for %s using pipbuild_data\n" % (package)
    print(msg)

    cmd = "conda pipbuild_data %s" % (package)
    err = subprocess.call(shlex.split(cmd), stdout=log_file,
                          stderr=subprocess.STDOUT)

    if err is 0:
        msg = "Succesfully created conda package for %s\n" % (package)
        pipbuild_data[package]['build_successful'] = True
    else:
        msg = "Failed to create conda package for %s\n" % (package)
        pipbuild_data[package]['build_successful'] = False
        packages_data[package]['package_available'] = True
        packages_data[package]['availability_type'] = 'pipbuild'
    print(msg)
    log_file.close()


def save_data():
    yaml.dump(packages_data, open('packages_data.yaml', 'w'))
    yaml.dump(recipes_data, open('recipes_data.yaml', 'w'))
    yaml.dump(build_data, open('build_data.yaml', 'w'))
    yaml.dump(pipbuild_data, open('pipbuild_data.yaml', 'w'))


def clean_data():
    unclean_pkgs = [pkg for pkg in recipes_data
                    if recipes_data[pkg]['recipe_available'] is None]
    for pkg in unclean_pkgs:
        recipes_data.pop(pkg)

    unclean_pkgs = [pkg for pkg in build_data
                    if build_data[pkg]['build_data_successful'] is None]
    for pkg in unclean_pkgs:
        build_data.pop(pkg)

    # for pkg in pipbuild:
    #     if pipbuild[pkg]['pipbuild_successful'] is None:
    #         pipbuild.pop(pkg)

    save_data()


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


def main(args):
    if args.n:
        new_packages = set(all_packages[:args.n])
        old_failed = set(pkg for pkg in packages_data if
                         packages_data[pkg]['package_available'] is not True)
        candidate_packages = new_packages.union(old_failed) \
            - (anaconda_packages.union(greylist_packages))

    # TODO: complete the part where list of packages is passed through
    # commandline
    for pkg in candidate_packages:
        if packages_data.has_key(pkg):
            packages_data[pkg] = dict()
        packages_data[pkg]['package_available'] = False
        packages_data[pkg]['availability_type'] = None

        if args.recipe:
            create_recipe(pkg, recipes_data)

        if args.build:
            build_recipe(pkg, build_data, packages_data)

        if args.pipbuild:
            if packages_data[pkg]['package_available']:
                print("Package already available through conda-build")
            else:
                pipbuild(pkg, pipbuild_data, packages_data)

    save_data()

main(args)
