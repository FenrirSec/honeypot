#!/bin/sh                                                                                                                                                                                     

if [ "$#" -ne "1" ];then
    echo "Usage : $0 INGRESS_SERVER_IP"
    exit 1
fi

INGRESS=$1

echo
echo "WARNING : This automatic setup script makes modifications to your system that might cause data loss and further issues."
echo "Make sure you UNDERSTAND them and agree with them. Keep in mind that this script has solely been made to easen deployment"
echo "of this honeypot on *throwaway* Ubuntu 20.04 servers."
echo "Press ENTER to continue or CTRL + C to stop there."

read

cd honeypot 2>/dev/null

apt-get update -y && apt-get install pip -y
pip install -r requirements.txt
mkdir keys
ssh-keygen -q -N "" -f keys/ssh_host_rsa_key
sed -i "s/localhost/$INGRESS/g" logger.py && echo $INGRESS

curl --insecure https://$INGRESS:5000/pubkey > keys/ingress_key.pub

openssl s_client -showcerts -connect $INGRESS:5000 </dev/null 2>/dev/null|openssl x509  > keys/ingress.crt

cp conf.py.example conf.py

sed -i "s/INGRESS_SERVER=None/INGRESS_SERVER='$INGRESS'/" conf.py

sed -i "s/#Port 22/Port 9101/g" /etc/ssh/sshd_config

./update_limits.sh

openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout keys/server.key -out keys/server.crt

echo
echo "Your SSH configuration has been changed, you might be disconnected, please reconnect using the port 9101. Bye!"

systemctl restart sshd
systemctl stop nginx 2>/dev/null
systemctl disable nginx 2>/dev/null
ufw disable

tmux new-session -s "honeypot" ./main.py
