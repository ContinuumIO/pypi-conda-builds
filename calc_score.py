from __future__ import print_function
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("--list-failed-recipes", action="store_true")
parser.add_argument("--list-failed-build", action="store_true")
args = parser.parse_args()

packages = yaml.load(file('packages.yaml', 'r'))

recipe_score = sum([1 for package in packages if package['recipe'] is True])
build_score = sum([1 for package in packages if package['build'] is True])

n = len(packages)

print("recipe score: %s/%s" % (recipe_score, n))
print("build score: %s/%s" % (build_score, n))

if args.list_failed_recipes:
    recipes = [package['name'] for package in packages
               if package['recipe'] is not True]
    print(recipes)

if args.list_failed_recipes:
    recipes = [package['name'] for package in packages if package['build'] is not True]
    print(recipes)
