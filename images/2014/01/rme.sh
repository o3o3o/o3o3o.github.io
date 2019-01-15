#!/bin/bash
set -o nounset
set -o errexit
#IMG_20140101_150819*
#IMG_20140101_150819-1024x768.jpg
mymv(){
    if [ $@ < 1 ]; then
        echo 'Bad args'
        exit 0
    fi
    local EXCEPT=$1
    local PATTERN="${1%%-*}*"

    echo "before pattern: $PATTERN"
    ls $PATTERN
    local rmf=$(ls $PATTERN |grep -v $EXCEPT)
    [ "$rmf" != "" ] && mv  $rmf ~/tmp/photobak
    #echo "mv $(ls $PATTERN |grep -v $EXCEPT) ~/tmp/photobak"
    echo "after"
    ls $PATTERN
}
mymv $@
