#!/bin/bash

ham=1
while read -a line
do
    label=${line[0]}
    filename=${line[1]}
    if [ "$label" == "$ham" ]
    then
    	cp $filename "ham/$filename"
    else
    	cp $filename "spam/$filename"
    fi   
done
