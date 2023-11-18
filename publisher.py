import time
import openpyxl
from google.cloud import pubsub_v1
from datetime import datetime
from secret import topic_name, project_id
from google.auth import jwt
import json

'''IMPORTANTE: Questo programma è da lanciare DOPO aver lanciato check_data_send_alert'''



# Funzione per leggere le righe da un file Excel e inviarle a Pub/Sub
def publish_excel_data(file_path):
    # Creare il publisher
    service_account_info = json.load(open("credentials.json"))
    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
    credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)
    publisher = pubsub_v1.PublisherClient(credentials=credentials)

    topic_path = publisher.topic_path(project_id, topic_name)
    print(topic_path)
    try:
        topic = publisher.create_topic(request={"name": topic_path})
        print(f"Created topic: {topic.name}")
    except Exception as e:
        print(e)
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(values_only=True):
        if len(row) == 6:  # Assicurati che ci siano 6 colonne nei dati
            # Converte la data nel formato "yyyy-mm-gg"
            date_str = str(row[0])
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            data_dict = {
                "Date": formatted_date,
                "Temperatura massima": float(row[1]),
                "Temperatura minima": float(row[2]),
                "Velocita del vento": float(row[3]),
                "Umidita": float(row[4]),
                "Precipitazioni": float(row[5])
            }
            #converti in json per risolvere problema dizionario non inviabile con pubsub
            data = json.dumps(data_dict)

        # Invia i dati al topic Pub/Sub
        publisher.publish(topic_path, data.encode('utf-8'))
        print(f'Dati inviati: {data}')

        # Intervalli di invio (ad esempio, 1 secondo)
        time.sleep(10)


if __name__ == '__main__':
    time.sleep(10)
    excel_file_path = 'Farm_Weather_Data.xlsx'
    publish_excel_data(excel_file_path)
