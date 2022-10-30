# Setup a Linux Server
## Install Debian
### Prepare USB
<em>Install Debian 11 as an ISO file and write it to a USB stick.</em>
- Download [Debian](https://www.debian.org/distrib/netinst)
- Install [Rufus](https://rufus.ie/en/)

### Install from USB
1. Boot the system and select the USB
2. Create two partitions, one with mount point root '/' ext4, one swap
3. Write to disk and start installation
4. Check with spacebar to install ssh server
---

## System Preferences
### Sudo

Add user to sudoers. First switch to root user:
```
su root
```
Then add user to sudoers
```
sudo usermod -aG sudo woflje
```
Then open a config to remove the password requirement for sudo:
```
sudo visudo
```
Add the line `woflje ALL=(ALL:ALL) NOPASSWD:ALL`

### Text Mode
Make the system boot in textmode:
```
sudo systemctl set-default multi-user.target
```
### SSH
Add the public key from a USB drive:
```
sudo mkdir /media/usbstickname
lsblk
sudo mount /dev/sda1 /media/usbstickname
sudo cp /media/usbstickname/authorized_keys /home/woflje/.ssh/authorized_keys
```
Remove the option to use password to ssh into the server:
```
sudo nano /etc/ssh/sshd_config
```
Change the following to:\
`ChallengeResponseAuthentication no`\
`PasswordAuthentication no`\
`UsePAM no`\
`PermitRootLogin no`

### WakeOnLAN
Install wakeonlan
```
sudo apt install wakeonlan
```
Find the mac address
```
ip a
```
Then from another system use
```
wakeonlan -i <ip> <mac>
```

### Reboot into windows
<em>Make sure to have chrome remote desktop enabled</em>\
Edit a file
```
sudo vim /etc/default/grub
```
Replace `GRUB_DEFAULT=0` with `GRUB_DEFAULT=saved`\
Create a bashfile
```
vim reboot_to_windows.sh
```
And in there write
```
sudo grub-reboot "$(grep -i windows /boot/grub/grub.cfg|cut -d"'" -f2)" && sudo reboot
```
Then do
```
chmod +x reboot_to_windows.sh
```
After, you can use
```
./reboot_to_windows.sh
```
To reboot into windows