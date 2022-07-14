#!/usr/bin/env sh

# BoBoBo


scrip_dir=$(cd "$(dirname "$0")"; pwd)
root_dir=$scrip_dir/../..

create_table_1=${root_dir}/db/sqlite3/schema/topy-desk.sql
db_path=${scrip_dir}/unit-test.db

if [ -f ${db_path} ]; then
    rm -f ${db_path}
fi

while getopts "p:" opts
do
    case $opts in
    p)
        db_path=$OPTARG;;
    esac
done

sqlite3 $db_path < $create_table_1
