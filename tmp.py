import sys
import subprocess
import os
import re
from _ast import List
from os import listdir
from os.path import isfile, isdir, join, dirname


#===============================================================================
# ARG : file resulting from "gg ' import ' > tmp_file"
#===============================================================================


# return full path
def get_path(filepath=None):
    filepath = os.path.abspath(filepath or dirname(__file__))
    return os.path.join(dirname(filepath), filepath)


# return list of all files in filepath te
def list_files(filepath, file_list=[]):
    if isfile(filepath):
        filepath = dirname(filepath)
        
    root, root_dir = os.path.split(filepath)
    
    for parent, dirs, files in os.walk(filepath):
        for f in files:
            root, dir = os.path.split(parent)
            file_list.append(os.path.join(root_dir, os.path.join(dir, f)))
    
    return file_list


# return output of "gg ' import '" (exec from filepath)
def list_imports(filepath):
    """
    :param filepath: root dir for the search
    :return: output of "git grep ' import '"
    """
    os.chdir(dirname(filepath))
    gg = subprocess.Popen(['git', 'grep', ' import '],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return gg.stdout.readlines()


# return
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


#===============================================================================


if __name__ == '__main__':
    filepath = get_path(sys.argv[1])
    print filepath

    # ===========================================================================
    # List of all files in chosen tree
    # ===========================================================================
    print " ALL FILES CONSIDERED : "
    for file in list_files(filepath):
        print "%s" % file

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
