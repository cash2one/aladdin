rd /Q /S D:\autopack\output\aladdin\installers\bind
rd /Q /S D:\autopack\output\aladdin\installers\bind1
rd /Q /S D:\autopack\output\aladdin\installers\bind2
rd /Q /S D:\autopack\output\aladdin\installers\src
rd /Q /S D:\autopack\output\aladdin\installers\unbind
rd /Q /S D:\autopack\output\aladdin\installers\update
xcopy /Y /E /S /I D:\autopack\output\backup\installers D:\autopack\output\aladdin\installers
python aladdin.py -bU