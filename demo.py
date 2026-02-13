"""
SQL Transfer Tool - Demo Script
Örnek kullanım senaryolarını gösterir
"""

import sys
import os

# Core modüllerini import et
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core import (
    DatabaseConnection,
    DataTransferEngine,
    TransferOptions,
    ConnectionStorage,
    create_connection_dict
)


def demo_connection_test():
    """Örnek: Bağlantı testi"""
    print("=" * 60)
    print("DEMO 1: Veritabanı Bağlantı Testi")
    print("=" * 60)
    
    # MySQL bağlantısı oluştur
    mysql_conn = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='test_db'
    )
    
    # Bağlantıyı test et
    success, message = mysql_conn.test_connection()
    print(f"MySQL Bağlantı Testi: {'✓ Başarılı' if success else '✗ Başarısız'}")
    print(f"Mesaj: {message}\n")


def demo_list_tables():
    """Örnek: Tabloları listeleme"""
    print("=" * 60)
    print("DEMO 2: Veritabanındaki Tabloları Listeleme")
    print("=" * 60)
    
    conn = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='test_db'
    )
    
    if conn.connect():
        tables = conn.get_tables()
        print(f"Bulunan tablolar ({len(tables)} adet):")
        for table in tables:
            print(f"  - {table}")
        conn.close()
    else:
        print("Bağlantı kurulamadı!")
    
    print()


def demo_save_connection():
    """Örnek: Bağlantı bilgilerini kaydetme"""
    print("=" * 60)
    print("DEMO 3: Bağlantı Bilgilerini Güvenli Kaydetme")
    print("=" * 60)
    
    storage = ConnectionStorage()
    
    # Bağlantı bilgilerini oluştur
    conn_info = create_connection_dict(
        db_type='postgresql',
        host='localhost',
        port=5432,
        username='postgres',
        password='secret_password',
        database='my_database'
    )
    
    # Kaydet
    if storage.save_connection('my_postgres_db', conn_info):
        print("✓ Bağlantı başarıyla kaydedildi!")
        
        # Kaydedilen bağlantıları listele
        saved = storage.get_connection_names()
        print(f"\nKayıtlı bağlantılar: {saved}")
        
        # Bağlantıyı geri yükle
        loaded = storage.load_connection('my_postgres_db')
        print(f"\nYüklenen bağlantı bilgileri:")
        print(f"  Tip: {loaded['db_type']}")
        print(f"  Host: {loaded['host']}")
        print(f"  Database: {loaded['database']}")
    else:
        print("✗ Kaydetme başarısız!")
    
    print()


def demo_transfer_tables():
    """Örnek: Veri aktarımı"""
    print("=" * 60)
    print("DEMO 4: Tablolar Arası Veri Aktarımı")
    print("=" * 60)
    
    # Kaynak bağlantısı (MySQL)
    source = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='source_db'
    )
    
    # Hedef bağlantısı (PostgreSQL)
    target = DatabaseConnection(
        db_type='postgresql',
        host='localhost',
        port=5432,
        username='postgres',
        password='password',
        database='target_db'
    )
    
    # Bağlantıları kur
    if not (source.connect() and target.connect()):
        print("✗ Bağlantı kurulamadı!")
        return
    
    print("✓ Her iki bağlantı da başarılı!")
    
    # Transfer engine oluştur
    engine = DataTransferEngine(source, target)
    
    # Aktarım seçenekleri
    options = TransferOptions(
        mode=TransferOptions.SCHEMA_AND_DATA,
        chunk_size=1000,
        truncate_before_insert=True
    )
    
    # İlerleme callback fonksiyonu
    def progress_callback(progress):
        percentage = int(progress.get_percentage())
        print(f"  [{percentage}%] {progress.current_table_name}: "
              f"{progress.current_rows}/{progress.total_rows} satır")
    
    # Aktarımı başlat
    print("\nAktarım başlatılıyor...")
    result = engine.transfer_tables(
        table_names=['users', 'products', 'orders'],
        options=options,
        progress_callback=progress_callback
    )
    
    # Sonuçları göster
    print(f"\n{'=' * 60}")
    print(f"Aktarım Tamamlandı!")
    print(f"İşlenen tablo sayısı: {result.current_table}")
    
    if result.errors:
        print(f"\nHatalar ({len(result.errors)} adet):")
        for error in result.errors:
            print(f"  ✗ {error}")
    else:
        print("\n✓ Tüm tablolar başarıyla aktarıldı!")
    
    # Bağlantıları kapat
    source.close()
    target.close()
    
    print()


