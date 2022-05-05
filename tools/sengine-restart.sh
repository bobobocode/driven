#!/usr/bin/env sh

# BoBoBo

ses=`ps aux | grep sengine_serv.py | wc -l`



if [ $ses -eq 2 ]; then
    echo 'Find SEngine running. Will stop it.'
    ps aux | grep sengine.py | tail -n 1 | awk '{print $2}' | xargs kill -9

    if [ -f sengine.output ]; then
        SENGINE_PORT=`grep SENGINE_PORT sengine.output | tail -n 1 | awk '{print $2}'`
        if [ '$SENGINE_CONF' == '' ];then
            SENGINE_CONF=`grep SENGINE_CONF sengine.output | tail -n 1 | awk '{print $2}'`
        fi
    fi
    if [ '$SENGINE_PORT' == '' ];then
        echo 'Found no SENGINE_PORT'
        echo 'Input SENGINE_PORT to stop:'
        read SENGINE_PORT
    fi
    if [ '$SENGINE_PORT' != '' ];then
        echo 'Stop process listening to '$SENGINE_PORT
        lsof -i tcp:${SENGINE_PORT} | tail -n 1 | awk '{print $2}' | xargs kill -9
    fi
fi


if [ '$SENGINE_PORT' == '' ];then
    SENGINE_PORT=8080
fi

echo 'SENGINE_PORT: '$SENGINE_PORT
echo 'SENGINE_CONF: '$SENGINE_CONF
nohup sengine.sh -p $SENGINE_PORT > sengine.output 2>&1 &
echo 'SEngine is starting...'

sleep 1
if [ -f sengine.output ]; then
    SENGINE_PORT_NEW=`grep SENGINE_PORT sengine.output | tail -n 1 | awk '{print $2}'`
fi

if [ '$SENGINE_PORT_NEW' != '' ];then
    ss=`lsof -i tcp:${SENGINE_PORT_NEW} | wc -l`
    while [ $ss -ne 2 ]
    do
        echo '...'
        sleep 1
        ss=`lsof -i tcp:${SENGINE_PORT_NEW} | wc -l`
    done
    echo 'SEngine started'
else
    echo 'Found no sengine.output in current dir.'
    echo 'SEngine failed to start.'
    exit 1
fi 
