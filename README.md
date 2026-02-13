# SQL Quick Transfer Tool

**Tek Tıkla SQL Veri Aktarım Aracı**

SQL Quick Transfer Tool, farklı SQL veritabanları arasında hızlı ve kolay veri aktarımı yapmanızı sağlayan bir araçtır. Hem web tabanlı hem de masaüstü arayüz seçenekleri sunar.

## ✨ Özellikler

- 🔌 **Çoklu Veritabanı Desteği**: MySQL, PostgreSQL ve SQLite
- 🔐 **Güvenli Bağlantı Yönetimi**: Şifrelenmiş bağlantı bilgisi saklama
- 📋 **Esnek Aktarım Seçenekleri**:
  - Sadece Yapı (Schema Only)
  - Yapı ve Veri (Schema & Data)
  - Sadece Veri (Data Only)
- ⚡ **Performans Optimizasyonu**: Chunk-based veri aktarımı ile büyük tablolar için optimize edilmiş performans
- 📊 **Gerçek Zamanlı İlerleme Takibi**: Detaylı ilerleme çubuğu ve log sistemi
- 🎨 **İki Farklı Arayüz**: Web tabanlı (Flask) ve Masaüstü (PyQt6)

## 📁 Proje Yapısı

```
sql_transfer_tool/
├── core/                          # Çekirdek modüller
│   ├── __init__.py               # Modül başlatma
│   ├── database_connection.py   # Veritabanı bağlantı yönetimi
│   ├── transfer_engine.py       # Veri aktarım motoru
│   └── connection_storage.py    # Güvenli bağlantı saklama
├── web/                          # Flask web uygulaması
│   └── app.py                   # Flask sunucu
├── desktop/                      # PyQt6 masaüstü uygulaması
│   └── main.py                  # Masaüstü ana dosya
├── templates/                    # HTML şablonlar
│   └── index.html               # Ana sayfa
├── static/                       # Statik dosyalar
│   ├── css/
│   │   └── style.css            # CSS stilleri
│   └── js/
│       └── main.js              # JavaScript fonksiyonları
├── requirements.txt              # Python bağımlılıkları
└── README.md                     # Bu dosya
```

## 🚀 Kurulum

### 1. Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### 2. Bağımlılıkları Yükleyin

```bash
# Proje dizinine gidin
cd sql_transfer_tool

# Virtual environment oluşturun (önerilir)
python -m venv venv

# Virtual environment'ı aktifleştirin
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

## 💻 Kullanım

### Web Uygulaması (Flask)

```bash
# Web sunucusunu başlatın
python web/app.py

# Tarayıcınızda açın:
# http://localhost:5000
```

#### Web Arayüzü Kullanımı:

1. **Kaynak Veritabanı Bağlantısı**:
   - Veritabanı tipini seçin (MySQL, PostgreSQL, SQLite)
   - Bağlantı bilgilerini girin
   - "Bağlantıyı Test Et" ile bağlantıyı doğrulayın
   - "Bağlan" butonuna tıklayın

2. **Hedef Veritabanı Bağlantısı**:
   - Aynı adımları hedef veritabanı için tekrarlayın

3. **Tablo Seçimi**:
   - Kaynak veritabanına bağlandıktan sonra tablolar otomatik yüklenir
   - Aktarmak istediğiniz tabloları seçin
   - "Tümünü Seç" veya tekil seçim yapabilirsiniz

4. **Aktarım Seçenekleri**:
   - Aktarım modunu seçin (Yapı ve Veri / Sadece Yapı / Sadece Veri)
   - Parça boyutunu ayarlayın (önerilen: 1000)
   - İsteğe bağlı: "Hedef tabloyu önce temizle" seçeneği

5. **Aktarımı Başlatın**:
   - "Aktarımı Başlat" butonuna tıklayın
   - İlerleme durumunu takip edin
   - İşlem günlüğünü inceleyin

### Masaüstü Uygulaması (PyQt6)

```bash
# Masaüstü uygulamasını başlatın
python desktop/main.py
```

#### Masaüstü Arayüzü Kullanımı:

1. Sol panelde kaynak, sağ panelde hedef veritabanı bilgilerini girin
2. Her iki bağlantıyı da test edin ve bağlanın
3. "Tabloları Yükle" butonuna tıklayın
4. Aktarmak istediğiniz tabloları seçin
5. Aktarım seçeneklerini ayarlayın
6. "Aktarımı Başlat" butonuna tıklayın

## 🔧 Yapılandırma

### Veritabanı Bağlantı Formatları

#### MySQL
```
Host: localhost
Port: 3306
Username: root
Password: ****
Database: mydb
```

#### PostgreSQL
```
Host: localhost
Port: 5432
Username: postgres
Password: ****
Database: mydb
```

#### SQLite
```
Database: /path/to/database.db
(Host, Port, Username, Password gerekli değil)
```

### Güvenlik Notları

- Bağlantı bilgileri `cryptography` kütüphanesi ile şifrelenir
- Şifreleme anahtarı `.secret.key` dosyasında saklanır
- **ÖNEMLİ**: `.secret.key` dosyasını güvenli tutun ve versiyon kontrolüne eklemeyin

## 📚 API Referansı

### Core Modülleri

#### DatabaseConnection
```python
from core import DatabaseConnection

