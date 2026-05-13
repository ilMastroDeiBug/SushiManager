# Usa un'immagine Python ufficiale come base
FROM python:3.11-slim

# Imposta la directory di lavoro nel contenitore
WORKDIR /app

# Copia i requisiti e installali prima, per velocizzare la build
# Assumiamo che tu abbia un file chiamato requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto dei file (sushi-app.py, ordini.json, static, templates)
COPY . .

# Espone la porta usata dall'applicazione Flask
EXPOSE 5000

# Comando per avviare l'applicazione
# Gunicorn è lo standard per i siti web, ma usiamo python per semplicità
CMD ["python", "sushi-app.py"]