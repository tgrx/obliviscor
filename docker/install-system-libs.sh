#!/bin/sh

echo "INSTALLING SYSTEM LIBS"

yum install -y \
        mysql \
        mysql-devel \
        python3-devel \


echo "DONE: INSTALLING SYSTEM LIBS"
