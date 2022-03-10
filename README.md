# SMART GREEN HOUSE using RaspberryPi3
## with docker and flask

### > requirements :
**1. docker & docker-compose**
  ```sh
  sudo apt update --fix-missing && sudo apt upgrade # update system first

  curl -fsSL https://get.docker.com -o get-docker.sh # get docker

  sudo sh -c ./get-docker.sh # install the script

  sudo usermod -aG docker ${USER} # add docker to user  groups

  sudo apt-get install -y python3 python3-pip # install the python for docker compose
  sudo pip3 install docker-compose

  sudo systemctl enable Docker # enable the docker daemon

  sudo reboot # restart the raspberry pi
  ```

**2. clone this Repo**
```sh
git clone --recursive https://github.com/RizalAchp/autogh-raspi.git
```

**3. run the app**
```sh
cd ./autogh-raspi
docker-compose up

# after docker done pulling, open your browser
# and open RaspberryPi3 ip Address in the browser
```

### > configuration
**1. default settings**
```sh
# if you want to change the default settings, go to directory config and change the config.json 
vim ./config/config.json #use vim
#of
code ./ #use vscode and open the config.json in config directory
```
**2. GPIO Settings**
  - all the gpio settings and process are in ./sensor_gpio_raspi.py

**3. Web Client Stuff**
  - html file in ./templates/index.html
  - css and js file in ./static

**4. PINOUTS**
```bash
                        |         3V3  (1) (2)  5V          | from here
                        |       GPIO2  (3) (4)  5V          |
                        |       GPIO3  (5) (6)  GND         |
                        |       GPIO4  (7) (8)  GPIO14      |
                        |         GND  (9) (10) GPIO15      |
                        |      GPIO17 (11) (12) GPIO18      |
                        |      GPIO27 (13) (14) GND         | 
                        |      GPIO22 (15) (16) GPIO23      |
                        |         3V3 (17) (18) GPIO24      |
                        |      GPIO10 (19) (20) GND         |
                        |       GPIO9 (21) (22) GPIO25      |
                        |      GPIO11 (23) (24) GPIO8       |
                        |         GND (25) (26) GPIO7       | to here is for( LCD )
                        |       GPIO0 (27) (28) GPIO1       |
              RELAY 1 > |       GPIO6 (29) (30) GND         |
              RELAY 2 > |       GPIO6 (31) (32) GPIO12      | > PIN DIGITAL ( SOIL MOISTURE SENSOR )
 ( DHT11 ) PIN DHT 11 > |      GPIO13 (33) (34) GND         |
              RELAY 3 > |      GPIO19 (35) (36) GPIO16      |
              RELAY 4 > |      GPIO26 (37) (38) GPIO20      | > PIN TRIGGER ( HCSR04 )
                        |         GND (39) (40) GPIO21      | > PIN ECHO    ( HCSR04 )
```


### ENJOY
