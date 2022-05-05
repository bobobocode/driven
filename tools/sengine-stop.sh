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
else
    echo 'Find no SEngine running.'
fi
