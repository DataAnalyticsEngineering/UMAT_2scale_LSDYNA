#!/usr/bin/env bash
# tested on Ubuntu 20.04
# run as: 
# chmod +x setup_dyna.sh
# bash /home/alameddin/simkom/src_pyrve/dyna/setup_dyna.sh q

dae_umat_2scale_lsdyna=/home/alameddin/simkom/src_dyna

cd $dae_umat_2scale_lsdyna
source set_env.sh

folder=lsdyna_object_version
folder_ref=lsdyna_object_version_ref

mode="$1"

if [[ "$mode" == "quick" ]] || [[ "$mode" == "q" ]]; then
  echo "Quick mode"
  rm -rf $folder
  cp -r $folder_ref $folder
elif [[ "$mode" == "debug" ]] || [[ "$mode" == "d" ]]; then
  echo "use edited files"
else
  echo "Normal mode"
  rm -rf $folder $folder_ref
  mkdir $folder_ref
  tar -xvf ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz -C $folder_ref
  mv $folder_ref/usermat/* $folder_ref/
  rm -rf $folder_ref/usermat
  cp -r $folder_ref $folder
fi

# fix file formatting, to install relevant tools: pip install yapf clang-format fprettify
yapf -i **/**/umat.py
clang-format -i **/**/*.cpp
fprettify **/**/umat_elastic_44_14.F90
fprettify **/**/umat_elastic_43_13.F90

# add new files from the git repo
ln -sf $(pwd)/lsdyna_added_files_ref/* $folder
cd $folder

# apply batches when not debugging
if [[ "$mode" != "debug" ]] && [[ "$mode" != "d" ]]; then    

  # patch files generated with diff -u old new > ***.patch
  # function defined in .env file

  # compiler options
  patch < Makefile.patch

  # subroutine umat43 & subroutine umat44 
  patch < dyn21umats.f.patch

  # subroutine umat43v & subroutine umat44v
  patch < dyn21umatv.f.patch

  # subroutine utan43 & subroutine utan43v
  # also fixes a BUG in dyn21utan -> urtanh -> aux33loc
  patch < dyn21utan.f.patch

  # subroutine thumat13 & subroutine thumat14
  patch < dyn21tumat.f.patch

  # change Fortran comments from `c` to `!` in order to include in .f90 files
  patch < nhisparm.inc.patch

  # call forpy_initialize and forpy_finalize only once
  patch < dyn21.f.patch
  patch < init_dyn21.f.patch

  # dae_rve
  patch < dyn21umat.f.patch

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

# Debugging
# meld lsdyna_object_version_ref lsdyna_object_version

# configure debugging flags
# gdb-oneapi lsdyna_object_version/lsdyna
# run
# i=input.k
 
