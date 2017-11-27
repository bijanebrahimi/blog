Title: Fine Tuned Shell Scripting and Bash Automated Testing System Using Bats
SubTitle: A brief presentation at MashhadBUG
Date: 2017-11-27 20:50
Category: Gist
Tags: Shell, Scripting, Bats, sh

# Introduction
Last Saturday, I gave a brief presentation on shell scripting and bats, a bash
based automated testing system at [MashhadBUG][16]. Please Don't forget to check
the references at the end of the post.

# Table of Contents

- PART I: [Shell Tables][2] by Isaac Levy
- PART II: [The 3 finger claw technique][1] by Isaac Levy
- PART III: [Bats][3]: Bash Automated Testing System

# PART I: [Shell Tables][2] by Isaac Levy

## I/O Redirection
```bash
$ prog > file		# direct stdout to file
$ prog >> file		# append stdout to file
$ prog < file		# take standard input from file
$ < file prog
$ prog1 | prog2	# connect standard output of p1 to standard input of p2
$ prog <<HEREDOC	# HereDoc
```

## Commands
```bash
$ prog1; prog2		# command terminator
$ prog1 & prog2		# like ; but doesn't wait for p1 to finish
$ `prog1`		# run command, output replaces
$ (prog1)		# run command in sub-shell
$ {prog1}		# run command in current-shell
```

## Shell Scripts
```bash
$0...$9 		# positional arguments
$#			# total number of arguments
$*			# all the arguments as a single string (expanded/double-quoted)
$@			# all the arguments as separate strings (expanded/double-quoted)
$$			# pid of current shell process
$!			# pid of last background command
$?			# exit status of previous command
```

## Evaluation and Substitution of Shell Variables
```bash
$var			# Value of 'var'
${var}			# useful if alphanumerics follows
${var-thing} 		# 'var' if defined, O.W thing
${var:-word}  		# 'var' if exists and isn't null, O.W 'word'
${var:=word}		# like above but changes var
${var:?message} 	# abort if var doesn't exist or is null
${var:+word}  		# returns word if var exists and isn't null
```

# PART II: [The 3 finger claw technique][1] by Isaac Levy

# The Original 3 short functions

```sh
shout() { echo "$0: $*" >&2; } 
barf() { shout "$*"; exit 100; } 
safe() { "$@" || barf "cannot $*"; }
```

# The 3 short functions
```sh
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }
```

# Using The 3 finger claw technique

```sh
#!/bin/sh

yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

# using it
try cd /some/place
tar tar xzvfp /another/place/stuff.tbz

exit 0
```

# PART III: [Bats][3]: Bash Automated Testing System

> Bats is a [TAP][4]-compliant testing framework for Bash. It provides a simple way to verify that the UNIX programs you write behave as expected.

## [TAP][4]: Test Anything Protocol

> TAP, the Test Anything Protocol, is a simple text-based interface between testing modules in a test harness. TAP started life as part of the test harness for Perl but now has implementations in C, C++, Python, PHP, Perl, Java, JavaScript, and others.

```
1..4
ok 1 - Input file opened
not ok 2 - First line of the input valid
ok 3 - Read the rest of the file
not ok 4 - Summarized correctly # TODO Not written yet
```

## [TAP][4]: Resources

- [TAP Specification][5]
- [TAP Producers][6]
- [TAP Consumers][7]
- [TAP History][8]

## [Bats][3]: Bash Automated Testing System

> Bats is a [TAP][4]-compliant testing framework for Bash. It provides a simple way to verify that the UNIX programs you write behave as expected.

## [Bats][3]: Installation
```bash
$ git clone https://github.com/sstephenson/bats.git
$ cd bats
$ doas ./install.sh /usr/local
```

## [Bats][3]: Writing Tests
```bash
$ cat test.bats
#!/usr/bin/env bats

@test "addition using bc" {
  result="$(echo 2+2 | bc)"
  [ "$result" -eq 4 ]
}

@test "addition using dc" {
  result="$(echo 2 2+p | dc)"
  [ "$result" -eq 4 ]
}
```

### [Bats][3]: Running Tests
```bash
$ bats test.bats 
 ✓ addition using bc
 ✓ addition using dc
```
 
**WAIT, THAT'S NOT TAP COMPLIANT**

### [Bats][3]: Running Tests (Cont.)
```bash
$ bats --tap test.bats
1..2
ok 1 addition using bc
ok 2 addition using dc
```

### [Bats][3]: Writing Tests; `run` command
```bash
@test "invoking foo with a nonexistent file prints an error" {
  run foo nonexistent_filename
  [ "$status" -eq 1 ]
  [ "$output" = "foo: no such file 'nonexistent_filename'" ]
}
```

### [Bats][3]: Writing Tests; `load` command
```bash
load test_helper
```

