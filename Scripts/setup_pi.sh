#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

echo "BaralabaBob Setup Script v1.0"
echo "Author: John Board"
echo "========================================"
cd /home/pi/
echo "Installing packages. User input required for some packages."
sudo apt-get update
sudo apt-get install screen htop vlc blender oracle-java7-jdk apache2 mysql-server php5 php5-mysql git python-rpyc python-pygame python-serial
git clone http://github.com/boar401s2/BaralabaBob
echo "Script finished."
exit 0