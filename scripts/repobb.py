#!/usr/bin/python
#coding=utf-8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        repobb.py                                 ##
##            █ █        █ █        RepoBareBones                             ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2017                        ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

################################################################################
## Imports                                                                    ##
################################################################################
import getopt;
import os.path;
import os;
import subprocess
import sys;
import shutil;


################################################################################
## Constants                                                                  ##
################################################################################
kShare_Dir="/usr/local/share/amazingcow-repobb";
kApp_Version="0.1.0";
kApp_CopyrightYears="2017";


################################################################################
## Functions                                                                  ##
################################################################################
## Git Functions
def get_git_repo_name(dir_path):
    cwd = os.getcwd();
    os.chdir(dir_path);

    process = subprocess.Popen(
        ["basename $(git config --get remote.origin.url) .git", dir_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    );

    name = process.stdout.read().decode("UTF-8").replace("\n", "");

    ## We don't find the repo name.
    if(name == u".git" or name == ".git"):
        name = "__PROJECT_NAME__";

    os.chdir(cwd);

    return name;

def get_git_repo_root(dir_path):
    cwd = os.getcwd();
    os.chdir(dir_path);

    process = subprocess.Popen(
        ["git rev-parse --show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    );

    name = process.stdout.read().decode("UTF-8").replace("\n", "");
    os.chdir(cwd);

    return name;


## File Functions
def read_text_from_file(filename):
    f = open(filename);

    all_lines = f.readlines();
    text      = "".join(all_lines);

    f.close();

    return text;

def write_text_to_file(filename, text):
    f = open(filename, mode="w");

    f.write(text);

    f.close();

def process_readme(owner_name, project_name, filename, src_path, dst_path):
    ## Not the correct readme, just skip...
    if(not owner_name in filename):
        return;

    src_fullpath = os.path.join(src_path, filename);
    dst_fullpath = os.path.join(dst_path, "README.md");

    if(os.path.exists(dst_fullpath)):
        print "(README.md) already exists. Refusing to overwrite it...";
        return;

    text          = read_text_from_file(src_fullpath);
    text_replaced = text.replace("__PROJECT_NAME__", project_name);

    write_text_to_file(dst_fullpath, text_replaced);


## Helper Functions
def show_error(*args):
    print("[FATAL] {0}".format(
        "".join(args)
    ));
    exit(1);


def show_help(exit_code):
    print """Usage:
repobb [--help | --version] [--n2omatt | --amazingcow]

Options:
  *-h --help     : Show this screen.
  *-v --version  : Show app version and copyright.

  --n2omatt    : Copy the README.md to n2omatt projects.
  --amazingcow : Copy the README.md to Amazing Cow projects. [Default]

Notes:
  Options marked with * are exclusive, i.e. the repobb will run that
  and exit after the operation.

  --amazingcow is the default target, with no options are given,
    it will be used to generate the README.md
"""
    exit(exit_code);

def show_version():
    print """gosh - {0} - N2OMatt <n2omatt@amazingcow.com>
Copyright (c) {1} - Amazing Cow
This is a free software (GPLv3) - Share/Hack it
Check opensource.amazingcow.com for more :)""".format(
        kApp_Version,
        kApp_CopyrightYears
    );

    exit(0);


def run(owner_name, dir_path, project_name = None):
    if(project_name == None):
        git_repo_name = get_git_repo_name(dir_path);
    else:
        git_repo_name = project_name;

    git_repo_root = get_git_repo_root(dir_path);

    print "Repo Name : ({0})".format(git_repo_name);
    print "Repo Root : ({0})".format(git_repo_root);
    print "Owner Name: ({0})".format(owner_name);

    for filename in os.listdir(kShare_Dir):
        ## We are dealing with one of the READMEs
        ## So we need check process it to replace the placeholders
        ## and write on the correct path.
        if(os.path.splitext(filename)[1] == ".md"):
            process_readme(
                owner_name,
                git_repo_name,
                filename,
                kShare_Dir,
                git_repo_root
            );
        ## Other files, just copy them...
        else:
            src_fullpath = os.path.join(kShare_Dir,    filename);
            dst_fullpath = os.path.join(git_repo_root, filename);

            if(os.path.exists(dst_fullpath)):
                print "({0}) already exists. Refusing to overwrite it...".format(
                    filename
                );
                continue;

            shutil.copyfile(src_fullpath, dst_fullpath);


################################################################################
## Script                                                                     ##
################################################################################
def main():
      ## Init the getopt.
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "",
            ["help", "version", "n2omatt", "amazingcow", "project-name="]
        );
    except Exception as e:
        show_error(str(e));

    ## Default vars...
    owner_name="amazingcow";
    project_name=None;

    ## Parse the given command line options.
    for option, argument in opts:
        ## Help / Version
        if("help" in option):
            show_help(0);
        elif("version" in option):
            show_version();

        ## Owner
        elif("n2omatt" in option):
            owner_name="n2omatt";
        elif("amazingcow" in option):
            owner_name="amazingcow";

        ## Project name
        elif("project-name" in option):
            project_name=argument;

    ## Run.
    try:
        run(owner_name, ".", project_name);
    except Exception as e:
        raise;
        # print(e);
        exit(1);


if __name__ == '__main__':
    main()
