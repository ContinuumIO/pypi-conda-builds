from __future__ import print_function
from os.path import isdir
import argparse
import subprocess
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-r", help="re-attempt failed recipes", action="store_true")
args = parser.parse_args()

packages = yaml.load(file('packages.yaml', 'r'))

log_dir = "./logs/"
recipes_dir = "./recipes/"

recipe_log_file = open(log_dir + 'recipe_log', 'w')

for package in packages:
    msg = "Creating Conda recipe for %s\n" % (package['name'])
    print(msg)
    cond = (package['recipe'] is None or
            (args.r is True and package['recipe'] is False))
    if cond:
        if not isdir(recipes_dir + package['name']):
            # XXX: the normalization of package names comes into way of
            # directory detection
            err = subprocess.call(['conda', 'skeleton', 'pypi',
                                   package['name'],
                                   '--output-dir',
                                   recipes_dir,
                                   '--recursive'],
                                  stdout=recipe_log_file,
                                  stderr=recipe_log_file)
        else:
            err = 0

        if err is 0:
            msg = "Succesfully created conda recipe for %s\n" % (package['name'])
            package['recipe'] = True
        else:
            msg = "Failed to create conda recipe for %s\n" % (package['name'])
            package['recipe'] = False
        print(msg)

open('packages.yaml', 'w').writelines(yaml.dump(packages))
recipe_log_file.close()
