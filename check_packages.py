#!/usr/bin/env python3
"""
Paket Kontrol Scripti
Hangi paketlerin kurulu/eksik olduğunu kontrol eder
"""

import sys

print("=" * 60)
print("   SQL TRANSFER TOOL - PAKET KONTROL")
print("=" * 60)
print()

# Kontrol edilecek paketler
packages = [
    ('sqlalchemy', 'SQLAlchemy (ZORUNLU)', True),
    ('flask', 'Flask (ZORUNLU - Web için)', True),
    ('cryptography', 'Cryptography (ZORUNLU)', True),
    ('mysql.connector', 'MySQL Connector (İsteğe bağlı)', False),
    ('psycopg2', 'PostgreSQL Driver (İsteğe bağlı)', False),
    ('PyQt6', 'PyQt6 (İsteğe bağlı - Masaüstü için)', False),
]

missing_required = []
missing_optional = []
installed = []

for package_name, display_name, required in packages:
    try:
        __import__(package_name)
        installed.append(display_name)
        print(f"✅ {display_name}")
    except ImportError:
        if required:
            missing_required.append((package_name, display_name))
            print(f"❌ {display_name} - EKSİK (ZORUNLU)")
        else:
            missing_optional.append((package_name, display_name))
            print(f"⚠️  {display_name} - Eksik (isteğe bağlı)")

print()
print("=" * 60)
print("ÖZET:")
print("=" * 60)
print(f"✅ Kurulu paketler: {len(installed)}")
print(f"❌ Eksik zorunlu paketler: {len(missing_required)}")
print(f"⚠️  Eksik isteğe bağlı paketler: {len(missing_optional)}")
print()

if missing_required:
    print("❌ HATA: Zorunlu paketler eksik!")
    print()
    print("Şu komutları çalıştırın:")
    print("-" * 60)
    for pkg_name, pkg_display in missing_required:
        if pkg_name == 'sqlalchemy':
            print(f"pip install sqlalchemy")
        elif pkg_name == 'flask':
            print(f"pip install Flask Flask-Cors")
        elif pkg_name == 'cryptography':
            print(f"pip install cryptography")
    print("-" * 60)
    print()
    print("Veya hepsini birden:")
    print("pip install sqlalchemy Flask Flask-Cors cryptography")
    print()
    sys.exit(1)

elif missing_optional:
    print("✅ Zorunlu paketler kurulu!")
    print()
    print("⚠️  İsteğe bağlı paketler eksik (kurabilirsiniz):")
    print("-" * 60)
    for pkg_name, pkg_display in missing_optional:
        if 'MySQL' in pkg_display:
            print(f"MySQL için: pip install mysql-connector-python")
        elif 'PostgreSQL' in pkg_display:
            print(f"PostgreSQL için: pip install psycopg2-binary")
        elif 'PyQt6' in pkg_display:
            print(f"Masaüstü uygulama için: pip install PyQt6")
    print("-" * 60)
    print()
    print("NOT: Bu paketleri sadece ihtiyacınız varsa kurun.")
    print()
    print("✅ Şu anda WEB uygulamasını (SQLite ile) çalıştırabilirsiniz!")
    print()

else:
    print("✅ TÜM PAKETLER KURULU!")
    print()
    print("Artık uygulamayı çalıştırabilirsiniz:")
    print("-" * 60)
    print("Web uygulaması için: python start.py web")
    print("Masaüstü için: python start.py desktop")
    print("Demo için: python demo.py")
    print("-" * 60)
    print()

print("=" * 60)
print()

# Python versiyonu kontrol
print("Python Bilgileri:")
print(f"Versiyon: {sys.version}")
print(f"Yürütülebilir: {sys.executable}")
print()
