"""
Bağlantı Bilgilerini Güvenli Saklama Modülü
Bu modül, veritabanı bağlantı bilgilerini şifreleyerek yerel dosyada saklar.
"""

import json
import os
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
import base64
import hashlib

class ConnectionStorage:
    """Bağlantı bilgilerini güvenli şekilde saklayan sınıf"""
    
    def __init__(self, storage_file: str = "connections.enc"):
        """
        Args:
            storage_file: Bağlantı bilgilerinin saklanacağı dosya adı
        """
        self.storage_file = storage_file
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        
    def _get_or_create_key(self) -> bytes:
        """
        Şifreleme anahtarını alır veya oluşturur
        
        Returns:
            Şifreleme anahtarı
        """
        key_file = ".secret.key"
        
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            # Yeni anahtar oluştur
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
    
    def save_connection(self, name: str, connection_info: Dict) -> bool:
        """
        Bağlantı bilgisini şifreleyerek kaydeder
        
        Args:
            name: Bağlantı adı
            connection_info: Bağlantı bilgileri (dict)
            
        Returns:
            Başarı durumu
        """
        try:
            # Mevcut bağlantıları yükle
            connections = self.load_all_connections()
            
            # Yeni bağlantıyı ekle veya güncelle
            connections[name] = connection_info
            
            # JSON'a çevir ve şifrele
            json_data = json.dumps(connections)
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            # Dosyaya yaz
            with open(self.storage_file, "wb") as f:
                f.write(encrypted_data)
            
            return True
            
        except Exception as e:
            print(f"Kaydetme hatası: {str(e)}")
            return False
    
    def load_connection(self, name: str) -> Optional[Dict]:
        """
        Belirtilen bağlantı bilgisini yükler
        
        Args:
            name: Bağlantı adı
            
        Returns:
            Bağlantı bilgileri veya None
        """
        connections = self.load_all_connections()
        return connections.get(name)
    
    def load_all_connections(self) -> Dict:
        """
        Tüm bağlantı bilgilerini yükler
        
        Returns:
            Bağlantı bilgileri dictionary'si
        """
        try:
            if not os.path.exists(self.storage_file):
                return {}
            
            # Dosyadan oku ve şifreyi çöz
            with open(self.storage_file, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            connections = json.loads(decrypted_data.decode())
            
            return connections
            
        except Exception as e:
            print(f"Yükleme hatası: {str(e)}")
            return {}
    
    def delete_connection(self, name: str) -> bool:
        """
        Belirtilen bağlantıyı siler
        
        Args:
            name: Bağlantı adı
            
        Returns:
            Başarı durumu
        """
        try:
            connections = self.load_all_connections()
            
            if name in connections:
                del connections[name]
                
                # Güncellenmiş listeyi kaydet
                json_data = json.dumps(connections)
                encrypted_data = self.cipher.encrypt(json_data.encode())
                
                with open(self.storage_file, "wb") as f:
                    f.write(encrypted_data)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Silme hatası: {str(e)}")
            return False
    
    def get_connection_names(self) -> List[str]:
        """
        Kayıtlı tüm bağlantı isimlerini döndürür
        
        Returns:
            Bağlantı isimleri listesi
        """
        connections = self.load_all_connections()
        return list(connections.keys())


def create_connection_dict(db_type: str, host: str, port: int,
                           username: str, password: str, database: str) -> Dict:
    """
    Bağlantı bilgilerinden dictionary oluşturur
    
    Args:
        db_type: Veritabanı tipi
        host: Sunucu adresi
        port: Port numarası
        username: Kullanıcı adı
        password: Şifre
        database: Veritabanı adı
        
    Returns:
        Bağlantı bilgileri dictionary'si
    """
    return {
        "db_type": db_type,
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "database": database
    }
