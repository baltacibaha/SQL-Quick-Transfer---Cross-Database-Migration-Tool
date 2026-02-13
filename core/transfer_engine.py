"""
Veri Aktarım Motor Modülü
Bu modül, kaynak ve hedef veritabanları arasında veri aktarımı yapar.
"""

from sqlalchemy import Table, MetaData, text, insert
from sqlalchemy.schema import CreateTable
from typing import List, Optional, Callable
import logging
from .database_connection import DatabaseConnection

logger = logging.getLogger(__name__)


class TransferOptions:
    """Aktarım seçeneklerini tutan sınıf"""
    
    SCHEMA_ONLY = "schema_only"
    SCHEMA_AND_DATA = "schema_and_data"
    DATA_ONLY = "data_only"
    
    def __init__(self, mode: str = SCHEMA_AND_DATA, 
                 chunk_size: int = 1000,
                 truncate_before_insert: bool = True):
        """
        Args:
            mode: Aktarım modu (schema_only, schema_and_data, data_only)
            chunk_size: Veri aktarımında kullanılacak parça boyutu
            truncate_before_insert: Veri eklemeden önce hedef tabloyu temizle
        """
        self.mode = mode
        self.chunk_size = chunk_size
        self.truncate_before_insert = truncate_before_insert


class TransferProgress:
    """Aktarım ilerlemesini takip eden sınıf"""
    
    def __init__(self, total_tables: int):
        self.total_tables = total_tables
        self.current_table = 0
        self.current_table_name = ""
        self.current_rows = 0
        self.total_rows = 0
        self.errors = []
        
    def update(self, table_name: str, rows_transferred: int, total_rows: int):
        """İlerleme bilgisini günceller"""
        self.current_table_name = table_name
        self.current_rows = rows_transferred
        self.total_rows = total_rows
        
    def next_table(self):
        """Bir sonraki tabloya geç"""
        self.current_table += 1
        self.current_rows = 0
        self.total_rows = 0
        
    def add_error(self, error: str):
        """Hata ekle"""
        self.errors.append(error)
        
    def get_percentage(self) -> float:
        """Toplam ilerleme yüzdesini hesaplar"""
        if self.total_tables == 0:
            return 0.0
        return (self.current_table / self.total_tables) * 100


class DataTransferEngine:
    """Veri aktarım işlemlerini gerçekleştiren ana sınıf"""
    
    def __init__(self, source: DatabaseConnection, target: DatabaseConnection):
        """
        Args:
            source: Kaynak veritabanı bağlantısı
            target: Hedef veritabanı bağlantısı
        """
        self.source = source
        self.target = target
        
    def transfer_tables(self, 
                       table_names: List[str], 
                       options: TransferOptions,
                       progress_callback: Optional[Callable] = None) -> TransferProgress:
        """
        Belirtilen tabloları aktarır
        
        Args:
            table_names: Aktarılacak tablo isimleri listesi
            options: Aktarım seçenekleri
            progress_callback: İlerleme bildirimi için callback fonksiyonu
            
        Returns:
            TransferProgress nesnesi
        """
        progress = TransferProgress(len(table_names))
        
        for table_name in table_names:
            try:
                logger.info(f"Tablo aktarılıyor: {table_name}")
                
                # Şema aktarımı
                if options.mode in [TransferOptions.SCHEMA_ONLY, TransferOptions.SCHEMA_AND_DATA]:
                    self._transfer_schema(table_name)
                
                # Veri aktarımı
                if options.mode in [TransferOptions.SCHEMA_AND_DATA, TransferOptions.DATA_ONLY]:
                    rows_transferred = self._transfer_data(
                        table_name, 
                        options, 
                        progress,
                        progress_callback
                    )
                    logger.info(f"{table_name}: {rows_transferred} satır aktarıldı")
                
                progress.next_table()
                
                if progress_callback:
                    progress_callback(progress)
                    
            except Exception as e:
                error_msg = f"{table_name} aktarılırken hata: {str(e)}"
                logger.error(error_msg)
                progress.add_error(error_msg)
                progress.next_table()
                
        return progress
    
    def _transfer_schema(self, table_name: str):
        """Tablo şemasını aktarır"""
        try:
            # Kaynak tablodan şemayı al
            source_metadata = MetaData()
            source_table = Table(table_name, source_metadata, autoload_with=self.source.engine)
            
            # Hedef veritabanında tablo var mı kontrol et
            target_inspector = inspect(self.target.engine)
            if table_name in target_inspector.get_table_names():
                logger.info(f"{table_name} hedefte zaten var, şema aktarımı atlanıyor")
                return
            
            # Hedef veritabanında tabloyu oluştur
            target_metadata = MetaData()
            target_table = Table(table_name, target_metadata)
            
            # Sütunları kopyala
            for column in source_table.columns:
                target_table.append_column(column.copy())
            
            # Tabloyu oluştur
            target_metadata.create_all(self.target.engine)
            logger.info(f"{table_name} şeması başarıyla oluşturuldu")
            
        except Exception as e:
            raise Exception(f"Şema aktarım hatası: {str(e)}")
    
    def _transfer_data(self, 
                      table_name: str, 
                      options: TransferOptions,
                      progress: TransferProgress,
                      progress_callback: Optional[Callable] = None) -> int:
        """
        Tablo verilerini aktarır
        
        Returns:
            Aktarılan satır sayısı
        """
        try:
            # Kaynak tablodan veriyi oku
            source_metadata = MetaData()
            source_table = Table(table_name, source_metadata, autoload_with=self.source.engine)
            
            # Hedef tabloyu al
            target_metadata = MetaData()
            target_table = Table(table_name, target_metadata, autoload_with=self.target.engine)
            
            # Toplam satır sayısını al
            with self.source.engine.connect() as conn:
                total_rows = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table_name}")
                ).scalar()
            
            progress.update(table_name, 0, total_rows)
            
            # Hedef tabloyu temizle (gerekirse)
            if options.truncate_before_insert:
                with self.target.engine.connect() as conn:
                    conn.execute(text(f"DELETE FROM {table_name}"))
                    conn.commit()
                logger.info(f"{table_name} temizlendi")
            
            # Veriyi parçalar halinde aktar
            rows_transferred = 0
            offset = 0
            
            while True:
                # Kaynak veriden bir parça al
                with self.source.engine.connect() as source_conn:
                    select_stmt = source_table.select().limit(options.chunk_size).offset(offset)
                    rows = source_conn.execute(select_stmt).fetchall()
                
                if not rows:
                    break
                
                # Hedef veritabanına ekle
                with self.target.engine.connect() as target_conn:
                    # Row nesnelerini dictionary'e çevir
                    rows_dict = [dict(row._mapping) for row in rows]
                    
                    if rows_dict:
                        target_conn.execute(insert(target_table), rows_dict)
                        target_conn.commit()
                
                rows_transferred += len(rows)
                offset += options.chunk_size
                
                # İlerleme güncelle
                progress.update(table_name, rows_transferred, total_rows)
                if progress_callback:
                    progress_callback(progress)
                
                logger.info(f"{table_name}: {rows_transferred}/{total_rows} satır aktarıldı")
            
            return rows_transferred
            
        except Exception as e:
            raise Exception(f"Veri aktarım hatası: {str(e)}")


# inspect import'unu ekleyelim
from sqlalchemy import inspect
