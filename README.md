# CPP + ROS + Jupyter Notebook

This is the accompanying code for my blog post: https://medium.com/@ardiya

# Usage
Generate Cling 3rd party library:
```
python3 generate_cling_3rd_party.py libname [--target-dir .]
```

Generate Cling boost library from Git:
```
git clone https://github.com/boostorg/boost.git && cd boost
git checkout boost-1.71.0 # Boost in Ubuntu 20.04
submodule update --init --recursive
python3 generate_cling_boost.py /path/to/boost_from_git [--target-dir .]
```
