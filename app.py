from datetime import datetime, timedelta

from flask import Flask, request, redirect, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin

import json
import requests
import urllib
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)
cors = CORS(app, resources={r"/compartilhar": {"origins": "*"}})
# cors = CORS(app)
api = Api(app)

#######################################################################
# Front -> Back


@app.route("/consent", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def criar_consentimento():
    # Postman
    # request_form = request.form

    # Frontend
    request_form = request.get_json()

    nome = request_form["nome"]
    cpf = request_form["cpf"]
    print(nome)
    print(cpf)
    instituicao = request_form["instituicao"]
    print(instituicao)
    
    return jsonify({"redirect_url": "https://mango-mockbank.herokuapp.com/auth/auth/?response_type=token&only_one_client_in_database=True/"}), 200, {'ContentType':'application/json'}
    # TODO Call mock bank

    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'loggedUser': {
                'document': {
                    'identification': cpf,
                    'rel': 'CPF',
                },
            },
            'permissions': [
                'ACCOUNTS_READ',
                'ACCOUNTS_OVERDRAFT_LIMITS_READ',
                'RESOURCES_READ',
            ],
            'expirationDateTime': (datetime.now()+timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'only_one_client_in_database': 'True',
        },
    }

    response = requests.post('https://mango-mockbank.herokuapp.com/auth/consents/consents/', headers=headers, json=json_data)
    
    response = jsonify({
        'resposta1': request.form,
        'resposta2': response.json()
    })

    redirect("https://mango-mockbank.herokuapp.com/auth/auth/?response_type=token&only_one_client_in_database=True/")

    return response

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
    # Redirecionamento para o Front passando CPF e nome
    return "Front", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
