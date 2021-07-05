#!/bin/env python3
"""
Scripts that takes a pkg-config library name and convert it to `#pragma cling` related code for loading the 3rd party
library in the C++ Jupyter Notebook

Usage:
/path/to/generate_cling_3rd_party.py libname [--target-dir .]
"""
import subprocess
from typing import List, Tuple

def get_pkg_config_flags(libname: str):
    raw_str = subprocess.check_output("pkg-config --cflags --libs %s"%libname, shell=True, universal_newlines=True)
    return raw_str.replace("\n", "").split(" ")

def split_cling_flags(flags: List[str])->Tuple[List[str], List[str], List[str]]:
    include_paths = list()
    library_paths = list()
    libraries = list()

    for flag in flags:
        if flag.startswith("-I"):
            include_paths.append(flag[2:])
        elif flag.startswith("-L"):
            library_paths.append(flag[2:])
        elif flag.startswith("-l"):
            libraries.append(flag[2:])
        else:
            libraries.append(flag)
    
    return include_paths, library_paths, libraries

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("generate_cling_3rd_party")
    parser.add_argument("libname", help="the name of the library in pkg-config", type=str)
    parser.add_argument("--target-dir", default=".", help="path to save the file", type=str)
    args = parser.parse_args()

    from os import makedirs
    makedirs(args.target_dir, exist_ok=True)

    libname = args.libname
    flags = get_pkg_config_flags(libname)
    include_paths, library_paths, libraries = split_cling_flags(flags)
    filename = "%s/load_%s.h"%(args.target_dir, libname)
    with open(filename, "w") as f:
        f.write("#pragma once\n\n")
        # -I to add_include_path()
        for x in include_paths:
            f.write('#pragma cling add_include_path("%s")\n' % x)
        # -L to add_library_path()
        for x in library_paths:
            f.write('#pragma cling add_library_path("%s")\n' % x)
        # -l & /path/to.so to load()
        for x in libraries:
            f.write('#pragma cling load("%s")\n' % x)


    print("Files written to", filename)