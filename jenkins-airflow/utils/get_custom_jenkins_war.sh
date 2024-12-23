#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1

cd "$abs_path"/"$JENKINS_PROJECT"
mvn clean install -DskipTests

cp -f "$abs_path"/"$JENKINS_PROJECT/war/target/jenkins.war" "$abs_path"/"$CURRENT_PROJECT"/compose/jenkins_files/
