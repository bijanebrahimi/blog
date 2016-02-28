Title: py3status Configuration
SubTitle: Using Font Awesome
Cover: http://bijanebrahimi.github.io/blog/assets/images/post_category_linux.jpg
Thumbnail: http://bijanebrahimi.github.io/blog/assets/images/post_category_linux_thumb.jpg
Date: 2016-02-28 17:07
Category: Gist
Tags: linux, i3, py3status, i3status, font-awesome


Follow changes via [gist](https://gist.github.com/bijanebrahimi/d39f8fbbfe12e945db67) repository.

**Screenshot**:

![py3status Configuration]({filename}/assets/images/py3status-conf-i3bar.png)

**Dependencies**:

- [py3status](https://github.com/ultrabug/py3status) is an extensible i3status wrapper written in python.
- <i class="fa fa-flag"></i> [Font Awesome](https://fortawesome.github.io/Font-Awesome/): Font Icons for i3-bar
- <i class="fa fa-camera"></i> [maim](https://github.com/naelstrof/maim): a utility that takes screenshots of your desktop
- <i class="fa fa-lock"></i> [i3lock](http://i3wm.org/i3lock/): is a simple screen locker like slock.
- <i class="fa fa-picture-o"></i> [feh](http://linux.die.net/man/1/feh): to randomly change wallpaper.
- <i class="fa fa-calendar"></i> [gahshomar](https://gahshomar.github.io/gahshomar/) is a calendar with simplicity in design and elegance in execution.


`~/.config/i3/config`
```
bar {
    ...
    status_command py3status -c ~/.config/i3/i3status.conf
	font pango:DejaVu Sans Mono, Awesome 10
	...
}

```

`~/.config/i3/i3status.conf`
```
# i3status configuration file.
# see "man i3status" for documentation.

# It is important that this file is edited as UTF-8.
# The following line should contain a sharp s:
# ß
# If the above line is not correctly displayed, fix your editor first!

general {
        colors = true
        interval = 5
}
order += "static_string i3lock"
order += "static_string screenshot"
order += "static_string wallpaper"
order += "net_rate"
order + = "online_status"
order += "keyboard_layout"
order += "battery_level"
order += "time local"

time {
	format = "   %A %e %B  %H:%M"
	on_click 1 = "exec --no-startup-id gahshomar"
}
battery_level{
	blocks = ""
	charging_character = ""
	format = " {percent} {icon} {time_remaining}"
	color_charging = "#FFFFFF"
	cache_timeout = 5
}
keyboard_layout {
	cache_timeout = 1
	format = "  {layout}"
	color = "#FFFFFF"
}
net_rate {
	format = "  {total}"
	precision = 0
}
online_status {
	cache_timeout = 10
	format_offline = ""
	format_online = ""
	timeout = 20
}
static_string wallpaper {
	format = ""
	on_click 1 = "exec --no-startup-id feh --bg-scale $(find /home/bijan/Pictures/wallpapers/ | shuf | head -n 1)"
}
static_string screenshot {
	format = ""
    # Taking Screenshot using maim
	on_click 1 = "exec --no-startup-id echo ~/Pictures/Screenshots/img-$(date +%Y-%m-%d)-${RANDOM}.png | xargs -I '{}' maim -s '{}' && notify-send 'Screenshot' 'Screenshot taken'"}
static_string i3lock {
	format = ""
    # Set background for lock screen using -i argument
	on_click 1 = "exec --no-startup-id i3lock -d -I 5"
}
```
