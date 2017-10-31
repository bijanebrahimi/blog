Title: Smallest and Longest Manpage you ever read
SubTitle: what's the longest manpage you actually read?
Date: 2017-10-31 21:53
Category: Gist
Tags: OpenBSD, Manpages,


# Introduction
Recently I asked a question on OpenSD IRC channel which led to a question
entirely different. What's the smallest/longest manpage you ever read?

```sh
$ find /usr/local/share/man -type f -exec wc -l {} \;  | sort
```

On OpenBSD 6.2, the smallest is [dcphy(4)][1] with 23 lines and the longest
(by far distance) is [perltoc(1)][2] with 33106 lines. But what's the longest
manpage you actually read?

[1]: https://man.openbsd.org/dcphy.4
[2]: https://man.openbsd.org/perltoc.1
