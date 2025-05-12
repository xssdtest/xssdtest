#! /usr/bin/python3
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
import os
import requests
import tarfile
import argparse
from tqdm import tqdm
def download_file(cli_version):
    """
    Downloads the source code package of nvme-cli for the specified version.

    Args:
        cli_version (str): The version number of nvme-cli, used to construct the download URL and filename.

    This function downloads the specified version of the nvme-cli source code package from GitHub and displays the download progress.
    """
    url = f"https://github.com/linux-nvme/nvme-cli/archive/refs/tags/{cli_version}.tar.gz"
    filename = f"nvme-cli-{cli_version}.tar.gz"

    print(f"Downloading nvme-cli source code ({cli_version})...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Get the total file size and initialize the progress bar
    total_size = int(response.headers.get("content-length", 0))
    progress = tqdm(total=total_size, unit="B", unit_scale=True)

    # Write the downloaded file to local storage
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                progress.update(len(chunk))
    progress.close()

def extract_tar(cli_version):
    """
    Extracts the nvme-cli source code package for the specified version.

    Args:
        cli_version (str): The version number of nvme-cli, used to construct the filename.

    This function extracts the downloaded tar.gz file to the current directory.
    """
    filename = f"nvme-cli-{cli_version}.tar.gz"
    print("Extracting source package...")
    with tarfile.open(filename, "r:gz") as tar:
        tar.extractall()

def get_extracted_dir():
    """
    Retrieves the directory name of the extracted nvme-cli source code.

    Returns:
        str: The name of the extracted directory.

    This function searches for directories in the current directory that start with "nvme-cli-" and returns the first matching directory name.
    If no directory is found, it raises a FileNotFoundError.
    """
    dirs = [d for d in os.listdir() if os.path.isdir(d) and d.startswith("nvme-cli-")]
    if not dirs:
        raise FileNotFoundError("Extracted directory not found")
    return dirs[0]

if __name__ == "__main__":
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="cli package downloader")
    # Add the nvme-cli version argument
    parser.add_argument("-cv", "--cli_version", type=str, dest="cli_version", default="v1.16", help="nvme-cli version, default is v1.16")
    # Parse the command-line arguments
    args = parser.parse_args()
    # Get the nvme-cli version
    cli_version = args.cli_version
    try:
        # Download the source code
        download_file(cli_version)

        # Extract the file
        extract_tar(cli_version)

        # Get the extracted directory
        source_dir = get_extracted_dir()
        print(f"Source directory: {source_dir}")

        # Compile and install
        os.chdir(source_dir)
        if os.system("make") == 0:
            print("Compilation successful")
        else:
            print("Compilation failed")
            exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        exit(1)
