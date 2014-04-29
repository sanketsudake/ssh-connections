#! /bin/sh
#
# sample.sh
# Copyright (C) 2014 sagar <sagar@sagar-liquid>
#
# Distributed under terms of the MIT license.

# ssh sagar@localhost 'bash -S' < sample.sh

# sshpass -p 'sagar_pc' ssh sagar@localhost
export DISPLAY=:0.0
# echo sagar_pc | sudo -S apt-get install mpg123
# echo sagar_pc | sudo -S apt-get update 
ssh -o StrictHostKeyChecking=no sagar@localhost "echo sagar_pc | sudo -S apt-get update"
sshpass -p 'nisarg' ssh -o StrictHostKeyChecking=no Nisarg@172.19.10.235 "date"
notify-send "Installed mpg123"
