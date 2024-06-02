#! /usr/bin/env bash

set -x
set -e
set -o pipefail

sudo apt update
sudo apt-get install -y git-core bash-completion

pip install -r /workspaces/league_predictions/app/requirements.txt
pip install -r /workspaces/league_predictions/tools/requirements.txt
