from typing import Optional
from flask import Flask, jsonify, request
from flask_pydantic_spec import(FlaskPydanticSpec, Response, Request)
from pydantic import BaseModel
from tinydb import TinyDB, Query

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Cartas de MTG')
spec.register(app)
database = TinyDB('Cartas.json')

cartas = [
    {
        'id': 1,
        'nome': "Bênção da capelã",
        'tipo': "feitiço",
        'texto': "Você ganha 5 pontos de vida."
    },
    {
        'id': 2,
        'nome': "Skywhaler's Shot",
        'tipo': "Mágica Instantânea",
        'texto': "Destroy target creature with power 3 or greater. Scry 1."
    },
    {
        'id': 3,
        'nome': "Banimento a lâmina",
        'tipo': "Mágica Instantânea",
        'texto': "Exile a criatura alvo com poder igual ou superior a 4."
    }
]

#consultar
@app.route('/cartas',methods=['GET'])
def obterCartas():
    return jsonify(cartas)

@app.route('/cartas/<int:id>',methods=['GET'])
def obterPorId(id):
    for carta in cartas:
        if carta.get('id') == id:
            return jsonify(carta)

#editar
@app.route('/cartas/<int:id>',methods=['PUT'])
def editarPorId(id):
    cartaAlterada = request.get_json()
    for indice, carta in enumerate(cartas):
        if carta.get('id') == id:
            cartas[indice].update(cartaAlterada)
            return jsonify(cartas[indice])
#criar
@app.route('/cartas',methods=['POST'])
def incluirCarta():
    novaCarta = request.get_json()
    cartas.append(novaCarta)

    return jsonify(cartas)

#excluir
@app.route('/cartas/<int:id>',methods=['DELETE'])
def excluirCarta(id):
    for indice, carta in enumerate(cartas):
        if carta.get('id' == id):
            del cartas[indice]
            return jsonify(cartas)

app.run(port=5000,host='localhost',debug=True)