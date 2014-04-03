#!/bin/bash
#####                            #####
## Bash file to make Shelfzilla RPM ##
#####                            #####

## Location
SCRIPT_NAME=$0
BASE_DIR="$(dirname $SCRIPT_NAME)"
GIT_DIR=$(readlink -f $BASE_DIR/../..)
SZ_DIR=$GIT_DIR
SPECS_DIR=$SZ_DIR/rpm/spec

## Params
VERSION=$1
REVISION=$2
RPM_DIR=$(rpm --eval '%{_rpmdir}')


sz_create_rpm () {
    if [ -n $1 ];then
         eval "rpmbuild -ba $1 -D \"_gs_version $VERSION\" -D \"_gs_revision $REVISION\" -D \"_gitdir $GIT_DIR\" $2";
    fi
    if [ $? -ne 0 ] 
    then
        echo "Error creating RPM from $1. Error $?"
        echo "Extra data: $2"
        return 1;
    fi; 
}

create_sz () {
    echo "Creating Shelfzilla RPM ..."
    sz_create_rpm $SPECS_DIR/shelfzilla.spec;
    if [ $? -eq 0 ];then
        echo "Shelfzilla RPM created!"
    fi;
}

create_sz
if [ $? -ne 0 ];then
    exit 1
fi