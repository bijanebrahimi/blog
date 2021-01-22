Title: Raspberry pi 3 as Home Wireless Router
SubTitle: A simple script to create a Home Wireless Router
Date: 2021-01-22 14:37
Category: Linux
Tags: linux, rasbperry pi, debian, buster, raspbian, router, wireless

I use The following script to configure a Raspbian OS on a Raspberry Pi 3
as a home wireless router.

**Note:** Please configure the following variable before running the script.


```sh
DEVICE=wlan1
PASWORD=password
HOST=10.0.0.1
DHCP_RANGE=10.0.0.2,10.0.0.20
COUNTRY_CODE=uk
SSID=home-router
DNS_1=1.0.0.1
DNS_2=1.1.1.1

apt update && apt upgrade

# Enable the wireless access point service and set it to start when your
# Raspberry Pi boots:
apt install hostapd dnsmasq && \
systemctl unmask hostapd && \
systemctl enable hostapd

# Enable the wireless access point service and set it to start when your
# Raspberry Pi boots:
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

# Define the wireless interface IP configuration:
cat >> /etc/dhcpcd.conf <<EOF
interface ${DEVICE}
    static ip_address=${HOST}/24
    static domain_name_servers=${DNS_1} ${DNS_2}
    nohook wpa_supplicant
EOF

# Enable routing and IP masquerading
cat > /etc/sysctl.d/routed-ap.conf <<EOF
# https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md
# Enable IPv4 routing
net.ipv4.ip_forward=1
EOF

#systemctl reboot

# update-alternatives --set iptables /usr/sbin/iptables-legacy
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
netfilter-persistent save

# Configure the DHCP and DNS services for the wireless network:
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat > /etc/dnsmasq.conf <<EOF
interface=${DEVICE} # Listening interface
dhcp-range=${DHCP_RANGE},255.255.255.0,24h
domain=wlan
address=/gw.wlan/${HOST}
EOF

# Ensure wireless operation
rfkill unblock wlan

# Configure the access point software:
cat > /etc/hostapd/hostapd.conf <<EOF
country_code=${COUNTRY_CODE}
interface=${DEVICE}
ssid=${SSID}
hw_mode=g
#hw_mode=a      # IEEE 802.11a (5 GHz)
#hw_mode=b      # IEEE 802.11b (2.4 GHz)
#hw_mode=g      # IEEE 802.11g (2.4 GHz)
#hw_mode=ad     # IEEE 802.11ad (60 GHz) 
channel=7
macaddr_acl=0
auth_algs=3
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=${PASWORD}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

systemctl reboot
```
