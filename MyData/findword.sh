#!/bin/sh
echo $1
foundline=`egrep ^$1$ similary_dic -n | cut -d : -f 1 $foundline`
echo $foundline
if [[ $foundline == '' ]]
then
  echo "not found $1"
  exit 0
fi
more +$foundline similary_dic
