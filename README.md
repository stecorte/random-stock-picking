# 📈 Investire a caso - Episodio 1

## 📝 Descrizione
Analisi Monte Carlo per investimenti casuali su azioni. Il processo:
1. Selezione randomica di una stock
2. Investimento totale del capitale disponibile
3. Liquidazione quando il valore esce dai limiti percentuali stabiliti

## 🚀 Setup e Avvio

### Prerequisiti
- Python installato sul sistema

### Configurazione ambiente

1. **Creazione ambiente virtuale**
   ```bash
   python -m venv venv
   ```

2. **Attivazione ambiente**
   ```bash
   # Windows
   .\venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Installazione dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Creazione del file cache.py**  
   Per evitare di perdere tutte le simulazioni se lo script dovesse interrompresi per qualasiasi motivo, è possibile salvare ogni simulazione in una "cache".  
    Per utilizzare la cache è necessario creare un file con questo comando:
    ```bash
   # Windows
   echo. > src\libs\cache.py

   # macOS/Linux
   touch src/libs/cache.py
   ```

   Per dsabilitare la cache basta modificare a `False` il parametro `USE_CACHE` dentro il file `src/main.py`

4. **Avvio applicazione**
   ```bash
   # Salva lo storico delle stock su un database SQLite creato in locale (da eseguire solo la prima volta)
   python src/store-stock-history.py

   python src/main.py
   ```

### Chiusura ambiente
```bash
deactivate
```

## 🔍 Note aggiuntive
- L'ambiente virtuale (`venv/`) non deve essere versionato
- Assicurarsi che tutti i requisiti siano installati prima dell'avvio