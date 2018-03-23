SHELL = bash

seaweb:
	@docker build -f Dockerweb.debian . -t seaweb

push:
	@`aws ecr get-login --no-include-email --region=us-west-2`
	@docker tag seaweb:unstable 703091623098.dkr.ecr.us-west-2.amazonaws.com/seaweb:unstable
	@docker push 703091623098.dkr.ecr.us-west-2.amazonaws.com/seaweb:unstable

clean:
	@for c in `sudo docker ps -a | grep -v CONTAINER | awk '{print $$1}'`; do sudo docker rm $$c; done
	@for i in `sudo docker images | grep -v IMAGE | grep -v ubuntu | awk '{print $$3}'`; do sudo docker rmi $$i; done
