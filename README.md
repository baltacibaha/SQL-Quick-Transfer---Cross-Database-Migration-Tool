# 🗄️ SQL Quick Transfer Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/yourusername/sql-transfer-tool)
[![Database](https://img.shields.io/badge/Database-MySQL%20%7C%20PostgreSQL%20%7C%20SQLite-orange.svg)](https://github.com/yourusername/sql-transfer-tool)

**One-click SQL data transfer tool for seamless database migration**

Transfer tables and data between different SQL databases (MySQL, PostgreSQL, SQLite) with just one click. Built for developers and database administrators who need quick, reliable data transfers without complex ETL processes.

---

## ✨ Features

- 🔄 **Multi-Database Support** - MySQL, PostgreSQL, and SQLite
- 🔐 **Secure Connection Management** - Encrypted credential storage using AES-256
- 📋 **Flexible Transfer Modes**:
  - Schema Only (structure without data)
  - Data Only (data without structure)
  - Schema + Data (complete table transfer)
- ⚡ **Performance Optimized** - Chunk-based transfer for large datasets
- 📊 **Real-time Progress Tracking** - Detailed progress bar and logging system
- 🎨 **Dual Interface Options**:
  - 🌐 Web Interface (Flask-based)
  - 🖥️ Desktop Application (PyQt6/Tkinter)
- 🛡️ **Safe Operations** - Validated SQL operations with error handling
- 🚀 **Easy Setup** - Automated installation scripts included

---

## 🎯 Use Cases

- 📦 **Database Migration** - Move data between different database systems
- 🧪 **Testing Environments** - Quickly populate test databases
- 💾 **Backup Operations** - Create database backups and snapshots
- 🔄 **Data Synchronization** - Keep multiple databases in sync
- 🏗️ **Development Setup** - Set up local development databases easily

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sql-transfer-tool.git
cd sql-transfer-tool

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Quick Run

**Option 1: Web Interface** (Recommended)
```bash
python start.py web
# Open browser: http://localhost:5000
```

**Option 2: Desktop Application** (Tkinter - No installation required)
```bash
python standalone_app.py
```

**Option 3: Desktop Application** (PyQt6 - Modern UI)
```bash
python desktop/main.py
```

---

## 📖 Usage Guide

### Web Interface

1. **Connect Source Database**
   - Select database type (MySQL/PostgreSQL/SQLite)
   - Enter connection details
   - Click "Test Connection" to verify
   - Click "Connect"

2. **Connect Target Database**
   - Repeat above steps for target database

3. **Select Tables**
   - Tables are automatically loaded from source
   - Select tables you want to transfer
   - Use "Select All" or individual selection

4. **Configure Transfer Options**
   - Choose transfer mode (Schema + Data / Schema Only / Data Only)
   - Set chunk size (recommended: 1000)
   - Optional: Enable "Truncate target table before insert"

5. **Start Transfer**
   - Click "Start Transfer"
   - Monitor progress in real-time
   - Check log for detailed information

### Desktop Application

1. Enter connection details in left panel (Source) and right panel (Target)
2. Test and connect both databases
3. Click "Load Tables" button
4. Select tables to transfer
5. Configure transfer options
6. Click "Start Transfer" and monitor progress

---

## 🔧 Configuration

### Database Connection Examples

**MySQL**
```python
Host: localhost
Port: 3306
Username: root
Password: your_password
Database: mydb
```

**PostgreSQL**
```python
Host: localhost
Port: 5432
Username: postgres
Password: your_password
Database: mydb
```

**SQLite**
```python
Database: /path/to/database.db
# No host, port, username, or password needed
```

---

## 💻 API Usage

### Python API Example

```python
from core import DatabaseConnection, DataTransferEngine, TransferOptions

# Create connections
source = DatabaseConnection(
    db_type='mysql',
    host='localhost',
    port=3306,
    username='root',
    password='password',
    database='source_db'
)

target = DatabaseConnection(
    db_type='postgresql',
    host='localhost',
    port=5432,
    username='postgres',
    password='password',
    database='target_db'
)

# Connect
source.connect()
target.connect()

# Create transfer engine
engine = DataTransferEngine(source, target)

# Configure transfer options
options = TransferOptions(
    mode=TransferOptions.SCHEMA_AND_DATA,
    chunk_size=1000,
    truncate_before_insert=True
)

# Transfer tables
result = engine.transfer_tables(
    table_names=['users', 'orders', 'products'],
    options=options
)

print(f"Transfer completed: {result.current_table} tables processed")
```

---

## 📁 Project Structure

```
sql_transfer_tool/
├── core/                      # Core modules
│   ├── database_connection.py # Database connection management
│   ├── transfer_engine.py     # Data transfer engine
│   └── connection_storage.py  # Secure credential storage
├── web/                       # Flask web application
│   └── app.py                # Web server
├── desktop/                   # Desktop applications
│   ├── main.py               # PyQt6 version
│   └── main_tkinter.py       # Tkinter version
├── templates/                 # HTML templates
│   └── index.html            # Main page
├── static/                    # Static files
│   ├── css/style.css         # Stylesheets
│   └── js/main.js            # JavaScript
├── standalone_app.py          # Standalone single-file app
├── start.py                   # Quick launcher
├── demo.py                    # Demo examples
└── requirements.txt           # Python dependencies
```

---

## ⚡ Performance Tips

### Chunk Size Optimization

| Table Size | Recommended Chunk Size |
|-----------|----------------------|
| Small (<10K rows) | 1,000 - 2,000 |
| Medium (10K-1M rows) | 5,000 - 10,000 |
| Large (>1M rows) | 10,000+ |

### Network Performance

- **Local transfers**: Increase chunk size for better speed
- **Remote transfers**: Decrease chunk size to avoid timeouts
- **Large datasets**: Transfer tables in batches

---

## 🐛 Troubleshooting

### Common Issues

**"Connection Error"**
- Ensure database server is running
- Check host and port configuration
- Verify firewall settings

**"Table Not Found"**
- Confirm table exists in source database
- Check user permissions

**"Memory Error"**
- Reduce chunk size (e.g., 500)
- Transfer large tables individually

**"Import Error"**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)

**"Windows Long Path Error" (PyQt6)**
- Use Tkinter version instead: `python standalone_app.py`
- Or enable Windows Long Path support (see documentation)

---

## 🔒 Security

- Connection credentials are encrypted using AES-256 via the `cryptography` library
- Encryption key is stored in `.secret.key` (automatically generated)
- **Important**: Never commit `.secret.key` to version control
- SQL operations use parameterized queries to prevent injection attacks

---

## 🧪 Development

### Setting Up Development Environment

```bash
# Create test databases
# MySQL
mysql -u root -p -e "CREATE DATABASE test_source;"
mysql -u root -p -e "CREATE DATABASE test_target;"

# PostgreSQL
psql -U postgres -c "CREATE DATABASE test_source;"
psql -U postgres -c "CREATE DATABASE test_target;"
```

### Running Tests

```bash
# Run demo examples
python demo.py

# Check package installation
python check_packages.py

# Test file structure
python check_files.py
```

### Code Standards

- Follow PEP 8 style guide
- Include docstrings for all functions and classes
- Use type hints where applicable
- Implement comprehensive error handling

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your PR:
- Includes relevant tests
- Updates documentation as needed
- Follows existing code style
- Includes a clear description of changes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit and ORM
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [Cryptography](https://cryptography.io/) - Encryption library

---

## 📞 Support

- 📖 [Documentation](https://github.com/yourusername/sql-transfer-tool/wiki)
- 🐛 [Issue Tracker](https://github.com/yourusername/sql-transfer-tool/issues)
- 💬 [Discussions](https://github.com/yourusername/sql-transfer-tool/discussions)

---

## ⚠️ Disclaimer

- Always test transfers in a safe environment before using in production
- Create backups before performing large data transfers
- Verify data integrity after transfer operations
- This tool is provided as-is without warranty

---

## 🗺️ Roadmap

- [ ] Add support for MongoDB and other NoSQL databases
- [ ] Implement data transformation capabilities
- [ ] Add scheduling/automation features
- [ ] Create Docker container
- [ ] Add REST API endpoints
- [ ] Implement incremental backup support
- [ ] Add CSV/Excel import/export
- [ ] Multi-language support (i18n)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by baltacibaha, for developers**
