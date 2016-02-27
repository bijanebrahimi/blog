Title: A dropdown Tiling Terminal for i3-wm
SubTitle: Using scratchpad and Terminator
Cover: http://bijanebrahimi.github.io/blog/assets/images/post_category_linux.jpg
Thumbnail: http://bijanebrahimi.github.io/blog/assets/images/post_category_linux_thumb.jpg
Date: 2016-02-27 14:27
Category: Gists
Tags: linux, terminal, terminator, i3, scratchpad


[Scratchpad](http://i3wm.org/docs/userguide.html#_scratchpad) is one of the
coolest, and unique features in [i3](http://i3wm.org). Scratchpad is basically a
hidden workspace that you can send your programs into it.

> There is no way to open that workspace. Instead, when using `scratchpad show`,
the window will be shown again, as a floating window, centered on your current
workspace

Using scratchpad, we can turn any terminal into a drop-down terminal. I'm using [terminator](www.tenshu.net/p/terminator.html) which supports tiling (and more)
and `F1` key as hot key to toggle terminator since I have no other use for formally
known help button key on linux.

```
# Add this to your i3 config (~/.config/i3/config) and restart i3 (Super+Shift+R)
exec --no-startup-id "terminator -m"
for_window [class="Terminator"] move scratchpad; [class="Terminator"] scratchpad show; move position 0 0; resize set 1366 768; move scratchpad
bindsym F1 [class="Terminator"]  scratchpad show; move position 0 0; resize set 1366 768;
```
You can also view the changes via [Github Gist](https://gist.github.com/bijanebrahimi/6641e8022dffb2e6a5dd).
