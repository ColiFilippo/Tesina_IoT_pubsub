# Tesina_IoT_pubsub
Tesina Smart Agriculture

Il codice è composto da 3 funzioni principali:

1 - Un publisher prende i dati presenti in un file excel e li invia a cadenza regolare al cloud tramite protocollo pub/sub.
2 - Una funzione web in Flask che permette di inserire gli utenti e delle soglie superate le quali si vogliono ricevere aggiornamenti via mail
3 - Una funzione che riceve i dati dalla funzione 1 e invia le mail di alert utilizzando le soglie inserite al punto 2

How to run on VM:
- Creare VM
- Caricare file credentials.json e secret.py
- sudo apt-get install python3-venv
- sudo apt-get install python3-pip
- sudo apt-get install git
- #opzionale :sudo apt-get install python3-venv / python3 -m venv venv / source venv/bin/activate {In realtà questo comando non permette di lanciare la web app, quindi è meglio non lanciarlo}
- git clone https://github.com/ColiFilippo/Tesina_IoT_pubsub.git
- mv credentials.json Tesina_IoT_pubsub
- mv secret.py Tesina_IoT_pubsub
- sudo pip install -r requirements.txt
- sudo nohup python3 web_app.py
- sudo nohup python3 alert.py & sudo nohup python3 publisher.py &
