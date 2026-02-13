# Windows Long Path Aktifleştirme - PowerShell Script
# Bu scripti YÖNETİCİ yetkisi ile çalıştırın!

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Windows Long Path Desteği Aktifleştirme" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Yönetici kontrolü
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "HATA: Bu script YÖNETİCİ yetkisi ile çalıştırılmalıdır!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Nasıl yapılır:" -ForegroundColor Yellow
    Write-Host "1. PowerShell'i YÖNETICI olarak açın" -ForegroundColor Yellow
    Write-Host "2. Bu scripti tekrar çalıştırın" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Veya:" -ForegroundColor Yellow
    Write-Host "Bu dosyaya SAĞ TIK -> 'PowerShell ile Çalıştır' (Yönetici olarak)" -ForegroundColor Yellow
    Write-Host ""
    Pause
    Exit 1
}

Write-Host "✓ Yönetici yetkisi doğrulandı" -ForegroundColor Green
Write-Host ""
Write-Host "Registry ayarı yapılıyor..." -ForegroundColor Yellow
Write-Host ""

try {
    # Registry değerini ayarla
    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
                     -Name "LongPathsEnabled" `
                     -Value 1 `
                     -PropertyType DWORD `
                     -Force | Out-Null
    
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "      ✓ BAŞARILI! Long Path Desteği Aktif!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "ÖNEMLİ: Değişikliklerin geçerli olması için BİLGİSAYARI YENİDEN BAŞLATMANIZ GEREKİYOR!" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Yeniden başlattıktan sonra:" -ForegroundColor Cyan
    Write-Host "1. install_windows.bat çalıştırın" -ForegroundColor White
    Write-Host "2. PyQt6 otomatik olarak kurulacak" -ForegroundColor White
    Write-Host ""
    
    $restart = Read-Host "Şimdi bilgisayarı yeniden başlatmak istiyor musunuz? (E/H)"
    
    if ($restart -eq "E" -or $restart -eq "e") {
        Write-Host ""
        Write-Host "Bilgisayar 10 saniye içinde yeniden başlatılacak..." -ForegroundColor Yellow
        Write-Host "Açık dosyalarınızı kaydetmeyi unutmayın!" -ForegroundColor Red
        Write-Host ""
        Start-Sleep -Seconds 3
        Restart-Computer -Force -Timeout 10
    } else {
        Write-Host ""
        Write-Host "Tamam. Hazır olduğunuzda bilgisayarı MANUEL olarak yeniden başlatın." -ForegroundColor Cyan
        Write-Host ""
        Pause
    }
    
} catch {
    Write-Host ""
    Write-Host "HATA: Registry ayarı yapılamadı!" -ForegroundColor Red
    Write-Host "Hata mesajı: $_" -ForegroundColor Red
    Write-Host ""
    Pause
    Exit 1
}
