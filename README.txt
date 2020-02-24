README - Setup Pricer Remote production test server on Raspberry Pi 4+ (Buster)
======================================================================
Code: All files can be pulled from  https://github.com/ftjerneld/rheaprodtest.git 

Operation: With Pricer Remote in factory reset mode, when scanning barcode Z9999999999999999 the Remote tries to connect to
wifi PRICER_TEST and send request http://192.168.4.1/rheaserver/+mac=<MAC>&rssi=<RSSI>&fw=<FW version>&plid=Z9999999999999999

Pass: Beep and light up three green LEDs. 
Fail: Triple beep and red LED.

1. Set Pi as Access point
Source: https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/168-raspberry-pi-hotspot-access-point-dhcpcd-method

i) Get latest rasbian version
sudo apt-get update
sudo apt-get upgrade

ii) Install hostapd and dnsmasq
sudo apt-get install hostapd
sudo apt-get install dnsmasq

Stop the services

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

iii) Configure hostapd
sudo nano /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
ssid=PRICER_TEST
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=pricerremote
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

sudo nano /etc/default/hostapd

Change:
#DAEMON_CONF=""
to
DAEMON_CONF="/etc/hostapd/hostapd.conf"

Check the DAEMON_OPTS="" is preceded by a #, so is #DAEMON_OPTS=""

iv) Configure dnsmasq
sudo nano /etc/dnsmasq.conf

Go to the bottom of the file and add the following lines

#RPiHotspot config - No Internet
interface=wlan0
domain-needed
bogus-priv
dhcp-range=192.168.4.1,192.168.4.20,255.255.255.0,12h

v) Configure DHCPCD.conf
sudo nano /etc/dhcpcd.conf

then scroll to the bottom of the file and add the line

nohook wpa_supplicant
interface wlan0
static ip_address=192.168.4.1/24
static routers=192.168.4.1

The line 'nohooks wpa_supplicant' will stop the network wifi from starting if you have an entry in /etc/wpa_supplicant/wpa_supplicant.conf . If this is not done then network wifi will override the hotspot.

!!! Comment the new lines above to enable the Pi's wifi again !!!

2. Autostart flask
Flask is used as webserver. To get it to auto start add service in /etc/systemd/system
- user shall be root in order to use port 80
- run sudo systemctl enable rheaserver.service
- run sudo systemctl daemon-reload after each modification

3. Install server
- Create folder /home/pi/rheaserver
- Copy the files in repo https://github.com/ftjerneld/rheaprodtest.git to the rheaserver folder. The file rheaserver.py is the actual server that receives the requests from the DUT 



