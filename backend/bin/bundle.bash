#!/bin/bash

# figure out where we are running and identify backend root
root=$(realpath $(dirname $0)/../)

# create directory for Lambda bundle
mkdir -p $root/build/bundle/
cp -R $root/src/* $root/build/bundle

# Create the Lambda bundle
cd $root/build/bundle
uv export --frozen --no-dev --no-editable -o requirements.txt
uv pip install \
   --no-installer-metadata \
   --no-compile-bytecode \
   --python-platform x86_64-manylinux2014 \
   --python 3.13 \
   --target . \
   -r requirements.txt
zip -r ../bundle.zip .
echo "Wrote Lambda bundle"