#!/bin/bash
# http://stackoverflow.com/a/10929511
while read line
do
    package_name=$line
    # Adding space around the number to not to match numbers in the package
    # name. When the download count is converted to number in python script
    # the spaces are automatically stripped off
    downloads=`vanity $package_name --quiet | grep -e " [0-9]* " -o`
    if [$? == 0]; then
        echo "$downloads" >> download_stats
        echo "$package_name was downloaded $downloads times"
    else
        echo $package_name >> non_package
    fi

done < $1

python ./sort_downloads.py $1 download_stats
