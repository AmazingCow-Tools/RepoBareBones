#!/bin/bash
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        update_version.sh                         ##
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

