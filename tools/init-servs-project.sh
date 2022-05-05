#!/usr/bin/env sh

# BoBoBo

cur_dir=`pwd`
work_dir=${cur_dir}
cd ${work_dir}

project_name=
while getopts 'n:' opts
do
    case $opts in
    n)
        project_name=$OPTARG;;
    esac
done
if [ -z "${project_name}" ]; then
    echo 'no project name'
    exit 1
fi

root_package=${project_name//-/_}
src_dir=${project_name}/${root_package}

echo 'in dir: '${work_dir}

if [ -d ${project_name} ]; then
    echo ${project_name}' exists, delete it [yes/no]?'
    read yorn
    if [ ${yorn} == 'yes' ]; then
        rm -rf ${project_name}
    else
        echo 'exit command'
        exit 1
    fi
fi
mkdir ${project_name}
mkdir ${src_dir}
touch ${src_dir}/__init__.py

touch ${project_name}/README.md
cat << END                                > ${project_name}/README.md
# ${project_name}
END

touch ${project_name}/requirements.txt
cat << END                                > ${project_name}/requirements.txt
pyyaml==5.3.1
END

touch ${project_name}/test-requirements.txt
cat << END                                > ${project_name}/test-requirements.txt
pyyaml==5.3.1
END

echo 'create project: '${project_name}
mkdir ${src_dir}/servs
touch ${src_dir}/servs/__init__.py

mkdir ${src_dir}/tests
touch ${src_dir}/tests/__init__.py

touch ${src_dir}/run_app.py
touch ${src_dir}/context.py


cat << END                                > ${src_dir}/run_app.py
#!/usr/bin/env python3


import driven.util as util
from drive.route import drive_app
import drive.embed.wsgi_server as server
from ${root_package}.init_context import build_context

args = util.get_server_cmdargs()
app = drive_app("${root_package}", build_context(args.conf_path))
server.bootstrap(args.host, args.port, app)
END


cat << END                                > ${src_dir}/context.py
#!/usr/bin/env python3


def build_context(conf_file):
    return {}
END
