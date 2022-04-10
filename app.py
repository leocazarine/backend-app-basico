from datetime import datetime, timedelta
from pickle import FALSE, TRUE

from flask import Flask, request, redirect, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin

import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/compartilhar": {"origins": "*"}})
# cors = CORS(app)
api = Api(app)

#######################################################################
# Front -> Back


# @app.route("/consent", methods=['POST'])
@app.route("/create_consent", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def criar_consentimento():
    # Postman
    # request_form = request.form

    # Frontend
    request_form = request.get_json()

    nome = request_form["nome"]
    cpf = request_form["cpf"]
    instituicao = request_form["instituicao"]
    print(nome)
    print(cpf)
    print(instituicao)

    headers = {
        # Already added when you pass json= but not when you pass data=
        'Content-Type': 'application/json'
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
        }
    }

    response = requests.post('https://mango-mockbank.herokuapp.com/auth/consents/consents/', headers=headers, json=json_data)
    

    return jsonify({"redirect_url": "https://mango-mockbank.herokuapp.com/auth/auth/?response_type=token&only_one_client_in_database=True/"}), 200, {'ContentType':'application/json'}
    

@app.route("/teste", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def teste():
    request_form = request.get_json()
    print(request_form)
    return "sucesso", 200


@app.route("/get_consent", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def lista_consentimentos():
    request_form = request.get_json()
    print(request_form)

    cpf = request_form["cpf"]

    # Mockbank
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'user_cpf': cpf,
            'only_one_client_in_database': 'True',
        },
    }

    response = requests.get('https://mango-mockbank.herokuapp.com/auth/consents/consents/', headers=headers, json=json_data)
    response_dict = response.json()
    print(response_dict)

    return response_dict, 200, {'ContentType':'application/json'}


@app.route("/delete_consent", methods=['POST']) # TODO verificar se o método seria um get
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def deletar_consentimento():
    request_form = request.get_json()
    print(request_form)

    cpf = request_form["cpf"] # 90841038074
    # token = request_form["token"] # JcGMN50CcdDmMxVoFUkFlhucGgdtJdBJkzb6ua2sum
    token = 'Bearer pVfjCd163h9xj3pYZ0Uj7v6LSbVOpXDke13RnPilDC'

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'user_cpf': cpf,
            'only_one_client_in_database': 'True',
        },
    }

    response = requests.delete('https://mango-mockbank.herokuapp.com/auth/consents/consents/', headers=headers, json=json_data)
    print("DELETADO")
    print(response)

    return "deletado", 200

#######################################################################
# Back -> Back


@app.route("/get_conta", methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_conta():
    # Postman
    request_form = request.form
    # Frontend
    # request_form = request.get_json()
    token = request_form["token"]

    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get('https://mango-mockbank.herokuapp.com/accounts/balances', headers=headers)

    return response.json(), 200


@app.route("/validate_consent", methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def validate_consent():
    # Postman
    request_form = request.form
    # Frontend
    # request_form = request.get_json()
    cpf = request_form["cpf"]

    # Mockbank
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'user_cpf': cpf,
            'only_one_client_in_database': 'True',
        },
    }

    response = requests.get('https://mango-mockbank.herokuapp.com/auth/consents/consents/', headers=headers, json=json_data)

    response_dict = response.json()
    status = response_dict['data']['status']
    expiration_date_time = datetime.strptime(response_dict['data']['expirationDateTime'], '%Y-%m-%dT%H:%M:%SZ')

    if status == "AUTHORISED" and expiration_date_time > datetime.now():
        return "True", 200
    else:
        return "False", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
