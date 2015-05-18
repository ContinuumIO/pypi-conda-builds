import argparse
from xmlrpclib import ServerProxy
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int)
parser.add_argument("--package-list",
                    action="store")
args = parser.parse_args()

url = 'https://pypi.python.org/pypi'
client = ServerProxy(url)

if not args.package_list:
    args.package_list = client.list_packages()
else:
    args.package_list = [package.strip() for package in
                         open(args.package_list, 'r').readlines()]

if args.n:
    args.package_list = args.package_list[:args.n]

downloads_dict = dict()
for package in args.package_list:
    versions = client.package_releases(package)
    try:
        latest_version = versions[0]
        downloads = max(client.release_data(package,
                        latest_version)['downloads'].values())
        downloads_dict[package] = downloads
    except:
        downloads_dict[package] = 0

pickle.dump(downloads_dict, open('downloads_dict.pkl', 'w'))
