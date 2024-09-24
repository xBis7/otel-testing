#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
with_build=${2:-"false"}

# Stop the docker env, if running.
cd "$abs_path"/"$CURRENT_PROJECT"/compose
docker compose down

if [ "$with_build" == "true" ]; then
  # Build jenkins.
  cd "$abs_path"/"$JENKINS_PROJECT"
  mvn clean install -DskipTests
fi

export USE_CUSTOM_WAR="true"

cp -f "$abs_path"/"$JENKINS_PROJECT/war/target/jenkins.war" "$abs_path"/"$CURRENT_PROJECT"/compose/jenkins_files/

cd "$abs_path"/"$CURRENT_PROJECT"/compose

echo ""
echo "Printing exported env variables for verification."
echo "USE_CUSTOM_WAR value: $USE_CUSTOM_WAR"

docker compose up -d --build

