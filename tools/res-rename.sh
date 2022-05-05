#!/usr/bin/env sh

# BoBoBo

# Run base current dir.
cur_dir=`pwd`
echo "Run base current dir: $cur_dir"
scrip_dir=$(cd "$(dirname "$0")"; pwd)

rename_strategy_unique=1
target_dir=${cur_dir}
while getopts 'd:u' opts
do
    case $opts in
    d)
        target_dir=$OPTARG;;
    u)
        rename_strategy_unique=1;;
    esac
done

for file in `ls ${target_dir}`
do
    if [ -f ${file} ]; then
        ext_name="${file##*.}"
        new_name=`md5sum ${file} | awk '{print $1}'`
        mv ${file} ${new_name}.${ext_name}
    fi
done
