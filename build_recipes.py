from __future__ import print_function
import argparse
import subprocess
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-r", help="re-attempt failed builds", action="store_true")
args = parser.parse_args()

packages = yaml.load(file('packages.yaml', 'r'))

log_dir = "./logs/"
recipes_dir = "./recipes/"

build_log_file = open(log_dir + 'build_log', 'w')

for package in packages:
    msg = "Creating Conda recipe for %s\n" % (package['name'])
    print(msg)
    if package['build'] is None or args.r is True:
        # TODO: log packages which are built recursively
        err = subprocess.call(['conda', 'build', recipes_dir + package['name']],
                              stdout=build_log_file, stderr=build_log_file)
        if err is 0:
            msg = "Succesfully build conda package for %s\n" % (package['name'])
            package['build'] = True
        else:
            msg = "Failed to conda package for %s\n" % (package['name'])
            package['build'] = False
        print(msg)

open('packages.yaml', 'w').writelines(yaml.dump(packages))
build_log_file.close()
