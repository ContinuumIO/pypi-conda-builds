import yaml
import shlex
import subprocess


log_dir = "./logs/"
emoji = {True: ":+1:",
         False: ":x:",
         None: ":!!:"}


def compile_main_report():
    packages = yaml.load(open('packages.yaml', 'r'))

    report_lines = ["|package|package availalbe|availability type|",
                    "|-------|:----------------|:-----------------|"]

    for package in packages:
        # We should probably seperate Not tried and tried and failed cases
        report = "|%s|%s|%s|" % (package,
                                 emoji[packages[package]['package_available']],
                                 packages[package]['availability_type'])

        report_lines.append(report)

    # Score
    N = len(packages)
    num_available_packages = sum([1 for package in packages if
                                  packages[package]['package_available']])
    report_lines.append("\nPackages Available: %s/%s" % (num_available_packages, N))

    anaconda = sum([1 for package in packages if
                    packages[package]['availability_type'] == 'anaconda'])
    report_lines.append("\nAnaconda: %s/%s" % (anaconda, N))

    conda_build = sum([1 for package in packages if
                       packages[package]['availability_type'] == 'conda-build'])
    report_lines.append("\nconda build: %s/%s" % (conda_build, N))

    pipbuild = sum([1 for package in packages if
                    packages[package]['availability_type'] == 'pipbuild'])
    report_lines.append("\npipbuild: %s/%s" % (pipbuild, N))

    open("main_report.md", "w").writelines("\n".join(report_lines))
    cmd = "pandoc main_report.md -o main_report.html"
    subprocess.call(shlex.split(cmd))


def compile_recipe_report():
    recipes = yaml.load(open('recipes.yaml', 'r'))

    report_lines = ["|package|recipe available|error type|",
                    "|-------|:---------------|:---------|"]

    for package in recipes:
        # We should probably seperate Not tried and tried and failed cases
        log_file = log_dir + "%s_recipe.log" % package
        report = "|%s|%s|[%s](%s)|" % (package,
                                       emoji[recipes[package]['recipe_available']],
                                       recipes[package]['error_type'],
                                       log_file)

        report_lines.append(report)

    # Score
    N = len(recipes)
    num_available_recipes = sum([1 for package in recipes
                                 if recipes[package]['recipe_available']])
    report_lines.append("\n: %s/%s" % (num_available_recipes, N))

    open("recipe_report.md", "w").writelines("\n".join(report_lines))
    cmd = "pandoc recipe_report.md -o recipe_report.html"
    subprocess.call(shlex.split(cmd))


def compile_build_report():
    build = yaml.load(open('build.yaml', 'r'))

    report_lines = ["|package|build successful|error type|",
                    "|-------|:---------------|:---------|"]

    for package in build:
        # We should probably seperate Not tried and tried and failed cases
        log_file = log_dir + "%s_build.log" % package
        report = "|%s|%s|[%s](%s)|" % (package,
                                       emoji[build[package]['build_successful']],
                                       build[package]['error_type'],
                                       log_file)

        report_lines.append(report)

    # Score
    N = len(build)
    num_available_build = sum([1 for package in build
                               if build[package]['build_successful']])
    report_lines.append("\n: %s/%s" % (num_available_build, N))

    open("build_report.md", "w").writelines("\n".join(report_lines))
    cmd = "pandoc build_report.md -o build_report.html"
    subprocess.call(shlex.split(cmd))


def compile_pipbuild_report():
    pass


def main():
    compile_main_report()
    compile_recipe_report()
    compile_build_report()


if __name__ == "__main__":
    main()
