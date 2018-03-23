# pi tuner

Files and config for the raspberry pi which receives and decodes the AIS traffic.


# Setup

 * Install [raspbian](https://www.raspberrypi.org/downloads/raspbian/) and [enable sshd](https://www.raspberrypi.org/documentation/remote-access/ssh/).
 * Run: `$ ansible -i ansible/inventory -l <hostname> ansible/playbooks/base.yaml`
 * Install docker. (need to do it this way because raspbian: https://docs.docker.com/install/linux/docker-ce/debian/#install-docker-ce)
```
$ curl -fsSL get.docker.com -o /tmp/get-docker.sh && sudo /tmp/get-docker.sh
```
