#!/usr/bin/env sh

# BoBoBo

check_conf_file(){
    conf_file=$1
    driven.sh -c check-conf-file -p ${conf_file}"+engine"
    if [ ! $? -eq 0 ];then
        echo "Invalid conf file: "${conf_file}
        exit 1
    fi
}

install_requirements(){
    driven_conf_file=$1
    driven.sh -c install-requirements -p ${driven_conf_file}
    if [ ! $? -eq 0 ];then
        echo "Failed to install: "${driven_conf_file}
        exit 1
    fi
}

# Run base current dir.
cur_dir=`pwd`
echo "Run Base Current Dir: $cur_dir"

scrip_dir=$(cd "$(dirname "$0")"; pwd)
server_py_path=${scrip_dir}/../driven/embed/sengine/sengine_serv.py
requirements_path=${scrip_dir}/../requirements.txt

conf_file=${cur_dir}/sengine.yaml
if [ ! -f $conf_file ]; then
    conf_file=${SENGINE_CONF}
fi

port=8080
sengine_signal=start
background_run=0
while getopts 'c:p:s:b' opts
do
    case $opts in
    c)
        conf_file=$OPTARG;;
    p)
        port=$OPTARG;;
    s)
        sengine_signal=$OPTARG;;
    b)
        background_run=1;;
    esac
done

echo 'SEngine '${sengine_signal}
if [ ${sengine_signal} == 'start' ]; then
    driven_pythonpath=${scrip_dir}/..
    export PYTHONPATH=${driven_pythonpath}

    if [ ! -f $conf_file ]; then
        echo 'ERROR: No sengine conf file.'
        exit 1
    fi

    echo 'SEngine conf file: '${conf_file}
    echo 'SEngine port: '${port}
    echo 'Prepare to start sengine...'
    echo 'Need pyyaml to start.'
    pip3 install pyyaml
    check_conf_file ${conf_file}
    install_requirements ${conf_file}

    if [ ${background_run} -eq 1 ]; then
        nohup ${server_py_path} --port ${port} --conf ${conf_file} >> sengine.output 2>&1 &
    else
        ${server_py_path} --port ${port} --conf ${conf_file}
    fi
elif [ ${sengine_signal} == 'restart' ]; then
    ${scrip_dir}/sengine-restart.sh
elif [ ${sengine_signal} == 'stop' ]; then
    ${scrip_dir}/sengine-stop.sh
fi
