#!/bin/sh
ip_serveur=10.11.77.15
ip_client=10.11.77.14
addr=$(ip address show enp0s31f6 | grep "inet\b" | awk '{print $2}' |cut -d/ -f1)
echo $addr

if [ $addr = $ip_serveur ]
then
   echo "je suis le serveur"
elif [ $addr = $ip_client ]
then
   echo "je suis le client"
fi

# nc -lp 1234
# penser a passer les adress ip en argument au fichier et le port
# nc cat text.txt | nc 10.11.77.15 1234