### [Bats][3]: Writing Tests; `skip` command
```bash
$ cat test.bats
@test "A test I don`t want to execute for now" {
  skip "This command will return zero soon, but not now"
  run foo
  [ "$status" -eq 0 ]
}
```

Running Skiped Tests
```bash
$ bats test.bats
 - A test I don`t want to execute for now (skipped: This command will return zero soon, but not now)

1 test, 0 failures, 1 skipped
```
### [Bats][3]: Writing Tests; `skip` command (Cont.)
```bash
@test "A test which should run only when bar is foo" {
  [ foo != bar ] && skip "foo isn't bar"

  run foo
  [ "$status" -eq 0 ]
}
```

### [Bats][3]: Writing Tests; `setup` and `teardown` functions
```bash
setup()
{
  /* Initialization call per test calls */
}

teardown()
{
  /* Finalization call per test calls */
}
```

## [Bats][3]: Continues Integration Support
```bash
$ cat .travis.yml
before_install:
  - sudo add-apt-repository ppa:duggan/bats --yes
  - sudo apt-get update -qq
  - sudo apt-get install -qq bats
script:
  - bats test/bats
```
### [Bats][3]: Helpers

- [bats-support][9]
- [bats-assert][10]
- Definitely your own helper

### [Bats][3]: Helpers (Cont)
```bash
config() {
  command=""
  while read line; do
    command+="-c '$line' "
  done
  bash -c "prog $command"
}
remote() {
 host="$1"
 command="${@:2}"
 ssh $host "$(typeset -f); $command"
}
```

# Resources
- [shell-fu, NYCBUG (2016)][15]
- [How to use Bats to test your command line tools][11]
- [Testing Your Shell Scripts, with Bats][12]
- [Automate Bash testing with Bats][13]
- [Testing CLI Apps with Bats][14]

[1]: http://www.nycbug.org/index.cgi?action=view&id=10640
[2]: http://blackskyresearch.net/shelltables.txt
[3]: https://github.com/sstephenson/bats
[4]: http://testanything.org/
[5]: http://testanything.org/tap-specification.html
[6]: http://testanything.org/producers.html
[7]: http://testanything.org/consumers.html
[8]: http://testanything.org/history.html
[9]: https://github.com/ztombol/bats-support
[10]: https://github.com/ztombol/bats-assert
[11]: https://www.engineyard.com/blog/bats-test-command-line-tools
[12]: https://medium.com/@pimterry/testing-your-shell-scripts-with-bats-abfca9bdc5b9
[13]: http://softwaretester.info/automate-bash-testing-with-bats/
[14]: http://rnowling.github.io/software/engineering/2017/02/04/testing-cli-apps-with-bats.html
[15]: http://www.nycbug.org/index.cgi?action=view&id=10640
[16]: # Table of Contents

- PART I: [Shell Tables][2] by Isaac Levy
- PART II: [The 3 finger claw technique][1] by Isaac Levy
- PART III: [Bats][3]: Bash Automated Testing System

# PART I: [Shell Tables][2] by Isaac Levy

## I/O Redirection
```bash
$ prog > file		# direct stdout to file
$ prog >> file		# append stdout to file
$ prog < file		# take standard input from file
$ < file prog
$ prog1 | prog2	# connect standard output of p1 to standard input of p2
$ prog <<HEREDOC	# HereDoc
```

## Commands
```bash
$ prog1; prog2		# command terminator
$ prog1 & prog2		# like ; but doesn't wait for p1 to finish
$ `prog1`		# run command, output replaces
$ (prog1)		# run command in sub-shell
$ {prog1}		# run command in current-shell
```

## Shell Scripts
```bash
$0...$9 		# positional arguments
$#			# total number of arguments
$*			# all the arguments as a single string (expanded/double-quoted)
$@			# all the arguments as separate strings (expanded/double-quoted)
$$			# pid of current shell process
$!			# pid of last background command
$?			# exit status of previous command
```

## Evaluation and Substitution of Shell Variables
```bash
$var			# Value of 'var'
${var}			# useful if alphanumerics follows
${var-thing} 		# 'var' if defined, O.W thing
${var:-word}  		# 'var' if exists and isn't null, O.W 'word'
${var:=word}		# like above but changes var
${var:?message} 	# abort if var doesn't exist or is null
${var:+word}  		# returns word if var exists and isn't null
```

# PART II: [The 3 finger claw technique][1] by Isaac Levy

# The Original 3 short functions

```sh
shout() { echo "$0: $*" >&2; } 
barf() { shout "$*"; exit 100; } 
safe() { "$@" || barf "cannot $*"; }
```

# The 3 short functions
```sh
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }
```

# Using The 3 finger claw technique

```sh
#!/bin/sh

yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

# using it
try cd /some/place
tar tar xzvfp /another/place/stuff.tbz

exit 0
```

# PART III: [Bats][3]: Bash Automated Testing System

> Bats is a [TAP][4]-compliant testing framework for Bash. It provides a simple way to verify that the UNIX programs you write behave as expected.

