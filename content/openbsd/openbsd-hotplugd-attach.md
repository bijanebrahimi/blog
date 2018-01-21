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

**UPDATE 2018-01-21**: Since [BSDNow][4] guys kindly mentioned this script at one of their
[latest episode][5], I managed to look at it again and enhance the script,
specifically permission-wise. So mounting MSDOS and NTFS partitions are now done
with proper user and grup permissions:

```sh
#!/bin/sh

DEVCLASS=$1
DEVNAME=$2
MOUNTROOT="/mnt"
DEBUG=1
mount_helper=/sbin/mount
group_prem=1000
user_perm=1000
export DISPLAY=:0.0
export HOME=/home/bijan

case $DEVCLASS in
2)
	# disk devices
        /sbin/disklabel $DEVNAME 2>&1 | awk -F '[ ]*' '/^  [abd-z]:/' | while read line;
        do
		mount_flags="-o noexec,noatime,nodev"
                slice=`echo $line | awk -F ':' '{print $1}'`
                type=`echo $line | awk -F '[ ]*' '{print $4}'`
                case $type in
		ISO9660 | 4.2BSD)
                        ;;
		ext2fs)
			mount_flags="$mount_flags -r"
			;;
		NTFS)
			mount_helper=/sbin/mount_ntfs
			mount_flags="$mount_flags -g $group_prem -u $user_perm"
			;;
		MSDOS)
			mount_helper=/sbin/mount_msdos
			mount_flags="$mount_flags -g $group_prem -u $user_perm"
			;;
		*)
			continue
			;;
                esac

                [ $DEBUG == 1 ] && logger -i "hotplugd attaching SLICE $slice of DEVICE $DEVNAME"
		[ ! -d $MOUNTROOT/$DEVNAME$slice ] && mkdir -p -m 1777 $MOUNTROOT/$DEVNAME$slice
		$mount_helper $mount_flags /dev/$DEVNAME$slice $MOUNTROOT/$DEVNAME$slice
		/usr/local/bin/notify-send "Mounted $DEVNAME$slice ($type)"
        done
        ;;
3)
	# network devices; requires hostname.$DEVNAME
	sh /etc/netstart $DEVNAME
	;;
esac
```

**Original**:

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
[4]: http://bsdnow.tv/
[5]: http://www.jupiterbroadcasting.com/121362/the-spectre-of-meltdown-bsd-now-228/
