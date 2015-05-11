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

recipe_log_file = open(log_dir + 'recipe_log', 'w')

successes = []
failures = []

for package in package_names:
    msg = "Creating Conda recipe for %s\n" % (package)
    recipe_log_file.write(msg)
    print(msg)
    err = subprocess.call(['conda', 'skeleton', 'pypi', package,
                           '--output-dir', recipes_dir],
                          stdout=recipe_log_file, stderr=recipe_log_file)
    if err is 0:
        successes.append(package)
    else:
        failures.append(package)

recipe_log_file.close()

successful_recipes_file = open(log_dir + 'successful_recipes', 'w')
failed_recipes_file = open(log_dir + 'failed_recipes', 'w')

successful_recipes_file.write('\n'.join(successes))
failed_recipes_file.write('\n'.join(failures))

successful_recipes_file.close()
failed_recipes_file.close()
