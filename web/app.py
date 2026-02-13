"""
SQL Transfer Tool - Flask Web Uygulaması
Web tabanlı veri aktarım arayüzü
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sys
import os

# Core modüllerini import et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database_connection import DatabaseConnection, ConnectionManager
from core.transfer_engine import DataTransferEngine, TransferOptions, TransferProgress
from core.connection_storage import ConnectionStorage, create_connection_dict

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.secret_key = 'sql-transfer-tool-secret-key-2024'  # Üretimde değiştirilmeli
CORS(app)

# Global nesneler
connection_manager = ConnectionManager()
connection_storage = ConnectionStorage()


@app.route('/')
def index():
    """Ana sayfa"""
    saved_connections = connection_storage.get_connection_names()
    return render_template('index.html', saved_connections=saved_connections)


@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Veritabanı bağlantısını test eder"""
    try:
        data = request.json
        
        db_conn = DatabaseConnection(
            db_type=data['db_type'],
            host=data['host'],
            port=int(data['port']),
            username=data['username'],
            password=data['password'],
            database=data['database']
        )
        
        success, message = db_conn.test_connection()
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/save-connection', methods=['POST'])
def save_connection():
    """Bağlantı bilgilerini kaydeder"""
    try:
        data = request.json
        name = data['name']
        
        conn_info = create_connection_dict(
            db_type=data['db_type'],
            host=data['host'],
            port=int(data['port']),
            username=data['username'],
            password=data['password'],
            database=data['database']
        )
        
        success = connection_storage.save_connection(name, conn_info)
        
        return jsonify({
            'success': success,
            'message': 'Bağlantı kaydedildi' if success else 'Kaydetme başarısız'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/load-connection/<name>', methods=['GET'])
def load_connection(name):
    """Kayıtlı bağlantı bilgilerini yükler"""
    try:
        conn_info = connection_storage.load_connection(name)
        
        if conn_info:
            return jsonify({
                'success': True,
                'connection': conn_info
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Bağlantı bulunamadı'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/connect', methods=['POST'])
def connect():
    """Kaynak veya hedef veritabanına bağlanır"""
    try:
        data = request.json
        conn_type = data['type']  # 'source' veya 'target'
        
        db_conn = DatabaseConnection(
            db_type=data['db_type'],
            host=data['host'],
            port=int(data['port']),
            username=data['username'],
            password=data['password'],
            database=data['database']
        )
        
        if connection_manager.add_connection(conn_type, db_conn):
            return jsonify({
                'success': True,
                'message': f'{conn_type.capitalize()} bağlantısı kuruldu'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Bağlantı başarısız'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/get-tables/<conn_type>', methods=['GET'])
def get_tables(conn_type):
    """Bağlantıdaki tabloları listeler"""
    try:
        db_conn = connection_manager.get_connection(conn_type)
        
        if not db_conn:
            return jsonify({
                'success': False,
                'message': 'Bağlantı bulunamadı'
            }), 404
        
        tables = db_conn.get_tables()
        
        return jsonify({
            'success': True,
            'tables': tables
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/transfer', methods=['POST'])
def transfer():
    """Veri aktarım işlemini başlatır"""
    try:
        data = request.json
        
        # Bağlantıları al
        source = connection_manager.get_connection('source')
        target = connection_manager.get_connection('target')
        
        if not source or not target:
            return jsonify({
                'success': False,
                'message': 'Kaynak veya hedef bağlantısı eksik'
            }), 400
        
        # Aktarım seçenekleri
        options = TransferOptions(
            mode=data['mode'],
            chunk_size=data.get('chunk_size', 1000),
            truncate_before_insert=data.get('truncate', True)
        )
        
        # Transfer engine oluştur
        engine = DataTransferEngine(source, target)
        
        # İlerleme takibi için liste
        progress_updates = []
        
        def progress_callback(progress: TransferProgress):
            """İlerleme güncellemelerini topla"""
            progress_updates.append({
                'current_table': progress.current_table,
                'total_tables': progress.total_tables,
                'table_name': progress.current_table_name,
                'current_rows': progress.current_rows,
                'total_rows': progress.total_rows,
                'percentage': progress.get_percentage()
            })
        
        # Aktarımı başlat
        result = engine.transfer_tables(
            table_names=data['tables'],
            options=options,
            progress_callback=progress_callback
        )
        
        return jsonify({
            'success': len(result.errors) == 0,
            'message': f'{result.current_table} tablo işlendi',
            'errors': result.errors,
            'progress_updates': progress_updates
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Aktarım hatası: {str(e)}'
        }), 400


@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    """Tüm bağlantıları kapatır"""
    try:
        connection_manager.close_all()
        return jsonify({
            'success': True,
            'message': 'Tüm bağlantılar kapatıldı'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
