#!/bin/bash
current_dir=`pwd`
cd recipes
while read line
do
    package_name=$line
    echo "Building conda recipe for $package_name"
    conda build $package_name
    if [ $? == 0 ]; then
        echo "$package_name" >> ../list_of_builds
    else
        echo "$package_name" >> ../list_of_failed_builds
    fi
done < $current_dir/list_of_recipies
