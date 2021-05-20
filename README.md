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

#### Connect OLED
![image](https://user-images.githubusercontent.com/50474972/118995585-393c9e00-b9c2-11eb-820f-fc4121860ed5.png)

### Execute 
- python3 oledControl.py

### Running Image

| Frame | OLED |
| --- | --- |
| ![외관](https://user-images.githubusercontent.com/50474972/119000504-21671900-b9c6-11eb-8494-38c5dcee6bcb.jpg) | ![OLED](https://user-images.githubusercontent.com/50474972/119000538-29bf5400-b9c6-11eb-9f71-a8fa7d39e60b.jpg) |
| ![외관_2](https://user-images.githubusercontent.com/50474972/119000790-62f7c400-b9c6-11eb-81f0-931c163dd5b3.jpg) | ![OLED_2](https://user-images.githubusercontent.com/50474972/119000847-6c812c00-b9c6-11eb-924c-319a11ea09d8.jpg) |

### Mechanism
![image](https://user-images.githubusercontent.com/50474972/119001404-e7e2dd80-b9c6-11eb-8029-e48e7fb956a3.png)
