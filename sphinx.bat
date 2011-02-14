set HOME=C:\cygwin\home\ajcarter

rem rd /S /Q C:\workspace\GIT_PYJACK\doc\build\doctrees
rem rd /S /Q C:\workspace\GIT_PYJACK\doc\build\html

rem LOCAL DOCS
rem C:\Python26\scripts\sphinx-build.exe -b html C:\workspace\GIT_PYJACK\doc\source C:\workspace\GIT_PYJACK\doc\build\html

UPLOAD DOCS
cd C:\workspace\GIT_PYJACK
C:\Python26\python.exe setup.py build_sphinx
C:\Python26\python.exe setup.py upload_sphinx

pause