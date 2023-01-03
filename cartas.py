from itertools import count
from typing import Optional
from flask import Flask, jsonify, request
from flask_pydantic_spec import(FlaskPydanticSpec, Response, Request)
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query


server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Cartas de MTG')
spec.register(server)
database = TinyDB('Cartas.json')
c = count()


class Carta(BaseModel):
    id: Optional[int] = Field(default_factory=lambda:next(c), autoincrement=True)
    qtd: int
    nome: str
    tipo: str
    texto: str

class Cartas(BaseModel):
    cartas: list[Carta]
    count: int


@server.get('/cartas')
@spec.validate(resp=Response(HTTP_200=Cartas))
def buscarCarta():
    """Retorna todas as Cartas na base de dados"""
    return jsonify(
        Cartas(
            cartas=database.all(),
            count=len(database.all())
        ).dict()
    )


@server.post('/cartas')
@spec.validate(
    body=Request(Carta), resp=Response(HTTP_200=Carta)
)
def inserirCarta():
    """Insere uma Carta na base de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body

@server.put('/cartas/<int:id>')
@spec.validate(
    body=Request(Carta), resp=Response(HTTP_200=Carta)
)
def alteraCarta(id):
    """Altera uma Carta na base de dados"""
    Carta = Query()
    body = request.context.body.dict()
    database.update(body, Carta.id == id)
    return jsonify(body)


@server.delete('/cartas/<int:id>')
@spec.validate(resp=Response('HTTP_204')
)
def deletaCarta(id):
    """Deleta uma Carta da base de dados"""
    Carta = Query()
    database.remove(Carta.id == id)
    return jsonify({})



server.run()