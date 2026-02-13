"""
SQL Transfer Tool - PyQt6 Masaüstü Uygulaması
Platform bağımsız masaüstü GUI uygulaması
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QListWidget,
    QProgressBar, QTextEdit, QTabWidget, QGroupBox, QFormLayout,
    QMessageBox, QSpinBox, QListWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

# Core modüllerini import et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database_connection import DatabaseConnection
from core.transfer_engine import DataTransferEngine, TransferOptions, TransferProgress
from core.connection_storage import ConnectionStorage, create_connection_dict


class TransferWorker(QThread):
    """Arka planda veri aktarımı yapan thread"""
    
    progress_updated = pyqtSignal(dict)
    transfer_completed = pyqtSignal(bool, str, list)
    
    def __init__(self, source, target, tables, options):
        super().__init__()
        self.source = source
        self.target = target
        self.tables = tables
        self.options = options
        
    def run(self):
        """Transfer işlemini çalıştırır"""
        try:
            engine = DataTransferEngine(self.source, self.target)
            
            def progress_callback(progress: TransferProgress):
                """İlerleme güncellemelerini emit et"""
                self.progress_updated.emit({
                    'current_table': progress.current_table,
                    'total_tables': progress.total_tables,
                    'table_name': progress.current_table_name,
                    'current_rows': progress.current_rows,
                    'total_rows': progress.total_rows,
                    'percentage': progress.get_percentage()
                })
            
            result = engine.transfer_tables(
                self.tables,
                self.options,
                progress_callback
            )
            
            success = len(result.errors) == 0
            message = f"{result.current_table} tablo işlendi"
            
            self.transfer_completed.emit(success, message, result.errors)
            
        except Exception as e:
            self.transfer_completed.emit(False, str(e), [str(e)])


class ConnectionPanel(QGroupBox):
    """Veritabanı bağlantı paneli widget'ı"""
    
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.connection = None
        self.init_ui()
        
    def init_ui(self):
        """UI bileşenlerini oluşturur"""
        layout = QFormLayout()
        
        # Veritabanı tipi
        self.db_type = QComboBox()
        self.db_type.addItems(['mysql', 'postgresql', 'sqlite'])
        self.db_type.currentTextChanged.connect(self.on_db_type_changed)
        layout.addRow('Veritabanı Tipi:', self.db_type)
        
        # Host
        self.host = QLineEdit('localhost')
        layout.addRow('Host:', self.host)
        
        # Port
        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.port.setValue(3306)
        layout.addRow('Port:', self.port)
        
        # Kullanıcı adı
        self.username = QLineEdit()
        layout.addRow('Kullanıcı Adı:', self.username)
        
        # Şifre
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow('Şifre:', self.password)
        
        # Veritabanı
        self.database = QLineEdit()
        layout.addRow('Veritabanı:', self.database)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        self.test_btn = QPushButton('🔍 Test Et')
        self.test_btn.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_btn)
        
        self.connect_btn = QPushButton('🔌 Bağlan')
        self.connect_btn.clicked.connect(self.connect_database)
        button_layout.addWidget(self.connect_btn)
        
        self.save_btn = QPushButton('💾 Kaydet')
        self.save_btn.clicked.connect(self.save_connection)
        button_layout.addWidget(self.save_btn)
        
        layout.addRow(button_layout)
        
        # Durum etiketi
        self.status_label = QLabel('')
        self.status_label.setWordWrap(True)
        layout.addRow(self.status_label)
        
        self.setLayout(layout)
        
    def on_db_type_changed(self, db_type):
        """Veritabanı tipi değiştiğinde port numarasını ayarlar"""
        if db_type == 'mysql':
            self.port.setValue(3306)
        elif db_type == 'postgresql':
            self.port.setValue(5432)
            
    def test_connection(self):
        """Bağlantıyı test eder"""
        try:
            conn = self.create_connection()
            success, message = conn.test_connection()
            
            if success:
                self.status_label.setText(f'✓ {message}')
                self.status_label.setStyleSheet('color: green;')
            else:
                self.status_label.setText(f'✗ {message}')
                self.status_label.setStyleSheet('color: red;')
                
        except Exception as e:
            self.status_label.setText(f'✗ Hata: {str(e)}')
            self.status_label.setStyleSheet('color: red;')
            
    def connect_database(self):
        """Veritabanına bağlanır"""
        try:
            self.connection = self.create_connection()
            
            if self.connection.connect():
                self.status_label.setText('✓ Bağlantı başarılı!')
                self.status_label.setStyleSheet('color: green;')
                return True
            else:
                self.status_label.setText('✗ Bağlantı başarısız')
                self.status_label.setStyleSheet('color: red;')
                return False
                
        except Exception as e:
            self.status_label.setText(f'✗ Hata: {str(e)}')
            self.status_label.setStyleSheet('color: red;')
            return False
            
    def save_connection(self):
        """Bağlantı bilgilerini kaydeder"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, 'Bağlantı Kaydet', 
                                        'Bağlantı adı:')
        if ok and name:
            storage = ConnectionStorage()
            conn_dict = create_connection_dict(
                self.db_type.currentText(),
                self.host.text(),
                self.port.value(),
                self.username.text(),
                self.password.text(),
                self.database.text()
            )
            
            if storage.save_connection(name, conn_dict):
                QMessageBox.information(self, 'Başarılı', 
                                      f'Bağlantı kaydedildi: {name}')
            else:
                QMessageBox.warning(self, 'Hata', 'Bağlantı kaydedilemedi')
                
    def create_connection(self):
        """Bağlantı nesnesi oluşturur"""
        return DatabaseConnection(
            db_type=self.db_type.currentText(),
            host=self.host.text(),
            port=self.port.value(),
            username=self.username.text(),
            password=self.password.text(),
            database=self.database.text()
        )
        
    def get_connection(self):
        """Aktif bağlantıyı döndürür"""
        return self.connection


class SQLTransferApp(QMainWindow):
    """Ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        self.setWindowTitle('SQL Quick Transfer Tool')
        self.setGeometry(100, 100, 1000, 800)
        
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Başlık
        title = QLabel('🗄️ SQL Quick Transfer Tool')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        subtitle = QLabel('Tek Tıkla SQL Veri Aktarım Aracı')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Bağlantı panelleri
        conn_layout = QHBoxLayout()
        
        self.source_panel = ConnectionPanel('📥 Kaynak Veritabanı')
        conn_layout.addWidget(self.source_panel)
        
        self.target_panel = ConnectionPanel('📤 Hedef Veritabanı')
        conn_layout.addWidget(self.target_panel)
        
        main_layout.addLayout(conn_layout)
        
        # Tablo seçimi
        table_group = QGroupBox('Tablolar')
        table_layout = QVBoxLayout()
        
        table_buttons = QHBoxLayout()
        
        self.load_tables_btn = QPushButton('📋 Tabloları Yükle')
        self.load_tables_btn.clicked.connect(self.load_tables)
        table_buttons.addWidget(self.load_tables_btn)
        
        self.select_all_btn = QPushButton('Tümünü Seç')
        self.select_all_btn.clicked.connect(self.select_all_tables)
        table_buttons.addWidget(self.select_all_btn)
        
        self.deselect_all_btn = QPushButton('Seçimi Temizle')
        self.deselect_all_btn.clicked.connect(self.deselect_all_tables)
        table_buttons.addWidget(self.deselect_all_btn)
        
        table_layout.addLayout(table_buttons)
        
        self.table_list = QListWidget()
        self.table_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        table_layout.addWidget(self.table_list)
        
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)
        
        # Aktarım seçenekleri
        options_group = QGroupBox('⚙️ Aktarım Seçenekleri')
        options_layout = QFormLayout()
        
        self.transfer_mode = QComboBox()
        self.transfer_mode.addItems([
            'Yapı ve Veri',
            'Sadece Yapı',
            'Sadece Veri'
        ])
        options_layout.addRow('Aktarım Modu:', self.transfer_mode)
        
        self.chunk_size = QSpinBox()
        self.chunk_size.setRange(100, 10000)
        self.chunk_size.setValue(1000)
        options_layout.addRow('Parça Boyutu:', self.chunk_size)
        
        self.truncate_check = QCheckBox('Hedef tabloyu önce temizle')
        self.truncate_check.setChecked(True)
        options_layout.addRow(self.truncate_check)
        
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)
        
        # Aktarım butonu
        self.transfer_btn = QPushButton('🚀 Aktarımı Başlat')
        self.transfer_btn.setMinimumHeight(50)
        self.transfer_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.transfer_btn.clicked.connect(self.start_transfer)
        main_layout.addWidget(self.transfer_btn)
        
        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Log alanı
        log_group = QGroupBox('📊 İşlem Günlüğü')
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
    def load_tables(self):
        """Kaynak veritabanından tabloları yükler"""
        source_conn = self.source_panel.get_connection()
        
        if not source_conn:
            QMessageBox.warning(self, 'Uyarı', 
                              'Önce kaynak veritabanına bağlanın!')
            return
            
        tables = source_conn.get_tables()
        
        self.table_list.clear()
        for table in tables:
            item = QListWidgetItem(table)
            self.table_list.addItem(item)
            
        self.log_text.append(f'✓ {len(tables)} tablo yüklendi')
        
    def select_all_tables(self):
        """Tüm tabloları seçer"""
        self.table_list.selectAll()
        
    def deselect_all_tables(self):
        """Tablo seçimini temizler"""
        self.table_list.clearSelection()
        
    def start_transfer(self):
        """Veri aktarımını başlatır"""
        # Bağlantıları kontrol et
        source = self.source_panel.get_connection()
        target = self.target_panel.get_connection()
        
        if not source or not target:
            QMessageBox.warning(self, 'Uyarı',
                              'Kaynak ve hedef bağlantılarını kurun!')
            return
            
        # Seçili tabloları al
        selected_items = self.table_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Uyarı',
                              'En az bir tablo seçin!')
            return
            
        tables = [item.text() for item in selected_items]
        
        # Transfer modunu ayarla
        mode_map = {
            'Yapı ve Veri': TransferOptions.SCHEMA_AND_DATA,
            'Sadece Yapı': TransferOptions.SCHEMA_ONLY,
            'Sadece Veri': TransferOptions.DATA_ONLY
        }
        
        options = TransferOptions(
            mode=mode_map[self.transfer_mode.currentText()],
            chunk_size=self.chunk_size.value(),
            truncate_before_insert=self.truncate_check.isChecked()
        )
        
        # İlerleme çubuğunu göster
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Log temizle
        self.log_text.clear()
        self.log_text.append(f'Aktarım başlatılıyor...')
        self.log_text.append(f'{len(tables)} tablo aktarılacak')
        
        # Worker thread oluştur ve başlat
        self.worker = TransferWorker(source, target, tables, options)
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.transfer_completed.connect(self.on_transfer_completed)
        self.worker.start()
        
        # Butonu devre dışı bırak
        self.transfer_btn.setEnabled(False)
        
    def on_progress_updated(self, data):
        """İlerleme güncellemelerini işler"""
        percentage = int(data['percentage'])
        self.progress_bar.setValue(percentage)
        
        if data['table_name']:
            msg = f"{data['table_name']}: {data['current_rows']}/{data['total_rows']} satır"
            self.log_text.append(msg)
            
    def on_transfer_completed(self, success, message, errors):
        """Aktarım tamamlandığında çağrılır"""
        self.transfer_btn.setEnabled(True)
        
        if success:
            self.progress_bar.setValue(100)
            self.log_text.append('✓ Aktarım başarıyla tamamlandı!')
            QMessageBox.information(self, 'Başarılı', message)
        else:
            self.log_text.append('✗ Aktarım hatası: ' + message)
            
            if errors:
                for error in errors:
                    self.log_text.append('  - ' + error)
                    
            QMessageBox.warning(self, 'Hata', message)


def main():
    """Uygulamayı başlatır"""
    app = QApplication(sys.argv)
    
    # Uygulama stili
    app.setStyle('Fusion')
    
    window = SQLTransferApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
