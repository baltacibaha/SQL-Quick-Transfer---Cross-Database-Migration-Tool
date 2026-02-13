// SQL Quick Transfer Tool - JavaScript Ana Dosyası

// Global değişkenler
let sourceConnected = false;
let targetConnected = false;
let selectedTables = [];

/**
 * Veritabanı bağlantısını test eder
 */
async function testConnection(type) {
    const data = getConnectionData(type);
    const statusEl = document.getElementById(`${type}Status`);
    
    statusEl.className = 'status-message info';
    statusEl.textContent = 'Bağlantı test ediliyor...';
    
    try {
        const response = await fetch('/api/test-connection', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            statusEl.className = 'status-message success';
            statusEl.textContent = '✓ ' + result.message;
        } else {
            statusEl.className = 'status-message error';
            statusEl.textContent = '✗ ' + result.message;
        }
    } catch (error) {
        statusEl.className = 'status-message error';
        statusEl.textContent = '✗ Bağlantı hatası: ' + error.message;
    }
}

/**
 * Veritabanına bağlanır
 */
async function connectDatabase(type) {
    const data = getConnectionData(type);
    data.type = type;
    const statusEl = document.getElementById(`${type}Status`);
    
    statusEl.className = 'status-message info';
    statusEl.textContent = 'Bağlanılıyor...';
    
    try {
        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            statusEl.className = 'status-message success';
            statusEl.textContent = '✓ ' + result.message;
            
            if (type === 'source') {
                sourceConnected = true;
                await loadTables();
            } else {
                targetConnected = true;
            }
            
            // Transfer bölümünü göster
            checkTransferReady();
        } else {
            statusEl.className = 'status-message error';
            statusEl.textContent = '✗ ' + result.message;
        }
    } catch (error) {
        statusEl.className = 'status-message error';
        statusEl.textContent = '✗ Bağlantı hatası: ' + error.message;
    }
}

/**
 * Bağlantı bilgilerini kaydeder
 */
async function saveConnection(type) {
    const name = prompt('Bu bağlantı için bir isim girin:');
    if (!name) return;
    
    const data = getConnectionData(type);
    data.name = name;
    
    try {
        const response = await fetch('/api/save-connection', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✓ Bağlantı kaydedildi: ' + name);
        } else {
            alert('✗ Kaydetme başarısız: ' + result.message);
        }
    } catch (error) {
        alert('✗ Hata: ' + error.message);
    }
}

/**
 * Form verilerinden bağlantı bilgilerini alır
 */
function getConnectionData(type) {
    return {
        db_type: document.getElementById(`${type}DbType`).value,
        host: document.getElementById(`${type}Host`).value,
        port: document.getElementById(`${type}Port`).value,
        username: document.getElementById(`${type}Username`).value,
        password: document.getElementById(`${type}Password`).value,
        database: document.getElementById(`${type}Database`).value
    };
}

/**
 * Kaynak veritabanındaki tabloları yükler
 */
async function loadTables() {
    try {
        const response = await fetch('/api/get-tables/source');
        const result = await response.json();
        
        if (result.success) {
            displayTables(result.tables);
            document.getElementById('sourceTables').style.display = 'block';
        } else {
            alert('Tablolar yüklenemedi: ' + result.message);
        }
    } catch (error) {
        alert('Hata: ' + error.message);
    }
}

/**
 * Tabloları listede gösterir
 */
function displayTables(tables) {
    const tableList = document.getElementById('sourceTableList');
    tableList.innerHTML = '';
    
    tables.forEach(table => {
        const div = document.createElement('div');
        div.className = 'table-item';
        div.innerHTML = `
            <input type="checkbox" id="table_${table}" value="${table}" onchange="updateSelectedTables()">
            <label for="table_${table}">${table}</label>
        `;
        tableList.appendChild(div);
    });
}

/**
 * Tüm tabloları seçer
 */
