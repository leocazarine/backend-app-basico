from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# cors = CORS(app, resources={r"/compartilhar": {"origins": "*"}})
api = Api(app)

#######################################################################
# Front -> Back

@app.route("/consent", methods=['POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def criar_consentimento():
    print("-- RESQUEST JSON --")
    dicionario = request.form.to_dict()
    print(dicionario)
    print()

    response = jsonify({'resposta': request.form})
    return response, 200
    # return variavel, 200

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
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def postar_novo_consentimento():
    variaveis = request.form
    nome = variaveis.get("name")
    cpf = variaveis.get("dpf")
    return variaveis, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
