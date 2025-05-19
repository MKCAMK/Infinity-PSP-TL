@echo off
setlocal enabledelayedexpansion
set "indir=%~dp1"
set "in=%~f1"

pushd "%~dp0"

if "%~1"=="" (
	echo no arguments
	goto error
)

if not defined pspsdk set "pspsdk=F:\psp_sdk_660"
if not defined pspsdktool set "pspsdktool=%pspsdk%\usr\local\psp\devkit\tool"
set "psmfenc=%pspsdktool%\PSMF_encoder\psmfenc.exe"
set "psmfmux=%pspsdktool%\PSMF_encoder\psmfmux.exe"
set "psmfcomposer=%pspsdktool%\PSMF_composer\PsmfComposerCMD.exe"

for %%i in ("%psmfenc%" "%psmfmux%" "%psmfcomposer%") do (
	if not exist "%%i" (
		echo failed to find %%i
		goto error
	)
)

ffmpeg -version >nul 2>&1
if errorlevel 1 (
	echo ffmpeg not found
	goto error
)

if exist "%~n1\" rd /s /q "%~n1"
if exist "%~n1.pmf" del "%~n1.pmf"
md "%~n1\atx" "%~n1\bsf" "%~n1\mps" "%~n1\pmf"
if exist "%~n1.ass" set "assfile=%~n1.ass"
if exist "%indir%%~n1.ass" set "assfile=%indir%%~n1.ass"
if defined assfile (
	set "assfile=!assfile:\=\\!"
	set "assfile=!assfile::=\:!"
	set "vfilter=-vf "ass='!assfile!'""
)
ffmpeg -y -i "%in%" -c:v huffyuv -an %vfilter% "%~n1.avi" || goto error
ffmpeg -y -i "%in%" "%~n1.wav" || goto error
%psmfenc% -video -2pass -peakb 4000 -avgb 2000 "%~n1.avi" "%~n1\bsf\%~n1.bsf" || goto error
%psmfenc% -audio -adjust_v "%~n1.avi" "%~n1.wav" "%~n1\atx\%~n1.atx" || goto error
%psmfmux% "%~n1\bsf\%~n1.bsf" "%~n1\atx\%~n1.atx" "%~n1\mps\%~n1.mps" || goto error
%psmfcomposer% "%~n1\mps\%~n1.mps" "%~n1\pmf\%~n1.pmf" || goto error
copy /y "%~n1\pmf\%~n1.pmf" "%~n1.pmf"

endlocal
popd
echo done
pause
exit /b

:error
endlocal
popd
echo error encountered!
pause
exit /b 1