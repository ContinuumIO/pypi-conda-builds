import yaml

package_list = yaml.load(file('target_packages.yaml', 'r'))

package_list = [dict([('name', name), ('recipe', None), ('build', None),
                ('requirements', [])])
                for name in package_list]

# TODO: be careful when the file aready exists
open('packages.yaml', 'w').writelines(yaml.dump(package_list))
