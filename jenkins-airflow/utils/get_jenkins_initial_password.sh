#!/bin/bash

set -e

source "./lib.sh"

docker exec -it "$JENKINS_HOSTNAME" cat /var/jenkins_home/secrets/initialAdminPassword


