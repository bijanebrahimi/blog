Title: OpenBSD hotplugd scripting
SubTitle: Mount removable USB devices when attached
Date: 2017-12-26 22:31
Category: OpenBSD
Tags: openbsd, hotplugd, mount

## The OpenBSD hotplugd script

> The hotplugd daemon monitors the [hotplug(4)][1] pseudo-device, acting on
> signaled events by executing the scripts in the `/etc/hotplug` directory.

The following is a modified version of [TuM'Fatig's Automount USB stick on OpenBSD][2].
You can also find [My OpenBSD Setup][3] post describing my personal experience
with OpenBSD as a desktop.

```sh
$ doas rcctl enable hotplugd
$ cat /etc/hotplug/attach
#!/bin/sh

DEVCLASS=$1
DEVNAME=$2
MOUNTROOT="/mnt"
DEBUG=1
export DISPLAY=:0.0
export HOME=/home/bijan

case $DEVCLASS in
2)
        # disk devices
        /sbin/disklabel $DEVNAME 2>&1 | awk -F '[ ]*' '/^  [abd-z]:/' | while read line;
        do
                slice=`echo $line | awk -F ':' '{print $1}'`
                fs=`echo $line | awk -F '[ ]*' '{print $4}'`
                case $fs in
                MSDOS | ISO9660 | ext2fs | 4.2BSD)
                        [ $DEBUG == 1 ] && logger -i "hotplugd attaching SLICE $slice of DEVICE $DEVNAME"
                        [ ! -d $MOUNTROOT/$DEVNAME$slice ] && mkdir -p -m 1777 $MOUNTROOT/$DEVNAME$slice
                        mount -o ro /dev/$DEVNAME$slice $MOUNTROOT/$DEVNAME$slice;
                        /usr/local/bin/notify-send "Mounted $DEVNAME$slice ($fs)"
                        ;;
                esac
        done
        ;;
3)
	# network devices; requires hostname.$DEVNAME
	sh /etc/netstart $DEVNAME
	;;
esac
```

[1]: http://man.openbsd.org/hotplugd.8
[2]: https://www.tumfatig.net/20110903/automount-usb-stick-on-openbsd/
[3]: {filename}/openbsd/my-openbsd-setup.md

