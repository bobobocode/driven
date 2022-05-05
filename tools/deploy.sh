#!/usr/bin/env sh

# BoBoBo

# Run base current dir.
cur_dir=`pwd`
echo "Run Base Current Dir: $cur_dir"

source_dir=$cur_dir
deploy_to_dir=

while getopts 'd:o:' opts
do
    case $opts in
    o)
        deploy_to_dir=$OPTARG;;
    s)
        source_dir=$OPTARG;;
    esac
done

confirm(){
    read -r -p $1"? [y/n]" input
    case $input in
        [yY][eE][sS]|[yY])
            return 1
            ;;
        [nN][oO]|[nN])
            return 0
            ;;
        *)
            return 0
            ;;
    esac
}


if [ -d ${deploy_to_dir} ]; then
    confirm "Delete:"${deploy_to_dir}
    if [ $? -eq 1 ]; then
        rm -rf ${deploy_to_dir}
    else
        exit 1
    fi
fi

confirm "From:"${source_dir}
if [ $? -eq 0 ]; then
    exit 1
fi

mkdir -p ${deploy_to_dir}
cp -r ${source_dir}/* ${deploy_to_dir}

cd ${deploy_to_dir}
find . -name "test-venv" | xargs rm -rf 
find . -name "__pycache__" | xargs rm -rf
find . -name "unit-test.db" | xargs rm -rf
find . -name "*.swp" | xargs rm -rf
find . -name "*.swo" | xargs rm -rf
find . -name ".DS_Store" | xargs rm -rf
find . -name ".pytest_cache" | xargs rm -rf
cd ${cur_dir}
