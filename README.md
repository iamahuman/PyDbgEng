# PyDbgEng - Debugger for fuzzing.

[![](https://img.shields.io/github/forks/walkerfuz/PyDbgEng.svg)](https://github.com/walkerfuz/PyDbgEng/network) 
[![](https://img.shields.io/github/stars/walkerfuz/PyDbgEng.svg)](https://github.com/walkerfuz/PyDbgEng/stargazers)

PyDbgEng is a python wrapper of debugger engines on windows, linux or osx, it's only aim to auto fuzzing.

## Usages

It's easy to use:

```Python
from PyDbgEng.windows import *
dbg = UserDebugger()
dbg.run("C:/Program Files/Internet Explorer/iexplore.exe http://127.0.0.1/fuzz")
# after process is crashed or terminated
print(dbg.crash_name)
print(dbg.crash_description)
```

You will get `dbg.crash_name` like this:
```Bash
EXPLOITABLE_WriteAV_0x1b75c019_0xb5221dd3.crash
```

and `dbg.crash_description` like this:
```Bash
|
   0	id: 2b8	create	name: iexplore.exe
.  1	id: 7a8	child	name: iexplore.exe
r
rax=0000000000000000 rbx=0000000000000000 rcx=000000000000fffb
rdx=0000000000000005 rsi=000000000720b068 rdi=000000000720afb8
rip=000007fef04019b9 rsp=000000000720ae30 rbp=0000000004d7af90
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
jscript!DllUnregisterServer+0x1e049:
000007fe`f04019b9 66214d30        and     word ptr [rbp+30h],cx ss:00000000`04d7afc0=????

.load C:\code\PyDbgEng-master\PyDbgEng\windows\utils\x64\MSEC.dll
!exploitable -m
VERSION:1.6.0.0
IDENTITY:HostMachine\HostUser
PROCESSOR:X64
CLASS:USER
QUALIFIER:USER_PROCESS
EVENT:DEBUG_EVENT_EXCEPTION
......
EXCEPTION_FAULTING_ADDRESS:0x4d7afc0
EXCEPTION_CODE:0xC0000005
EXCEPTION_LEVEL:FIRST_CHANCE
EXCEPTION_TYPE:STATUS_ACCESS_VIOLATION
EXCEPTION_SUBTYPE:WRITE
FAULTING_INSTRUCTION:000007fe`f04019b9 and word ptr [rbp+30h],cx
MAJOR_HASH:0x1b75c019
MINOR_HASH:0xb5221dd3
STACK_DEPTH:32
STACK_FRAME:jscript!DllUnregisterServer+0x1e049
STACK_FRAME:jscript!DllUnregisterServer+0x28f46
......
INSTRUCTION_ADDRESS:0x000007fef04019b9
INVOKING_STACK_FRAME:0
DESCRIPTION:User Mode Write AV
SHORT_DESCRIPTION:WriteAV
CLASSIFICATION:EXPLOITABLE
BUG_TITLE:Exploitable - User Mode Write AV ..
EXPLANATION:User mode write access violations that are not near NULL are exploitable.
```

If debugged process is terminated, `dbg.crash_name` and `dbg.crash_description` will set to None.

## Features

* The automated monitoring module specially developed for Fuzzing.
* Support Exploitable plugin to determine the crash is exploitable or not.
* Support for Windows, linux and Mac OS.

## Requirements

### windows

`Warning`: Because of using MSEC.dll to check crash exploit or not, `Visual C++ Redistributable for Visual Studio 2012` should be installed first.

* Required
	* python3
	* comtypes

### install

0. download visual Redistributable 2012 and setup.
1. pip install comtypes.
2. download PyDbgEng and run python setup.py install.

## Versions
The current version is `v0.0.5`, PyDbgEng can run in windows currectly:

  * fix bug when comtypes.gen isn't exist.
  * fix bug when killing debugged process and child process.

details [here](https://github.com/walkerfuz/PyDbgEng/blob/master/version.md).

------

If you want to report any bug or suggestion, please contact to walkerfuz#outlook.com.
