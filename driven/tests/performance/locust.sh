#!/usr/bin/env sh

# BoBoBo

cur_dir=`pwd`
scrip_dir=$(cd "$(dirname "$0")"; pwd)

request_url_file=
while getopts 'u:' opts
do
    case $opts in
    u)
        request_url_file=$OPTARG;;
    esac
done

if [ ${request_url_file} != '' ]; then
    pip3 install locust
    pip3 install pyyaml
    echo 'parse host of '${request_url_file}
    export LOCUST_REQUEST_FILE=${request_url_file}
    host_line=$(head -n 1 ${request_url_file})
    echo 'request host: '${host_line}
    host=${host_line//#!/}
    echo 'request host: '${host}
    locust -f request_user.py  --host=${host}
else
    echo 'no request url yaml file'
fi
