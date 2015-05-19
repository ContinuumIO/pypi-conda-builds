from __future__ import print_function
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("package_list", help="List of packages for which" +
                    " recipies will be created")
parser.add_argument("-n", help="Number of packages to build", type=int)
args = parser.parse_args()

package_names = [package.strip() for package in
                 open(args.package_list, 'r').readlines()]

if args.n:
    package_names = package_names[:n]

log_dir = "./logs/"
recipes_dir = "./recipes/"

recipe_log_file = open(log_dir + 'recipe_log', 'w')

successes = []
failures = []

for package in package_names:
    msg = "Creating Conda recipe for %s\n" % (package)
    print(msg)
    err = subprocess.call(['conda', 'skeleton', 'pypi', package,
                           '--output-dir', recipes_dir, '--recursive'],
                          stdout=recipe_log_file, stderr=recipe_log_file)
    if err is 0:
        msg = "Succesfully created conda recipe for %s\n" % (package)
        successes.append(package)
    else:
        msg = "Failed to create conda recipe for %s\n" % (package)
        failures.append(package)
    print(msg)

recipe_log_file.close()

successful_recipes_file = open(log_dir + 'successful_recipes', 'w')
failed_recipes_file = open(log_dir + 'failed_recipes', 'w')

successful_recipes_file.write('\n'.join(successes))
failed_recipes_file.write('\n'.join(failures))

successful_recipes_file.close()
failed_recipes_file.close()
