import re
import yaml

error_types = ["no package found",
               "unclassified"]


def classify_build_log(log_file):
    """
    Takes a build log file object as an input and returns
    a tupe `(category, sub-category, sub-category)`

    - missing dependency:
        - Build Dependency
        - Test Dependency
    - Runtime error (other than missing dependency)
    """
    log = log_file.readlines()
    if no_packages_found(log):
        return "no package found"
    if has_missing_test_dependency(log):
        return "missing test dependency"

    return "unclassified"
    pass


def has_missing_test_dependency(log):
    """
    Return: (Status, missing packages)
    """
    None


def no_packages_found(log):
    p = re.compile(r"Error: No packages found")
    return any([re.match(p, line) for line in log])


def classify_all_logs():
    packages = yaml.load(file('packages.yaml', 'r'))
    log_dir = "./logs/"

    for package in packages:
        if package['build'] is False:
            log_file_name = log_dir + "%s_build.log" % (package['name'])
            log_file = open(log_file_name, 'r')
            error_type = classify_build_log(log_file)
        else:
            error_type = None
        package['build_error_type'] = error_type
    open('packages.yaml', 'w').writelines(yaml.dump(packages))


if __name__ == "__main__":
    classify_all_logs()
