#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
project=$2

buildProject "$abs_path" "$project"
