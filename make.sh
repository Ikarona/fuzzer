#! /bin/bash
pwd
export PIN_ROOT=$(pwd)/pin/pin
wget https://www.cs.columbia.edu/~vpk/research/libdft/libdft-3.1415alpha.tar.gz
tar -xzf libdft-3.1415alpha.tar.gz --directory=libdft/
ln -s /pin/pin pin
sudo apt-get install bmagic
pip install BitVector
pip3 install BitVector