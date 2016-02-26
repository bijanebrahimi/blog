Title: rofi-todo
SubTitle: a rofi script to do the dirty job
Cover: http://bijanebrahimi.github.io/blog/assets/images/post_category_linux.jpg
Thumbnail: http://bijanebrahimi.github.io/blog/assets/images/post_category_linux_thumb.jpg
Date: 2016-02-26 18:15
Category: Projects
Tags: linux, rofi, rofi-todo, rofi-script, bash, project


If you're unfamiliar with [rofi](https://davedavenport.github.io/rofi/):

> It's a popup window switcher roughly based on [superswitcher](http://code.google.com/p/superswitcher/),
requiring only xlib and pango

Rofi has multiple modes.

1. **RUN**: Shows a list of executables in $PATH and can launch them (optional in a terminal).
2. **DRUN**: Same as the run launches, but the list is created from the installed desktop files.
3. **Window**: Show a list of all the windows and allow switching between them.
4. **WindowCD**: Shows a list of the windows on the current desktop and allows switching between them.
5. **SSH**: Shows a list of SSH targets based on your ssh config file, and allows to quickly ssh into them.
6. **Script**: Allows custom scripted Modi to be added.

Using `script` mode, one can extend the rofi. There are plenty scripts
other there. you should definitely check [them](https://davedavenport.github.io/rofi/p07-Scripts.html) out.

## TODO List Script

Script modi can be enabled using `name:script` syntax. Just save the following
script somewhere in your `PATH` directory like `/usr/local/bin`, make sure it's
executable and run the following:

```
rofi -modi TODO:/usr/local/bin/rofi_todo.sh -key-todo SuperL+t
```

![rofi-todo]({filename}/assets/images/rofi_todolist-rofi_todo.png)

```bash
#!/bin/bash

TODO_FILE=~/.rofi_todos

if [[ ! -a "${TODO_FILE}" ]]; then
    touch "${TODO_FILE}"
fi

function list_todos()
{
    TODO=$(cat "${TODO_FILE}")
    if [[ -z "${TODO}" ]]; then
        TODDO="\n"
    fi
    echo "${TODO}"
}

if [ -z "$@" ]
then
    list_todos
else
    TODO=$(echo "${@}" | sed "s/\([^a-zA-Z0-9]\)/\\\\\\1/g")
    TODO_UNSCAPED=${@}

    MATCHING=$(grep "^${TODO}$" "${TODO_FILE}")
    if [[ -n "${MATCHING}" ]]; then
        sed -i "/^${TODO}$/d" "${TODO_FILE}"
    else
        echo -e "`date +"%B %d %H:%M"` ${TODO_UNSCAPED}" >> "${TODO_FILE}"
    fi
    list_todos
fi
```

**Instructions**:
- To **Add new TODO**, just type it (It should be Unique, BTW) at TODO prompt
- To **Delete one**, Just Select the one and hit Enter

If you're already using rofi, just add `TODO` modi to your existing command-line:

```
rofi -modi DRun,Run,Window,TODO:/usr/local/bin/rofi_todo.sh -key-todo SuperL+t -show TODO
```
