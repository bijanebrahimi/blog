title: Multiseat Linux Desktop, Multiple X servers
SubTitle: A Walkthrough to How I managed to run my first multiseat solution
Date: 2014-10-22 10:35
Category: Linux
tags: X11, config, xephyr

This is the first solution in the main Article [Multiseat Linux Desktop]({filename}/multiseat-linux-desktop.md). you may also find other solutions for multiseat configuration in there as well.

### Hardware Requirements

for each user, we need seperate:

* mouse
* keyboard
* monitor
* Video Card

each Monitor will be attached to a seperate Video Card.

### Introduction

the [X Window System](https://en.wikipedia.org/wiki/X_Window_System) is a system program which implements the hardware layer and the basis for graphical user interfaces (GUIs). to run seperate Desktop Environment in linux, we need to run seperate X servers as well. each X server will use separate Video card, Mouse and Keyboard (input devices). for that we have to configure the X server to do that. but first we have to identify the devices we have plugged to the computer to address them later in the X configuration file.
<!-- BREAK -->
### Hardware Detection

we can find our input devices (Mouse & Keyboards) in `/dev/input` directory. lets look to see what have we here:

	$ ls -la /dev/input
	drwxr-xr-x  4 root root    320 Apr 23 09:57 .
	drwxr-xr-x 15 root root   3060 Apr 23 09:59 ..
	drwxr-xr-x  2 root root    160 Apr 23 09:57 by-id
	drwxr-xr-x  2 root root    220 Apr 23 09:57 by-path
	crw-------  1 root root 13, 64 Apr 23 09:57 event0
	crw-------  1 root root 13, 65 Apr 23 09:57 event1
	crw-------  1 root root 13, 66 Apr 23 09:57 event2
	crw-------  1 root root 13, 67 Apr 23 09:57 event3
	crw-------  1 root root 13, 68 Apr 23 09:57 event4
	crw-------  1 root root 13, 69 Apr 23 09:57 event5
	crw-------  1 root root 13, 70 Apr 23 09:57 event6
	crw-------  1 root root 13, 71 Apr 23 09:57 event7
	crw-------  1 root root 13, 72 Apr 23 09:57 event8
	crw-------  1 root root 13, 63 Apr 23 09:57 mice
	crw-------  1 root root 13, 32 Apr 23 09:57 mouse0
	crw-------  1 root root 13, 33 Apr 23 09:57 mouse1

before explaining what is each of these files and directories, first we have to look at their permissions. they belogs to root user and group. so for reading them, we have to have read permission. run the below commands as super user or just run them using the `sudo` command which i did.

each `/dev/input/event*` file is an input device file. to find out which one is related to which input device we can print the files and see if it contains output when we move our mouse or press a key. so i did run the command and played with my input devices to see which one is which.

	$ sudo cat /dev/input/event0

do this till you find all of your input devices.

an alternative way (which i preffer) is to look into `/dev/input/by-id/` directory. your Input devices should be listed there with their human readable names.

	$ ls -la /dev/input/by-id/
	drwxr-xr-x 2 root root 160 Apr 23 09:57 .
	drwxr-xr-x 2 root root 160 Apr 23 09:57 .
	drwxr-xr-x 4 root root 320 Apr 23 09:57 ..
	lrwxrwxrwx 1 root root   9 Apr 23 09:57 usb-15ca_USB_Optical_Mouse-event-mouse -> ../event2
	lrwxrwxrwx 1 root root   9 Apr 23 09:57 usb-15ca_USB_Optical_Mouse-mouse -> ../mouse0
	lrwxrwxrwx 1 root root   9 Apr 23 09:57 usb-CHICONY_USB_Keyboard-event-if01 -> ../event4
	lrwxrwxrwx 1 root root   9 Apr 23 09:57 usb-CHICONY_USB_Keyboard-event-kbd -> ../event3
	lrwxrwxrwx 1 root root   9 Apr 23 09:57 usb-Logitech_Logitech_USB_Keyboard-event-if01 -> ../event1
	lrwxrwxrwx 1 root root   9 Apr 23 09:57 usb-Logitech_Logitech_USB_Keyboard-event-kbd -> ../event0

since you may notice, there may be a lot more input devices there. that's because linux will create several input device files for devices like Keyboards which have fancy buttons. try the old `cat` command to find out which one is your proper device driver file. i did it this way:

	$ sudo cat /dev/input/by-id/usb-15ca_USB_Optical_Mouse-event-mouse

write your input device names with their related device file name somewhere cause we're going to need those later.

at last for Video Cards. Video cards are identified by their address on the PCI bus. so to find them we can use `lspci` command.

	$ lspci |  grep VGA
	00:09.0 VGA compatible controller: nVidia Corporation NV18 [GeForce4 MX 4000 AGP 8x] (rev c1)
	00:0a.0 VGA compatible controller: nVidia Corporation NV18 [GeForce4 MX 4000 AGP 8x] (rev c1)

this command lists the pci devices connected to the computer and filters the lines containing VGA. the number on the left is the device PCI address. now we have the table below for our multiseat configuration:

* Seat number one
 * mouse: /dev/input/event2
 * keyboard: /dev/input/event0
 * Video Card: 00:09.0
* Seat number two
 * mouse: /dev/input/event8
 * keyboard: /dev/input/event3
 * Video Card: /dev/input/event8

### X Configuration

the X keeps it's configuration file in `/etc/X11` directory. we can directly modify it's current configuration file `xorg.conf` or we can simply create an alternative configuration file and tell X to read from it manually. that will help us to run X with default configurations if our configuration somehow didn't work.

	$ sudo touch /etc/X11/xorg.conf.multiseat
	$ sudo nano xorg.conf.multiseat

First of all, we need to set [basic Xorg configuration](https://wiki.archlinux.org/index.php/Xorg_multiseat#The_basics).

	Section "ServerFlags"
		Option "AutoAddDevices"     "false"
		Option "AutoEnableDevices"  "false"
		Option "AllowMouseOpenFail" "on"
		Option "AllowEmptyInput" "on"
		Option "ZapWarning"         "on"
		Option "HandleSpecialKeys"  "off" # Zapping on
		Option "DRI2" "on"
		Option "Xinerama" "off"
	EndSection

after that we need to define input devices, screens, monitors and layouts. do the following configuration for each seat you want to have. so first we need to define out input devices. look at the "Option Device". it is the device file name we detect earlier:

	Section "InputDevice"
		Identifier      "Keyboard0"
		Driver          "evdev"
		Option          "Device"                "/dev/input/event0"
		Option "xkb_rules" "evdev"
		Option "xkb_model" "evdev"
		Option "xkb_layout" "us"
		Option "GrabDevice" "on" # prevent send event to other X-servers
	EndSection
	Section "InputDevice"
		Identifier "Mouse0"
		Driver "evdev"
		Option "Device" "/dev/input/event2"
		Option "GrabDevice" "on"
	EndSection

now we need to define Screen with uses Monitor and Device which is our Video Card (you can tweak the Modes and ... if you like). the BusId Option is the PCI address we also found earlier.

	Section "Device"
		Identifier      "Nvidia0"
		Driver          "nouveau"
		BusId           "PCI:00:09.0"
	EndSection
		Section "Monitor"
		Identifier      "Lg0"
		HorizSync       30-93
		VertRefresh     60
		Option          "dpms"
	EndSection
	Section "Screen"
		Identifier              "Screen0"
		Device                  "Nvidia0"
		Monitor                 "Lg0"
		DefaultDepth    24
		Option                  "DPI"   "100x100"
		Subsection "Display"
			Depth   24
			Modes   "1280x1024"     "1024x768"
		EndSubsection
	EndSection

and finally, we need to define a Layout which we will later tell X to load it. it simply gathers the defined input devices and Screens.

	Section "ServerLayout"
		Identifier      "Seat0"
		Screen          1               "Screen0"       1                   1
		InputDevice     "Mouse0"        "CorePointer"
		InputDevice     "keyboard0"      "CoreKeyboard"
		Option "Clone" "off"
		Option "AutoAddDevices" "off"
		Option "DisableModInDev" "true"
		Option "SingleCard" "on"   # use this to simplfied isolatedevice option
	EndSection

that's it. do this process again for the next seats and then you're done.

### Test The Configuration

to test if everything is OK, we can run X using our multiseat configuration file and defined Layout. so we need to tell X where to look for COnfiguration file and load Which layout.

	$ startx -- :1 -layout Seat0 -config xorg.conf.multiseat

in the above code, i used `startx`. it is a front-end script to xinit. you can also simply run the X directly:

	$ X -novtswitch -sharevts -nolisten tcp -config xorg.conf.multiseat -layout Seat0 :1

you may need to go to the 7th console to use it (CTRL+F7) as the second seat will be available on the 8th console and so on.

	$ startx -- :2 -layout Seat0 -config xorg.conf.multiseat

if anything happend,read the log files and search the web.

### Configure Display Managers

it is possible to configure your Display Manager (like KDM or GDM) to behave properly with Multiseat configuration at boot-up, but since i dont use any Display Manager, i can not tell you exactly how to do it. search the web for that matter. you can do it the easy way by configuring your Display Manager rc file or the hard way by editing the `/etc/inittab` file if you have systemV.
