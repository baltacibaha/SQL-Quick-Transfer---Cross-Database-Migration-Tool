@echo off
REM Windows Long Path Destegini Aktif Etme Scripti
REM Bu script YONETİCİ yetkisi ile calistirilmalidir!

echo ================================================
echo   Windows Long Path Destegi Aktiflestirilyor
echo ================================================
echo.
echo UYARI: Bu script YONETİCİ yetkisi gerektirir!
echo.
echo Devam etmek istiyor musunuz? (E/H)
set /p confirm="Seciminiz: "

if /i not "%confirm%"=="E" (
    echo Iptal edildi.
    pause
    exit /b 0
)

echo.
echo Registry ayari yapiliyor...
echo.

REM Registry'de LongPathsEnabled degerini 1 yap
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f

if errorlevel 1 (
    echo.
    echo ================================================
    echo   HATA: Islem basarisiz!
    echo ================================================
    echo.
    echo Bu script YONETICI yetkisi ile calistirilmalidir.
    echo.
    echo Nasil yapilir:
    echo 1. Bu dosyaya SAG TIKLAYIN
    echo 2. "Yonetici olarak calistir" secin
    echo 3. "Evet" deyin
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo      BASARILI! Long Path Destegi Aktif!
echo ================================================
echo.
echo Simdi yapmaniz gerekenler:
echo.
echo 1. BİLGİSAYARI YENİDEN BASLATMANIZ GEREKİYOR
echo    (Bu cok onemli - yeniden baslatmadan calismaz!)
echo.
echo 2. Yeniden baslattiktan sonra:
echo    install_windows.bat
echo.
echo 3. Veya PyQt6'yi manuel kurun:
echo    pip install PyQt6
echo.
echo Simdi bilgisayari yeniden baslatmak istiyor musunuz? (E/H)
set /p restart="Seciminiz: "

if /i "%restart%"=="E" (
    echo.
    echo Bilgisayar 10 saniye icinde yeniden baslatilacak...
    echo Acik dosyalarinizi kaydetmeyi unutmayin!
    echo.
    shutdown /r /t 10 /c "Windows Long Path destegi aktif edildi. Yeniden baslatiliyor..."
) else (
    echo.
    echo Tamam. Hazir oldugunuzda bilgisayari MANUEL olarak yeniden baslatin.
    echo.
    pause
)
