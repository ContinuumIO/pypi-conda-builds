#!/bin/bash
current_dir=`pwd`
    cd recipes
while read line
do
    package_name=$line
    cat ../list_of_recipies | grep -e $package_name -q
    in_recipies=$?
    cat ../list_of_failed_recipies | grep -e $package_name -q
    in_failed_recipies=$?
    if [ $in_recipies == 1 ] && [ $in_failed_recipies == 1 ]; then
        echo "Creating conda recipe for $package_name"
        conda skeleton pypi $package_name
        if [ $? == 0 ]; then
            echo "$package_name" >> ../list_of_recipies
        else
            echo "$package_name" >> ../list_of_failed_recipies
        fi
    else
        echo "Recipe for $package_name has already been created"
    fi
done < $current_dir'/'$1
