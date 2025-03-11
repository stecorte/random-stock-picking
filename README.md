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

4. **Salvataggio dello storico delle stock in locale**  
   Per evitare di chiamare in continuazone le API di Yahoo finance, esegui questo script per salvare in locale le performance di ogni stock nel mercato selezionato:
   ```bash 
   python src/store-stock-history.py
   ```

   I dati vengono salvati in un database SQLite dentro la cartella del progetto.

5. **Creazione del file cache.py**  
   Per evitare di perdere tutte le simulazioni se lo script dovesse interrompersi per qualasiasi motivo, è possibile salvare ogni simulazione in una "cache".  
    Per utilizzare la cache è necessario creare un file con questo comando:
    ```bash
   # Windows
   echo. > src\libs\cache.py

   # macOS/Linux
   touch src/libs/cache.py
   ```

   Per disabilitare la cache basta modificare a `False` il parametro `USE_CACHE` dentro il file `src/main.py`

6. **Avvio applicazione**
   ```bash
   python src/main.py
   ```

7. **Bonus**  
   Utilizza questo script per ricevere una stock random:
   ```bash
   python src/random-stock.py
   ```

### Chiusura ambiente
```bash
deactivate
```

## 🔍 Note aggiuntive
- L'ambiente virtuale (`venv/`) non deve essere versionato
- Assicurarsi che tutti i requisiti siano installati prima dell'avvio