#!/bin/bash --login

# directory of the current script
# https://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo $SCRIPTPATH

source /opt/intel/oneapi/setvars.sh --force

export PYTHONPATH=$SCRIPTPATH/umat:$PYTHONPATH
export PYTHONPATH=$SCRIPTPATH/external_packages:$PYTHONPATH
export PYTHONPATH=$SCRIPTPATH/mixed_languages:$PYTHONPATH

repo_files=repo_files
folder=lsdyna_object_version
folder_ref=lsdyna_object_version_ref

generate_patch() { diff -u $folder_ref/$1 $folder/$1 > $repo_files/$1.patch; }

mode="$1"

if [[ "$mode" == "quick" ]] || [[ "$mode" == "q" ]]; then
  echo "Quick mode"
  rm -rf $folder
  cp -r $folder_ref $folder
elif [[ "$mode" == "debug" ]] || [[ "$mode" == "d" ]]; then
  echo "use edited files"
else
  echo "Normal mode"

  # Install lsprepost
  wget -q https://ftp.lstc.com/anonymous/outgoing/lsprepost/4.9/linux64/lsprepost-4.9.11-common-22Nov2022.tgz -O ${PROJECT_DIR}/lsprepost.tgz 
  tar xf ${PROJECT_DIR}/lsprepost.tgz -C ${PROJECT_DIR}

  rm -rf $folder $folder_ref
  tar xf ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz && mv -f usermat $folder_ref
  cp -rf $folder_ref $folder
fi

# fix file formatting, to install relevant tools: pip install yapf clang-format fprettify
# yapf -i **/**/umat.py
# clang-format -i **/**/*.cpp
# fprettify **/**/umat_elastic_44_14.F90
# fprettify **/**/umat_elastic_43_13.F90

# add new files from the git repo
ln -sf $(pwd)/$repo_files/* $folder
cp $folder/patch_files/* $folder
cd $folder

# apply batches when not debugging
if [[ "$mode" != "debug" ]] && [[ "$mode" != "d" ]]; then    

  # patch files generated with diff -u old new > ***.patch
  # function defined in set_env.sh file

  # call forpy_initialize and forpy_finalize only once
  patch < init_dyn21.f.patch
  patch < dyn21.f.patch

  # compiler options
  patch < Makefile.patch

  # change Fortran comments from `c` to `!` in order to include in .f90 files
  patch < nhisparm.inc.patch
  
  # comment subroutine umat43 & subroutine umat44 
  patch < dyn21umats.f.patch

  # comment subroutine umat43v & subroutine umat44v
  patch < dyn21umatv.f.patch

  # comment subroutine utan43, utan43v, utan44, utan44v
  # also fixes a BUG in dyn21utan -> urtanh -> aux33loc
  patch < dyn21utan.f.patch

  # comment subroutine thumat13 & subroutine thumat14
  patch < dyn21tumat.f.patch
  
  # dae_rve [discontinued]
  # patch < dyn21umat.f.patch

  rm -rf *.patch

  # patch files are generated via:
  # generate_patch Makefile
  # generate_patch dyn21umats.f
  # generate_patch dyn21umatv.f
  # generate_patch dyn21utan.f
  # generate_patch dyn21tumat.f
  # generate_patch nhisparm.inc
  # generate_patch dyn21.f
  # generate_patch init_dyn21.f
  # generate_patch dyn21umat.f
fi

make -B

cd $SCRIPTPATH
chmod -R 777 lsdyna*
chmod -R 777 lsprepost*

# Debugging
# meld lsdyna_object_version_ref lsdyna_object_version

# configure debugging flags
# gdb-oneapi lsdyna_object_version/lsdyna
# run
# i=input.k