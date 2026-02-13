"""
Dosya Kontrol Scripti
Proje dosyalarinin dogru yerde olup olmadigini kontrol eder
"""

import os
import sys

print("=" * 60)
print("   PROJE DOSYA KONTROLU")
print("=" * 60)
print()

# Mevcut dizin
current_dir = os.getcwd()
print(f"Bulundugunuz dizin: {current_dir}")
print()

# Kontrol edilecek dosya ve klasorler
required_items = [
    ('desktop', 'klasor', 'Masaustu uygulama dosyalari'),
    ('web', 'klasor', 'Web uygulama dosyalari'),
    ('core', 'klasor', 'Cekirdek moduller'),
    ('templates', 'klasor', 'HTML sablonlar'),
    ('static', 'klasor', 'CSS/JS dosyalari'),
    ('start.py', 'dosya', 'Ana baslangic scripti'),
    ('demo.py', 'dosya', 'Demo uygulamasi'),
    ('check_packages.py', 'dosya', 'Paket kontrol scripti'),
    ('README.md', 'dosya', 'Dokumantasyon'),
]

missing = []
found = []

print("DOSYA KONTROLU:")
print("-" * 60)

for item_name, item_type, description in required_items:
    path = os.path.join(current_dir, item_name)
    
    if item_type == 'klasor':
        exists = os.path.isdir(path)
    else:
        exists = os.path.isfile(path)
    
    if exists:
        print(f"✅ {item_name:20s} - {description}")
        found.append(item_name)
    else:
        print(f"❌ {item_name:20s} - EKSIK! ({description})")
        missing.append((item_name, item_type, description))

print("-" * 60)
print()

if missing:
    print("❌ SORUN: Bazi dosyalar/klasorler eksik!")
    print()
    print("Eksik olanlar:")
    for item_name, item_type, description in missing:
        print(f"  - {item_name} ({item_type})")
    print()
    print("=" * 60)
    print("COZUM:")
    print("=" * 60)
    print()
    print("1. DOGRU KLASORDEYIM:")
    print("   Projeyi dogru bir sekilde indirip cikarttiniz mi?")
    print("   Tum zip icerigini ayni klasore cikartin.")
    print()
    print("2. YANLIS KLASORDEYIM:")
    print("   Bulundugunuz dizin:", current_dir)
    print()
    print("   Dogru dizine gidin:")
    print("   cd C:\\Users\\Baha-Batu\\Desktop\\sql_transfer_tool")
    print()
    print("   Sonra tekrar calistirin:")
    print("   python check_files.py")
    print()
    print("3. TEKRAR INDIRIN:")
    print("   Zip dosyasini tekrar indirin ve cikarttin.")
    print("   Tum dosyalarin mevcut oldugunu kontrol edin.")
    print()
    
else:
    print("✅ HARIKA! Tum dosyalar mevcut!")
    print()
    print("Artik uygulamayi calistirabilirsiniz:")
    print()
    print("Web icin:")
    print("  python start.py web")
    print()
    print("Masaustu icin:")
    print("  python start.py desktop")
    print()
    print("  veya direkt:")
    print("  python desktop/main_tkinter.py")
    print()

print("=" * 60)

# Mevcut dizindeki dosyalari listele
print()
print("Bulundugunuz dizindeki dosya ve klasorler:")
print("-" * 60)

items = os.listdir(current_dir)
items.sort()

for item in items[:20]:  # ilk 20'yi goster
    path = os.path.join(current_dir, item)
    if os.path.isdir(path):
        print(f"  📁 {item}/")
    else:
        print(f"  📄 {item}")

if len(items) > 20:
    print(f"  ... ve {len(items) - 20} tane daha")

print("-" * 60)
