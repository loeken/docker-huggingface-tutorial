## Ubuntu 22.04 - dependency installation

### update the drivers
in the the “software updater” update drivers to the last version of the prop driver.

### reboot
to switch using to new driver

```bash
sudo apt update
sudo apt-get install curl

sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose -y

sudo usermod -aG docker $USER
newgrp docker
```

### docker & container toolkit
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/ubuntu22.04/amd64 /" | \
sudo tee /etc/apt/sources.list.d/nvidia.list > /dev/null 

sudo apt update

sudo apt install nvidia-docker2 nvidia-container-runtime -y
sudo systemctl restart docker
```