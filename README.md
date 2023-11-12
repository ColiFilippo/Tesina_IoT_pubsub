# Tesina_IoT_pubsub
Tesina Smart Agriculture

Il codice è composto da 3 funzioni principali:

1 - Un publisher prende i dati presenti in un file excel e li invia a cadenza regolare al cloud tramite protocollo pub/sub.
2 - Una funzione web in Flask che permette di inserire gli utenti e delle soglie superate le quali si vogliono ricevere aggiornamenti via mail
3 - Una funzione che riceve i dati dalla funzione 1 e invia le mail di alert utilizzando le soglie inserite al punto 2

Come lanciare l'applicazione online:
1 - Installare requirements
2 - Lanciare funzione 3
3 - Lanciare funzione 1
4 - Lanciare funzione 2
5 - Accedere al seguente link per accedere all'applicazione web: 34.154.96.24

Caricare file credentials.json e secret.py

sudo apt-get install python3-venv
sudo apt-get install python3-pip
sudo apt-get install git
python3 -m venv venv
source venv/bin/activate



git clone https://github.com/ColiFilippo/Tesina_IoT_pubsub.git

mv credentials.json Tesina_IoT_pubsub
mv secret.py Tesina_IoT_pubsub

sudo pip install -r requirements.txt

sudo python3 web_add_user_threshold.py
sudo python3 web_add_user_threshold.py & check_data_send_alert.py & pub_data_from_xlsx.py


