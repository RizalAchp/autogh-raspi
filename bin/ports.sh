#!/usr/bin/sh
# for port 80 server
firewall-cmd --add-forward-port=port=80:proto=tcp:toport=5000 --permanent
firewall-cmd --add-forward-port=port=5000:proto=tcp:toport=80 --permanent

