from flask import Flask, request
import paho.mqtt.client as mqtt
import ssl
import os  # Permet d'interagir avec le système et l'environnement

app = Flask(__name__)

# Python va chercher la valeur de 'HIVEMQ_HOST' définie sur Render
BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT", 8883))
USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


@app.route("/niveau, methods=["POST"])
def recevoir_niveau():

    niveau = request.args.get("niveau")
    reservoir = request.args.get("id")

    print("Réservoir :", reservoir)
    print("Niveau :", niveau)

    client = mqtt.Client()

    client.username_pw_set(USERNAME, PASSWORD)

    client.tls_set(
        tls_version=ssl.PROTOCOL_TLS
    )

    client.connect(BROKER, PORT)

    topic = "reservoir/" + reservoir + "/niveau"

    client.publish(topic, niveau)

    client.disconnect()

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
