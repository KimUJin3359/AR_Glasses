# AR_Glasses

### Needed
#### Hardware
- Raspberry pi zero w with SD card
- 0.96`` monochrome oled display
- Wireless LAN Card
- Glasses


### Setting Environment
#### Raspberry pi OS
- [Downloads](https://www.raspberrypi.org/downloads/)

#### Setting a Wifi
1. Use Raspberry pi Newer Version( ex) Raspberry pi 4 )
  - VNC with computer
  - setting a wifi
2. Use SD Card(OS downloaded)
  - find /boot/wpa_supplicant.conf
  ```
  network = {
    ssid = "wifi name"
    psk = "password of wifi"
    key_mgmt = WPA-PSK
  }
  // expression of WPA-PSK2 is same with WPA-PSK
  ```
#### Connect on ssh
- using MobaXterm, ssh on Mac etc..

#### Setting SPI Interface
```
sudo raspi-config
Interfcae Options > SPI
```

#### Setting OLED
1. use git
```
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python3 setup.py install
```
2. if 1 doesn't work, use pip
```
pip install Adafruit-SSD1306
# test with Adafruit_Python_SSD1306/examples
```

#### Download Pillow
```
pip3 install pillow
```

#### Setting Timezone
```
sudo raspi-config
# Locallisation Options > Timezone > Asia,Seoul
```

