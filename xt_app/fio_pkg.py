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
import argparse
import requests
import sys
import time
import math
import tarfile
import shutil
def convert_size(size_bytes):
    """
    Convert the number of bytes into a human-readable format.

    Parameters:
    size_bytes (int): The number of bytes to convert.

    Returns:
    str: The converted human-readable string, e.g., "1.23 MB".
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def download_fio(version):
    """
    Download the specified version of the fio package and extract it.

    Parameters:
    version (str): The version number of fio, e.g., "3.19".

    Returns:
    None: The function exits the program upon successful execution.
    """
    url = f"https://github.com/axboe/fio/archive/refs/tags/fio-{version}.tar.gz"
    filename = f"fio-{version}.tar.gz"
    extract_dir = f"fio-fio-{version}"

    # Check if the file already exists
    if os.path.exists(filename):
        # If the directory already exists, skip the download
        if os.path.isdir(extract_dir):
            print(f"{extract_dir} already exists, skip download")
            sys.exit(0)
        else:
            # If the file is successfully downloaded, extract it
            print(f"\nStarting to extract {filename}...")
            with tarfile.open(filename, 'r:gz') as tar:
                tar.extractall()

            # Check if the extraction directory exists
            if not os.path.exists(extract_dir):
                raise Exception(f"Extraction directory {extract_dir} does not exist")

            print(f"File extracted to: {extract_dir}")

    try:
        # Send an initial request to get file information
        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()

            # Get the total file size
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()

            # Display initial progress information
            print(f"Downloading file: {filename}")
            print(f"File size: {convert_size(total_size) if total_size else 'Unknown'}")

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Calculate download progress
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed if elapsed > 0 else 0

                        # Progress display logic
                        if total_size > 0:
                            percent = downloaded / total_size * 100
                            status = f"{percent:.1f}% [{convert_size(downloaded)} / {convert_size(total_size)}]"
                        else:
                            status = f"{convert_size(downloaded)}"

                        speed_status = f"{convert_size(speed)}/s"

                        # Dynamically update progress information
                        sys.stdout.write(f"\rProgress: {status.ljust(30)} Speed: {speed_status.ljust(15)}")
                        sys.stdout.flush()

            # Print a new line after download completes
            print("\nDownload complete!")
            print(f"File saved to: {filename}")

    except KeyboardInterrupt:
        print("\n\nDownload interrupted, deleting incomplete file")
    except Exception as err:
        print(f"\nAn error occurred: {str(err)}")

    # If the file is successfully downloaded, extract it
    print(f"\nStarting to extract {filename}...")
    with tarfile.open(filename, 'r:gz') as tar:
        tar.extractall()

    # Check if the extraction directory exists
    if not os.path.exists(extract_dir):
        raise Exception(f"Extraction directory {extract_dir} does not exist")

    print(f"File extracted to: {extract_dir}")

    # Display installation instructions
    os.chdir(extract_dir)
    os.system("make")
    if os.path.exists("fio"):
        print("Compilation successful")
    else:
        print("Please install the required dependencies first:")


if __name__ == "__main__":
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="fio package downloader")
    # Add the fio version argument
    parser.add_argument("-fv", "--fio_version", type=str, dest="fio_version", default="3.19", help="fio version, default is 3.19")
    # Parse the command-line arguments
    args = parser.parse_args()
    # Get the fio version
    version = args.fio_version
    try:
        download_fio(version)
    except Exception as err:
        print(f"\nAn error occurred: {str(err)}")
        sys.exit(1)




