from __future__ import print_function
from os.path import isdir
import argparse
import subprocess
import yaml
import shlex
import sys
if sys.version_info < (3,):
    from xmlrpclib import ServerProxy, Transport, ProtocolError
else:
    from xmlrpc.client import ServerProxy


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
parser.add_argument("--packages",
                    help="List of names of packags to create",
                    nargs="+",
                    action="store")
parser.add_argument("--all",
                    help="Apply process at all the packages including the ones"
                         " those passed in earlier builds",
                    action="store_true")
args = parser.parse_args()


def create_recipe(package, recipes_data):
    log_file_name = log_dir + "%s_recipe.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in recipes_data.keys():
        recipes_data[package] = dict()

    msg = "Creating Conda recipe for %s\n" % (package)
    print(msg)

    # Remove the old recipe
    if not isdir(recipes_dir + package):
        cmd = "conda skeleton pypi %s --output-dir %s" \
            " --recursive --no-prompt --all-extras --noarch-python"
        cmd = cmd % (package, recipes_dir)
        err = subprocess.call(shlex.split(cmd), stdout=log_file,
                              stderr=subprocess.STDOUT)
    else:
        err = 0
        print("Recipe already available")

    if err is 0:
        msg = "Succesfully created conda recipe for %s\n" % (package)
        recipes_data[package]['recipe_available'] = True
    else:
        msg = "Failed to create conda recipe for %s\n" % (package)
        recipes_data[package]['recipe_available'] = False
        print(msg)
    log_file.close()


def build_recipe(package, build_data, packages_data):
    log_file_name = log_dir + "%s_build.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in build_data.keys():
        build_data[package] = dict()

    msg = "Building Conda recipe for %s\n" % (package)
    print(msg)

    cmd = "conda build %s" % (recipes_dir + package)
    err = subprocess.call(shlex.split(cmd), stdout=log_file,
                          stderr=subprocess.STDOUT)

    if err is 0:
        msg = "Succesfully build conda package for %s\n" % (package)
        build_data[package]['build_successful'] = True
    else:
        msg = "Failed to build conda package for %s\n" % (package)
        build_data[package]['build_successful'] = False
        packages_data[package]['package_available'] = True
        packages_data[package]['availability_type'] = 'conda-build'
    print(msg)
    log_file.close()


def pipbuild(package, pipbuild_data, packages_data):
    log_file_name = log_dir + "%s_pipbuild.log" % (package)
    log_file = open(log_file_name, 'w')

    if package not in pipbuild_data.keys():
        pipbuild_data[package] = dict()

    msg = "Creating Conda recipe for %s using pipbuild\n" % (package)
    print(msg)

    cmd = "conda pipbuild %s --noarch-python" % (package)
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


pypi_url = 'http://pypi.python.org/pypi'
client = ServerProxy(pypi_url)

log_dir = "./logs/"
recipes_dir = "./recipes/"

all_packages = yaml.load(open('sorted_packages.yaml', 'r'))
anaconda_packages = set(yaml.load(open('anaconda.yaml', 'r')))
greylist_packages = set(yaml.load(open('greylist.yaml', 'r')))
packages_data = yaml.load(open('packages_data.yaml', 'r'))
recipes_data = yaml.load(open('recipes_data.yaml', 'r'))
build_data = yaml.load(open('build_data.yaml', 'r'))
pipbuild_data = yaml.load(open('pipbuild_data.yaml', 'r'))


def get_packages_list(n):
    """
    Gives the list of top n packages sorted by download count
    """
    return [pkg for (pkg, downloads) in client.top_packages(n)]


def get_previous_build_timestamp():
    """
    Return the time of previous build in second since Epoch[1]. Returns 0 if
    timestamp file is not available

    [1]: https://en.wikipedia.org/wiki/Unix_time

    """
    file_name = 'timestamp'
    try:
        timestamp = int(open(file_name, 'r').readline().strip())
    except FileNotFoundError:
        timestamp = 0

    return timestamp


def save_timestamp():
    """
    Save the current timestamp to file 'timestamp'
    """
    import time
    file_name = 'timestamp'
    with open(file_name, 'w') as timestamp_file:
        timestamp_file.write(int(time.time))


def main(args):
    save_timestamp()

    if args.n:
        top_n_packages = set(get_packages_list(args.n))
    else:
        top_n_packages = set()

    if args.all:
        old_pkgs = packages_data.keys()
    else:
        changed_pkgs = set(client.changed_package(get_previous_build_timestamp()))
        # Include old failed or changed packages
        old_pkgs = set(pkg for pkg in packages_data if
                       packages_data[pkg]['package_available'] is not True or
                       pkg in changed_pkgs)

    candidate_packages = top_n_packages.union(old_pkgs) \
        - (anaconda_packages.union(greylist_packages))



    # TODO: complete the part where list of packages is passed through
    # commandline
    for pkg in candidate_packages:
        if pkg not in packages_data.keys():
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
