from __future__ import print_function
import yaml

packages = yaml.load(file('packages.yaml', 'r'))

recipe_score = sum([1 for package in packages if package['recipe'] is True])
build_score = sum([1 for package in packages if package['build'] is True])

n = len(packages)

print("recipe score: %s/%s" % (recipe_score, n))
print("build score: %s/%s" % (build_score, n))
