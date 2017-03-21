from macpath import abspath
__author__ = 'Kazesoushi'

import os
import sys
import re
import subprocess
from parser import PARSER as p 


# ===============================================================================
#       BASIC SYSTEM COMMANDS
# ===============================================================================


def pwd():
    print os.path.abspath(os.curdir)


def cd(path):
    if os.path.isfile(path):
        print "%s is FILE\nGoing in parent dir %s" % (path, os.path.dirname(path))
        path = os.path.dirname(path)
    os.chdir(path)


def mkdir(path):
    if os.path.exists(path):
        print "%s already exists" % path
    else:
        os.makedirs(path)

def grep(pattern, stdin):
    """
    Python version of grep
    :param pattern: the pattern to search for
    :param stdin: the text to search through
    :return: subprocess.Popen.stdout object. Must be called with read() or 
    readlines() method for example (see gg)
    """
    #===========================================================================
    # subprocess.call(('grep', pattern), stdin=stdin)
    #===========================================================================
    g = subprocess.Popen(['grep', pattern],
                         stdin=stdin,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return g.stdout

def gg(pattern):
    """
    :param pattern: the pattern to recursively search for
    :return: output of "git grep pattern"
    """
    gg = subprocess.Popen(['git', 'grep', pattern],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return gg.stdout.readlines()


# ===============================================================================
#       CUSTOM SYSTEM COMMANDS
# ===============================================================================


def get_path(path=None):
    """
    :param path: relative path to file or dir (default is root dir)
    :return: absolute path.
    """
    #path = os.path.abspath(path or os.path.dirname(__file__))
    path = os.path.abspath(path or os.path.dirname(__file__))
    return os.path.join(os.path.dirname(path), path)


def dir_content(path=None):
    """
    :param path: working directory by default
    :return: list of files in path
    """
    return os.listdir(get_path(path))


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

        #         print "FOUND LINE : %s" % line
        # f = open(get_dir(files[0]))
        # for line in f:


# ===============================================================================
#         METHODS FOR INHERITANCE ANALYSIS
# ===============================================================================

def list_file_classes(filepath):
    parents = []
    children = []

    cat = subprocess.Popen(('cat', get_path(filepath)), stdout=subprocess.PIPE)
    for line in grep('class', cat.stdout).readlines():
        pattern = re.compile(r"class (?P<child>.*)\((?P<parent>.*)\)", re.VERBOSE)
        match = pattern.match(line)

        if match:
            child = match.group("child")
            parent = match.group("parent")
            print line
            print "parent : %s" % parent
            parents.append(parent)
            print "child : %s" % child
            children.append(child)
            build_tree(parent, child)
        else:
            pass
            #print "\nFail REGEX : %s" % line

def build_tree(parent, child):
    pass

def list_classes(path=None):
    """
    """
    path = get_path(path)
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if ".py" not in file:
                    continue
                file = os.path.join(root, file)
                print file
                list_file_classes(file)
    elif os.path.isfile(path):
        print file
        list_file_classes(path)

#===============================================================================
#         METHODS FOR CLASS SKELETON
#===============================================================================

def class_skel(filepath):
    cat = subprocess.Popen(('cat', get_path(filepath)), stdout=subprocess.PIPE)
    print grep('class\|def', cat.stdout).read()

# ===============================================================================
#         METHODS FOR IMPORT ANALYSIS
# ===============================================================================


def list_file_imports(dirpath, dict={}, detailed=False):
    """
    Executes a "gg ' import '" in given dirpath
    :param dirpath: The dir to analyze from.
    :param dict: dict to build. Default is empty, use this to add entries to a dict
    :param detailed: True for more details
    :return: { import_statement => [dirpath, dirpath, ...] } dict. Represents all files importing from a same source
    """

    # check path, call git grep
    cd(dirpath)
    text = gg(' import ')

    # PARSE GIT GREP RESULT
    # line = "/dirpath/to/file: from x.y.z import Xyz"
    for line in text:
        splitline = line.split(':')

        filepath = splitline[0]
        impor = splitline[1].rstrip()

        # FORMATTING 
        # detailed=True: "from * import *" STATEMENT
        # detailed=False: "from *" STATEMENT
        if re.match(r"from", impor):
            if detailed:
                impor = re.sub(r"\s*\(\s*$", '', impor)
            else:
                impor = re.sub(r"import.*$", '', impor)

        # Fill object { import => [filepath1, ..., filepathN] }
        if impor in dict:
            if filepath not in dict[impor]:
                dict[impor].add(filepath)
        else:
            dict[impor] = {filepath}

    return dict


def print_proj_dependencies(path):
    # Specific funcs : git grep import & build dict={'import_statement'=>['path', ...]}
    import_dict = list_file_imports(filepath, detailed=False)

    # Print import <=> [module, module, ...]
    print "DIC CONTENT : "
    for key in sorted(import_dict.iterkeys()):
        print "\n%s" % key
        # TODO option -s (short) to skip one-liners
        for filename in sorted(import_dict[key]):
            print "    %s" % filename


#===============================================================================
# METHOD FOR NEW NTFC TESTS
#===============================================================================

def ntfc_test(test_name):
    cmd = "ntfc its dut=vm:router=vm:tnl=vm:tnr=vm %s -d dut=ubuntu-16.04/6wg -V DEBUG -b FAIL -f html" % test_name
    subprocess.call(cmd, shell=True)

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
    print "LAUNCHING MAIN"

#===============================================================================
#     try:
#         filepath = get_path(sys.argv[1])
#     except:
#         filepath = get_path()
# 
#     print "PATH %s" % filepath
# 
#     class_skel(filepath)
#===============================================================================

    try:
        arg = sys.argv[1]
    except:
        arg = None
    list_classes(arg)

    # ntfc_test(test_name)

    #===========================================================================
    # List of all files in chosen tree
    #===========================================================================
    #===========================================================================
    # print " ALL FILES CONSIDERED : "
    # for file in iter_files(filepath):
    #     print "ITER %s" % file
    #===========================================================================

    # Kinda useless in the end...
    # But good basis for smthg smarter
    #===========================================================================
    # print_proj_dependencies(filepath)
    #===========================================================================