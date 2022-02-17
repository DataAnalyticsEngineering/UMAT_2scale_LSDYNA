#!/usr/bin/env bash

current_dir=$(pwd)
parent_dir=$(dirname $(pwd))
ln -sf $current_dir/setup_dyna.sh $parent_dir/setup_dyna.sh
ln -sf $current_dir/set_env.sh $parent_dir/set_env.sh
ln -sf $current_dir/setup_quick.sh $parent_dir/setup_quick.sh
ln -sf $current_dir/setup_full.sh $parent_dir/setup_full.sh
ln -sf $current_dir/setup_debug.sh $parent_dir/setup_debug.sh
