# piWebCtrl
Basic controls from a Web UI for your Raspberry Pi.
Running it in Background, open any web browser and point it to your Pi network IP address.

### Install

* Login into ssh on your Pi and go to "/home/pi" folder;

`cd /home/pi`

* Clone the GIT into the home directory;

`git clone https://github.com/levelKro/piWebCtrl.git`

* move the Autostart script into the init.d folder;

`sudo mv /home/pi/piWebCtrl/piwebctrl.sh /etc/init.d/piwebctrl.sh`

* Make it executable;

`sudo chmod +x /etc/init.d/piwebctrl.sh`

* Install it for the boot;

`sudo systemctl enable piwebctrl.sh`

* Configure the piWebCtrl (port and password);

`nano /home/pi/piWebCtrl/piwebctrl.py`

* Run the service;

`sudo systemctl start piwebctrl`

* For use it, point any web browser to `http://<ip of pi>:9000` (if 9000 is the configured port)
