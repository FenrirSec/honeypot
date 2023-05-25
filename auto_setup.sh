#!/bin/sh                                                                                                                                                                                     

if [ "$#" -ne "1" ];then
    echo "Usage : $0 INGRESS_SERVER_IP"
    exit 1
fi

INGRESS=$1

cd honeypot 2>/dev/null

pip install -r requirements.txt
mkdir keys
ssh-keygen -q -N "" -f keys/ssh_host_rsa_key
sed -i "s/localhost/$INGRESS/g" logger.py && echo $INGRESS
curl --insecure https://$INGRESS:5000/pubkey > keys/server_key.pub

sed -i "s/#Port 22/Port 9101/g" /etc/ssh/sshd_config

./update_limits.sh

openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout keys/server.key -out keys/server.crt

echo "Your SSH configuration has been changed, you might be disconnected, please reconnect using the port 9101. Bye!"

systemctl restart sshd
systemctl stop nginx
systemctl disable nginx
ufw disable

tmux new-session -s "honeypot" ./main.py
