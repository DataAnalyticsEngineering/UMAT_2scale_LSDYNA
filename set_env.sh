#!/usr/bin/env bash

export intel_dir=/opt/intel
source $intel_dir/oneapi/setvars.sh --force

export PYTHONPATH=/home/alameddin/simkom/src_dyna/lsdyna_added_files_ref/umat:$PYTHONPATH
export PYTHONPATH=/home/alameddin/simkom/src_dyna/lsdyna_added_files_ref/external_packages:$PYTHONPATH
export PYTHONPATH=/home/alameddin/simkom/src_dyna/lsdyna_added_files_ref/mixed_languages:$PYTHONPATH

generate_patch() { diff -u lsdyna_object_version_ref/$1 lsdyna_object_version/$1 > lsdyna_added_files_ref/$1.patch; }


# export dyna_folder="/home/alameddin/.dontsync/packages/lsdyna"
# export umatdyna_folder="/home/alameddin/simkom/src_dyna/lsdyna_object_version"
# export PATH=$dyna_folder:$umatdyna_folder:$PATH