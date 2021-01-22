Title: Extending The Battery Life in Linux
SubTitle: A Walkthrough to How I managed to extend my laptop battery life
Date: 2016-02-25 14:20
Category: Linux
Tags: linux, powertop, power


Before Running any tunning, the average estimated lifetime of my battery was
about 3 hours (below image). Through this post we learn how to extend it to
almost 4 and a half hours. It's more than 50 percent increase!

> **Note**: I'm currently using a lenovo G50 laptop with Quad-Core AMD CPU equiped
with a 4-cell battery and running `i3-wm`, a lightweight tilling window manager
(no Gnome/KDE craps for me) on ArchLinux.
So depending on your hardware and programs you have running and your daily usage
pattern, the results may vary for you.

![Gnome Battery Bench]({static}/assets/images/extend_linux_battery_life-battery_bench_before_tunning.png "Gnome Battery Bench - Before Tunning")

First, run `powertop` to find out which devices/processes are draining power the most.
In The `Overview Tab` you can actually see what processes/devices are draining
how much power and By applying the Good option in `Tunables Tab`, powertop
automatically tunes them. you can do this manually for every item in Tunable tab
or just use the `--auto-tune` option.

```
$ sudo powertop --auto-tune
```

That single command will probably add a noticeable extra minutes to your battery
life. But there are still other ways to improve it more. Let's Go to powertop's
`Overview Tab` again:

```
Power est.  Usage        Events/s    Category    Description
  5.18 W    0.4 pkts/s               Device      Network interface: wlp2s0 (wl)
  3.80 W    100.0%                   Device      Display backlight
  1.26 W    165.5 ms/s   123.3       Process     /usr/share/atom/atom --type=zygote --no-sandbox
  675 mW    95.9 ms/s    5.3         Process     atom
  660 mW    94.0%                    Device      USB device: USB2.0-CRW (Generic)
  262 mW    27.0 ms/s    90.1        Process     /usr/share/atom/atom --executed-from=/home/bijan --pid=1109
  247 mW    27.2 ms/s    70.4        Process     /usr/lib/xorg-server/Xorg :0 -seat seat0 -auth /run/lightdm/root/:0 -nolisten tc
  103 mW    2.0 ms/s     109.7        kWork      od_dbs_timer
```

According to above, after my wireless interface (which i use), the display backlight,
USB CD-RW and my Ethernet interface are the most draining power sources.
The last two I never/rarely use.

### Turning Off unnecessary devices

Since I never/rarely use my CD-RW and I never connect to Internet through wired
connection, so it seems logical to me to disable them. to find my CD-RW device
power location, I used powertop `Tunable Tab`:

```
# Disable CR-RW
$ echo 0 | s tee /sys/bus/usb/devices/1-1.3/power/autosuspend_delay_ms
$ echo auto | s tee /sys/bus/usb/devices/1-1.3/power/control
```

To disable my Ethernet device, first I have to find it's device number:

```
# Find Ethernet domain:bus:slot number
$ lspci | grep -i ethernet
03:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller (rev 10)

# Find relative device on /sys/devices
$ find /sys/devices -name "*03:00.0"
/sys/devices/pci0000:00/0000:00:02.4/0000:03:00.0

# Turn off device
echo 1 | s tee /sys/devices/pci0000:00/0000:00:02.4/0000:03:00.0/remove
```

### Backlight

To reduce the brightness LED backlight, I set a brightness value (between 0 and 255):

```
# Brightness
basedir="/sys/class/backlight/"
handler=$basedir$(ls $basedir)"/"

chmod 666 $handler/brightness
echo 100 > handler/brightness
```

# Running as a Service

To execute the above commands at boot up, I created a shell script and run that
as a service.

```
#!/bin/bash
# /usr/local/bin/powertop_tuning.sh

# Auto-tune powertop
powertop --auto-tune

# Disable CR-RW
echo 0 | s tee /sys/bus/usb/devices/1-1.3/power/autosuspend_delay_ms
echo auto | s tee /sys/bus/usb/devices/1-1.3/power/control

# Disable Ethernet
echo 1 | s tee /sys/devices/pci0000:00/0000:00:02.4/0000:03:00.0/remove

# Brightness
chmod 666 /sys/class/backlight/radeon_bl0/brightness
echo 80 > /sys/class/backlight/radeon_bl0/brightness
```

And to create proper systemd service:

```
# /etc/systemd/system/powertop_tuning.service
[Unit]
Description="PowerTop Tuning config"
ConditionPathExists=/usr/local/bin/powertop_tuning.sh

[Service]
Type=oneshot
RemainAfterExit=yes
KillMode=none
ExecStart=/usr/local/bin/powertop_tuning.sh
ExecStop=exit

[Install]
WantedBy=multi-user.target
```

So, to make `powertop_tuning` service run automatically, just enable the service:

```
$ sudo systemctl enable powertop_tuning.service
```

# Conclusion

The result is very satisfactory. In daily usage, my battery life went up
from about 3 hours to almost 4 and a half hours.

![Gnome Battery Bench]({static}/assets/images/extend_linux_battery_life-battery_bench_after_tunning.png "Gnome Battery Bench - After Tunning")

> **Disclaimer**: The tests and battery benchmark did not placed in a controlled
environment but it seems logical to expect similar effects.
