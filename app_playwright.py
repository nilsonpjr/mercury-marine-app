from flask import Flask, render_template, request, jsonify
from funcoes_playwright import pesqpreco_playwright
from biblioteca_playwright import ConsultaGarantia_playwright
import asyncio

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pesquisar_preco", methods=["POST"])
async def pesquisar_preco():
    item = request.form["item"]
    resultados = await pesqpreco_playwright(item)
    return jsonify(resultados)

@app.route("/consultar_garantia", methods=["POST"])
async def consultar_garantia():
    nro_motor = request.form["nro_motor"]
    resultado = await ConsultaGarantia_playwright(nro_motor)
    return jsonify(resultado)

if __name__ == "__main__":
    # Para rodar o Flask com funções assíncronas, é necessário usar um loop de eventos
    # ou um servidor ASGI como o Gunicorn com worker gevent/eventlet.
    # Para simplificar o teste, vamos rodar com um loop de eventos aqui.
    # Em produção, você usaria um servidor ASGI.
    app.run(debug=True)

