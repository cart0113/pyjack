set HOME=C:\cygwin\home\ajcarter
rd /S /Q C:\workspace\GIT_PYJACK\doc\build\doctrees
rd /S /Q C:\workspace\GIT_PYJACK\doc\build\html

rem LOCAL DOCS
C:\Python26\scripts\sphinx-build.exe -b html C:\workspace\GIT_PYJACK\doc\source C:\workspace\GIT_PYJACK\doc\build\html

rem UPLOAD DOCS
rem cd C:\workspace\GIT_PYJACK
rem C:\Python26\python.exe setup.py build_sphinx
rem C:\Python26\python.exe setup.py upload_sphinx

pause