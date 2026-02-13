#!/usr/bin/env python3
"""
SQL Quick Transfer Tool - Hızlı Başlatıcı
Web veya masaüstü uygulamasını hızlıca başlatmanızı sağlar
"""

import sys
import os
import subprocess


def print_banner():
    """Başlık yazdır"""
    print("=" * 60)
    print("        🗄️  SQL QUICK TRANSFER TOOL")
    print("       Tek Tıkla SQL Veri Aktarım Aracı")
    print("=" * 60)
    print()


def check_requirements():
    """Gereksinimlerin kurulu olup olmadığını kontrol et"""
    try:
        import sqlalchemy
        import flask
        from PyQt6 import QtWidgets
        import cryptography
        return True
    except ImportError as e:
        print("⚠️  Eksik bağımlılıklar tespit edildi!")
        print(f"   Hata: {e}")
        print("\nLütfen önce gereksinimleri yükleyin:")
        print("   pip install -r requirements.txt")
        return False


def start_web_app():
    """Web uygulamasını başlat"""
    print("🌐 Flask web uygulaması başlatılıyor...")
    print("   URL: http://localhost:5000")
    print("   Durdurmak için: Ctrl+C\n")
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, 'web/app.py'])


def start_desktop_app():
    """Masaüstü uygulamasını başlat"""
    print("🖥️  Masaüstü uygulaması başlatılıyor...\n")
    
    # PyQt6'nın kurulu olup olmadığını kontrol et
    try:
        import PyQt6
        print("PyQt6 bulundu, PyQt6 sürümü başlatılıyor...\n")
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([sys.executable, 'desktop/main.py'])
    except ImportError:
        print("⚠️  PyQt6 kurulu değil!")
        print("Tkinter sürümü başlatılıyor (Windows Long Path sorunu yok)...\n")
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([sys.executable, 'desktop/main_tkinter.py'])


def run_demo():
    """Demo scriptini çalıştır"""
    print("🎯 Demo uygulaması başlatılıyor...\n")
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, 'demo.py'])


def show_menu():
    """Ana menüyü göster"""
    print_banner()
    
    if not check_requirements():
        return
    
    print("Hangi uygulamayı başlatmak istersiniz?\n")
    print("  1. 🌐 Web Uygulaması (Flask)")
    print("  2. 🖥️  Masaüstü Uygulaması (PyQt6)")
    print("  3. 🎯 Demo ve Örnekler")
    print("  4. ❌ Çıkış")
    print()
    
    choice = input("Seçiminiz (1-4): ").strip()
    
    if choice == '1':
        start_web_app()
    elif choice == '2':
        start_desktop_app()
    elif choice == '3':
        run_demo()
    elif choice == '4':
        print("\n👋 Görüşmek üzere!")
    else:
        print("\n⚠️  Geçersiz seçim!")


def main():
    """Ana fonksiyon"""
    try:
        # Eğer komut satırı argümanı varsa direkt başlat
        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()
            if arg in ['web', 'w', '-w', '--web']:
                start_web_app()
            elif arg in ['desktop', 'd', '-d', '--desktop']:
                start_desktop_app()
            elif arg in ['demo', '-demo', '--demo']:
                run_demo()
            else:
                print(f"⚠️  Bilinmeyen argüman: {arg}")
                print("Kullanım: python start.py [web|desktop|demo]")
        else:
            # Menüyü göster
            show_menu()
    
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {str(e)}")


if __name__ == '__main__':
    main()
