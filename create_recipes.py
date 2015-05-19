from __future__ import print_function
import argparse
import subprocess
import yaml

packages = yaml.load(file('packages.yaml', 'r'))

log_dir = "./logs/"
recipes_dir = "./recipes/"

recipe_log_file = open(log_dir + 'recipe_log', 'w')

for package in packages:
    msg = "Creating Conda recipe for %s\n" % (package['name'])
    print(msg)
    if package['recipe'] is None:
        # TODO: log recipes creation for
        err = subprocess.call(['conda', 'skeleton', 'pypi', package['name'],
                              '--output-dir', recipes_dir, '--recursive'],
                              stdout=recipe_log_file, stderr=recipe_log_file)
        if err is 0:
            msg = "Succesfully created conda recipe for %s\n" % (package['name'])
            package['recipe'] = True
        else:
            msg = "Failed to create conda recipe for %s\n" % (package['name'])
            package['recipe'] = False
        print(msg)

open('packages.yaml', 'w').writelines(yaml.dump(packages))
recipe_log_file.close()
