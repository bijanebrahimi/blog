Title: GCC Cross-Compiler
SubTitle: a gcc cross-compiler for freebsd in linux
Date: 2017-02-17 12:04
Category: Gist
Tags: gist, gcc, cross-compiler, freebsd, linux, compiler


# Introduction
> A cross compiler is a compiler capable of creating executable code for a platform other than the one on which the compiler is running. For example, a compiler that runs on a Windows 7 PC but generates code that runs on Android smartphone is a cross compiler.
>
> --[Wikipedia](https://en.wikipedia.org/wiki/Crosscompiler)

Before we continue, there issome definitions we need to decide.

* **Build**: The machine you are building on which in our case, we're building our cross-compiler on a linux machine (`--host` option).
* **Host**: The machine that you are building for and again, it's a linux machine we're trying to build our binaries (`--host` option).
* **Target**: The machine that GCC will produce code for which is a freebsd machine (`--target` option).

**Note**: To decide the values of the above configuration, simply run `gdb --version` on the native machine. for a linux machine it's `x86_64-pc-linux-gnu` and for my target machine it's `amd64-marcel-freebsd9.2`. Since we're building and running our cross-compile on the same machine (`x86_64-pc-linux-gnu`), we don't need to specify the build and the host configuration which gcc will pick automatically.

```
$ export TARGET=amd64-marcel-freebsd9.2
```

And since, we don't wan to mix our cross-compile toolchains with our native binaries, we install our cross-compiler toolchains in the `/usr/cross-build` directory:
```
$ export PREFIX=/usr/cross-build
$ export TARGET_PREFIX=$PREFIX/$TARGET
$ export PATH=$PATH:$PREFIX/bin
```

One more important note before start compiling is that we need the head-files and libraries of the target machine. So we should copy `/lib` and `/include` directories from our freebsd machine to our cross-build directory:
```
$ mkdir -p $TARGET_PREFIX{,/lib,/include}
# copy /lib and /include directories from our freebsd machine in our target $TARGET_PREFIX directory.
```

GCC requires that a compiled copy of binutils be available for each targeted platform. So we need to download the source code of binutils and compile it for the freebsd machine.
```
$ mkdir -p build-binutils
$ wget https://ftp.gnu.org/gnu/binutils/binutils-2.27.tar.gz
$ tar zxvf binutils-2.27.tar.gz
$ cd build-binutils
$ ../binutils-2.27/configure --target=$TARGET --prefix=$PREFIX -v
$ make -j 4
$ sudo make install
```

GCC also depends on the following components:
* GMP: GNU Multiple Precision Arithmetic Library
* MPFR: GNU Multiple-precision floating-point rounding library
* MPC: GNU Multiple-precision C library

To build our cross-compiler, we need to compile these dependencies but since these dependencies should produce code for our target machine, we need to build them for the host option set to our tagret (`--host=amd64-marcel-freebsd9.2`):
```
$ mkdir build-gmp
$ wget https://ftp.gnu.org/gnu/gmp/gmp-6.1.1.tar.xz
$ tar xvf gmp-6.1.1.tar.xz
$ cd build-gmp
$ ../gmp-6.1.1/configure --prefix=$PREFIX --enable-shared --enable-static --enable-mpbsd --enable-fft --enable-cxx --host=$TARGET
$ make -j 4
$ sudo make install
$ cd ..

$ mkdir build-mpfr
$ wget https://ftp.gnu.org/gnu/mpfr/mpfr-3.1.5.tar.xz
$ tar xvf mpfr-3.1.5.tar.xz
$ cd build-mpfr
$ ../mpfr-3.1.5/configure --prefix=$PREFIX  --with-gnu-ld --with-gmp=$PREFIX --enable-static --enable-shared --host=$TARGET
$ make -j 4
$ sudo make install
$ cd ..

$ mkdir build-mpci
$ wget https://ftp.gnu.org/gnu/mpc/mpc-1.0.3.tar.gz
$ tar zxvf mpc-1.0.3.tar.gz
$ cd build-mpc
$ ../mpc-1.0.3/configure --prefix=$PREFIX --with-gnu-ld --with-gmp=$PREFIX --with-mpfr=$PREFIX --enable-static --enable-shared --host=$TARGET
$ make -j 4
$ sudo make install
$ cd ..
```

Finally, to compile gcc we need to specify where to look for it's dependencies above:
```
$ mkdir build-gcc
$ wget https://ftp.gnu.org/gnu/gcc/gcc-6.2.0/gcc-6.2.0.tar.gz
$ tar zxvf gcc-6.2.0.tar.gz
$ cd build-gcc
$ ../gcc-6.2.0/configure --without-headers --with-gnu-as --with-gnu-ld --enable-languages=c,c++ --disable-nls --enable-libssp --enable-gold --enable-ld --target=$TARGET --prefix=$PREFIX --with-gmp=$PREFIX --with-mpc=$PREFIX --with-mpfr=$PREFIX --disable-libgomp
$ LD_LIBRARY_PATH=$PREFIX/lib make -j 4
$ sudo make install
```

Now, we should have our own cross-compiler's toolchain in `/usr/cross-build/bin` directory. To use it we should include it in our `$PATH`:
```
export PATH=$PATH:$PREFIX/bin
```

To test our own cross-compiler, we simply run:
```
$ gcc main.c -o helloworld-linux
$ file helloword-linux
main: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=ca5ba57ac722ef8521d50ee8ecbbdca4b44a76e1, not stripped
$ LD_LIBRARY_PATH=$PREFIX/lib amd64-marcel-freebsd9.2-gcc helloworld.c -o helloworld-freebsd
$ file helloworld-freebsd
main: ELF 64-bit LSB executable, x86-64, version 1 (FreeBSD), dynamically linked, interpreter /libexec/ld-elf.so.1, for FreeBSD 9.2, not stripped
```

If you need a cross-compile version of gdb, simply compile the gdb for the target machine like above:
```
$ wget https://ftp.gnu.org/gnu/gdb/gdb-7.11.tar.xz
$ tar xvf gdb-7.11.tar.xz
$ ../gdb-7.11.1/configure --prefix=$PREFIX --target=$TARGET
$ make -j 4
$ sudo make install
```

You can see the whole compile process in my [github gist](https://gist.github.com/bijanebrahimi/62596745808f8667c40ff91b07d9e7b8).
