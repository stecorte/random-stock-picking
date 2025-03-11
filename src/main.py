"""
[IT]
Analisi Monte Carlo investendo a caso su una stock alla volta presa dal mercato desiderato.

Si parte dalla giornata di START_DATE.
Si prende una stock a caso e la si tiene nel portafoglio fino a quando il suo valore scende sotto MIN_PERC_THRESHOLD oppure supera MAX_PERC_THRESHOLD rispetto al prezzo di acquisto.
Quando esce da questo range la si vende, se ne acquista un'altra e la si vende seguendo la stessa regola.
Si fa lo stesso procedimento fino ad arrivare al giorno corrente.

Questa simulazione viene effettuata per ITERATIONS volte.
Il numero minimo di iterazioni per avere dei risultati consistenti è 10.000. Più sale il numero di iterazioni più precisa sarà l'analisi.

Per ogni acquisto o vendita si può settare COMMISSIONS_PERC per simulare la % che bisogna pagare per eseguire l'operazione oppure/e la fee fissa.

Non si acquista un numero definito di stock ma quote frazionate. Se si parte con 1000$ e compro Apple, verranno acquistate 4,197 stock (al valore del 28 Gennaio 2025 ovvero 238,26$).

Si reinveste sempre tutto il valore delle vandita.

[EN]
Monte Carlo Analysis by randomly investing in one stock at a time from the desired market.

Starting from START_DATE, the simulation:
- Randomly selects a stock.
- Holds it until its value drops below MIN_PERC_THRESHOLD or exceeds MAX_PERC_THRESHOLD relative to purchase price
- Upon exiting this range, sells it and purchases another random stock following the same rule
- Continues this process until reaching the current date

The simulation runs ITERATIONS times. Minimum iterations for consistent results is 10,000. Higher iterations yield more precise analysis.

COMMISSIONS_PERC can be set for each buy/sell to simulate percentage-based commissions and/or fixed fees.

Fractional shares are used instead of whole shares. Example: With $1000 initial investment buying Apple, 4.197 shares would be purchased (at January 28, 2025 price of $238.26).

All sale proceeds are reinvested.
"""

from libs.companies import stock_markets
import libs.utilities as utils
from datetime import datetime, timedelta
import libs.cache as cache
import importlib
import libs.database as db

"""
CONFIGURATION PARAMETERS
"""
STOCK_MARKET_NAME = "nasdaq100"
STOCK_MARKET = stock_markets[STOCK_MARKET_NAME]
MIN_PERC_THRESHOLD = -1
MAX_PERC_THRESHOLD = 1
ITERATIONS = 10000
START_DATE = "2024-02-04"
END_DATE = "2025-02-09"
COMMISSIONS_PERC = 0
COMMISSIONS_FEE = 0
INITIAL_INVESTMENT_USD = 1000
USE_CACHE=True
BENCHMARK = 27.96


start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
if END_DATE is not None:
    end_date = datetime.strptime(END_DATE, "%Y-%m-%d").date()
else:
    end_date = (datetime.now() - timedelta(days=1)).date()

print(f"Start date: {start_date.strftime('%Y-%m-%d')}\n")
print(f"End date: {end_date.strftime('%Y-%m-%d')}\n")

db.create_db_if_not_exists()

"""
Creo la struttura dati per i risultati. 
Creo tutti i range di risultati possibili, uno ogni 5%, sia in positivo che in negativo.
"""
bins = {}
results = {
    "history": [],
}

for i in [0, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101]:
    bins[utils.calculate_roi_bin(i)] = 0

for i in [-1, -6, -11, -16, -21, -26, -31, -36, -41, -46, -51]:
    bins[utils.calculate_roi_bin(i)] = 0

# Recupero le simulazioni già fatta dalla cache
if USE_CACHE:
    cache_key = f"{STOCK_MARKET_NAME}_{str(MIN_PERC_THRESHOLD).replace('-', '_')}_{str(MAX_PERC_THRESHOLD).replace('-', '_')}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}_{str(COMMISSIONS_PERC).replace('.', '_')}_{str(COMMISSIONS_FEE).replace('.', '_')}_{str(INITIAL_INVESTMENT_USD).replace('.', '_')}"
    utils.write_cache_key_if_not_exists(cache_key)
    importlib.reload(cache) # Ricarico il modulo. Serve se ho appena creato la chiave
    cache = getattr(cache, cache_key)
    print(f"\nCi sono {len(cache)} simulazioni in cache\n")
    for simulation_in_cache in cache:
        results["history"].append(simulation_in_cache)

