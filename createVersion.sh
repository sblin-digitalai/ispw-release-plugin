#!/bin/bash

if [ $# -lt 1 ]; then
	echo 1>&2 "$0: not enough arguments"
	exit 2
elif [ $# -gt 1 ]; then
	echo 1>&2 "$0: too many arguments"
	exit 2
fi

echo -------------------
echo Creating version $1
echo -------------------

version=$1
cd src/main/resources
filename="xlr-ispw-plugin-${version}"

zip -r $filename.zip *.* ispw web trustmanager
mv $filename.zip $filename.jar
cd ../../..

echo ------------------------
echo Version $version created
echo ------------------------