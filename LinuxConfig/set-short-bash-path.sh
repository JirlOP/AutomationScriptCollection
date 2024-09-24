#!/bin/bash
# We have to be in the same directory as the .bashrc file

sed -i '/PS1=/s#\\w#\\W#g' .bashrc
source .bashrc
