import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

from google.auth import jwt
from google.cloud import firestore, pubsub_v1

from secret import smtp_username, smtp_password, topic_name, project_id

'''IMPORTANTE: Questo programma è da lanciare prima di pub_data_from_xlxs'''


# Configura publisher e subscriber
service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = subscriber.topic_path(project_id, topic_name)
try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)

# Configura il client Firestore
db = firestore.Client.from_service_account_json('credentials.json')

# Configura le informazioni del server SMTP per inviare email
smtp_server = 'smtp.gmail.com'
#smtp_port = 465
smtp_port = 587

def send_email(subject, message, recipient):
    # Configura il messaggio email
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    # Inizializza il client SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    print("Connessione SMTP iniziata...")
    # Invia l'email
    server.sendmail(smtp_username, recipient, msg.as_string())
    print(f"Mail Inviata a {recipient}")
    # Chiudi la connessione SMTP
    server.quit()
    print("Connessione SMTP chiusa...")

def process_sensor_data(data):
    # Recupera tutti gli utenti dal database
    users = db.collection('users').stream()
    for user in users:
        user_data = user.to_dict()
        threshold_value = user_data['threshold_value']
        sensor_type = user_data['sensor_type']
        if data.get(sensor_type) is not None and data[sensor_type] > threshold_value:
            subject = f"Green Metrica - Soglia superata per {sensor_type}"
            message = f"Il valore di {sensor_type} ha superato la soglia di {threshold_value}."
            send_email(subject, message, user.id)

if __name__ == '__main__':

    # Configura il client Pub/Sub
    subscription_name = 'pubsub1'
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    print(subscription_path)
    # create subscription
    try:
        subscriber.create_subscription(name=subscription_path, topic=topic_path)
    except Exception as e:
        print(e)

    def callback(message):
        #Decodifica il messaggio
        data_json = message.data.decode('utf-8')
        data = json.loads(data_json)
        print("Dati ricevuti: "+data_json)
        process_sensor_data(data)
        message.ack()

    streaming_pull = subscriber.subscribe(subscription_path, callback=callback)
    streaming_pull.result()
    print('In attesa di dati dal sensore...')



