#!/usr/bin/env sh

# BoBoBo

scrip_dir=$(cd "$(dirname "$0")"; pwd)
driven_script=${scrip_dir}/../driven/command/execute.py
requirements_file=${scrip_dir}/../requirements.txt

export PYTHONPATH=${PYTHONPATH}:${scrip_dir}/..
pip3 install -r ${requirements_file}
${driven_script} $*
