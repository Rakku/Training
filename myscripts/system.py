__author__ = 'Kazesoushi'

import os
import sys
import re
import subprocess


# ===============================================================================
#       BASIC SYSTEM COMMANDS
# ===============================================================================


def pwd():
    print os.path.abspath(os.curdir)


def cd(path):
    os.chdir(path)


def create_dir(path):
    os.makedirs(path)


# ===============================================================================
#       CUSTOM SYSTEM COMMANDS
# ===============================================================================


def dir_content(path=None):
    """
    :param path: working directory by default
    :return: list of files in path
    """
    return os.listdir(get_path(path))


def get_path(path=None):
    """
    :param path: relative path
    :return: absolute path (default is current dir)
    """
    path = os.path.abspath(path) or os.path.dirname(__file__)
    return os.path.join(os.path.dirname(path), path)


def iter_files(path, filter=' ', dirs=False, depth=0):
    """
    :param path: root directory for the iteration
    :param filter: exclude files when absolute path contains :param filter:
    :param dirs: Include dirs in result. Default is False
    :param depth: not functional
    :return: all files in :param path: and its subdirectories
    """
    if os.path.isfile(path):
        print "Did you really mean to iter on a single file ?"
    for parent, dirs, files in os.walk(get_path(path)):
        for f in files:
            if filter not in parent:
                yield os.path.join(parent, f)
        # By default, dirs are not returned
        if dirs:
            for d in dirs:
                if filter not in parent:
                    yield os.path.join(parent, d)


# ===============================================================================
#       CANT HANDLE ITER_FILES
# ===============================================================================
# def list_files(filepath, file_list=[]):
#     if os.path.isfile(filepath):
#         filepath = os.path.dirname(filepath)
#
#     root, root_dir = os.path.split(filepath)
#
#     for parent, dirs, files in os.walk(filepath):
#         for f in files:
#             root, dir = os.path.split(parent)
#             file_list.append(os.path.join(root_dir, os.path.join(dir, f)))
#
#     return file_list


def print_tree(path=None):
    """
    :param path: path to print tree from. Default is cur dir
    :return: None. This is a display method
    """
    print "\nTREE FROM : %s ON : %s" % (get_path(), get_path(path))
    for parent, dirs, files in os.walk(get_path(path)):
        print "\nCONTENT OF : %s" % parent
        print "DIRS :"
        for d in dirs:
            print get_path(d)
        print "FILES :"
        for f in files:
            print get_path(f)
        # f = files[0]
        # print files[0]
        # print f
        # # open(f)
        # f_abs = get_path(f)
        # print get_path(f)
        # print f_abs
        # # open(f_abs)


        #     if "=" in line:
        #         print "FOUND LINE : %s" % line
        # f = open(get_dir(files[0]))
        # for line in f:

# ===============================================================================
#       METHODS FOR IMPORT ANALYSIS     -   Try to make it more generic
# ===============================================================================

def list_imports(filepath):
    """
    :param filepath: root dir for the search (must be a git rep)
    :return: output of "git grep ' import '"
    """
    os.chdir(os.path.dirname(filepath))
    gg = subprocess.Popen(['git', 'grep', ' import '],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return gg.stdout.readlines()


def get_dependencies(text, dict={}, detailed=False):
    """
    :param text: text to build dict from. Expected format : PATH:IMPORT_PY
    :param dict: dict to build. Default is empty, use this to add entries to a dict
    :param detailed: True for more details
    :return: { import_statement => [filepath, filepath, ...] } dict. Represents all files importing from a same source
    """
    for line in text:
        # Split : " filepath : from *** import *** "
        splitline = line.split(':')

        filepath = splitline[0]
        impor = splitline[1].rstrip()

        # Parsing import statement
        # If selective (from * import *), drop detailed imports
        if re.match(r"from", impor):
            if detailed:
                impor = re.sub(r"\s*\(\s*$", '', impor)
            else:
                impor = re.sub(r"import.*$", '', impor)

        # Filling object
        if impor in dict:
            if filepath not in dict[impor]:
                dict[impor].add(filepath)   # PKG => filepath not linked yet
        else:
            dict[impor] = {filepath}    # dict[PKG] doesn't exist

    return dict


# ===============================================================================
#       MAIN
# ===============================================================================


if __name__ == 'nope':
    print "ITER"
    for f in iter_files(get_path("..")):
        # if ".idea" in f:
        #     continue
        print f
        if os.path.isfile(f):
            for line in open(f):
                pass
        if os.path.isdir(f):
            print "DIR it is"
    print "LIST"
    # for f in list_files(get_path("../tmp.py")):
    #     print f


if __name__ == '__main__':
    filepath = get_path()
    print "PATH %s" % filepath

    # ===========================================================================
    # List of all files in chosen tree
    # ===========================================================================
    print " ALL FILES CONSIDERED : "
    for file in iter_files(filepath):
        print "ITER %s" % file

    # Specific funcs : git grep import & build dict={'import_statement'=>['path', ...]}
    out = list_imports(filepath)
    dep = get_dependencies(out, detailed=False)

    # Print import <=> [module, module, ...]
    print "DIC CONTENT : "
    for key in sorted(dep.iterkeys()):
        print "\n%s" % key
        # TODO option -s (short) to skip one-liners
        for filename in sorted(dep[key]):
            print "    %s" % filename