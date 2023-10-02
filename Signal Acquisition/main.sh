#! /usr/bin/bash
./pi_one.sh & ./pi_two.sh 

sshpass -p 'group2' scp group2@192.168.29.97:recording_1.wav .
sshpass -p 'group2' scp group2@192.168.29.43:recording_2.wav .


