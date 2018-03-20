#!/bin/bash

# extract the latest binaries from the docker builder images
docker run --rm -v $(pwd)/ansible/playbooks/files/binaries:/tmp us.gcr.io/rsa-servers/rtlais:latest sh -c "cp /usr/local/bin/rtl_ais /tmp"
docker run --rm -v $(pwd)/ansible/playbooks/files/binaries:/tmp us.gcr.io/rsa-servers/kalibrate:latest sh -c "cp /usr/local/bin/kal /tmp"

ansible-playbook -i ansible/inventory ansible/playbooks/base.yaml