## [TAP][4]: Test Anything Protocol

> TAP, the Test Anything Protocol, is a simple text-based interface between testing modules in a test harness. TAP started life as part of the test harness for Perl but now has implementations in C, C++, Python, PHP, Perl, Java, JavaScript, and others.

```
1..4
ok 1 - Input file opened
not ok 2 - First line of the input valid
ok 3 - Read the rest of the file
not ok 4 - Summarized correctly # TODO Not written yet
```

## [TAP][4]: Resources

- [TAP Specification][5]
- [TAP Producers][6]
- [TAP Consumers][7]
- [TAP History][8]

## [Bats][3]: Bash Automated Testing System

> Bats is a [TAP][4]-compliant testing framework for Bash. It provides a simple way to verify that the UNIX programs you write behave as expected.

## [Bats][3]: Installation
```bash
$ git clone https://github.com/sstephenson/bats.git
$ cd bats
$ doas ./install.sh /usr/local
```

## [Bats][3]: Writing Tests
```bash
$ cat test.bats
#!/usr/bin/env bats

@test "addition using bc" {
  result="$(echo 2+2 | bc)"
  [ "$result" -eq 4 ]
}

@test "addition using dc" {
  result="$(echo 2 2+p | dc)"
  [ "$result" -eq 4 ]
}
```

### [Bats][3]: Running Tests
```bash
$ bats test.bats 
 ✓ addition using bc
 ✓ addition using dc
```
 
**WAIT, THAT'S NOT TAP COMPLIANT**

### [Bats][3]: Running Tests (Cont.)
```bash
$ bats --tap test.bats
1..2
ok 1 addition using bc
ok 2 addition using dc
```

### [Bats][3]: Writing Tests; `run` command
```bash
@test "invoking foo with a nonexistent file prints an error" {
  run foo nonexistent_filename
  [ "$status" -eq 1 ]
  [ "$output" = "foo: no such file 'nonexistent_filename'" ]
}
```

### [Bats][3]: Writing Tests; `load` command
```bash
load test_helper
```

### [Bats][3]: Writing Tests; `skip` command
```bash
$ cat test.bats
@test "A test I don`t want to execute for now" {
  skip "This command will return zero soon, but not now"
  run foo
  [ "$status" -eq 0 ]
}
```

Running Skiped Tests
```bash
$ bats test.bats
 - A test I don`t want to execute for now (skipped: This command will return zero soon, but not now)

1 test, 0 failures, 1 skipped
```
### [Bats][3]: Writing Tests; `skip` command (Cont.)
```bash
@test "A test which should run" {
  [ foo != bar ] && skip "foo isn't bar"

  run foo
  [ "$status" -eq 0 ]
}
```

### [Bats][3]: Writing Tests; `setup` and `teardown` functions
```bash
setup()
{
  /* Initialization call per test calls */
}

teardown()
{
  /* Finalization call per test calls */
}
```

## [Bats][3]: Continues Integration Support
```bash
$ cat .travis.yml
before_install:
  - sudo add-apt-repository ppa:duggan/bats --yes
  - sudo apt-get update -qq
  - sudo apt-get install -qq bats
script:
  - bats test/bats
```
### [Bats][3]: Helpers

- [bats-support][9]
- [bats-assert][10]
- Definitely your own helper

### [Bats][3]: Helpers (Cont)
```bash
config() {
  command=""
  while read line; do
    command+="-c '$line' "
  done
  bash -c "prog $command"
}
remote() {
 host="$1"
 command="${@:2}"
 ssh $host "$(typeset -f); $command"
}
```

# Any Questions

# Resources
- [shell-fu, NYCBUG (2016)][15]
- [How to use Bats to test your command line tools][11]
- [Testing Your Shell Scripts, with Bats][12]
- [Automate Bash testing with Bats][13]
- [Testing CLI Apps with Bats][14]

[1]: http://www.nycbug.org/index.cgi?action=view&id=10640
[2]: http://blackskyresearch.net/shelltables.txt
[3]: https://github.com/sstephenson/bats
[4]: http://testanything.org/
[5]: http://testanything.org/tap-specification.html
[6]: http://testanything.org/producers.html
[7]: http://testanything.org/consumers.html
[8]: http://testanything.org/history.html
[9]: https://github.com/ztombol/bats-support
[10]: https://github.com/ztombol/bats-assert
[11]: https://www.engineyard.com/blog/bats-test-command-line-tools
[12]: https://medium.com/@pimterry/testing-your-shell-scripts-with-bats-abfca9bdc5b9
[13]: http://softwaretester.info/automate-bash-testing-with-bats/
[14]: http://rnowling.github.io/software/engineering/2017/02/04/testing-cli-apps-with-bats.html
[15]: http://www.nycbug.org/index.cgi?action=view&id=10640
[16]: http://mashhadbug.org
