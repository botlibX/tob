T O B
=====


**NAME**


|
| ``tob`` - TOB
|


**SYNOPSIS**


|
| ``tob <cmd> [key=val] [key==val]``
| ``tob -cvaw [init=mod1,mod2]``
| ``tob -d`` 
| ``tob -s``
|

**DESCRIPTION**


``TOB`` has all you need to program a unix cli program, such as disk
perisistence for configuration files, event handler to handle the
client/server connection, deferred exception handling to not crash
on an error, etc.

``TOB`` contains python3 code to program objects in a functional way.
it provides an "clean namespace" Object class that only has dunder
methods, so the namespace is not cluttered with method names. This
makes storing and reading to/from json possible.

``TOB`` is a python3 IRC bot, it can connect to IRC, fetch and
display RSS feeds, take todo notes, keep a shopping list and log
text. You can run it under systemd for 24/7 presence in a IRC channel.


``TOB`` is Public Domain.


**INSTALL**


installation is done with pipx

|
| ``$ pipx install tob``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ tob srv > tob.service``
| ``$ sudo mv tob.service /etc/systemd/system/``
| ``$ sudo systemctl enable tob --now``
|
| joins ``#tob`` on localhost
|


**USAGE**


use ``tob`` to control the program, default it does nothing

|
| ``$ tob``
| ``$``
|

see list of commands

|
| ``$ tob cmd``
| ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
| ``pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``
|

start console

|
| ``$ tob -c``
|

start console and run irc and rss clients

|
| ``$ tob -c init=irc,rss``
|

list available modules

|
| ``$ tob mod``
| ``err,flt,fnd,irc,llm,log,mbx,mdl,mod,req,rss,``
| ``rst,slg,tdo,thr,tmr,udp,upt``
|

start daemon

|
| ``$ tob -d``
| ``$``
|

start service

|
| ``$ tob -s``
| ``<runs until ctrl-c>``
|


**COMMANDS**


here is a list of available commands

|
| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``err`` - show errors
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``log`` - log text
| ``mre`` - display cached output
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``req`` - reconsider
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``tdo`` - add todo item
| ``thr`` - show running threads
| ``upt`` - show uptime
|

**CONFIGURATION**


irc

|
| ``$ tob cfg server=<server>``
| ``$ tob cfg channel=<channel>``
| ``$ tob cfg nick=<nick>``
|

sasl

|
| ``$ tob pwd <nsnick> <nspass>``
| ``$ tob cfg password=<frompwd>``
|

rss

|
| ``$ tob rss <url>``
| ``$ tob dpl <url> <item1,item2>``
| ``$ tob rem <url>``
| ``$ tob nme <url> <name>``
|

opml

|
| ``$ tob exp``
| ``$ tob imp <filename>``
|


**PROGRAMMING**


``tob`` has it's modules in the package, so edit a file in tob/modules/<name>.py
and add the following for ``hello world``

::

    def hello(event):
        event.reply("hello world !!")


``tob`` uses loading on demand of modules and has a ``tbl`` command to
generate a table for this.


|
| ``$ tob tbl > tob/modules/tbl.py``
|

a md5sum can be added to verify the modules md5sums are matching.

|
| ``$ tob md5``
|

put this value in tob/modules/__init__.py and ``tob`` can execute the ``hello``
command now.

|
| ``$ tob hello``
| ``hello world !!``
|

Commands run in their own thread and the program borks on exit, output gets
flushed on print so exceptions appear in the systemd logs. Modules can contain
your own written python3 code, see the tob/modules directory for examples.


**FILES**

|
| ``~/.tob``
| ``~/.local/bin/tob``
| ``~/.local/pipx/venvs/tob/*``
|

**AUTHOR**

|
| ``Bart Thate`` <``bthate@dds.nl``>
|

**COPYRIGHT**

|
| ``TOB`` is Public Domain.
|
