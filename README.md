Create automatics conda packages from PyPi

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