function selectAllTables() {
    const checkboxes = document.querySelectorAll('.table-list input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = true);
    updateSelectedTables();
}

/**
 * Tablo seçimini temizler
 */
function deselectAllTables() {
    const checkboxes = document.querySelectorAll('.table-list input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = false);
    updateSelectedTables();
}

/**
 * Seçili tabloları günceller
 */
function updateSelectedTables() {
    const checkboxes = document.querySelectorAll('.table-list input[type="checkbox"]:checked');
    selectedTables = Array.from(checkboxes).map(cb => cb.value);
}

/**
 * Transfer bölümünün gösterilmesi için kontrol
 */
function checkTransferReady() {
    if (sourceConnected && targetConnected) {
        document.getElementById('transferSection').style.display = 'block';
    }
}

/**
 * Veri aktarımını başlatır
 */
async function startTransfer() {
    if (selectedTables.length === 0) {
        alert('Lütfen en az bir tablo seçin!');
        return;
    }
    
    const transferData = {
        tables: selectedTables,
        mode: document.getElementById('transferMode').value,
        chunk_size: parseInt(document.getElementById('chunkSize').value),
        truncate: document.getElementById('truncateTable').checked
    };
    
    // İlerleme bölümünü göster
    const progressSection = document.getElementById('progressSection');
    progressSection.style.display = 'block';
    progressSection.scrollIntoView({ behavior: 'smooth' });
    
    // Log mesajlarını temizle
    const logMessages = document.getElementById('logMessages');
    logMessages.innerHTML = '';
    
    addLog('Aktarım başlatılıyor...', 'info');
    addLog(`${selectedTables.length} tablo aktarılacak`, 'info');
    
    try {
        const response = await fetch('/api/transfer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(transferData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // İlerleme güncellemelerini göster
            if (result.progress_updates) {
                result.progress_updates.forEach(update => {
                    updateProgress(update);
                    addLog(`${update.table_name}: ${update.current_rows}/${update.total_rows} satır`, 'success');
                });
            }
            
            updateProgress({ percentage: 100 });
            addLog('✓ Aktarım başarıyla tamamlandı!', 'success');
            
        } else {
            addLog('✗ Aktarım hatası: ' + result.message, 'error');
            
            if (result.errors && result.errors.length > 0) {
                result.errors.forEach(error => {
                    addLog('  - ' + error, 'error');
                });
            }
        }
    } catch (error) {
        addLog('✗ Beklenmeyen hata: ' + error.message, 'error');
    }
}

/**
 * İlerleme çubuğunu günceller
 */
function updateProgress(data) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const progressDetails = document.getElementById('progressDetails');
    
    const percentage = Math.round(data.percentage || 0);
    progressFill.style.width = percentage + '%';
    progressText.textContent = percentage + '%';
    
    if (data.table_name) {
        progressDetails.innerHTML = `
            <p><strong>Şu an aktarılan:</strong> ${data.table_name}</p>
            <p><strong>Tablo:</strong> ${data.current_table}/${data.total_tables}</p>
            <p><strong>Satırlar:</strong> ${data.current_rows}/${data.total_rows}</p>
        `;
    }
}

/**
 * Log mesajı ekler
 */
function addLog(message, type = 'info') {
    const logMessages = document.getElementById('logMessages');
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    
    const timestamp = new Date().toLocaleTimeString('tr-TR');
    entry.textContent = `[${timestamp}] ${message}`;
    
    logMessages.appendChild(entry);
    logMessages.scrollTop = logMessages.scrollHeight;
}

/**
 * Veritabanı tipi değiştiğinde port numarasını otomatik ayarlar
 */
document.addEventListener('DOMContentLoaded', () => {
    // Kaynak veritabanı
    document.getElementById('sourceDbType').addEventListener('change', (e) => {
        const port = document.getElementById('sourcePort');
        if (e.target.value === 'mysql') port.value = 3306;
        else if (e.target.value === 'postgresql') port.value = 5432;
    });
    
    // Hedef veritabanı
    document.getElementById('targetDbType').addEventListener('change', (e) => {
        const port = document.getElementById('targetPort');
        if (e.target.value === 'mysql') port.value = 3306;
        else if (e.target.value === 'postgresql') port.value = 5432;
    });
});
