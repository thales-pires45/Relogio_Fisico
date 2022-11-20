from flask import Flask
from flask import jsonify, request
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)

horarioAtual = datetime.now()
hora = horarioAtual.hour
minuto = horarioAtual.minute
segundo = horarioAtual.second

relogio_servidor = timedelta(hours=hora, minutes=minuto, seconds=segundo)

relogio_sicronizado = []

horas = []
minuto = []
segundo = []

s = relogio_servidor
server = str(s)
horas.append(int(server.split(':')[0]))
minuto.append(int(server.split(':')[1]))
segundo.append(int(server.split(':')[2]))

relogio_clientes = [
    {
        'id': 0,
        'hora': '',
    }
]


@app.route('/relogio', methods=['GET'])
def obter_relogio():
    return jsonify(relogio_clientes)


@app.route('/relogio/<int:id>', methods=['GET'])
def att_relogio(id):
    calcular()
    for hora in relogio_clientes:
        if hora.get('id') == int(id):
            time = hora.get('hora')
            if str(relogio_sicronizado[-1]) == str(time):
                return jsonify(hora)
            else:
                server = str(relogio_sicronizado[-1])
                relogio_atual = timedelta(hours=(int(server.split(':')[0])),
                                          minutes=(int(server.split(':')[1])),
                                          seconds=(int(server.split(':')[2])))
                rel = {
                    'id': hora.get('id'),
                    'hora': str(relogio_atual)
                }
                return jsonify(rel)


@app.route('/relogio/', methods=['POST'])
def receber_hora():
    tempo = request.get_json()
    hora = str(tempo['hora'])
    horas.append(int(hora.split(':')[0]))
    minuto.append(int(hora.split(':')[0]))
    segundo.append(int(hora.split(':')[0]))
    relogio_clientes.append(tempo)
    return jsonify(relogio_clientes)


@app.route('/relogio/<int:id>', methods=['PUT'])
def atualizar_hora(id):
    tempo = request.get_json()
    for indice, relogio in enumerate(relogio_clientes):
        if relogio.get('id') == id:
            hora = str(tempo['hora'])
            horas.append(int(hora.split(':')[0]))
            minuto.append(int(hora.split(':')[0]))
            segundo.append(int(hora.split(':')[0]))
            relogio_clientes[indice].update(tempo)
            return jsonify(relogio_clientes[indice])


def calcular():
    relogio = timedelta(
        hours=int(np.average(horas)),
        minutes=int(np.average(minuto)),
        seconds=int(np.average(segundo)))
    relogio_sicronizado.append(relogio)
    print(relogio_sicronizado[-1])

if __name__ == "__main__":
    print('Servidor executando...')
    app.run(debug=True)
