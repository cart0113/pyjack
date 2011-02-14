set HOME=C:\cygwin\home\ajcarter
cd C:\workspace\GIT_PYJACK
C:\Python24\python setup.py bdist_egg register upload --identity="Andrew Carter" --sign --quiet
C:\Python25\python setup.py bdist_egg register upload --identity="Andrew Carter" --sign --quiet
C:\Python26\python setup.py bdist_egg register upload --identity="Andrew Carter" --sign --quiet
C:\Python27\python setup.py bdist_egg register upload --identity="Andrew Carter" --sign --quiet
C:\Python24\python setup.py bdist_wininst --target-version=2.4 register upload --identity="Andrew Carter" --sign --quiet
C:\Python25\python setup.py bdist_wininst --target-version=2.5 register upload --identity="Andrew Carter" --sign --quiet
C:\Python26\python setup.py bdist_wininst --target-version=2.6 register upload --identity="Andrew Carter" --sign --quiet
C:\Python27\python setup.py bdist_wininst --target-version=2.7 register upload --identity="Andrew Carter" --sign --quiet
C:\Python26\python setup.py sdist register upload --identity="Andrew Carter" --sign
C:\Python26\python setup.py build_sphinx
C:\Python26\python setup.py upload_sphinx
pause