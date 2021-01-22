Title: Raspbian on 1G SD-Card
SubTitle: How to Create a alter the Rasbian image to fit into 1G SD-Card
Date: 2021-01-22 13:20
Category: Linux
Tags: linux, rasbperry pi, debian, buster, raspbian

Recently I setup a raspberry pi as my home wireless router. It worked great,
until I accidently broke the sd-card. I had a spare SD-Card but it was only
1GB. Considering the 1.8GB raspbian image, something had to be done to shrink
the image size to fit into a 1GB SD-Card. Here's the **How To** but I should
warn, the following instructions to beexecuted very carefully or you might wipe
the wrong storage and lose data.

**Note:** Most of the following commands are to be executed with root privileges.
Please ensure you understand them before trying to execute them.

First I needed to create an image, with the right size to fit exactly into my
1GB SC-Card. To check the size of the media, simply execute `fdisk -l`. My SD-Card
has around **940MB** capacity, So the following command creates a image file
with that exact size:

```sh
truncate -s 940M sd-card.img
```

the next step is to create block devices from the raspberry image and my own image.

```sh
losetup /dev/loop1 2020-05-27-raspios-buster-lite-armhf.img
losetup /dev/loop2 sd-card.img
```
So, from now on, the `/dev/loop1` device, represents the raspbian image and the
`/dev/loop2` device should represents my custom image device.

Then, we need to properly copy the boot instructions from the Raspbian image. The
boot instructions are located after the partition table at sector zero and before
the start position of the first partition. 

```sh
fdisk -l /dev/loop1
<sniped>
Units: sectors of 1 * 512 = 512 bytes
<sniped>
Device       Boot  Start     End Sectors  Size Id Type
/dev/loop1p1        8192  532479  524288  256M  c W95 FAT32 (LBA)
/dev/loop1p2      532480 3620863 3088384  1.5G 83 Linux
```

From the `fdisk` output, it's clear that I need to copy the sectors from `0` to
`8191`, just efore the start of the first partition.

```sh
sudo dd if=/dev/loop1 of=/dev/loop2 bs=512 count=8192
```

Then, I needed to recreate the **boot** and **root** partitions according to the
size of the media. So, I reserved `55MB` for the boot partition and the reset for
the root partition. The following script, did just that:

```sh
sudo fdisk/dev/loop2 <<EOF
d
1
d
2
n
p
1
8192
+55M
t
c
n
p
2
120832

p
w
EOF
```

After creating the new paritions with the right size, I needed to force the kernel
to re-read the new partition table containing the new partition sizes and then
reformat.

```sh
partprobe /dev/loop2
sudo mkfs.fat /dev/loop2p1
sudo mkfs.ext4 /dev/loop2p2
```

Now, all left to do is to copy all the files to the new image excluding the ones
that's not actually useful, just to spare some space on SD-Card. First the boot
partition:

```sh
mkdir -p /tmp/raspbian-boot
mkdir -p /tmp/sdcard-boot

mount /dev/loop1p1 /tmp/raspbian-boot
mount /dev/loop2p1 /tmp/sdcard-boot
cp -a /tmp/raspbian-boot/* /tmp/sdcard-boot

# Enable ssh automatically on boot
touch /tmp/sdcard-boot/ssh

umount /dev/loop1p1
umount /dev/loop2p1
rmdir /tmp/raspbian-boot
rmdir /tmp/sdcard-boot
```

Then, to Copy the root filesystem contents, I decided copy all the files except
the files that are not necessary, like man-pages, linux kernel modules for
different kernel versions and so one. The following commands copies exactly the
needed files to boot on regular Raspberry pi 3:

```sh
mkdir -p /tmp/raspbian-root
mkdir -p /tmp/sdcard-root

mount /dev/loop1p2 /tmp/raspbian-root
mount /dev/loop2p2 /tmp/sdcard-root

mkdir -p /tmp/sdcard-root/lib/modules
mkdir -p /tmp/sdcard-root/usr/{games,src,local,include,share}


# Copy LFSH
cp -a /tmp/raspbian-root/{boot,media,mnt,proc,srv,sys,tmp,dev,root,run,home,etc,sbin,bin,var} /tmp/sdcard-root
cp -a /tmp/raspbian-root/lib/{arm-linux-gnueabihf,cpp,dhcpcd,ifupdown,klibc-fAGGTaZfOmYXUytsXgfSuL5MT48.so,ld-linux.so.3,modprobe.d,resolvconf,terminfo,console-setup,crda,firmware,init,ld-linux-armhf.so.3,lsb,systemd,udev} /tmp/sdcard-root/lib/
cp -a /tmp/raspbian-root/lib/modules/4.19.118-v7+ /tmp/sdcard-root/lib/modules/
cp -a /tmp/raspbian-root/usr/{sbin,bin,lib} /tmp/sdcard-root/usr/
cp -a /tmp/raspbian-root/usr/lib /tmp/sdcard-root/usr/
sudo cp -a /tmp/raspbian-root/usr/share/{GeoIP,X11,aclocal,adduser,alsa,applications,apport,apps,apt-listchanges,avahi,base-files,base-passwd,bash-completion,binfmts,bug,build-essential,ca-certificates,calendar,cmake,common-licenses,console-setup,consolefonts,consoletrans,dbus-1,debconf,debhelper,debianutils,dhcpcd,dict,distro-info,doc-base,dpkg,file,gcc-8,gdb,gettext,glib-2.0,gnupg,groff,hal,i18n,icons,info,initramfs-tools,iptables,iso-codes,java,keyrings,keyutils,libc-bin,lintian,luajit-2.1.0-beta3,man,man-db,menu,metainfo,mime,misc,nano,nfs-common,openssh,pam,pam-configs,perl,perl5,pixmaps,pkg-config-crosswrapper,pkg-config-dpkghook,pkgconfig,polkit-1,publicsuffix,pyshared,python,python-apt,python3,raspi-config,readline,sensible-utils,sounds,systemd,tabset,tasksel,terminfo,usb_modeswitch,vim,vl805fw,xml,zoneinfo,zsh} /tmp/sdcard-root/usr/share/

# Remove unnecessary files
rm /tmp/sdcard-root/var/cache/apt/srcpkgcache.bin
rm -rf /tmp/sdcard-root/usr/share/{GeoIP,i18n,man,bash-completion,sounds,misc}

umount /dev/loop1p2
umount /dev/loop2p2
rmdir /tmp/raspbian-root
rmdir /tmp/sdcard-root
```

That's it. Hopefully after boot, there's enough space for upgrade and installing
missing softwares. If it's not, try removing other unnecessary files. Lucky for
me, the home wireless router worked (almost) out of the box and very little installation
was needed.
