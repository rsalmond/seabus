SHELL = bash

seaweb:
	@docker build -f Dockerweb.debian . -t seaweb

clean:
	@for c in `sudo docker ps -a | grep -v CONTAINER | awk '{print $$1}'`; do sudo docker rm $$c; done
	@for i in `sudo docker images | grep -v IMAGE | grep -v ubuntu | awk '{print $$3}'`; do sudo docker rmi $$i; done
