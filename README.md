# piWebCtrl
Basic controls from a Web UI for your Raspberry Pi.
Running it in Background, open any web browser and point it to your Pi network IP address.

![Preview](https://forum.raspberry-pi.fr/uploads/default/original/2X/3/3304d0a2889081b005b3593f0201bf8cffe24896.png)

### Install

* Login into ssh on your Pi and go to "/home/pi" folder;

`cd /home/pi`

* Clone the GIT into the home directory;

`git clone https://github.com/levelKro/piWebCtrl.git`

* Move the Autostart script into the init.d folder;

`sudo cp /home/pi/piWebCtrl/_systemd/piwebctrl.service /etc/systemd/system/piwebctrl.service`

* Install it for the boot;

`sudo systemctl enable piwebctrl`

* Configure the piWebCtrl (port and password);

`nano /home/pi/piWebCtrl/piwebctrl.py`

* Run the service;

`sudo systemctl start piwebctrl`

* For use it, point any web browser to `http://<ip of pi>:<port>` (9000 is the default port)

### CLI

This tool can be used like a cURL request from a CLI for remotly reboot or power off the Raspberry Pi.

* Reboot : `http://<ip of pi>:<port>/run/reboot?pass=<password>`
* Power off : `http://<ip of pi>:<port>/run/poweroff?pass=<password>`
* Service : `http://<ip of pi>:<port>/run/service/<start|stop|restart>/<servicename>?pass=<password>`
* Stats (JSon) : `http://<ip of pi>:<port>/stats.json?pass=<password>`
