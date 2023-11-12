from google.cloud import firestore

# Configura il client Firestore
db = firestore.Client.from_service_account_json('credentials.json')

# Funzione per inserire i dati soglia e l'email nel database
def setup_threshold_and_alert():
    # Input
    email = input("Inserisci il tuo indirizzo email: ")
    threshold_value = float(input("Inserisci il valore di soglia: "))
    sensor_type = input("Inserisci la metrica da monitorare (Umidita, Velocita del vento, Temperatura massima, Temperatura minima, Precipitazioni): ")
    # Crea un riferimento al documento nel database
    user_ref = db.collection('users').document(email)
  # Controlla se l'utente esiste già nel database
    user_data = user_ref.get()
    if user_data.exists:
        print(f"Utente {email} esiste già nel database.")
        return

    # Inserisci i dati soglia e l'email nel documento
    user_ref.set({
        'email': email,
        'threshold_value': threshold_value,
        'sensor_type': sensor_type
    })


if __name__ == '__main__':
    setup_threshold_and_alert()
