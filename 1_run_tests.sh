#!/bin/bash --login

$set_intel_var
# Test external packages
cd ${REPO_DIR}/external_packages && ./test_ttb.sh && ./test_forpy.sh && ./test_ezh5.sh

# Test mixed language programming
cd ${REPO_DIR}/mixed_languages && ./test_call_cpp.sh && ./test_call_py.sh