# Bağlantı oluşturma
conn = DatabaseConnection(
    db_type='mysql',
    host='localhost',
    port=3306,
    username='root',
    password='password',
    database='mydb'
)

# Bağlantıyı test etme
success, message = conn.test_connection()

# Tabloları listeleme
tables = conn.get_tables()
```

#### DataTransferEngine
```python
from core import DataTransferEngine, TransferOptions

# Transfer engine oluşturma
engine = DataTransferEngine(source_conn, target_conn)

# Aktarım seçenekleri
options = TransferOptions(
    mode=TransferOptions.SCHEMA_AND_DATA,
    chunk_size=1000,
    truncate_before_insert=True
)

# Aktarım başlatma
result = engine.transfer_tables(
    table_names=['users', 'orders'],
    options=options
)
```

## 🐛 Sorun Giderme

### Yaygın Hatalar

1. **"Bağlantı Hatası"**:
   - Veritabanı sunucusunun çalıştığından emin olun
   - Host ve port bilgilerini kontrol edin
   - Firewall ayarlarını kontrol edin

2. **"Tablo Bulunamadı"**:
   - Kaynak veritabanında tablonun var olduğundan emin olun
   - Kullanıcı yetkilerini kontrol edin

3. **"Bellek Hatası"**:
   - Chunk size değerini azaltın (örn: 500)
   - Büyük tabloları tek tek aktarmayı deneyin

4. **"Import Hatası"**:
   - Tüm bağımlılıkların yüklendiğinden emin olun
   - `pip install -r requirements.txt` komutunu tekrar çalıştırın

## 🔄 Performans İpuçları

1. **Chunk Size Optimizasyonu**:
   - Küçük tablolar (<10K satır): 1000-2000
   - Orta tablolar (10K-1M satır): 5000-10000
   - Büyük tablolar (>1M satır): 10000+

2. **Ağ Performansı**:
   - Yerel aktarımlar için chunk size'ı artırabilirsiniz
   - Uzak sunuculara aktarımda chunk size'ı azaltın

3. **Eş Zamanlı Aktarım**:
   - Büyük projelerde tabloları gruplara ayırıp sırayla aktarın
   - Her grup için ayrı transfer işlemi başlatın

## 📝 Geliştirme

### Test Ortamı Kurulumu

```bash
# Test veritabanları oluşturma
# MySQL
mysql -u root -p -e "CREATE DATABASE test_source;"
mysql -u root -p -e "CREATE DATABASE test_target;"

# PostgreSQL
psql -U postgres -c "CREATE DATABASE test_source;"
psql -U postgres -c "CREATE DATABASE test_target;"
```

### Kod Standartları

- PEP 8 kod standartlarına uyun
- Docstring'ler ekleyin
- Type hints kullanın
- Error handling ekleyin

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje eğitim ve ticari olmayan kullanım için serbestçe kullanılabilir.

## 🙏 Teşekkürler

- SQLAlchemy - Veritabanı toolkit
- Flask - Web framework
- PyQt6 - GUI framework
- Cryptography - Şifreleme kütüphanesi

## 📞 İletişim

Sorularınız veya önerileriniz için issue açabilirsiniz.

---

**Notlar**:
- Üretim ortamında kullanmadan önce kapsamlı test yapın
- Yedekleme yapmadan büyük veri aktarımları yapmayın
- Güvenlik için bağlantı bilgilerini asla versiyon kontrolüne eklemeyin
