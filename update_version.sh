#!/bin/bash
##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : update_version.sh                                             ##
##  Project   : RepoBareBones                                                 ##
##  Date      : Aug 09, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2017                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

################################################################################
## CONFIG                                                                     ##
################################################################################
SRC_FIlE="./scripts/repobb.py";


################################################################################
## Vars                                                                       ##
################################################################################
MAJOR=$(echo $@ | cut -d. -f1);
MINOR=$(echo $@ | cut -d. -f2);
REVISION=$(echo $@ | cut -d. -f3);


################################################################################
## Sanity                                                                     ##
################################################################################
#Thanks to Charles Duffy in SO.
#http://stackoverflow.com/questions/806906/how-do-i-test-if-a-variable-is-a-number-in-bash
re='^[0-9]+$' #Check if is number.

if ! [[ $MAJOR =~ $re ]] ; then
   echo "MAJOR Not a number" >&2;
   exit 1
fi

if ! [[ $MINOR =~ $re ]] ; then
   echo "MINOR Not a number" >&2;
   exit 1
fi

if ! [[ $REVISION =~ $re ]] ; then
   echo "REVISION Not a number" >&2;
   exit 1
fi


################################################################################
## Update the Version Number                                                  ##
################################################################################
cat $SRC_FIlE                                                                    \
  | sed s/kApp_Version=\"*.\.*.\.*.\"/kApp_Version=\"$MAJOR.$MINOR.$REVISION\"/g \
  > $SRC_FIlE.new;


################################################################################
## CHECKING                                                                   ##
################################################################################
## CHECK IF OPERATION WAS OK ##
cat $SRC_FIlE.new;

echo "Is this correct?[y/n]";
read CORRECT;

if [ "$CORRECT" = "y" ]; then
    echo "Updating the files..."
    mv $SRC_FIlE.new  $SRC_FIlE;
else
  rm $SRC_FIlE.new
fi;

