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
    Siccome le API di Yahoo Finance, se stressate, possono dare errore di rate limit, è possibile salvare ogni simulazione in una "cache".  
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
   python src/main.py
   ```

### Chiusura ambiente
```bash
deactivate
```

## 🔍 Note aggiuntive
- L'ambiente virtuale (`venv/`) non deve essere versionato
- Assicurarsi che tutti i requisiti siano installati prima dell'avvio