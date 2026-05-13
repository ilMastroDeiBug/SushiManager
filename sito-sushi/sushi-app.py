from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "ordini.json"

# --- GESTIONE DATI ---
def carica_ordini():
    if not os.path.exists(DATA_FILE): return {}
    try:
        with open(DATA_FILE, 'r') as f: return json.load(f)
    except: return {}

def salva_ordini(ordini):
    with open(DATA_FILE, 'w') as f: json.dump(ordini, f, indent=4)

# --- HOME PAGE ---
@app.route('/')
def home():
    dati = carica_ordini()
    
    # --- 1. GESTIONE "LA MIA LISTA" ---
    nome_cercato = request.args.get('cerca_nome')
    lista_personale = []
    totale_personale = 0
    
    if nome_cercato and nome_cercato in dati:
        for piatto, qta in dati[nome_cercato].items():
            lista_personale.append({'piatto': piatto, 'qta': qta})
            totale_personale += qta
            
        # ORDINAMENTO FIXATO (Numeri prima, parole poi)
        lista_personale.sort(key=lambda x: (0, int(x['piatto'])) if x['piatto'].isdigit() else (1, x['piatto'].lower()))

    # --- 2. GESTIONE "LISTA GENERALE" ---
    tutti_i_piatti = set()
    for ordini_utente in dati.values():
        tutti_i_piatti.update(ordini_utente.keys())
    
    # ORDINAMENTO FIXATO PER LA LISTA GENERALE
    piatti_ordinati = sorted(list(tutti_i_piatti), key=lambda x: (0, int(x)) if x.isdigit() else (1, x.lower()))

    lista_generale = []
    totale_generale_pezzi = 0

    for piatto in piatti_ordinati:
        qta_totale_piatto = 0
        dettagli_nomi = []

        for utente, ordini in dati.items():
            if piatto in ordini:
                qta = ordini[piatto]
                qta_totale_piatto += qta
                dettagli_nomi.append(f"{utente} ({qta})")
        
        totale_generale_pezzi += qta_totale_piatto
        
        lista_generale.append({
            "nome": piatto,
            "totale": qta_totale_piatto,
            "dettagli": ", ".join(dettagli_nomi)
        })

    return render_template('index.html', 
                           lista_generale=lista_generale, 
                           totale_generale=totale_generale_pezzi,
                           lista_personale=lista_personale,
                           totale_personale=totale_personale,
                           nome_cercato=nome_cercato)

# --- AGGIUNGI ORDINE ---
@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    utente = request.form.get('utente').strip()
    piatto = request.form.get('piatto').strip().upper() # Metto tutto maiuscolo per evitare duplicati (Sake vs sake)
    
    try:
        qta = int(request.form.get('quantita'))
    except:
        qta = 1

    dati = carica_ordini()

    if utente not in dati: dati[utente] = {}
    
    if piatto in dati[utente]:
        dati[utente][piatto] += qta
    else:
        dati[utente][piatto] = qta

    salva_ordini(dati)
    return redirect(f'/?cerca_nome={utente}') 

# --- NUOVA FUNZIONE RIMUOVI ---
@app.route('/rimuovi/<utente>/<piatto>')
def rimuovi(utente, piatto):
    dati = carica_ordini()
    
    # Se l'utente e il piatto esistono, rimuoviamo il piatto
    if utente in dati and piatto in dati[utente]:
        del dati[utente][piatto]
        
        # Pulizia: se l'utente non ha più piatti, togliamo l'utente
        if not dati[utente]:
            del dati[utente]
            
        salva_ordini(dati)
    
    return redirect(f'/?cerca_nome={utente}')

# --- RESET ---
@app.route('/reset')
def reset():
    salva_ordini({})
    return redirect('/')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    pass