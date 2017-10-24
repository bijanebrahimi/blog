Title: Priveleged Seperated Processes
SubTitle: Part I: talking to the other side
Date: 2017-10-24 20:17
Category: OpenBSD
Tags: openbsd, imsg_init, socket_pair, privsep

## An Intorduction
> In computer programming and computer security, privilege separation is a
> technique in which a program is divided into parts which are limited to the
> specific privileges they require in order to perform a specific task. This is
> used to mitigate the potential damage of a computer security vulnerability.
>
> [Privilege Separation][1]

There are [many great resources][2] describing the architecture of a priviledge
separated process and the need for such architecrues, which I'm sure you already
read or will ;-)

What I'm really interested in, is the way the priviledged separated processes
are able to talk to each other. Hope you haveare already familliar with Unix
IPCs, but if you don't, here's [Beej's Guide to Unix IPC][3].

This is (hopefully) the first of a few posts about writing privsep processes.
Hope it helps.

## socketpair(2)

> The socketpair() call creates an unnamed pair of connected sockets in the
> specified domain d, of the specified type, and using the optionally
> specified protocol.  The descriptors used in referencing the new sockets
> are returned in sv[0] and sv[1].  The two sockets are indistinguishable.

Unlike [pipe(2)][5] which are uni-directional way of sending messages,
[socket(2)][6] are bi-directional, which means they are perfect for processes to talk
back to each others. [socketpair(2)][7] will create two of them for us. each
connected to the other using the specified Protocol.

{% graphviz
dot {
digraph G {
  graph [label="socketpair (AF_UNIX, SOCK_STREAM, PF_UNSPEC, fd)"]
  rankdir=LR
  fd0->fd1 [dir=both]
  fd0 [label="fd[0]"]
  fd1 [label="fd[1]"]
  subgraph cluster0 {fd0 label="Parent" style=dashed}
  subgraph cluster1 {fd1 label="Child" style=dashed}
}
}
%}

The above, Illustrates a socketpair of type `UNIX Sockets` shared by the aprent
and the child. Since the sockets are indistinguishable, there's no difference
which uses which.

The following snippet, Creates a socket pair and pass it to the child:

```c
#include <stdio.h>
#include <unistd.h>
#include <err.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/socket.h>

#define MAX_BUF_SIZE      128

int child_process (int fd);
int parent_process (int fd, pid_t pid);


int
main (int argc, const char **argv)
{
	pid_t child_pid;
	int fd[2];
	
	if (socketpair (AF_UNIX, SOCK_STREAM, PF_UNSPEC, fd) == -1)
		errx (1, "Failed to open socketpair");
	
	if ((child_pid = fork()) == -1)
		errx (2, "Failed to fork the process");

	if (child_pid > 0)
		return parent_process (fd[0], child_pid);
	else
		return child_process (fd[1]);
	
	return 0; /* Not reachable */
}

int
child_process (int fd)
{
	char buf[MAX_BUF_SIZE];

	snprintf(buf, MAX_BUF_SIZE, "Hello World");
	if (write (fd, buf, MAX_BUF_SIZE) == -1)
		errx (1, "Failed to write Message");
	
	return 0;
}

int
parent_process (int fd, pid_t pid)
{
	int status = 0;
	ssize_t nbytes;
	char buf[MAX_BUF_SIZE];
	
	if ((nbytes = read (fd, buf, MAX_BUF_SIZE- 1)) == -1)
		warn ("Failed to read");
	else if (nbytes > 0) {
                buf[nbytes] = '\0';
		printf ("Received \"%s\" from the Child\n", buf);
        }

	waitpid (pid, &status, WAIT_ANY);
	return WEXITSTATUS(status);
}
```

And the output is:

```sh
$ gcc -o privsep main.c
$ ./main
Received "Hello World" from the Child
```

Tips:

- Since the child process shares rge same memory address with it's parent, it
has access to all the descriptors the parent has opened, so it is a good
practice to close all unnecessary descriptors (like standard I/O) before
actually running the child's logic after calling the `fork(2)`.

In the next post, I will introduce the `imsg_init(3)`. The OpenBSD way of
writing privsep processes.

[1]: https://en.wikipedia.org/wiki/Privilege_separation
[2]: http://www.openbsd.org/papers/ven05-deraadt/
[3]: http://beej.us/guide/bgipc/
[4]: http://beej.us/guide/bgipc/output/html/multipage/unixsock.html
[5]: http://man.openbsd.org/pipe.2
[6]: http://man.openbsd.org/socket.2
[7]: http://man.openbsd.org/socketpair.2

