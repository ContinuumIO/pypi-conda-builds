from __future__ import print_function
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("package_list", help="List of packages for which" +
                    " recipies will be created")
args = parser.parse_args()

package_names = [package.strip() for package in
                 open(args.package_list, 'r').readlines()]

log_dir = "./logs/"
recipes_dir = "./recipes/"

build_log_file = open(log_dir + 'build_log', 'w')

successes = []
failures = []

for package in package_names:
    msg = "Creating Conda recipe for %s\n" % (package)
    print(msg)
    err = subprocess.call(['conda', 'build', recipes_dir + package],
                          stdout=build_log_file, stderr=build_log_file)
    if err is 0:
        msg = "Succesfully build conda package for %s\n" % (package)
        successes.append(package)
    else:
        msg = "Failed to conda package for %s\n" % (package)
        failures.append(package)
    print(msg)

build_log_file.close()

successful_recipes_file = open(log_dir + 'successful_builds', 'w')
failed_recipes_file = open(log_dir + 'failed_builds', 'w')

successful_recipes_file.write('\n'.join(successes))
failed_recipes_file.write('\n'.join(failures))

successful_recipes_file.close()
failed_recipes_file.close()
