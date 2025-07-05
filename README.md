# VM File Transfer Project

A guide to transferring files from a host PC to a Linux Virtual Machine (VM) using Python HTTP server and client scripts.

## Overview

This project explains how to transfer files from a host PC (IP: `172.20.10.x`) to a Linux Virtual Machine (IP: `10.0.2.x`) using Python scripts. The VM runs a server ([`file_server.py`](#)) to receive files, and the host runs a client ([`file_client.py`](#)) to send them over HTTP on port `8000`.

**Network Details:**
- **Wireless LAN Adapter Wi-Fi:**
  - **IPv4 Address**: `172.20.10.x`
  - **Subnet Mask**: `255.255.255.0`
  - **Default Gateway**: `172.20.10.x`

## Requirements

- **Python 3.12** installed on both host and VM (e.g., `sudo apt install python3` on Debian-based VM).
- [**`requests` library**](#) on the host (`pip install requests`).
- [**`lsof`**](#) on the VM for port management (`sudo apt install lsof`).
- Port `8000` open on the VM's firewall (`sudo ufw allow 8000`).
- Network connectivity between host and VM (Bridged mode in VM software).

## Setup

### On the VM (Server)
1. Save [`file_server.py`](#) to a directory (e.g., `/home/YourName`).
2. Ensure the upload directory (`/tmp/uploads`) has write permissions.
3. Install dependencies:
   ```bash
   sudo apt install python3 lsof

### On the Host (Client)
1. Save the file_client.py script to a directory.
2. Install requests: pip install requests.
3. Update the server_url to http://10.0.2.xx:8000 and file_path to your file's path.

Full Guide at: https://www.jinetinnovations.com/ee101/file_transfer_guide.html
