import yaml
import shlex
import subprocess
from classify_logs import classify_all_logs, error_types

log_dir = "./logs/"
recipes_dir = "./recipes/"


def compile_report():
    # Calculate classes
    classify_all_logs()

    packages = yaml.load(file('packages.yaml', 'r'))

    report_lines = ["|package|recipe|build|anaconda|build error type|",
                    "|-------|:-----|:----|:-------|:---------------|"]

    for package in packages:
        recipe_log = log_dir + "%s_recipe.log" % (package['name'])
        build_log = log_dir + "%s_build.log" % (package['name'])
        report = "|%s|[%s](%s)|[%s](%s)|%s|%s|" % (package['name'],
                                               package['recipe'],
                                               recipe_log,
                                               package['build'],
                                               build_log,
                                               package['anaconda'],
                                               package['build_error_type'])

        report_lines.append(report)

    # Add score
    recipe_score = sum([1 for package in packages if package['recipe'] is True])
    build_score = sum([1 for package in packages if package['build'] is True])

    n = len(packages)

    report_lines.append("\nrecipe score: %s/%s\n" % (recipe_score, n))
    report_lines.append("\nbuild score: %s/%s\n" % (build_score, n))

    report_lines.append("\n* * *\n")

    num_failed_builds = n - build_score
    for error in error_types:
        num_error = sum([1 for package in packages if
                         package['build_error_type'] == error])
        report_lines.append("\n%s: %s/%s\n" % (error, num_error, num_failed_builds))

    report_lines.append("\n* * *\n")

    # Write to file and convert to html
    open("report.md", "w").writelines("\n".join(report_lines))
    cmd = "pandoc report.md -o report.html"
    subprocess.call(shlex.split(cmd))


if __name__ == "__main__":
    compile_report()
