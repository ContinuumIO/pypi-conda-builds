"""
Automatically builds conda packages from pypi.
"""
from __future__ import print_function
from os.path import isdir
import argparse
import subprocess
import yaml
import shlex

parser = argparse.ArgumentParser()
parser.add_argument("--init",
                    help="Initialize packages.yaml",
                    action="store_true")
parser.add_argument("-n",
                    help="Number of packages (only works with --init)",
                    type=int)
parser.add_argument("--anaconda",
                    help="Build pacakges included in Anaconda")
parser.add_argument("--commit-and-push",
                    help="Commit the reports and logs and push to gh-pages",
                    action="store_true")
args = parser.parse_args()


def init_packages_yaml(n):
    sorted_file = open('sorted_packages', 'r')
    package_list = [package.strip() for package in sorted_file.readlines()][:n]

    anaconda = set([package.strip() for package in
                    open('anaconda', 'r').readlines()])

    package_list = [dict([('name', name), ('recipe', None), ('build', None),
                    ('requirements', []), ('anaconda', name.lower() in anaconda)])
                    for name in package_list]

    open('packages.yaml', 'w').writelines(yaml.dump(package_list))


def create_recipe(package):
    log_file_name = log_dir + "%s_recipe.log" % (package['name'])
    log_file = open(log_file_name, 'w')

    msg = "Creating Conda recipe for %s\n" % (package['name'])
    print(msg)

    err = 0
    cond = package['recipe'] is None and package['anaconda'] is False
    if cond:
        if not isdir(recipes_dir + package['name']):
            # XXX: the normalization of package names comes into way of
            # directory detection
            cmd = "conda skeleton pypi %s --output-dir %s --recursive"
            cmd = cmd % (package['name'], recipes_dir)
            err = subprocess.call(shlex.split(cmd), stdout=log_file,
                                  stderr=subprocess.STDOUT)
        else:
            err = 0

    if err is 0:
        msg = "Succesfully created conda recipe for %s\n" % (package['name'])
        package['recipe'] = True
    else:
        msg = "Failed to create conda recipe for %s\n" % (package['name'])
        package['recipe'] = False
        print(msg)
    log_file.close()

    return package['recipe'], log_file_name


def build_recipe(package):
    log_file_name = log_dir + "%s_build.log" % (package['name'])
    log_file = open(log_file_name, 'w')

    msg = "Building Conda recipe for %s\n" % (package['name'])
    print(msg)

    err = 0
    if package['build'] is None and package['anaconda'] is False:
        cmd = "conda build %s" % (recipes_dir + package['name'])
        err = subprocess.call(shlex.split(cmd), stdout=log_file,
                              stderr=subprocess.STDOUT)

    if err is 0:
        msg = "Succesfully build conda package for %s\n" % (package['name'])
        package['build'] = True
    else:
        msg = "Failed to build conda package for %s\n" % (package['name'])
        package['build'] = False
    print(msg)
    log_file.close()

    return package['build'], log_file_name


def compile_report():
    report_lines = ["|package|recipe|build|anaconda|",
                    "|-------|:-----|:----|:-------|"]

    for package in packages:
        recipe_log = log_dir + "%s_recipe.log" % (package['name'])
        build_log = log_dir + "%s_build.log" % (package['name'])
        report = "|%s|[%s](%s)|[%s](%s)|%s" % (package['name'], package['recipe'],
                                               recipe_log, package['build'],
                                               build_log, package['anaconda'])

        report_lines.append(report)

    # Add score
    recipe_score = sum([1 for package in packages if package['recipe'] is True])
    build_score = sum([1 for package in packages if package['build'] is True])

    n = len(packages)

    report_lines.append("\nrecipe score: %s/%s\n" % (recipe_score, n))
    report_lines.append("\nbuild score: %s/%s\n" % (build_score, n))

    # Write to file and convert to html
    open("report.md", "w").writelines("\n".join(report_lines))
    cmd = "pandoc report.md -o report.html"
    subprocess.call(shlex.split(cmd))


def commit_and_push():
    cmd1 = "git checkout gh-pages"
    cmd2 = "git add --all logs"
    cmd3 = "git add report.md report.html"
    cmd4 = "git commit -m \"Auto commit\""
    cmd5 = "git push origin gh-pages -f"
    cmd6 = "git checkout master"

    subprocess.call(shlex.split(cmd1))
    subprocess.call(shlex.split(cmd2))
    subprocess.call(shlex.split(cmd3))
    subprocess.call(shlex.split(cmd4))
    subprocess.call(shlex.split(cmd5))
    subprocess.call(shlex.split(cmd6))


if args.init:
    init_packages_yaml(args.n)

packages = yaml.load(file('packages.yaml', 'r'))
log_dir = "./logs/"
recipes_dir = "./recipes/"

for package in packages:
    create_recipe(package)
    build_recipe(package)
open('packages.yaml', 'w').writelines(yaml.dump(packages))

compile_report()

if args.commit_and_push:
    commit_and_push()
