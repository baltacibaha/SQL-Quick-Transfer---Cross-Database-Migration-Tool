"""
Dosya Duzenleme Scripti
Karisik dosyalari dogru klasorlere tasir
"""

import os
import shutil

print("=" * 60)
print("   DOSYA DUZENLEME SCRIPTI")
print("=" * 60)
print()

# Mevcut dizin
current_dir = os.getcwd()
print(f"Bulundugunuz dizin: {current_dir}")
print()

# Klasor olustur
def create_folder(name):
    path = os.path.join(current_dir, name)
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✓ {name}/ klasoru olusturuldu")
    return path

# Dosya tasi
def move_file(filename, destination_folder):
    src = os.path.join(current_dir, filename)
    if os.path.exists(src) and os.path.isfile(src):
        dst = os.path.join(destination_folder, filename)
        # Eger hedefte zaten varsa, silme
        if not os.path.exists(dst):
            shutil.move(src, dst)
            print(f"  {filename} -> {os.path.basename(destination_folder)}/")
        return True
    return False

print("Klasorler olusturuluyor...")
print("-" * 60)

# Klasorleri olustur
desktop_dir = create_folder('desktop')
web_dir = create_folder('web')
core_dir = create_folder('core')
templates_dir = create_folder('templates')
static_dir = create_folder('static')
css_dir = create_folder('static/css')
js_dir = create_folder('static/js')

print()
print("Dosyalar tasiniyor...")
print("-" * 60)

# Desktop dosyalari
print("\nDesktop klasorune:")
move_file('main.py', desktop_dir)
move_file('main_tkinter.py', desktop_dir)

# Web dosyalari
print("\nWeb klasorune:")
move_file('app.py', web_dir)

# Core dosyalari
print("\nCore klasorune:")
move_file('database_connection.py', core_dir)
move_file('connection_storage.py', core_dir)
move_file('transfer_engine.py', core_dir)
move_file('__init__.py', core_dir)

# Templates dosyalari
print("\nTemplates klasorune:")
move_file('index.html', templates_dir)

# Static/CSS dosyalari
print("\nStatic/CSS klasorune:")
move_file('style.css', css_dir)

# Static/JS dosyalari
print("\nStatic/JS klasorune:")
move_file('main.js', js_dir)

print()
print("=" * 60)
print("   TAMAMLANDI!")
print("=" * 60)
print()
print("Artik klasor yapisi dogru!")
print()
print("Simdi calistirabileceginiz komutlar:")
print()
print("1. Tkinter uygulamasi:")
print("   python desktop/main_tkinter.py")
print()
print("2. Web uygulamasi:")
print("   python web/app.py")
print()
print("3. Veya start.py kullanin:")
print("   python start.py desktop")
print("   python start.py web")
print()
print("=" * 60)

input("\nDevam etmek icin Enter'a basin...")
