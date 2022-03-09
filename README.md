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


### ENJOY
