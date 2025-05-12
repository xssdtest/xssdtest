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
import sys
import os
import signal
import time
import datetime
import argparse
import paramiko
import socket
class SSH(object):
    """
    SSH class for securely connecting to a remote host.

    This class uses the `paramiko` library to establish an SSH connection to a remote machine.
    It initializes with user credentials and hostname, sets up automatic host key acceptance,
    and establishes the connection during initialization.

    Attributes:
        ssh (paramiko.SSHClient): The SSH client instance used to interact with the remote host.
        close_flag (bool): A flag indicating whether the connection is closed.
        user (str): The username used for authentication.
        password (str): The password used for authentication.
        hostname (str): The IP address or hostname of the remote system.
    """

    def __init__(self, user=None, password=None, hostname=None):
        """
        Initialize a new SSH connection instance.

        Establishes an SSH connection using provided credentials and hostname.
        Uses AutoAddPolicy to automatically accept unknown host keys.

        Parameters:
            user (str): Username for SSH authentication.
            password (str): Password for SSH authentication.
            hostname (str): Hostname or IP address of the target SSH server.

        Raises:
            paramiko.AuthenticationException: If login credentials are invalid.
            paramiko.SSHException: If there's an SSH protocol issue.
            Exception: For any other general connection failure.
        """
        self.close_flag = False
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.user = user
        self.password = password
        self.hostname = hostname
        self.ssh.connect(hostname=self.hostname, port=22, username=self.user, password=self.password)


    def con_ready(self, timeout=10):
        """
        Checks if the SSH connection to the remote host is ready by attempting to establish a socket connection to port 22.

        This method tests whether the target host is reachable over SSH by creating and closing
        a low-level TCP socket connection to port 22. It does not perform full SSH authentication,
        just checks for connectivity.

        Parameters:
            timeout (int): Connection timeout in seconds. Default is 10 seconds.

        Returns:
            bool: True if the connection can be established (host is reachable on port 22),
                  False otherwise (connection timed out or was refused).

        Example:
            >>> ssh = SSH(hostname='192.168.1.100')
            >>> ssh.con_ready()
            True
        """
        try:
            # Set global default timeout for socket operations
            socket.setdefaulttimeout(timeout)
            # Attempt to connect and immediately close the socket
            socket.create_connection((self.hostname, 22)).close()
            return True  # Connection successful
        except socket.error:
            return False  # Connection failed


    def reconnect(self, timeout=5 * 60, wait_time=10):
        """
        Attempts to re-establish an SSH connection to the remote server within a specified timeout.

        This method repeatedly checks if the host is reachable (via `con_ready()`) and attempts
        to reconnect using SSH. It will continue retrying at intervals until the total timeout
        is reached.

        Parameters:
            timeout (int): Total time in seconds to keep trying to reconnect. Default is 300 seconds (5 minutes).
            wait_time (int): Time in seconds to wait between each reconnection attempt. Default is 10 seconds.

        Returns:
            None: If connection is successfully re-established, it breaks the loop and returns silently.

        Raises:
            AssertionError: If the connection cannot be re-established within the specified timeout period.
        """
        stime = time.time()
        while time.time() - stime < timeout:
            if self.con_ready():
                try:
                    self.ssh.connect(hostname=self.hostname, port=22, username=self.user, password=self.password)
                    break
                except:
                    pass  # Try again if connection fails temporarily
            time.sleep(wait_time)
        else:
            # Final attempt after timeout
            if self.con_ready():
                self.ssh.connect(hostname=self.hostname, port=22, username=self.user, password=self.password)
            else:
                assert False, print("Reconnect to hostname %s failed after timeout of %s seconds" % (self.hostname, timeout))

    def session_run(self, cmdline):
        """
        Execute a command on the remote host using an SSH session.

        :param cmdline: The command to be executed on the remote host.
        :return:
            - 0 if the command executes successfully.
            - -1 if the SSH connection fails.
            - 1 or other values if the command execution encounters an error.
        """
        # Open an SSH session
        session = self.ssh.get_transport().open_session()
        # Print the command being executed with a timestamp
        print("%s@xt:%s $%s" % (self.user, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cmdline))
        # Execute the command on the remote host
        session.exec_command(cmdline)
        # Initialize variables for output collection and loop control
        output, endline = '', True
        # Combine standard error with standard output for simplified handling
        session.set_combine_stderr(True)
        # Prepare to read the command output
        stdout = session.makefile("r", -1)
        # Get the channel for non-blocking reads
        channel = stdout.channel
        # Set the channel to non-blocking mode
        channel.setblocking(False)
        # Enable keepalive to maintain the connection
        transport = channel.get_transport()
        transport.set_keepalive(60)
        # Continuously read the output until the command execution is complete
        while not channel.exit_status_ready():
            try:
                output = channel.recv(512)
            except TimeoutError:
                print(datetime.datetime.now(), "recv data timeout")
                continue
            except paramiko.SSHException as e:
                print("connect error %s"%e)
                break
            except Exception:
                continue
            if output:
                output = output.decode('utf-8', 'ignore')
                print(output, end='')
                endline = True if output[-1] == '\n' else False
        # Ensure a newline is printed if the output doesn't end with one
        if not endline:
            print()
        # Check the connection status and close the SSH connection if needed
        if not self.con_ready():
            self.close_flag = True
            self.ssh.close()
            return -1
        # Return the command execution status
        return 0 if channel.exit_status == 0 else 1


    def execute_command(self, command, timeout=10):
        """
        Executes a command on the remote host over SSH and returns its output and error streams.

        Functionality:
        - Runs the specified command on the remote system using SSH.
        - Reads both standard output and standard error from the command execution.
        - Handles exceptions gracefully by returning an error code if an exception occurs.

        Parameters:
        - command (str): The shell command to execute on the remote host.
        - timeout (int): The maximum time (in seconds) to wait for the command to complete. Default is 10 seconds.

        Returns:
        - tuple: A tuple containing two strings: (stdout_output, stderr_output).
        - int: Returns -1 if any exception occurs during execution.
        """
        try:
            # Execute the command over SSH and capture stdin/stdout/stderr
            stdin, stdout, stderr = self.ssh.exec_command(command, timeout=timeout)

            # Read and decode output streams
            output = stdout.read().decode()
            error = stderr.read().decode()

            # Return captured output and error
            return output, error
        except Exception as e:
            # On any exception, return error code -1
            return -1

    def ssh_ftp(self, from_path, to_path, method="get"):
        """
        Transfers files via SFTP between local and remote systems.

        This method uses Paramiko's SFTP client to transfer files either from or to the remote host.
        It supports two modes:
          - "get": Download a file from the remote host to the local system.
          - "put": Upload a file from the local system to the remote host.

        Parameters:
            from_path (str): Source file path. For "get", it's a remote path; for "put", it's a local path.
            to_path (str): Destination file path. For "get", it's a local path; for "put", it's a remote path.
            method (str): Transfer direction. Valid values are:
                          - "get" (default): Copy file from remote to local.
                          - "put": Copy file from local to remote.

        Returns:
            None: No explicit return value, but raises exceptions on failure.

        Raises:
            paramiko.SFTPError: If an SFTP-related error occurs during transfer.
            IOError: If there are issues accessing local files.
            Exception: For any unexpected error during the transfer process.
        """
        # Create an SFTP client using the existing SSH transport
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())

        # Perform the file transfer based on the specified method
        if method == "get":
            # Download file from remote to local
            sftp.get(from_path, to_path)
        elif method == "put":
            # Upload file from local to remote
            sftp.put(from_path, to_path)
