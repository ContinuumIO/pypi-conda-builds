import sys
packages = [package for package in
            open(sys.argv[1]).readlines()]
downloads = [int(download.replace('\n', '')) for download in
             open(sys.argv[2]).readlines()]

packages.sort(key=dict(zip(packages, downloads)).get, reverse=True)

write_file = open('sorted_packages.md', 'w')
write_file.writelines(packages)
write_file.close()
