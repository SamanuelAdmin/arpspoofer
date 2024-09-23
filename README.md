# [Test varsion] Modules for simple MITM atack

#### [DISCLAIMER] Its just software for pentesting. Do not use for atack, which can harm someone network or devices!
<br>

#### This script is only for linux! Has been tested on manjaro.

![photo_2024-09-23_23-10-31](https://github.com/user-attachments/assets/947e5fbf-4cad-4264-9509-8c35a030c8ed)

<strong>ARP spoofing</strong> is a network attack where an attacker sends falsified ARP (Address Resolution Protocol) messages over a local network. 
The goal is to associate the attacker's MAC (Media Access Control) address with the IP address of a legitimate device on the network. 
Once the attacker is linked to the victim’s IP, they can intercept, modify, or block traffic intended for that device.

<br>

[![ARPPoisoningSpoofing](https://github.com/user-attachments/assets/793a4b69-352d-437a-91e8-f7b6a29237cb)](https://img.youtube.com/vi/example/maxresdefault.jpg)

<br>
<br>

#### How to use it?

<ol>
  <li><strong>Install dependencies</strong></li>
  
  ```
pip3 install scapy
pip install uuid
  ```

  <li><strong>Start as an admin</strong></li>
  Use this syntax:

  ```
sudo python3 arpspoofer.py -rip ROUTER_IP -rm ROUTER_MAC -cip CLIENT_IP -cm CLIENT_MAC
  ```
  For example:
  sudo python3 arpspoofer.py -rip 192.168.68.1 -rm f0:a7:31:fd:f0:68 -cip 192.168.68.202 -cm dc:85:de:1e:8e:21
  
</ol>
