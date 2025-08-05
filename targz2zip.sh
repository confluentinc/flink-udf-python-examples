#!/bin/bash

if [[ $# -lt 1 ]]
then
    echo "usage: $0 PKG_TAR_GZ"
    echo "Takes a .tar.gz file and re-archives it as a .zip file."
    exit 1
fi

intar=$(realpath "$1")
outzip=${intar%.tar.gz}.zip

tmpdir=$(mktemp -d)
echo "Extracting $intar"
tar -xf "$intar" -C "$tmpdir"
echo "Writing $outzip"
(cd "$tmpdir" || exit; rm -f "$outzip"; zip -qr "$outzip" .)
rm -rf "$tmpdir"