def demo_schema_only():
    """Örnek: Sadece şema aktarımı"""
    print("=" * 60)
    print("DEMO 5: Sadece Tablo Yapısı (Schema) Aktarımı")
    print("=" * 60)
    
    source = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='production_db'
    )
    
    target = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='test_db'
    )
    
    if source.connect() and target.connect():
        engine = DataTransferEngine(source, target)
        
        # Sadece şema aktarımı
        options = TransferOptions(mode=TransferOptions.SCHEMA_ONLY)
        
        print("Sadece tablo yapıları aktarılıyor (veri yok)...")
        result = engine.transfer_tables(
            table_names=['users', 'settings'],
            options=options
        )
        
        print(f"✓ {result.current_table} tablo yapısı aktarıldı")
        
        source.close()
        target.close()
    else:
        print("✗ Bağlantı hatası!")
    
    print()


def demo_data_only():
    """Örnek: Sadece veri aktarımı"""
    print("=" * 60)
    print("DEMO 6: Sadece Veri Aktarımı (Yapı Mevcut)")
    print("=" * 60)
    
    print("Bu mod, hedef veritabanında tablonun zaten var olduğunu varsayar.")
    print("Sadece veriyi aktarır, tablo yapısını oluşturmaz.\n")
    
    source = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='backup_db'
    )
    
    target = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='live_db'
    )
    
    if source.connect() and target.connect():
        engine = DataTransferEngine(source, target)
        
        # Sadece veri aktarımı
        options = TransferOptions(
            mode=TransferOptions.DATA_ONLY,
            truncate_before_insert=True  # Mevcut veriyi temizle
        )
        
        print("Veriler aktarılıyor...")
        result = engine.transfer_tables(
            table_names=['logs'],
            options=options
        )
        
        if not result.errors:
            print("✓ Veriler başarıyla aktarıldı!")
        else:
            print(f"✗ Hatalar oluştu: {result.errors}")
        
        source.close()
        target.close()
    else:
        print("✗ Bağlantı hatası!")
    
    print()


def main():
    """Ana demo fonksiyonu"""
    print("\n" + "=" * 60)
    print("SQL QUICK TRANSFER TOOL - DEMO UYGULAMASI")
    print("=" * 60)
    print("\nBu script, SQL Transfer Tool'un temel özelliklerini gösterir.")
    print("\nNot: Demo'ların çalışması için veritabanlarının kurulu olması gerekir.")
    print("Eğer veritabanlarınız yoksa, sadece kod örnekleri olarak inceleyebilirsiniz.\n")
    
    # Her demo fonksiyonunu çalıştır
    demos = [
        ("Bağlantı Testi", demo_connection_test),
        ("Tabloları Listeleme", demo_list_tables),
        ("Bağlantı Kaydetme", demo_save_connection),
        ("Veri Aktarımı", demo_transfer_tables),
        ("Sadece Şema Aktarımı", demo_schema_only),
        ("Sadece Veri Aktarımı", demo_data_only)
    ]
    
    print("Mevcut Demolar:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    
    print("\nHangi demo'yu çalıştırmak istersiniz? (1-6, 0=Tümü): ", end="")
    
    try:
        choice = input().strip()
        
        if choice == '0':
            # Tüm demolari çalıştır
            for name, demo_func in demos:
                try:
                    demo_func()
                except Exception as e:
                    print(f"✗ Hata: {str(e)}\n")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Seçilen demo'yu çalıştır
            name, demo_func = demos[int(choice) - 1]
            try:
                demo_func()
            except Exception as e:
                print(f"✗ Hata: {str(e)}\n")
        else:
            print("Geçersiz seçim!")
    
    except KeyboardInterrupt:
        print("\n\nDemo sonlandırıldı.")
    
    print("\n" + "=" * 60)
    print("Demo tamamlandı!")
    print("=" * 60)


if __name__ == '__main__':
    main()
