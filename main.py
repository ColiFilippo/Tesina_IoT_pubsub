# Importa le funzioni dalle diverse parti del tuo programma
from pub_data_from_xlsx import publish_excel_data
from check_data_send_alert import send_alert
from add_user_threshold import setup_threshold_and_alert
from google.cloud import firestore
import time

def main():
    # Esegui la funzione per leggere il file Excel e inviare dati a Pub/Sub
    send_alert()
    time.sleep(60)

    # Esegui la funzione per gestire le notifiche
    excel_file_path = 'Farm_Weather_Data.xlsx'
    publish_excel_data(excel_file_path)

    # Esegui la funzione per gestire gli utenti e le soglie
    # Configura il client Firestore
    db = firestore.Client.from_service_account_json('credentials.json')
    setup_threshold_and_alert()


if __name__ == "__main__":
    main()
