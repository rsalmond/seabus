SHELL = bash

seaweb:
	@sudo docker build -t seaweb -f Dockerweb . 

clean:
	@for c in `sudo docker ps -a | grep -v CONTAINER | awk '{print $$1}'`; do sudo docker rm $$c; done
	@for i in `sudo docker images | grep -v IMAGE | grep -v ubuntu | awk '{print $$3}'`; do sudo docker rmi $$i; done
