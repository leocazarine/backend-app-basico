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
    # token = request_form["token"] # 4bELgfHogA7TzfgS7c78jSYI9kxQx6F69IijXX8Vq9

    headers = {
        # 'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'user_cpf': str(cpf),
            'only_one_client_in_database': 'True',
        },
    }
    print(json_data)

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
    request_json = request.get_json()
    # Frontend
    # request_form = request.get_json()
    cpf = request_json["cpf"]
    print ("cpf: ", cpf)

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
    print ("validou token")
    print (response.json())
    response_dict = response.json()
    status = response_dict['data']['status']
    expiration_date_time = datetime.strptime(response_dict['data']['expirationDateTime'], '%Y-%m-%dT%H:%M:%SZ')

    if status == "AUTHORISED" and expiration_date_time > datetime.now():        
        token = request_json["token"]
        headers = {
            'Authorization': f'Bearer {token}',
        }
        print ("vai get conta")
        response = requests.get('https://mango-mockbank.herokuapp.com/accounts/balances', headers=headers)
        print('response getconta',response.json())

        return response.json(), 200
    else:
        return {"mensagem": "TOKEN_NOT_AUTHORIZED"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
