Title: OpenBSD 6.2 Upgrade
SubTitle: The story of my first OpenBSD upgrade
Date: 2017-10-10 22:49
Category: OpenBSD
Tags: openbsd, upgrade

The Upgrading Process is stupidly easy. The process is [well documented][1] for each release
and is available after the release of binary packages and when install images are out but
before going any further, please read the OpenBSD 6.2 [new features](4) for the list of
changes and improvements. 

The process is split into two separate processes:

- First, You should upgrade the base system using one of two possibles. Using a bootable disk
image or using the manual process which is not recommended.
- Second, Upgrading the binary packages.

I choose Upgrading via a bootable media since it is the highly recommended way:
```sh
$curl -o install62.fs https://openbsd.mirror.netelligent.ca/pub/OpenBSD/6.2/amd64/install62.fs
```

Writing the image to the USB stick was a matter of executing `dd` command (as always):

```sh
$ sysctl hw.disknames
hw.disknames=sd0:da0bedc25009303c,cd0:,sd1:9e5b01f8dc3ea3f3
$ doas dd if=install62.fs of=/dev/rsd1c bs=1m
```

Again, if you're unfamiliar with anything like OpenBSD way of [dealing with storage devices][2] and
other things, please consider reading the entire [FAQ][3]. It really pays off, I promise ;-)

Now the next move is follow the pre-upgrade which I actually forgot. For my currect
setup, it was only to manually remove the man pages to avoid having old manpages in
the new system after successfull upgrade:

```sh
$ doas rm -rf /usr/share/man/
```

Now, Just rebooted the machine and booted from the USB stick and Press (U)pgrade and that was it.
After confirming the keyboard layout and my laptop's primary disk where my OpenBSD installation
resides, the process of Upgrading **The Base System** was done. After completion and rebooting
the machine, the first thing the new OS did was retrieving the newer firmwares which I skipped
since at the time, I had no (reliable) Internet connection, but don't worry, you can do it later:

```
$ uname -a
OpenBSD localhost.lenovo 6.2 GENERIC.MP#134 amd64
$ doas fw_update
```

Now, it's time to **update the binary packages** since their dependencies on the base system has
just been upgraded. But that was just one command away:

```sh
$ doas pkg_add -u
```

That was it. Hope to write more about OpenBSD in the near future.

[1]: https://www.openbsd.org/faq/upgrade62.html
[2]: https://www.openbsd.org/faq/faq14.html
[3]: https://www.openbsd.org/faq/
[4]: https://www.openbsd.org/62.html
