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
import requests
from bs4 import BeautifulSoup
import re
import platform
import os

def get_platform_info():
    """
    Retrieves the current platform and architecture information.

    This function uses the `platform` module to fetch the operating system name and architecture,
    and then converts them into a standardized format. If the operating system or architecture
    is unsupported, the function raises a `ValueError`.

    Returns:
        tuple: A tuple containing two elements. The first element is the platform name
               (e.g., 'Linux', 'Windows', 'MacOSX'), and the second element is the
               architecture name (e.g., 'x86_64', 'arm64').

    Raises:
        ValueError: If the operating system or architecture is unsupported.
    """
    system = platform.system()
    machine = platform.machine()

    # Convert system name to a standardized platform name
    if system == 'Linux':
        plat = 'Linux'
    elif system == 'Windows':
        plat = 'Windows'
    elif system == 'Darwin':
        plat = 'MacOSX'
    else:
        raise ValueError(f"Unsupported system: {system}")

    # Convert architecture information to a standardized architecture name
    if machine in ('x86_64', 'AMD64'):
        arch = 'x86_64'
    elif machine in ('arm64', 'aarch64'):
        arch = 'arm64'
    else:
        raise ValueError(f"Unsupported architecture: {machine}")

    return plat, arch


def get_installer_links():
    """
    Retrieve all installer package links.

    This function accesses the Anaconda archive repository page, parses its content, and extracts all links that end with .sh, .exe, or .pkg.

    Returns:
        list: A list containing all valid installer package links. If the page access fails, the program will exit and display an error message.
    """
    url = 'https://repo.anaconda.com/archive/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Attempt to access the Anaconda archive repository page; exit the program and display an error message if the request fails
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Failed to access repository: {e}")

    # Parse the page content using BeautifulSoup and extract all valid links
    soup = BeautifulSoup(response.text, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True)
            if a['href'].endswith(('.sh', '.exe', '.pkg'))]


def parse_filename(filename):
    """
    Parses the filename to extract information such as year, month, build number, platform, and architecture.

    Parameters:
    filename (str): The filename to be parsed, expected in the format 'Anaconda3-YYYY.MM-Build-Platform-Arch.ext'.

    Returns:
    dict: A dictionary containing the parsed information with the following key-value pairs:
        - 'version': A tuple containing the year, month, and build number (year, month, build).
        - 'platform': The platform name, e.g., 'Linux', 'Windows', 'MacOSX'.
        - 'arch': The architecture name, e.g., 'x86_64', 'arm64'.
        - 'filename': The original filename.

    If the filename does not match the expected format, returns None.
    """
    pattern = r'''
        ^Anaconda3-
        (\d{4})\.(\d{2})-  # Year and month
        (\d+)-              # Build number
        (Linux|Windows|MacOSX)-
        (x86_64|arm64)      # Architecture
        \.(sh|exe|pkg)$     # File extension
    '''
    # Use regex to match the filename
    match = re.fullmatch(re.compile(pattern, re.X), filename)
    if not match:
        return None

    # Extract and convert year, month, and build number to integers
    year, month, build = map(int, match.groups()[:3])

    # Return the parsed information as a dictionary
    return {
        'version': (year, month, build),
        'platform': match.group(4),
        'arch': match.group(5),
        'filename': filename
    }


def find_latest_installer(target_platform, target_arch):
    """
    Finds and returns the latest installer package for the specified platform and architecture.

    Parameters:
    target_platform (str): The target platform, e.g., 'Linux', 'Windows', 'MacOSX'.
    target_arch (str): The target architecture, e.g., 'x86_64', 'arm64'.

    Returns:
    dict: A dictionary containing information about the latest installer package, including version, platform, architecture, and filename.

    Raises:
    ValueError: If no installer is found for the specified platform and architecture.
    """
    installers = []
    # Iterate through all installer links, parse the filename, and filter by platform and architecture
    for link in get_installer_links():
        info = parse_filename(link)
        if info and info['platform'] == target_platform and info['arch'] == target_arch:
            installers.append(info)

    # Raise an error if no matching installer is found
    if not installers:
        raise ValueError("No available installer for current platform")

    # Sort installers by version in descending order to get the latest one
    installers.sort(key=lambda x: x['version'], reverse=True)
    return installers[0]


def download_with_progress(url, filename):
    """
    Downloads a file with progress display.

    This function downloads a file from the specified URL and saves it to the given filename. It displays the download progress in real-time. If the download fails, the incomplete file is deleted, and an error message is displayed.

    Parameters:
    url (str): The URL of the file to be downloaded.
    filename (str): The name of the file to save the downloaded content.

    Returns:
    None. The function prints the download progress and the final save location of the file. If the download fails, it exits the program with an error message.
    """
    try:
        # Initiate an HTTP GET request with streaming enabled
        with requests.get(url, stream=True) as r:
            # Check if the request was successful; raise an exception if not
            r.raise_for_status()
            # Get the total size of the file from the response headers
            total_size = int(r.headers.get('content-length', 0))

            # Open the file in binary write mode
            with open(filename, 'wb') as f:
                downloaded = 0
                # Read the file in chunks and write to the local file
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    # Print the download progress, overwriting the same line
                    print(f"Download progress: {downloaded}/{total_size} bytes ({downloaded / total_size:.2%})", end='\r')
    except requests.exceptions.RequestException as e:
        # If the download fails, delete the incomplete file
        os.remove(filename)
        # Exit the program and display the error message
        raise SystemExit(f"Download failed: {e}")

    # Print the final save location of the file
    print(f"\nFile saved to: {os.path.abspath(filename)}")


if __name__ == "__main__":
    # Initialize a variable to store the latest installer information
    latest = None
    try:
        # Retrieve platform information to determine the target platform and architecture
        target_platform, target_arch = get_platform_info()
        print(f"Target platform: {target_platform}/{target_arch}")

        # Find the latest installer package compatible with the target platform and architecture
        latest = find_latest_installer(target_platform, target_arch)
        print(f"Latest version found: {latest['filename']}")

        # Check if the file already exists; if it does, exit the program
        if os.path.exists(latest['filename']):
            print(f"File already exists: {latest['filename']}")
            exit(0)

        # Construct the download URL and initiate the download with progress display
        download_url = f"https://repo.anaconda.com/archive/{latest['filename']}"
        print(f"Starting download: {download_url}")
        download_with_progress(download_url, latest['filename'])

        # If the downloaded file is a shell script, make it executable
        if latest['filename'].endswith('.sh'):
            os.chmod(latest['filename'], 0o777)
    except Exception as e:
        # Handle and print any exceptions that occur during the process
        print(f"An error occurred: {str(e)}")

        # If an error occurs and a file was partially downloaded, remove it
        if latest and os.path.exists(latest['filename']):
            os.remove(latest['filename'])

