#!/bin/sh
BUILD_DIR=$1
echo $BUILD_DIR

mkdir -p $BUILD_DIR
cd $BUILD_DIR
wget -O speedtest.tgz https://bintray.com/ookla/download/download_file?file_path=ookla-speedtest-1.0.0-x86_64-linux.tgz
tar xfz speedtest.tgz
rm -rf speedtest.*
chmod +x speedtest