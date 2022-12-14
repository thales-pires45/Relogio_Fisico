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
minutos = []
segundos = []

server = str(relogio_servidor)
horas.append(int(server.split(':')[0]))
minutos.append(int(server.split(':')[1]))
segundos.append(int(server.split(':')[2]))

relogio_clientes = [
    {
        'id': 0,
        'hora': str(relogio_servidor),
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
                rel = {
                    'id': hora.get('id'),
                    'hora': str(relogio_sicronizado[-1])
                }
                servidor(rel)
                return jsonify(rel)


@app.route('/relogio/', methods=['POST'])
def receber_hora():
    tempo = request.get_json()
    hora = str(tempo['hora'])
    horas.append(int(hora.split(':')[0]))
    minutos.append(int(hora.split(':')[1]))
    segundos.append(int(hora.split(':')[2]))
    relogio_clientes.append(tempo)
    return jsonify(relogio_clientes)


def calcular():
    print(f'{horas}:{minutos}:{segundos}')
    relogio = timedelta(
        hours=(np.average(horas)),
        minutes=(np.average(minutos)),
        seconds=(np.average(segundos)))

    relogio_sicronizado.append(relogio)
    print(relogio_sicronizado[-1])


def servidor(rel):
    for indice, relogio in enumerate(relogio_clientes):
        if relogio.get('id') == rel.get('id'):
            relogio_clientes[indice].update(rel)
        else:
            if relogio.get('id') == 0:
                relogio_clientes[0]['hora'] = rel.get('hora')


if __name__ == "__main__":
    print('Servidor executando...')
    app.run(debug=True)
