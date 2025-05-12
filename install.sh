#!/usr/bin/env bash
###############################################################################
 #    BSD LICENSE
 #
 #    Copyright (c) Saul Han <2573789168@qq.com>
 #
 #    Redistribution and use in source and binary forms, with or without
 #    modification, are permitted provided that the following conditions
 #    are met:
 #
 #       Redistributions of source code must retain the above copyright
 #        notice, this list of conditions and the following disclaimer.
 #       Redistributions in binary form must reproduce the above copyright
 #        notice, this list of conditions and the following disclaimer in
 #        the documentation and/or other materials provided with the
 #        distribution.
 #
 #    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 #    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 #    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 #    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 #    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 #    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 #    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 #    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 #    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 #    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 #    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'
function usage() {
    # Output the script's usage instructions
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -h, --help      Display help information"
    echo "  -a, --install-anaconda  install newest anaconda from net"
    echo "  -p, --install-python  install python from net"
    echo "  -f, --install-fio install fio with fio version"
    echo "  -n, --install-nvme-cli install fio with nvme-cli version"
    echo "  -s, --init-spdk init spdk environment"
}

OS="unknown"
if [ "$(uname)" == "Darwin" ]; then
    OS="macOS"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    fi
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    OS="windows"
fi

install_python_pip() {
    echo -e "${BLUE}Detected operating system: ${OS}${RESET}"
    case $OS in
        "debian"|"ubuntu")
            sudo apt update && sudo apt install -y python3 python3-pip
            ;;
        "fedora")
            sudo dnf install -y python3 python3-pip
            ;;
        "centos"|"rhel")
            sudo yum install -y python3 python3-pip
            ;;
        "macOS")
            if ! command -v python3 &> /dev/null; then
                echo -e "${YELLOW}Installing Python via Homebrew..${RESET}"
                brew install python@3
            fi
            ;;
        *)
            echo -e "${RED}For unsupported Linux distributions, please install Python 3 and pip manually.${RESET}"
            exit 1
            ;;
    esac
    python3 -m pip install --upgrade pip || { echo "pip upgrade failed"; exit 1; }
    python3 -m pip install -r requirements.txt || { echo "Dependency installation failed"; exit 1; }
}

function install_anaconda() {
    if [ ! -d "/home/anaconda3" ]; then
        if [ -d "xt_app" ]; then
            pushd xt_app || { echo "Cannot enter xt_app directory"; exit 1; }
            ./anaconda_pkg.sh || { echo "anaconda_pkg.sh execution failed"; exit 1; }
            python3 -m pip install --upgrade pip || { echo "pip upgrade failed"; exit 1; }
            python3 -m pip install -r requirements.txt || { echo "Dependency installation failed"; exit 1; }
            popd || { echo "Cannot return to previous directory"; exit 1; }
        else
            echo "xt_app directory does not exist"
            exit 1
        fi
    else
        echo "anaconda3 is already installed"
    fi
}

if [ $# -eq 0 ]; then
    usage
fi

while [ "$#" -gt 0 ]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -a|--install-anaconda)
            install_anaconda
            ;;
        -p|--install-python)
            install_python_pip
            ;;
        -f|--install-fio)
            if [ -n "$2" ]; then
                if type process_file &>/dev/null; then
                    process_file "$2"
                fi
                python3 xt_app/fio_pkg.py -fv "$2" || { echo "fio installation failed"; exit 1; }
                shift  # Skip the processed file parameter
            else
                echo "Error: -f requires specifying fio version, e.g., -f 3.1"
                exit 3
            fi
            ;;
        -n|--install-nvme-cli)
            if [ -n "$2" ]; then
                python3 xt_app/nvme-cli_pkg.py -cv "$2" || { echo "nvme-cli installation failed"; exit 1; }
                shift  # Skip the processed file parameter
            else
                echo "Error: -n requires specifying nvme-cli version, e.g., -n 1.0"
                exit 3
            fi
            ;;
        -s|--init-spdk)
            if [ ! -d "xt_platform/spdk/scripts" ]; then
                git submodule update --init --recursive || { echo "git submodule update failed"; exit 1; }
                git submodule update --remote --recursive || { echo "git submodule update failed"; exit 1; }
            fi
            pushd xt_platform/spdk || { echo "Cannot enter xt_platform/spdk/scripts directory"; exit 1; }
            sudo ./scripts/pkgdep.sh || { echo "SPDK initialization failed"; exit 1; }
            popd || { echo "Cannot return to previous directory"; exit 1; }
            ;;
        *)
            echo "Error: Unknown option '$1'"
            usage
            ;;
    esac
    shift  # Move to the next parameter
done

##config and make spdk
if [ ! -d "xt_platform/spdk/scripts" ]; then
    git submodule update --init --recursive || { echo "git submodule update failed"; exit 1; }
    git submodule update --remote --recursive || { echo "git submodule update failed"; exit 1; }
    pushd xt_platform/spdk || { echo "Cannot enter xt_platform/spdk directory"; exit 1; }
    sudo ./scripts/pkgdep.sh || { echo "SPDK initialization failed"; exit 1; }
    popd || { echo "Cannot return to previous directory"; exit 1; }
fi
pushd xt_platform/spdk || { echo "Cannot enter xt_platform/spdk directory"; exit 1; }
sudo ./configure --without-isal || { echo "SPDK configuration failed"; exit 1; }
sudo make -j32 || { echo "SPDK compilation failed"; exit 1; }
popd || { echo "Cannot return to previous directory"; exit 1; }


#build xssd_test platform
pushd xt_platform || { echo "Cannot enter xt_platform/spdk/scripts directory"; exit 1; }
sudo ./build.sh || { echo "xssd_test platform build failed"; exit 1; }


