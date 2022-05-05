#!/usr/bin/env sh

# BoBoBo

# Run base current dir.
cur_dir=`pwd`
echo "Run Base Current Dir: $cur_dir"

opt_test_target=.
opt_all_new=0
opt_just_env=0
opt_test_require=${cur_dir}/../../test-requirements.txt
opt_environment=${cur_dir}/driven-test-environment

while getopts 'eat:r:' opts
do
    case $opts in
    e)
        opt_just_env=1;;
    a)
        opt_all_new=1;;
    t)
        opt_test_target=$OPTARG;;
    r)
        opt_test_require=$OPTARG;;
    esac
done



if [  -d test-venv ]; then
    if [ ${opt_all_new} -eq 1 ]; then
        rm -rf test-venv
        python3 -m venv test-venv
        cat ${opt_environment} >> ./test-venv/bin/activate
        echo "Set environment."
        . ./test-venv/bin/activate
        pip install -r ${opt_test_require}
        pip install pytest
        echo "Recreate test-venv."
    else
        . ./test-venv/bin/activate
    fi
else
    python3 -m venv test-venv
    cat ${opt_environment} >> ./test-venv/bin/activate
    echo "Set environment."
    . ./test-venv/bin/activate
    pip install -r ${opt_test_require}
    pip install pytest
    echo "Create test-venv."
fi

if [ ${opt_just_env} -eq 0 ]; then
    echo "Starting to run pytest: $target"
    ./test-venv/bin/pytest -s $opt_test_target
fi
