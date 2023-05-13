from flask import Flask,jsonify,request
from V1.SolicitudesBPV1 import solicitudBP
from V2.SolicitudesBPV2 import solicitudBPV2

from V1.model import Opcion,db,Solicitud


app=Flask(__name__)
app.register_blueprint(solicitudBP)
app.register_blueprint(solicitudBPV2)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://titulatec_soa:Hola.123@localhost:3305/TitulaTEC_SOA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False



@app.route('/',methods=['GET'])
def init():
    return {"mensaje":"Escuchando el Servicio REST de Solicitudes"}

#Rutta para el listado general de solicitudes
@app.route('/Solicitudes/V1',methods=['GET'])
def listadoSolicitudes():
    solicitud=Solicitud()
    return solicitud.consultaGeneral()

#Ruta para el listado indvidual de solicitudes en base al id de la solicitud
@app.route('/Solicitudes/V1/<int:id>',methods=['GET'])
def listarSolicitud(id):
    solicitud=Solicitud()
    return solicitud.consultaIndividual(id)

#Ruta para agregar una solicitud
@app.route('/Solicitudes/V1',methods=['POST'])
def agregarSolicitud():
    solicitud = Solicitud()
    data=request.get_json()
    return solicitud.agregar(data)

#Ruta para editar los datos de una solicitud
@app.route('/Solicitudes/V1',methods=['PUT'])
def editarSolicitud():
    solicitud=Solicitud()
    data=request.get_json()
    return solicitud.editar(data)

#Ruta para eliminar una solicitud
@app.route('/Solicitudes/V1/<int:id>',methods=['DELETE'])
def eliminarSolicitud(id):
    solicitud=Solicitud()
    return solicitud.eliminar(id)

#Ruta para el listado de las opciones disponibles para titulación
@app.route('/opciones',methods=['GET'])
def consultaOpciones():
    try:
        opcion=Opcion()
        return jsonify(opcion.consultaGeneral())
    except:
        respuesta = {"estatus": "Error", "mensaje": "Recurso no disponible, contacta al administrador del servicio jiji"}
        return respuesta

#Manipulaciones de errores
@app.errorhandler(404)
def errorinterno(e):
    respuesta={"estatus":"Error","mensaje":"Recurso no disponible, contacta al administrador del servicio jiji"}
    return respuesta

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)

