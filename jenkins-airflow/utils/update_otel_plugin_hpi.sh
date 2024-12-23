#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1

cd "$abs_path"/"$OTEL_PLUGIN_PROJECT"

mvn clean install -DskipTests

# The update can happen on the fly. jenkins picks up the new version automatically.
# Same way jenkins updates the plugins without restarts.

# .hpi (Hudson Plugin Interface) and .jpi (Jenkins Plugin Interface) files are the same.
# 'jpi' is the new file naming for jenkins plugins.
# Rename the file extension to be consistent with the rest of the plugin file names.
docker cp "$abs_path"/"$OTEL_PLUGIN_PROJECT"/target/opentelemetry.hpi "$JENKINS_HOSTNAME":/var/jenkins_home/plugins/opentelemetry.jpi

# Check the version on the UI to verify that the update was successful.

docker exec -it -u root "$JENKINS_HOSTNAME" chown jenkins:jenkins /var/jenkins_home/plugins/opentelemetry.jpi

# For verification.
# docker exec -it -u root "$JENKINS_HOSTNAME" ls -lah /var/jenkins_home/plugins | grep 'opentelemetry'

# Restart jenkins to pick up the version update.
docker restart "$JENKINS_HOSTNAME"
