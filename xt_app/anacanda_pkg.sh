#!/bin/bash
set -e

# Dependency management function
check_dependencies() {
    # Check if curl is installed
    if ! command -v curl &> /dev/null; then
        echo "Detected missing dependency: curl"
        echo "Attempting to install automatically..."

        # Install curl based on the available package manager
        if command -v apt-get &> /dev/null; then
            sudo apt-get update -qq && sudo apt-get install -y curl
        elif command -v yum &> /dev/null; then
            sudo yum install -y curl
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y curl
        elif command -v zypper &> /dev/null; then
            sudo zypper install -y curl
        elif command -v pacman &> /dev/null; then
            sudo pacman -Sy --noconfirm curl
        elif command -v brew &> /dev/null; then
            brew install curl
        else
            echo "Error: Unable to install curl automatically. Please install it manually and rerun the script."
            echo "Installation instructions:"
            echo "  Debian/Ubuntu: sudo apt install curl"
            echo "  RHEL/CentOS:   sudo yum install curl"
            echo "  macOS:         brew install curl"
            exit 1
        fi

        # Verify if the installation was successful
        if ! command -v curl &> /dev/null; then
            echo "Failed to install curl. Please install it manually and try again."
            exit 1
        fi
        echo "curl installed successfully"
    fi
}

# Platform detection function
# Returns: The current operating system platform (Linux, MacOSX, Windows, Unknown)
get_platform() {
    case "$(uname -s)" in
        Linux*)  echo "Linux";;
        Darwin*) echo "MacOSX";;
        *CYGWIN*|*MINGW*|*MSYS*) echo "Windows";;
        *)       echo "Unknown";;
    esac
}

# Architecture detection function
# Returns: The current system architecture (x86_64, arm64, x86, Unknown)
get_arch() {
    case "$(uname -m)" in
        x86_64)  echo "x86_64";;
        arm64)   echo "arm64";;
        aarch64) echo "arm64";;
        i*86)    echo "x86";;
        *)       echo "Unknown";;
    esac
}

# Installer package finder function
# Parameters:
#   $1: Platform type (Linux, MacOSX, Windows)
#   $2: Architecture type (x86_64, arm64, x86)
# Returns: The filename of the latest Anaconda installer package
find_latest_installer() {
    local platform=$1
    local arch=$2

    # Fetch the list of all installer packages from the Anaconda repository and filter the latest one matching the platform and architecture
    curl -s https://repo.anaconda.com/archive/ | \
    grep -Eo 'href="Anaconda3-[^"]*' | \
    sed 's/href="//' | \
    awk -v plat="$platform" -v arch="$arch" -F- '
    {
        split($2, date, ".");
        year = date[1];
        month = date[2];
        split($3, build, "-");
        build_num = build[1];

        file_plat = $4;
        file_arch = $5;
        sub(/\..*/, "", file_arch);

        if (file_plat == plat && file_arch == arch) {
            printf "%04d%02d%03d %s\n", year, month, build_num, $0
        }
    }' | \
    sort -nr | \
    head -1 | \
    awk '{print $2}'
}

# Main function
main() {
    check_dependencies  # First, check dependencies

    platform=$(get_platform)
    arch=$(get_arch)

    echo "Detected platform: $platform/$arch"

    if [[ "$platform" == "Unknown" || "$arch" == "Unknown" ]]; then
        echo "Error: Unsupported platform/architecture combination"
        exit 1
    fi

    installer=$(find_latest_installer "$platform" "$arch")

    if [ -z "$installer" ]; then
        echo "Error: Unable to find an installer for $platform/$arch"
        echo "Possible reasons:"
        echo "1. Network connection issue"
        echo "2. Anaconda has changed its naming convention"
        echo "3. Incompatible architecture (try x86_64)"
        exit 1
    fi

    echo "Downloading: $installer"
    curl -# -O "https://repo.anaconda.com/archive/$installer"
    echo "Download complete. File size: $(du -sh "$installer" | cut -f1)"
    sudo chmod 777 "$installer"
    sudo ./$installer -b -p /home/anaconda3
    sudo ln -fs /home/anaconda3/bin/python /usr/bin/python3
    sudo ln -fs /home/anaconda3/bin/python /bin/python3
    rm -fr $installer
}

# Execute the main program
main
