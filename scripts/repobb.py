#!/usr/bin/python
##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : repobb.py                                                     ##
##  Project   : RepoBareBones                                                 ##
##  Date      : Jun 27, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2017                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

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
kApp_Version="0.2.0";
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

def process_readme(
    owner_name,
    project_name,
    filename,
    src_path,
    dst_path,
    force = False
):
    ## Not the correct readme, just skip...
    if(not owner_name in filename):
        return;

    src_fullpath = os.path.join(src_path, filename);
    dst_fullpath = os.path.join(dst_path, "README.md");

    if(os.path.exists(dst_fullpath) and force == False):
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
repobb [--help | --version] [--n2omatt | --amazingcow] [--force] [project-name]

Options:
  *-h --help     : Show this screen.
  *-v --version  : Show app version and copyright.

  --n2omatt    : Copy the README.md to n2omatt projects.
  --amazingcow : Copy the README.md to Amazing Cow projects. [Default]

  --force : Overwrite previous files.

  project-name : Specify the name of the project. Otherwise repobb will try
                 to get it from the git info.

Notes:
  Options marked with * are exclusive, i.e. the repobb will run that
  and exit after the operation.

  --amazingcow is the default target, with no options are given,
    it will be used to generate the README.md
"""
    exit(exit_code);

def show_version():
    print """repobb - {0} - N2OMatt <n2omatt@amazingcow.com>
Copyright (c) {1} - Amazing Cow
This is a free software (GPLv3) - Share/Hack it
Check opensource.amazingcow.com for more :)""".format(
        kApp_Version,
        kApp_CopyrightYears
    );

    exit(0);


def run(owner_name, dir_path, project_name = None, force = False):
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
                git_repo_root,
                force
            );
        ## Other files, just copy them...
        else:
            src_fullpath = os.path.join(kShare_Dir,    filename);
            dst_fullpath = os.path.join(git_repo_root, filename);

            if(os.path.exists(dst_fullpath) and force == False):
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
            [
                "help", "version",
                "n2omatt", "amazingcow",
                "project-name=", "force"
            ]
        );
    except Exception as e:
        show_error(str(e));

    ## Default vars...
    owner_name   = "AmazingCow Labs";
    project_name = None;
    force        = False;

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
            owner_name="AmazingCow Labs";

        ## Project name
        elif("project-name" in option):
            project_name=argument;

        ## Force
        elif("force" in option):
            force = True;

    ## Run.
    try:
        run(owner_name, ".", project_name, force);
    except Exception as e:
        raise;
        exit(1);


if __name__ == '__main__':
    main()
