import random
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from libs.database import get_stock_history


def get_random_stock(stocks_list):
    return random.choice(list(stocks_list.items()))


def get_stock_price_history(ticker, start_date):
    return get_stock_history(stock=ticker, since=start_date)


"""
Percorre lo storico della stock e quando il suo valore esce dai limiti di min_perc_threshold e max_perc_threshold
ritorna la data di uscita, il valore della stock e il valore del portafoglio aggiornato
"""
def get_stock_data_on_exit(stock_history, props, balance):
    initial_price = None
    min_price = None
    max_price = None
    stocks_purchased = 0

    commissions = {
        "commissions_perc": props["commissions_perc"],
        "commissions_fee": props["commissions_fee"]
    }

    for stock_data in stock_history:
        # Prendo il prezzo di entrata
        if initial_price is None: 
            initial_price = stock_data['close_price']
            min_price = stock_data['close_price'] * (1 + props["min_perc_threshold"]/100)
            max_price = stock_data['close_price'] * (1 + props["max_perc_threshold"]/100)
            stocks_purchased = balance / initial_price
            balance = stocks_purchased * initial_price

            print(f"\tEntering {props["current_stock"]} on {stock_data['stock_date']} at ${initial_price:.2f} per share ({stocks_purchased:.2f} shares)")
            
        # Controllo quando (e se) il valore della stock esce dai limiti
        if stock_data['close_price'] < min_price or stock_data['close_price'] > max_price:
            balance = stocks_purchased * stock_data['close_price']
            print(f"\tExiting {props["current_stock"]} on {stock_data['stock_date']} at ${stock_data['close_price']:.2f} per share")
            balance = sub_commissions_to_balance(balance=balance, commissions=commissions)
            return stock_data['stock_date'], stock_data['close_price'], balance
        
    balance = sub_commissions_to_balance(balance=balance, commissions=commissions)
    return stock_data['stock_date'], stock_data['close_price'], balance


def sub_commissions_to_balance(balance, commissions):
    if isinstance(commissions["commissions_perc"], (int, float)):
        balance = balance - (balance * (commissions["commissions_perc"] / 100))
    
    if isinstance(commissions["commissions_fee"], (int, float)):
        balance = balance - commissions["commissions_fee"]

    return balance


def calculate_roi_bin(roi):
    if roi <= -50: return "[(100)-(50)]"
    if roi > 100: return "[100-inf]"

    if roi < 0:
        base = int(roi // 10) * 10 
        return f"[({abs(base)})-({abs(base + 10)})]"
    
    if roi >= 0:
        base = int(roi // 5) * 5
        return f"[{base}-{base + 5}]"


def create_bins_histogram_chart(bins, params):
    bins_percentages = {k: (v/params["simulations"])*100 for k, v in bins.items()}

    positive_ranges = {k: v for k, v in bins_percentages.items() if not k.startswith('[(')}
    negative_ranges = {k: v for k, v in bins_percentages.items() if k.startswith('[(')}

    # Invertiamo l'ordine dei dizionari
    negative_ranges = dict(reversed(list(negative_ranges.items())))

    plt.figure(figsize=(15,6))

    # Plot dei valori negativi con percentuali
    x_neg = np.arange(len(negative_ranges))
    plt.bar(x_neg, list(negative_ranges.values()), 
            align='center', 
            alpha=0.8,
            color='lightcoral',
            label='Negative bins')
    
    # Plot dei valori positivi con percentuali
    x_pos = np.arange(len(negative_ranges), len(negative_ranges) + len(positive_ranges))
    plt.bar(x_pos, list(positive_ranges.values()), 
            align='center',
            alpha=0.8,
            color='skyblue',
            label='Positive bins')
    
    # Creazione etichette nell'ordine corretto
    all_labels = list(negative_ranges.keys()) + list(positive_ranges.keys())

    # Personalizzazione del grafico
    plt.xlabel('Bins')
    plt.ylabel('Probability (%)')
    plt.title('Intervals distribution')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Rotazione labels
    plt.xticks(np.arange(len(bins)), 
               all_labels,
               rotation=45,
               ha='right')
    
    # Aggiustare layout
    plt.tight_layout()

    # Salvataggio grafico
    plt.savefig(f"bins_intervals_distribution_{params['start_date']}_{params['end_date']}_[MIN_PERC_THRESHOLD={params['min_perc_threshold']}]_[MAX_PERC_THRESHOLD={params['max_perc_threshold']}].png", dpi=300, bbox_inches='tight')

    # Mostra il grafico
    plt.show()


def write_cache_key_if_not_exists(cache_key):
    lib_dir = os.path.dirname(os.path.abspath(__file__))
    cache_file = os.path.join(lib_dir, 'cache.py')

    try:
        # Leggiamo il contenuto attuale
        with open(cache_file, 'r') as file:
            content = file.read()
            lines = content.split('\n')
    except FileNotFoundError:
        lines = []
        with open(cache_file, 'w') as file:
            file.write('')  # Crea un file vuoto

    # Controlliamo se la variabile esiste già
    variable_exists = False
    for i, line in enumerate(lines):
        if line.startswith(f"{cache_key} ="):
            variable_exists = True
            break

    if not variable_exists:
        if lines and lines[-1].strip():
            lines.append('')
        lines.append(f"{cache_key} = []")

    with open(cache_file, 'w') as file:
        file.write('\n'.join(lines))
        if lines:
            file.write('\n')


def append_to_cache_key(cache_key, data):
    lib_dir = os.path.dirname(os.path.abspath(__file__))
    cache_file = os.path.join(lib_dir, 'cache.py')

    # Funzione per convertire numpy float in float Python
    def convert_numpy_floats(obj):
        if isinstance(obj, dict):
            return {k: convert_numpy_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_floats(v) for v in obj]
        elif str(type(obj)).find('numpy') != -1:  # Controllo generico per tipi numpy
            return float(obj)  # Converte in float Python
        return obj

    # Convertiamo i dati prima di inserirli
    cleaned_data = convert_numpy_floats(data)

    try:
        # Leggiamo il contenuto attuale
        with open(cache_file, 'r') as file:
            content = file.read()
            lines = content.split('\n')
    except FileNotFoundError:
        print(f"File {cache_file} non trovato")
        return

    # Cerchiamo la variabile e aggiorniamo il valore
    for i, line in enumerate(lines):
        if line.startswith(f"{cache_key} ="):
            current_value = line.split('=')[1].strip()
            try:
                current_list = eval(current_value)
                if not isinstance(current_list, list):
                    print(f"Il valore di {cache_key} non è una lista")
                    return
                # Aggiungiamo il nuovo dato convertito
                current_list.append(cleaned_data)
                # Aggiorniamo la linea nel file
                lines[i] = f"{cache_key} = {current_list}"
                break
            except:
                print(f"Errore nel parsing del valore di {cache_key}")
                return
    else:
        print(f"Cache key {cache_key} non trovata nel file")
        return

    # Scriviamo il contenuto aggiornato
    with open(cache_file, 'w') as file:
        file.write('\n'.join(lines))
        if lines:
            file.write('\n')
        