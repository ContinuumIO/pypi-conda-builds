#!/bin/bash
current_dir=`pwd`
cd recipes
while read line
do
    package_name=$line
    echo "Creating conda recipe for $package_name"
    conda skeleton pypi $package_name
    if [ $? == 0 ]; then
        echo "$package_name" >> ../list_of_recipies
    else
        echo "$package_name" >> ../list_of_failed_recipies
    fi
done < $current_dir'/'$1
