Title: Pelican on OpenBSD
SubTitle: How to make Pelican's Makefile BSD friendly
Date: 2017-10-13 22:49
Category: OpenBSD
Tags: bsd, openbsd, pelican, Makefile, python

If you haven't introduced to Pelican yet, you should probably read from this
blog:
> Pelican is a static site generator, written in Python, that requires no
> database or server-side logic.
>
> [blog.getpelican.com][1]

By creating a pelican project, a Mekfile will be created (by your confirmation)
to ease the process of writing and publishing your posts, However the format of
this Makefile is in GNU Make format and you'll get the following errors if you
run it on your BSD (FreeBSD and OpenBSD as I am aware of):

```sh
$ make devserver
No closing parenthesis in archive specification
*** Parse error in /path/to/pelican/project: Error in archive specification: "(0, 1)" (Makefile:31)
*** Parse error: Need an operator in 'endif' (Makefile:33)
No closing parenthesis in archive specification
*** Parse error: Error in archive specification: "(0, 1)" (Makefile:36)
*** Parse error: Need an operator in 'endif' (Makefile:38)
*** Parse error: Need an operator in 'PORT' (Makefile:74)
*** Parse error: Need an operator in 'else' (Makefile:76)
*** Parse error: Need an operator in 'endif' (Makefile:78)
*** Parse error: Need an operator in 'SERVER' (Makefile:81)
*** Parse error: Need an operator in 'else' (Makefile:83)
*** Parse error: Need an operator in 'endif' (Makefile:85)
*** Parse error: Need an operator in 'PORT' (Makefile:89)
*** Parse error: Need an operator in 'else' (Makefile:91)
*** Parse error: Need an operator in 'endif' (Makefile:93)
```

There's plentty of good resources online, referencing the differences. For
portable makefiles, you should probably read [Features of GNU make][3] and 
[Features of GNU make][4] and of course, The OpenBSD's [make(1)][5] and The
FreeBSD's [make(1)][6]


The following patch illustrates the changes and I hope it helps others:

```patch
diff --git a/Makefile b/Makefile
index d1ddf80..d87b1e9 100644
--- a/Makefile
+++ b/Makefile
@@ -2,7 +2,7 @@ PY?=python3
 PELICAN?=pelican
 PELICANOPTS=
 
-BASEDIR=$(CURDIR)
+BASEDIR=$(.CURDIR)
 INPUTDIR=$(BASEDIR)/content
 OUTPUTDIR=$(BASEDIR)/output
 CONFFILE=$(BASEDIR)/pelicanconf.py
@@ -28,14 +28,14 @@ DROPBOX_DIR=~/Dropbox/Public/
 GITHUB_PAGES_BRANCH=gh-pages
 
 DEBUG ?= 0
-ifeq ($(DEBUG), 1)
+.if $(DEBUG) == 1
        PELICANOPTS += -D
-endif
+.endif
 
 RELATIVE ?= 0
-ifeq ($(RELATIVE), 1)
+.if $(RELATIVE) == 1
        PELICANOPTS += --relative-urls
-endif
+.endif
 
 help:
        @echo 'Makefile for a pelican Web site                                           '
@@ -71,26 +71,26 @@ regenerate:
        $(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
 
 serve:
-ifdef PORT
+.ifdef PORT
        cd $(OUTPUTDIR) && $(PY) -m pelican.server $(PORT)
-else
+.else
        cd $(OUTPUTDIR) && $(PY) -m pelican.server
-endif
+.endif
 
 serve-global:
-ifdef SERVER
+.ifdef SERVER
        cd $(OUTPUTDIR) && $(PY) -m pelican.server 80 $(SERVER)
-else
+.else
        cd $(OUTPUTDIR) && $(PY) -m pelican.server 80 0.0.0.0
-endif
+.endif
 
 
 devserver:
-ifdef PORT
+.ifdef PORT
        $(BASEDIR)/develop_server.sh restart $(PORT)
-else
+.else
        $(BASEDIR)/develop_server.sh restart
-endif
+.endif
 
 stopserver:
        $(BASEDIR)/develop_server.sh stop
```

More to Read:

- [What is the difference between GNU Makefile and BSD Makefile?][7]

[1]: https://blog.getpelican.com/
[2]: http://docs.getpelican.com/en/3.1.1/getting_started.html
[3]: https://www.gnu.org/software/make/manual/html_node/Features.html
[4]: https://www.gnu.org/software/make/manual/html_node/Missing.html
[5]: https://man.openbsd.org/make.1
[6]: https://www.freebsd.org/cgi/man.cgi?query=make(1)
[7]: https://www.quora.com/What-is-the-difference-between-GNU-Makefile-and-BSD-Makefile
