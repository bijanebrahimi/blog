Title: Freebsd's .mount.conf
SubTitle: How to boot FreeBSD's ISO image file from GRUB
Date: 2017-02-24 22:05
Category: FreeBSD
Tags: freebsd, grub, iso, mount.conf


# Introduction
As I'm getting more and more familiar with the FreeBSD Operating System and
it's wonderfull architeture and design, I found the need to work with different
versions of FreeBSD live (specially at work) and since it's not a good idea to install
every single version I needed into a USB flash drive, I tried Grub to boot a given
Freebsd ISO image (admittedly I'm still unfamiliar with the powers of FreeBSD's
own boot loader program).

# How Grub is booting an ISO image
Essentially what the grub does, is loading the given ISO image using `loopback`
command as a loop device and mount it in a special `(loop)` directory. That's
pretty much all that grub does before loading the kernel into memory thus
executing it. After passing the execution process to the kernel, the special loop device
is lost and kernel at some point needs to remount it again in order to
complete it's booting process. This process of mounting the root filesystem 
may differ between operating systems. For example, Ubuntu uses a parameter passed
to kernel named `iso-scan/filename` which essentially tells the kernel to look for
which file to mount as root filesystem. Kernel does this by mounting every existing
partitions looking for this speific path and when it finds it, it mounts it as
root filesystem and the process of booting the kernel continues.

# How to boot FreeBSD from an ISO image
As I searched the web, I found a few other people having the same problem booting
FreeBSD from ISO images and found a few interesting solutions like
[mfsBSD](http://mfsbsd.vx.sk/) which is a set of scripts building a special
FreeBSD kernel loaded entirely into RAM thus no need to mounting the root
filesystem at the first place. But that wasn't my solution till I find FreeBSD's
mount configuration file manual.

# FreeBSD's `.mount.conf` To Rescue
FreeBSD provides a kind of scriptable process of finding and mounting
the root filesystem via a file named `.mount.conf`. The process of mounting the
root filesystem is fully described in the [man page](https://www.freebsd.org/cgi/man.cgi?query=mount.conf):

What is interesting is that the kernel can follow the intructions in the `.mount.conf`
file in the root filesystem it mounts (if exists) and change it's current root
filesystem accordingly:

> `{FS}:{MOUNTPOINT} {OPTIONS}`
> The kernel will try to mount this in an operation equivalent to:
>
> `mount -t {FS} -o {OPTIONS} {MOUNTPOINT} /`
>
> If this is successfully mounted, further lines in .mount.conf
> are ignored.  If all lines in .mount.conf have been processed
> and no root file system has been successfully mounted, then
> the action specified by `.onfail` is performed.
>
> `.ask` When the kernel processes this	line, a	`mountroot>` command-
> line prompt is displayed. At this prompt, the operator can
> enter the the root mount.
> 
> `.md file` Create a memory backed [md(4)](https://www.freebsd.org/cgi/man.cgi?query=md) virtual disk, using file as the
> backing store.

So what the really need to do is to put a mount config file in our USB flash drive's
root directory which should contain a `md` command creating a memory backed
virtual disk from our FreeBSD's iso image and then mount it as our new root
filesystem:

```
.timeout 3
.md /iso/FreeBSD-11.0-RELEASE-amd64-dvd1.iso
.timeout 4
cd9660:/dev/md# ro
.ask
```

**Important**: please note that when the kernel mounts the new rootfilesystem, 
there should be a directory named `dev` inside the new root filesystem for kernerl
to remount the `devfs` on it. The whole process fails (sadly with no proper 
message) if the `dev` doesn't exist.

# The Solution
The following is the whole process plus formatting and installing grub from a
debian-based linux distro:

```
# Installing GRUB, Assuming /dev/sdb is the USB flash drive device
$ mount /dev/sdb1 /mnt
$ mkdir /mnt/boot
$ grub-install --boot-directory=/mnt/boot /dev/sdb

# Copy FreeBSD iso image and creating proper grub configuration file
$ mkdir /mnt/iso
$ cp ~/Downloads/FreeBSD-11.0-RELEASE-amd64-dvd1.iso /mnt/iso
$ cat > /mnt/boot/grub/grub.cfg << EOF
insmod loopback
insmod iso9660
insmod ufs2
insmod ntfs
menuentry "FreeBSD 11.0 amd64" {
  set isofile="/iso/FreeBSD-11.0-RELEASE-amd64-dvd1.iso"
  loopback loop (hd0,1)$isofile
  kfreebsd  (loop)/boot/kernel/kernel
}
EOF

# Create FreeBSD mount configuration file
$ mkdir /mnt/dev
$ cat > /mnt/.mount.conf << EOF
.timeout 3
.md /iso/FreeBSD-11.0-RELEASE-amd64-dvd1.iso
.timeout 4
cd9660:/dev/md# ro
.ask
EOF
```

That's It. Now after reboot and booting the USB flash drive, GRUB loads the
freebsd kernel from it's `loopback` device, and when FreeBSD kernel loads, it
fails mounting the root filesystem and drops into a prompt command line asking
for the root filesystem. We can Enter `?` to first get a list of known devies
and Then mount our USB flash drive partition as a temporary root filesystem
allowing kernel to find our `.mount.conf` file:

```
mountroot> msdosfs:/dev/da0s1
```

This last step can be avoided by setting the `FreeBSD.vfs.root.mountfrom` option
from grub which I have not tested yet:
```
set FreeBSD.vfs.root.mountfrom=msdosfs:/dev/da0s1
```

If nothing goes wrong (specially if you didn't forget to create a `dev`
directory in USB flash drive's root directory) you should login into your FreeBSD
iso image:

```
$ df
Filesystem 1K-blocks    Used  Avail Capcity  Mounted on
/dev/md0      286146 2861416      8    100%  /
/dev/da0s1   7561408 6621600  99808     88%  /mnt
devfs              1       1      0    100%  /dev
/dev/md1       31260     308  28452      1%  /var
/dev/md2       19356      28  17780      0%  /tmp
``` 

Look that the old root filesystem (`/dev/da0s1`) is re-mounted on `/mnt` as
described in manual. Hope it helps other :-)
