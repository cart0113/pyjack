set HOME=C:\Users\Owner
rd /S /Q C:\eclipse\workspace\GIT_MOD2DOCTEST\doc\build\doctrees
rd /S /Q C:\eclipse\workspace\GIT_MOD2DOCTEST\doc\build\html

rem LOCAL DOCS
C:\Python26\scripts\sphinx-build.exe -b html C:\eclipse\workspace\GIT_MOD2DOCTEST\doc\source C:\eclipse\workspace\GIT_MOD2DOCTEST\doc\build\html

rem UPLOAD DOCS
cd C:\eclipse\workspace\GIT_MOD2DOCTEST
C:\Python26\python.exe setup.py build_sphinx
C:\Python26\python.exe setup.py upload_sphinx

pause