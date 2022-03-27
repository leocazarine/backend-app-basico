import re
from flask import Flask, request, redirect, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# cors = CORS(app, resources={r"/compartilhar": {"origins": "*"}})
cors = CORS(app)
api = Api(app)

#######################################################################
# Front -> Back


@app.route("/consent", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def criar_consentimento():
    print("-- criar_consentimento --")
    request_form = request.form

    print("####")
    print(request_form.to_dict())

    nome = request_form.get("nome")
    cpf = request_form.get("cpf")
    objetivoCompatilhamento = request_form.get("objetivoCompatilhamento")
    instituicao = request_form.get("instituicao")
    dadosObrigatorios = request_form.get("dadosObrigatorios")
    prazo = request_form.get("prazo")

    # TODO Call mock bank

    response = jsonify({'resposta': request.form})
    return response, 200


@app.route("/consents", methods=['GET'])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def lista_consentimentos():
    variavel = [1, 2, 3]
    return variavel, 200


@app.route("/consents/<consentID>", methods=['DELETE'])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def deletar_consentimento(consentID):
    consentID
    return consentID, 200

#######################################################################
# Back -> Back


@app.route("/get_conta", methods=['GET'])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_conta_indo():
    algo = request.form
    return algo, 200


@app.route("/post_new_consent", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def postar_novo_consentimento():
    form = request.form
    nome = form.get("name")
    cpf = form.get("cpf")

    print("####")
    print(nome)
    print(cpf)

    # response = request.post(url='http://localhost:3000/compartilhamento')

    # return form, 200

    return redirect('http://localhost:3000/compartilhamento')

    # print("####")

    # return form, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
