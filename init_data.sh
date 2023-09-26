#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"
echo "Initialising card images..."

data/sets/system_gateway/doit.sh
echo
data/sets/system_update_2021/doit.sh
echo
data/sets/midnight_sun/doit.sh
echo
data/sets/parhelion/doit.sh
echo
data/sets/the_automata_initiative/doit.sh
echo

echo "Done!"
