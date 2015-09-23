#!/usr/bin/env bash
sudo python tcp_serial_bridge.py -p /dev/ttyAMA0 -b 115200 -P 1997 --spy -c --net-nl=LF --ser-nl=CR
