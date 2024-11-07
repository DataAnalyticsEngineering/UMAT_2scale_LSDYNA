#!/bin/bash --login

$set_intel_var
cd ${REPO_DIR}/examples/analytical_mat_parameter && ./run_example.sh

cd ${REPO_DIR}/examples/two_scale/homogeneous_single_track && ./run_example.sh

cd ${REPO_DIR}/examples_extra/model_generation && ./gen.sh

cd ${REPO_DIR}/examples_extra/model_generation && ./run_example.sh