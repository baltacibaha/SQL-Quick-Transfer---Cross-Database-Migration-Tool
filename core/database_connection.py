"""
Veritabanı Bağlantı Yöneticisi
Bu modül, farklı SQL veritabanlarına bağlantı kurma ve yönetme işlemlerini sağlar.
"""

from sqlalchemy import create_engine, inspect, MetaData, Table, text
from sqlalchemy.engine import Engine
from typing import Dict, List, Optional, Tuple
import logging

# Logging yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Veritabanı bağlantısı için temel sınıf"""
    
    def __init__(self, db_type: str, host: str, port: int, 
                 username: str, password: str, database: str):
        """
        Args:
            db_type: Veritabanı tipi (mysql, postgresql, sqlite)
            host: Sunucu adresi
            port: Port numarası
            username: Kullanıcı adı
            password: Şifre
            database: Veritabanı adı
        """
        self.db_type = db_type.lower()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.engine: Optional[Engine] = None
        self.metadata = MetaData()
        
    def get_connection_string(self) -> str:
        """Veritabanı tipine göre bağlantı string'i oluşturur"""
        if self.db_type == 'mysql':
            return f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.db_type == 'postgresql':
            return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.db_type == 'sqlite':
            # SQLite için dosya yolu kullanılır
            return f"sqlite:///{self.database}"
        else:
            raise ValueError(f"Desteklenmeyen veritabanı tipi: {self.db_type}")
    
    def connect(self) -> bool:
        """Veritabanına bağlantı kurar"""
        try:
            connection_string = self.get_connection_string()
            self.engine = create_engine(connection_string, echo=False)
            
            # Bağlantı testini yap
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info(f"{self.db_type} veritabanına başarıyla bağlanıldı: {self.database}")
            return True
            
        except Exception as e:
            logger.error(f"Bağlantı hatası: {str(e)}")
            return False
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Bağlantıyı test eder
        
        Returns:
            (başarı_durumu, mesaj)
        """
        try:
            if self.connect():
                return True, "Bağlantı başarılı!"
            else:
                return False, "Bağlantı kurulamadı."
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def get_tables(self) -> List[str]:
        """Veritabanındaki tüm tabloları listeler"""
        try:
            if not self.engine:
                self.connect()
            
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            logger.info(f"{len(tables)} tablo bulundu")
            return sorted(tables)
            
        except Exception as e:
            logger.error(f"Tablo listesi alınamadı: {str(e)}")
            return []
    
    def get_table_schema(self, table_name: str) -> Optional[Table]:
        """
        Belirtilen tablonun şemasını alır
        
        Args:
            table_name: Tablo adı
            
        Returns:
            SQLAlchemy Table nesnesi
        """
        try:
            if not self.engine:
                self.connect()
            
            metadata = MetaData()
            table = Table(table_name, metadata, autoload_with=self.engine)
            return table
            
        except Exception as e:
            logger.error(f"Tablo şeması alınamadı ({table_name}): {str(e)}")
            return None
    
    def close(self):
        """Bağlantıyı kapatır"""
        if self.engine:
            self.engine.dispose()
            logger.info("Bağlantı kapatıldı")


class ConnectionManager:
    """Birden fazla veritabanı bağlantısını yöneten sınıf"""
    
    def __init__(self):
        self.connections: Dict[str, DatabaseConnection] = {}
    
    def add_connection(self, name: str, connection: DatabaseConnection) -> bool:
        """Yeni bir bağlantı ekler"""
        try:
            if connection.connect():
                self.connections[name] = connection
                return True
            return False
        except Exception as e:
            logger.error(f"Bağlantı eklenemedi: {str(e)}")
            return False
    
    def get_connection(self, name: str) -> Optional[DatabaseConnection]:
        """İsimle bağlantı getirir"""
        return self.connections.get(name)
    
    def remove_connection(self, name: str):
        """Bağlantıyı kaldırır"""
        if name in self.connections:
            self.connections[name].close()
            del self.connections[name]
    
    def close_all(self):
        """Tüm bağlantıları kapatır"""
        for connection in self.connections.values():
            connection.close()
        self.connections.clear()
