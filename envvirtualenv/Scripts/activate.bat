@echo off

set VIRTUAL_ENV=C:\home\src\camtran_austin\camtran\envvirtualenv

if not defined PROMPT (
    set PROMPT=$P$G
)
if not defined PYTHONPATH (
    set PYTHONPATH=
) 

if defined _OLD_VIRTUAL_PROMPT (
    set PROMPT=%_OLD_VIRTUAL_PROMPT%
)

if defined _OLD_VIRTUAL_PYTHONHOME (
    set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%
)

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(envvirtualenv) %PROMPT%

if defined PYTHONHOME (
    set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
    set PYTHONHOME=
)

if defined _OLD_VIRTUAL_PATH (
	set PATH=%_OLD_VIRTUAL_PATH%
	goto SKIPPATH
)

set _OLD_VIRTUAL_PATH=%PATH%
set _OLD_PYTHONPATH=%PYTHONPATH%

:SKIPPATH
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set PYTHONPATH=%VIRTUAL_ENV%\Lib;%VIRTUAL_ENV%\Lib\site-packages;%PYTHONPATH%

:END
