#!/bin/bash

set -e

source "./env_variables.sh"

checkProjectExists() {
  path=$1
  project=$2

  if ls $path | grep $project; then
    echo 0
  else
    echo 1
  fi
}

exitIfProjectNotExist() {
  path=$1
  project=$2

  res=$(checkProjectExists "$path" "$project")

  if [ "$res" == 1 ]; then
    echo "Project '$project' doesn't exist. Exiting..."
    exit 1
  else
    echo "Project '$project' exists."
  fi
}

cloneProjectIfNotExist() {
  base_path=$1
  project_name=$2
  github_user=$3

  existsLocally=$(checkProjectExists $base_path $project_name)

  if [ "$existsLocally" == 1 ]; then
    echo "'$project_name' doesn't exist locally, cloning..."
    echo ""
    cd "$base_path"
    if git clone "git@github.com:$github_user/$project_name.git"; then
      echo ""
      echo "Cloning '$project_name' succeeded."
      echo ""
    else
      echo "Cloning '$project_name' failed. Exiting..."
      exit 1
    fi
  else
    echo ""
    echo "'$project_name' exists locally."
    echo ""
  fi
}

checkoutToProjectCommit() {
  base_path=$1
  project_name=$2
  github_remote_user=$3
  github_commit_sha=$4

  echo "Updating '$project_name' repo."
  cd "$base_path/$project_name"

  if [ "$github_remote_user" != "origin" ]; then
    if git remote -v | grep "$github_remote_user"; then
      echo "Remote from user '$github_remote_user', already exists in project '$project_name'."
    else
      echo "Remote from user '$github_remote_user', doesn't exist in project '$project_name', adding..."

      if git remote add "$github_remote_user" "git@github.com:$github_remote_user/$project_name.git"; then
        echo "Adding remote repo for project '$project_name' succeeded."
      else
        echo "Adding remote repo for project '$project_name' failed. Exiting..."
        exit 1
      fi
    fi
  fi

  if git fetch $github_remote_user; then
    echo "Fetching '$github_remote_user' succeeded."
  else
    echo "Fetching '$github_remote_user' failed. Exiting..."
    exit 1
  fi

  if git checkout $github_commit_sha; then
    echo "Checking out to commit '$github_commit_sha' succeeded."
  else
    echo "Checking out to commit '$github_commit_sha' failed. Exiting..."
    exit 1
  fi

  echo ""
  echo "Finished fetching and checking-out for '$project_name' repo."
  echo ""
}

buildProject() {
  abs_path=$1
  project=$2

  build_dotnet_tester=0
  build_java_tester=0

  if [ "$project" == "dotnet" ]; then
    build_dotnet_tester=1
  elif [ "$project" == "java" ]; then
    build_java_tester=1
  elif [ "$project" == "all" ]; then
    build_dotnet_tester=1
    build_java_tester=1
  else
    echo "Value '$project' is invalid. Try one of the following: 'dotnet', 'java', 'all'."
  fi

  if [ "$build_dotnet_project" != 0 ]; then
    cd "$abs_path"/"$CURRENT_PROJECT"/partial-spans

    dotnet build OtelTestSolution.sln
  fi

  if [ "$build_java_project" != 0 ]; then
    cd "$abs_path"/"$CURRENT_PROJECT"/partial-spans/otel-java-test

    ./gradlew clean build --no-configuration-cache
  fi
}
