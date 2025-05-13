# xssdtest

> xssdtest is a SSD testing platform that supports customization by different manufacturers
***
# Source Code
```
git clone https://github.com/xssdtest/xssdtest.git
```
***
# Set UP Environment And Test Script
### Set up SPDK and Python environment
#### If the environment is not configured
```
cd xssdtest
sudo ./install.sh
```
#### If the environment has already been configured
```
cd xssdtest
git submodule update --init --recursive
git submodule update --remote --recursive
cd xt_platform/spdk; ./configure --without-isal;make -j32
cd ../; sudo ./build.sh
```
***
### Test script with null engine
```
sudo python3 xt_scripts/data_path/xt_datapath_sample.py
```
***
# Features
1. Support different types of engines and drivers
1. Support firmware simulation, requires firmware support
1. Support multiple Linux systems
1. Unified test cases: test scripts at different stages do not need to be rewritten
1. Complete white box verification solution
1. Rich data comparison
1. Compatibility solution for different protocols
1. Efficient and non-repetitive full disk random generation solution
1. Rich tool support
1. Open source, continuously updated
***
# Contact
* The current version has not been fully verified. Welcome suggestions for changes or joining xssdtest in joint development.
* Email: 2573789168@qq.com