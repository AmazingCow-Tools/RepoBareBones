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
kApp_Version="0.3.0";
kApp_CopyrightYears="2017";



################################################################################
## Helper Functions                                                           ##
################################################################################
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
Check floss.amazingcow.com for more :)""".format(
        kApp_Version,
        kApp_CopyrightYears
    );

    exit(0);


################################################################################
## Git Functions                                                              ##
################################################################################
def get_project_url(dir_path):
    cwd = os.getcwd();
    os.chdir(dir_path);

    process = subprocess.Popen(
        ["git config --get remote.origin.url", dir_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    );

    name = process.stdout.read().decode("UTF-8")
    name = name.replace("\n", "").replace(".git", "");

    os.chdir(cwd);

    return name;

def get_project_name(dir_path):
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

def get_project_root(dir_path):
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


################################################################################
## File Functions                                                             ##
################################################################################
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

def process_file(src, dst, force, replace_dict):
    if(os.path.exists(dst) and force == False):
        print "({0}) already exists. Refusing to overwrite it...".format(
            os.path.basename(dst)
        );
        return;

    text = read_text_from_file(src);
    for key in replace_dict.keys():
        text = text.replace(key, replace_dict[key]);

    write_text_to_file(dst, text);


################################################################################
## Script                                                                     ##
################################################################################
def run(owner_name, dir_path, project_name = None, force = False):
    if(project_name == None):
        project_name = get_project_name(dir_path);

    project_root     = get_project_root(dir_path);
    clean_owner_name = owner_name.replace(" ", "_").lower();

    print "Repo Name       : ({0})".format(project_name    );
    print "Repo Root       : ({0})".format(project_root    );
    print "Owner Name      : ({0})".format(owner_name      );
    print "Clean Owner Name: ({0})".format(clean_owner_name);
    print "---";

    ## Get all template files and process them.
    for filename in os.listdir(kShare_Dir):
        print "[Processing]: {0}".format(filename);
        ## We are dealing with one of the READMEs
        ## So we need check process it to replace the placeholders
        ## and write on the correct path.
        if(os.path.splitext(filename)[1] == ".md"):
            ## Not the correct readme, just skip...
            if(not clean_owner_name in filename):
                continue;

            replace_dict = { "__PROJECT_NAME__" : project_name };
            process_file(
                os.path.join(kShare_Dir,   "README_{0}.md".format(clean_owner_name)),
                os.path.join(project_root, "README.md"),
                force,
                replace_dict
            );

        ## Docs folder...
        elif(filename == "docs"):
            docs_input  = os.path.join(kShare_Dir,   "docs");
            docs_output = os.path.join(project_root, "docs");

            os.system("mkdir -p {0}".format(docs_output));
            for docs_filename in os.listdir(docs_input):
                print "[Processing]: docs/{0}".format(docs_filename);

                replace_dict = {
                    "__PROJECT_NAME__" : project_name,
                    "__GITHUB_URL__"   : get_project_url(project_root),
                    "__OWNER_NAME__"   : owner_name,
                };
                process_file(
                    os.path.join(docs_input,  docs_filename),
                    os.path.join(docs_output, docs_filename),
                    force,
                    replace_dict
                );


################################################################################
## Entry point                                                                ##
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
