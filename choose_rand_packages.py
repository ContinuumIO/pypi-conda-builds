import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("package_list", help="List of packages you want to " +
                    "choose from")
parser.add_argument("output_file")
parser.add_argument("-n", type=int)
args = parser.parse_args()

packages = [package.strip() for package in
            open(args.package_list, 'r').readlines()]

if args.n > len(packages):
    args.n = len(packages)
output_file = open(args.output_file, 'w')
rand_packages = np.random.choice(packages, args.n, replace=False)
output_file.write('\n'.join(rand_packages))
output_file.close()
