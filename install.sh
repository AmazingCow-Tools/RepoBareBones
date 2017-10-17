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
##  File      : install.sh                                                    ##
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
## Vars                                                                       ##
################################################################################
SHARE_PATH="/usr/local/share/amazingcow-repobb";
BIN_PATH="/usr/local/bin";


################################################################################
## Script                                                                     ##
################################################################################

echo "Installing resouces at : ($SHARE_PATH)";
echo "Installing script at   : ($BIN_PATH)";

## Clean up the possible previous installation.
rm    -rf "$SHARE_PATH";
mkdir -p  "$SHARE_PATH";

## Copy everything to the right places.
cp -rf ./resources/*       $SHARE_PATH;
cp -rf ./scripts/repobb.py $BIN_PATH/repobb;

## Make the script executable.
chmod 755 $BIN_PATH/repobb

echo "Done...";
