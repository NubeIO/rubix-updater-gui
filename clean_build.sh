#!/bin/bash
# Console colors
GREEN=$'\e[0;32m'
RED=$'\e[0;31m'
NC=$'\e[0m'
YELLOW=$'\e[1;33m'

echo "${YELLOW}-----CHECK data/rubix-wires -----${NC}"
DIST="dist"
BUILD="build"
echo "CHECK: DIR $DIST exists"
if [ -d $DIST ]; then
    echo "${GREEN}DOES exists${NC}"
    sudo rm -r $DIST
else
    echo "${RED} NOT FOUND $DIST ${NC}"
fi


echo "CHECK: DIR $BUILD exists"
if [ -d $BUILD ]; then
    echo "${GREEN}DOES exists${NC}"
    sudo rm -r $BUILD

else
    echo "${RED} NOT FOUND $BUILD  ${NC}"
fi

pyinstaller --onefile --windowed  src/ui/main.py
dist/./main
