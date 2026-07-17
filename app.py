from flask import Flask, request
import paho.mqtt.client as mqtt
import ssl

app = Flask(__name__)

BROKER = "TON_CLUSTER.hivemq.cloud"
PORT = 8883
USERNAME = "TON_UTILISATEUR"
PASSWORD = "TON_MOT_DE_PASSE"


@app.route("/niveau")
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
