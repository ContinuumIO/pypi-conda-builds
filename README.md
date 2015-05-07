Create automatics conda packages from PyPi

**Create List of Packages Sorted with number of Downloads**

* I'm using [Vanity](https://pypi.python.org/pypi/vanity) to get the download
stats from PyPi.
* The list of packages is downloaded from [PyPi Simple Index](https://pypi.python.org/simple/)

```
./sort_packages.sh <list_of_packages>
```
A new list will be created with name `sorted_packages.md` which has packages of
`<list_of_packages>` sorted from most downloaded to least downloaded.

**Create Recipes**

* Add executable permissions to `create_recipes.sh`
```
chmod +x create_recipes.sh
```

* Create Recipes for a list of packages
```
./create_recipes.sh ./small_list.md
```

**Build Recipes**

* Add executable permissions to `build_recipes.sh`
```
chmod +x build_recipes.sh
```

* Build recipes
```
./build_recipes.sh
```
