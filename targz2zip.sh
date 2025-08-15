#!/bin/bash

if [[ $# -lt 1 ]]
then
    echo "usage: $0 PKG_TAR_GZ"
    echo "Takes a .tar.gz file and re-archives it as a .zip file."
    exit 1
fi

intar="$1"
absin=$(realpath "$1")
outzip=${intar%.tar.gz}.zip
absout=${absin%.tar.gz}.zip

# remove the /*.tar.gz from the intar to get the dir
# if intar is dist/example_udf-0.1.0.tar.gz
# how to get base dir dist
intar_dir=$(dirname "$absin")

echo "writing $outzip"
(cd $intar_dir || exit; zip -r "$absout" .)
