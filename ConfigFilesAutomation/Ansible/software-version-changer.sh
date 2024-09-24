#!/bin/bash

# This script will change the software version in the config file

grep -ri '  name: ' *container_playbook.yml | sed 's#_playbook.yml:##g' | sed 's#  name:#package -> #' > ContainerDependencyPackages.txt
