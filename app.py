from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import ssl
import os

app = Flask(__name__)

# Récupération des variables d'environnement sur Render
BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT", 8883))
USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

@app.route("/niveau", methods=['POST', 'GET'])
def recevoir_niveau():
    # 1. Extraction des données (supporte JSON ou paramètre URL)
    if request.is_json:
        data = request.get_json()
        niveau = data.get("niveau")
        reservoir = data.get("id", "defaut")
    else:
        niveau = request.args.get("niveau")
        reservoir = request.args.get("id", "defaut")

    # Si aucune donnée n'est envoyée
    if niveau is None:
        return "Erreur : Paramètre 'niveau' manquant", 400

    print(f"Réservoir : {reservoir} | Niveau : {niveau}")

    try:
        # 2. Configuration du client MQTT
        client = mqtt.Client()
        client.username_pw_set(USER, PASSWORD)  # ✅ Correction : USER au lieu de USERNAME
        client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        
        # 3. Connexion et publication
        client.connect(BROKER, PORT)
        topic = f"reservoir/{reservoir}/niveau"
        client.publish(topic, str(niveau))
        client.disconnect()

        return f"Donnée transmise à HiveMQ sur {topic}", 200

    except Exception as e:
        print(f"Erreur MQTT : {e}")
        return f"Erreur lors de l'envoi : {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
