@echo off
setlocal enabledelayedexpansion

:: Retrieve platform information
:: Use the systeminfo command to get the OS name and system type, and filter the relevant information using findstr
for /f "tokens=1,2 delims=:" %%i in ('systeminfo ^| findstr /B /C:"OS Name" /C:"System Type"') do (
    if "%%i"=="OS Name" (
        set "osname=%%j"
    ) else if "%%i"=="System Type" (
        set "arch=%%j"
    )
)

:: Standardize platform information
:: Determine and set the platform type (Windows, Linux, MacOSX) based on the retrieved OS name
if not "%osname%"=="" (
    echo %osname% | find "Windows" > nul && set platform=Windows
    echo %osname% | find "Linux" > nul && set platform=Linux
    echo %osname% | find "Mac" > nul && set platform=MacOSX
)

:: Standardize architecture information
:: Determine and set the architecture type (x86_64, arm64) based on the retrieved system type
if not "%arch%"=="" (
    echo %arch% | find "x64" > nul && set arch=x86_64
    echo %arch% | find "ARM64" > nul && set arch=arm64
)

:: Find the latest installer package (requires curl and jq)
:: Use curl to fetch the list of Anaconda installer packages, and use grep, sort, and head to find the latest one
for /f "delims=" %%a in ('curl -s https://repo.anaconda.com/archive/ ^| grep -oP "Anaconda3-\d{4}\.\d{2}-\d+-%platform%-%arch%\.exe" ^| sort -r ^| head -1') do (
    set installer=%%a
)

:: Download the file
:: Use curl to download the latest installer package
curl -# -O https://repo.anaconda.com/archive/%installer%