for i in range(ITERATIONS):
    print(f"Iteration n° {i+1}")
    
    date_iteration = start_date.date()
    balance = INITIAL_INVESTMENT_USD

    while date_iteration <= end_date:
        _, current_stock = utils.get_random_stock(STOCK_MARKET)

        """ 
        Recupero 1 anno di storico. Ipotizzo che almeno un giorno in questo periodo la stock esca dal range.
        Se pensi che serva più tempo (perché magari ha inserito una soglia molto ampia) modifica il periodo all'interno della funzione.
        Serve anche a ridurre le chiamate a Yahoo. Altrimenti bisognerebbe fare una chiamata per ogni giorno.
        """
        stock_history = utils.get_stock_price_history(ticker=current_stock, start_date=date_iteration)

        """
        Calcolo quando uscire in base alla soglia. 
        La funzione restituisce il balance e la data di uscita.
        """
        props = {
            "current_stock": current_stock,
            "min_perc_threshold": MIN_PERC_THRESHOLD,
            "max_perc_threshold": MAX_PERC_THRESHOLD,
            "commissions_perc": COMMISSIONS_PERC,
            "commissions_fee": COMMISSIONS_FEE
        }
        date_iteration, stock_value, balance = utils.get_stock_data_on_exit(stock_history=stock_history, props=props, balance=balance)
        
        date_iteration = date_iteration + timedelta(days=1)

    return_on_investment = ((balance - INITIAL_INVESTMENT_USD) / INITIAL_INVESTMENT_USD) * 100

    simulation = {
        "initial_balance": INITIAL_INVESTMENT_USD,
        "final_balance": balance,
        "return_on_investment": return_on_investment,
    }

    results["history"].append(simulation)

    # Inserisco la simulazione dentro la cache
    if USE_CACHE:
        utils.append_to_cache_key(cache_key, data=simulation)

    print(f"Iteration completed.")
    print(f"Initial balance: ${INITIAL_INVESTMENT_USD}")
    print(f"Final balance ${balance:.2f}")
    print(f"Return on investment: {return_on_investment:.1f}%")
    print("") 

# Smisto i risultati nei bin e genero statistiche ad alto livello
positive_results = 0
negative_results = 0
results_above_benchmark = 0
results_above_than_20perc = 0
results_less_than_20perc = 0
results_less_than_50perc = 0

for simulation in results["history"]:
    if simulation["return_on_investment"] >= 0:
        positive_results += 1
    else:
        negative_results += 1

    if simulation["return_on_investment"] > BENCHMARK:
        results_above_benchmark += 1

    if simulation["return_on_investment"] < -20:
        results_less_than_20perc += 1

    if simulation["return_on_investment"] < -50:
        results_less_than_50perc += 1

    if simulation["return_on_investment"] > 20:
        results_above_than_20perc += 1

    bins[utils.calculate_roi_bin(simulation["return_on_investment"])] += 1

print(f"Benchmark: {BENCHMARK}%")
print(f"Results above benchmark: {results_above_benchmark} ({(results_above_benchmark / len(results['history'])) * 100:.2f}%)\n")

print(f"Positive results: {positive_results} ({(positive_results / len(results["history"])) * 100:.2f}%)")
print(f"Negative results: {negative_results} ({(negative_results / len(results["history"])) * 100:.2f}%)\n")

print(f"Results above than +20%: {results_above_than_20perc} ({(results_above_than_20perc / len(results['history'])) * 100:.2f}%)")
print(f"Results less than -20%: {results_less_than_20perc} ({(results_less_than_20perc / len(results['history'])) * 100:.2f}%)")
print(f"Results less than -50%: {results_less_than_50perc} ({(results_less_than_50perc / len(results['history'])) * 100:.2f}%)\n")

params = {
    "min_perc_threshold": MIN_PERC_THRESHOLD,
    "max_perc_threshold": MAX_PERC_THRESHOLD,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
    "simulations": len(results["history"]),
}
utils.create_bins_histogram_chart(bins, params)