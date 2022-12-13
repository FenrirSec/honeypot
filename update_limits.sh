CONTENT="net.core.somaxconn = 16384\nnet.ipv4.tcp_max_orphans = 16384\nnet.ipv4.tcp_max_syn_backlog = 16384\nnet.core.netdev_max_backlog = 262144\nnet.ipv4.ip_local_port_range = 1024 65535\nfs.file-max = 16777216\nfs.pipe-max-size = 134217728"

if ! grep 16384 /etc/sysctl.conf;then
    echo "Patching /etc/sysctl.conf"
    echo -e $CONTENT >> /etc/sysctl.conf
    sysctl -p
fi
