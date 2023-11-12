from flask import Flask, render_template, request
from google.cloud import firestore

app = Flask(__name__)
base_url = "http://localhost:80"

# Configura il client Firestore
db = firestore.Client.from_service_account_json('credentials.json')

# Funzione per inserire i dati soglia e l'email nel database
def setup_threshold_and_alert(email, threshold_value, sensor_type):
    # Crea un riferimento al documento nel database
    user_ref = db.collection('users').document(email)

    # Controlla se l'utente esiste già nel database
    user_data = user_ref.get()
    if user_data.exists:
        user_ref.set({
            'email': email,
            'threshold_value': float(threshold_value),
            'sensor_type': sensor_type
        })
        return f"L'utente {email} era già presente nel database e la sua soglia è stata sovrascritta come segue: " \
               f"L'utente sarà avvisato quando la metrica {sensor_type} supererà il valore di {threshold_value}"


    # Inserisci i dati soglia e l'email nel documento
    user_ref.set({
        'email': email,
        'threshold_value': float(threshold_value),
        'sensor_type': sensor_type
    })
    return (f"Nuova soglia impostata per l'utente {email}: " \
           f"L'utente sarà avvisato quando la metrica {sensor_type} supererà il valore di {threshold_value}")



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        threshold_value = request.form['threshold_value']
        sensor_type = request.form['sensor_type']

        result = setup_threshold_and_alert(email, threshold_value, sensor_type)
        return render_template('result.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
