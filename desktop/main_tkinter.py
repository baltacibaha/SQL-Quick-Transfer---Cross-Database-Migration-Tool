"""
SQL Transfer Tool - Tkinter Masaüstü Uygulaması
PyQt6 yerine alternatif - Windows Long Path sorunu olmadan!
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from threading import Thread

# Core modüllerini import et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database_connection import DatabaseConnection
from core.transfer_engine import DataTransferEngine, TransferOptions, TransferProgress
from core.connection_storage import ConnectionStorage, create_connection_dict


class ConnectionFrame(ttk.LabelFrame):
    """Veritabanı bağlantı çerçevesi"""
    
    def __init__(self, parent, title):
        super().__init__(parent, text=title, padding=10)
        self.connection = None
        self.create_widgets()
        
    def create_widgets(self):
        """Widget'ları oluştur"""
        row = 0
        
        # Veritabanı tipi
        ttk.Label(self, text="Veritabanı Tipi:").grid(row=row, column=0, sticky='w', pady=2)
        self.db_type = ttk.Combobox(self, values=['mysql', 'postgresql', 'sqlite'], state='readonly', width=20)
        self.db_type.set('mysql')
        self.db_type.grid(row=row, column=1, sticky='ew', pady=2)
        self.db_type.bind('<<ComboboxSelected>>', self.on_db_type_changed)
        row += 1
        
        # Host
        ttk.Label(self, text="Host:").grid(row=row, column=0, sticky='w', pady=2)
        self.host = ttk.Entry(self, width=23)
        self.host.insert(0, 'localhost')
        self.host.grid(row=row, column=1, sticky='ew', pady=2)
        row += 1
        
        # Port
        ttk.Label(self, text="Port:").grid(row=row, column=0, sticky='w', pady=2)
        self.port = ttk.Entry(self, width=23)
        self.port.insert(0, '3306')
        self.port.grid(row=row, column=1, sticky='ew', pady=2)
        row += 1
        
        # Username
        ttk.Label(self, text="Kullanıcı Adı:").grid(row=row, column=0, sticky='w', pady=2)
        self.username = ttk.Entry(self, width=23)
        self.username.grid(row=row, column=1, sticky='ew', pady=2)
        row += 1
        
        # Password
        ttk.Label(self, text="Şifre:").grid(row=row, column=0, sticky='w', pady=2)
        self.password = ttk.Entry(self, width=23, show='*')
        self.password.grid(row=row, column=1, sticky='ew', pady=2)
        row += 1
        
        # Database
        ttk.Label(self, text="Veritabanı:").grid(row=row, column=0, sticky='w', pady=2)
        self.database = ttk.Entry(self, width=23)
        self.database.grid(row=row, column=1, sticky='ew', pady=2)
        row += 1
        
        # Butonlar
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Test Et", command=self.test_connection).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Bağlan", command=self.connect).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Kaydet", command=self.save_connection).pack(side='left', padx=2)
        row += 1
        
        # Durum
        self.status = ttk.Label(self, text="", foreground='blue')
        self.status.grid(row=row, column=0, columnspan=2, pady=5)
        
        self.columnconfigure(1, weight=1)
        
    def on_db_type_changed(self, event=None):
        """Veritabanı tipi değiştiğinde port'u ayarla"""
        db_type = self.db_type.get()
        if db_type == 'mysql':
            self.port.delete(0, tk.END)
            self.port.insert(0, '3306')
        elif db_type == 'postgresql':
            self.port.delete(0, tk.END)
            self.port.insert(0, '5432')
            
    def test_connection(self):
        """Bağlantıyı test et"""
        try:
            conn = self.create_connection()
            success, message = conn.test_connection()
            
            if success:
                self.status.config(text=f"✓ {message}", foreground='green')
            else:
                self.status.config(text=f"✗ {message}", foreground='red')
        except Exception as e:
            self.status.config(text=f"✗ Hata: {str(e)}", foreground='red')
            
    def connect(self):
        """Bağlan"""
        try:
            self.connection = self.create_connection()
            if self.connection.connect():
                self.status.config(text="✓ Bağlantı başarılı!", foreground='green')
                return True
            else:
                self.status.config(text="✗ Bağlantı başarısız", foreground='red')
                return False
        except Exception as e:
            self.status.config(text=f"✗ Hata: {str(e)}", foreground='red')
            return False
            
    def save_connection(self):
        """Bağlantıyı kaydet"""
        name = tk.simpledialog.askstring("Kaydet", "Bağlantı adı:")
        if name:
            storage = ConnectionStorage()
            conn_dict = create_connection_dict(
                self.db_type.get(),
                self.host.get(),
                int(self.port.get()),
                self.username.get(),
                self.password.get(),
                self.database.get()
            )
            
            if storage.save_connection(name, conn_dict):
                messagebox.showinfo("Başarılı", f"Bağlantı kaydedildi: {name}")
            else:
                messagebox.showerror("Hata", "Bağlantı kaydedilemedi")
                
    def create_connection(self):
        """Bağlantı nesnesi oluştur"""
        return DatabaseConnection(
            db_type=self.db_type.get(),
            host=self.host.get(),
            port=int(self.port.get()),
            username=self.username.get(),
            password=self.password.get(),
            database=self.database.get()
        )
        
    def get_connection(self):
        """Aktif bağlantıyı döndür"""
        return self.connection


