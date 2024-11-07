#!/bin/bash --login

$set_intel_var
# Test external packages
cd ${REPO_DIR}/external_packages && echo && ./test_ttb.sh && echo && ./test_forpy.sh && echo && ./test_ezh5.sh

# Test mixed language programming
cd ${REPO_DIR}/mixed_languages && echo && ./test_call_cpp.sh && echo && ./test_call_py.sh
