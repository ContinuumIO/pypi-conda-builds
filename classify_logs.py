import re
import yaml

error_types = ["no package found",
               "missing build dependency",
               "invalid syntax",
               "test failure",
               "unclassified"]


def has_missing_test_dependency(log):
    """
    Return: (Status, missing packages)
    """
    None


def no_packages_found(log):
    p = re.compile(r"Error: No packages found")
    return any([re.match(p, line) for line in log])


# def split_build_and_test(log):
#     # XXX: This can be very memory inefficient
#     # Maybe don't even need to split the test and build parts
#
#     try:
#         p = re.compile("TEST START")
#         test_start = [re.match(p, line) is not None for line in log]
#         start_index = test_start.index(True)
#         return log[:start_index], log[start_index:]
#     except ValueError:
#         return log, []


def has_test_failure(log):
    p = re.compile("TESTS FAILED")
    return re.match(p, log[-1]) is not None


def has_missing_build_dependency(log):
    p = re.compile("RuntimeError: Setuptools downloading is disabled")
    return any([re.match(p, line) for line in log])


def has_invalid_syntax(log):
    p = re.compile("SyntaxError: invalid syntax")
    return any([re.match(p, line) for line in log])


def classify_build_log(log_file, package):
    """
    Takes a build log file object as an input and returns
    a tupe `(category, sub-category, sub-category)`

    - missing dependency:
        - Build Dependency
        - Test Dependency
    - Runtime error (other than missing dependency)
    """
    if package['recipe'] is False:
        return "No recipe available"

    log = log_file.readlines()
    if no_packages_found(log):
        return "no package found"

    if has_test_failure(log):
        return "test failure"

    if has_missing_build_dependency(log):
        return "missing build dependency"

    if has_invalid_syntax(log):
        return "invalid syntax"

    return "unclassified"


def classify_all_logs():
    packages = yaml.load(file('packages.yaml', 'r'))
    log_dir = "./logs/"

    for package in packages:
        if package['build'] is False:
            log_file_name = log_dir + "%s_build.log" % (package['name'])
            log_file = open(log_file_name, 'r')
            error_type = classify_build_log(log_file, package)
        else:
            error_type = None
        package['build_error_type'] = error_type

    open('packages.yaml', 'w').writelines(yaml.dump(packages))


if __name__ == "__main__":
    packages = yaml.load(file('packages.yaml', 'r'))
    classify_all_logs()
    package_dict = dict([(package['name'], i) for i, package in enumerate(packages)])