class SQLTransferApp(tk.Tk):
    """Ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        
        self.title("SQL Quick Transfer Tool - Tkinter")
        self.geometry("900x700")
        
        # Stil
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        # Başlık
        title_frame = ttk.Frame(self)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title = ttk.Label(title_frame, text="🗄️ SQL Quick Transfer Tool", 
                         font=('Arial', 16, 'bold'))
        title.pack()
        
        subtitle = ttk.Label(title_frame, text="Tkinter Sürümü - Windows Long Path sorunu yok!")
        subtitle.pack()
        
        # Bağlantı çerçeveleri
        conn_frame = ttk.Frame(self)
        conn_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.source_frame = ConnectionFrame(conn_frame, "📥 Kaynak Veritabanı")
        self.source_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.target_frame = ConnectionFrame(conn_frame, "📤 Hedef Veritabanı")
        self.target_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        # Tablo listesi
        table_frame = ttk.LabelFrame(self, text="Tablolar", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        btn_frame = ttk.Frame(table_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="📋 Tabloları Yükle", 
                  command=self.load_tables).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Tümünü Seç", 
                  command=self.select_all).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Seçimi Temizle", 
                  command=self.deselect_all).pack(side='left', padx=2)
        
        # Listbox + Scrollbar
        list_frame = ttk.Frame(table_frame)
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.table_list = tk.Listbox(list_frame, selectmode='multiple', 
                                     yscrollcommand=scrollbar.set)
        self.table_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.table_list.yview)
        
        # Seçenekler
        options_frame = ttk.LabelFrame(self, text="⚙️ Aktarım Seçenekleri", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(options_frame, text="Mod:").grid(row=0, column=0, sticky='w', padx=5)
        self.mode = ttk.Combobox(options_frame, values=[
            'Yapı ve Veri', 'Sadece Yapı', 'Sadece Veri'
        ], state='readonly', width=20)
        self.mode.set('Yapı ve Veri')
        self.mode.grid(row=0, column=1, sticky='w', padx=5)
        
        ttk.Label(options_frame, text="Parça Boyutu:").grid(row=0, column=2, sticky='w', padx=5)
        self.chunk_size = ttk.Spinbox(options_frame, from_=100, to=10000, width=10)
        self.chunk_size.set(1000)
        self.chunk_size.grid(row=0, column=3, sticky='w', padx=5)
        
        self.truncate = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Hedef tabloyu önce temizle", 
                       variable=self.truncate).grid(row=1, column=0, columnspan=4, 
                                                   sticky='w', pady=5)
        
        # Aktarım butonu
        ttk.Button(self, text="🚀 Aktarımı Başlat", command=self.start_transfer,
                  ).pack(pady=10)
        
        # İlerleme
        self.progress = ttk.Progressbar(self, mode='determinate')
        self.progress.pack(fill='x', padx=10, pady=5)
        
        # Log
        log_frame = ttk.LabelFrame(self, text="📊 İşlem Günlüğü", padding=5)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log.pack(fill='both', expand=True)
        
    def load_tables(self):
        """Tabloları yükle"""
        source = self.source_frame.get_connection()
        if not source:
            messagebox.showwarning("Uyarı", "Önce kaynak veritabanına bağlanın!")
            return
            
        tables = source.get_tables()
        self.table_list.delete(0, tk.END)
        
        for table in tables:
            self.table_list.insert(tk.END, table)
            
        self.add_log(f"✓ {len(tables)} tablo yüklendi")
        
    def select_all(self):
        """Tümünü seç"""
        self.table_list.select_set(0, tk.END)
        
    def deselect_all(self):
        """Seçimi temizle"""
        self.table_list.selection_clear(0, tk.END)
        
    def start_transfer(self):
        """Aktarımı başlat"""
        source = self.source_frame.get_connection()
        target = self.target_frame.get_connection()
        
        if not source or not target:
            messagebox.showwarning("Uyarı", "Kaynak ve hedef bağlantıları kurun!")
            return
            
        selected = self.table_list.curselection()
        if not selected:
            messagebox.showwarning("Uyarı", "En az bir tablo seçin!")
            return
            
        tables = [self.table_list.get(i) for i in selected]
        
        # Thread'de çalıştır
        thread = Thread(target=self.do_transfer, args=(source, target, tables))
        thread.daemon = True
        thread.start()
        
    def do_transfer(self, source, target, tables):
        """Aktarımı gerçekleştir"""
        self.add_log("Aktarım başlatılıyor...")
        self.progress['value'] = 0
        
        mode_map = {
            'Yapı ve Veri': TransferOptions.SCHEMA_AND_DATA,
            'Sadece Yapı': TransferOptions.SCHEMA_ONLY,
            'Sadece Veri': TransferOptions.DATA_ONLY
        }
        
        options = TransferOptions(
            mode=mode_map[self.mode.get()],
            chunk_size=int(self.chunk_size.get()),
            truncate_before_insert=self.truncate.get()
        )
        
        engine = DataTransferEngine(source, target)
        
        def progress_callback(progress):
            percentage = int(progress.get_percentage())
            self.progress['value'] = percentage
            
            if progress.current_table_name:
                msg = f"{progress.current_table_name}: {progress.current_rows}/{progress.total_rows}"
                self.add_log(msg)
                
        try:
            result = engine.transfer_tables(tables, options, progress_callback)
            
            if result.errors:
                self.add_log("✗ Hatalar oluştu:")
                for error in result.errors:
                    self.add_log(f"  - {error}")
                messagebox.showerror("Hata", "Aktarım sırasında hatalar oluştu!")
            else:
                self.add_log("✓ Aktarım başarıyla tamamlandı!")
                messagebox.showinfo("Başarılı", "Tüm tablolar aktarıldı!")
                
        except Exception as e:
            self.add_log(f"✗ Hata: {str(e)}")
            messagebox.showerror("Hata", str(e))
            
        self.progress['value'] = 100
        
    def add_log(self, message):
        """Log mesajı ekle"""
        self.log.config(state='normal')
        self.log.insert(tk.END, message + '\n')
        self.log.see(tk.END)
        self.log.config(state='disabled')


def main():
    """Uygulamayı başlat"""
    import tkinter.simpledialog
    app = SQLTransferApp()
    app.mainloop()


if __name__ == '__main__':
    main()
