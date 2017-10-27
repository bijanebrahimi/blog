Title: Building FreeBSD Custom Kernel
SubTitle: Small Tips on how to build kernels faster
Date: 2017-10-27 11:21
Category: FreeBSD
Tags: freebsd, kernel, compile

According to [FreeBSD Handbook][1], there are two ways of building a custom
kernel: [The Traditional Way][2] and [The New Way][3].

Either way, we should create a custom kernel configuration file, Then we use
this custom kernel configuration for building the new kernel:


```sh
$ cd /usr/src
$ cp sys/amd64/config/GENERIC sys/amd64/config/CUSTOM
```

For example, we can enable kernel debuggings enabled in our custom
configuration:

```sh
$ cat >> sys/amd64/config/CUSTOM <EOF
makeoptions -g
options KDB
options DDB
EOF
```

Now, to compile the new kernel with our custom configuration:

```sh
make -j 16 buildkernel KERNCONF=CUSTOM
make -j 16 installkernel KERNCONF=CUSTOM
```

If you're experiencing modifying kernel and trying to avoid re-
compiling the kernel every time you have a small change in the
source code, use the following command:

```sh
make -j 16 buildkernel KERNCONF=CUSTOM -DKERNFAST
```

**Tips**: Remember to remove the multiple make jobs `-j` flags
if you have errors in compiling the source to easily spot the
error message:

```sh
make buildkernel KERNCONF=CUSTOM -DKERNFAST
```

[1]: https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook
[2]: https://www.freebsd.org/doc/en_US.ISO8859-1/books/developers-handbook/kernelbuild.html
[3]: https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/kernelconfig-building.html
