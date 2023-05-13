from pymongo import MongoClient
from datetime import date
from bson import ObjectId

class Conexion ():
    def __init__(self):
        self.cliente = MongoClient()
        self.bd = self.cliente.titulatec_soa
        self.col = self.db.solicitudes


    def insertar_solicitud(self, solicitud):
        resp = {"estatus": "", "mensaje": ""}
        alumno=self.bd.usuarios.find_one({"tipo": "E", "alumno.idAlumno": solicitud["idAlumno"], "alumno.estatus":"E", "estatus": "A"}, projection= {"alumno": True, "_id": False})
        if alumno:
            carrera=self.bd.carreras.find_one({":$and":[{"_id":alumno.get("alumno").get("carrera").get("idCarrera")},{"planesEstudio":{"$elemMatch":{"clave":alumno.get("alumno").get("carrera").get("plan"),"creditos":alumno.get("alumno").get("creditos")}}}]},
                                              projection={"jefePrograma":True, "_id":False})
            if carrera:
                count=self.coleccion.count_documents({"idAlumno":solicitud["idAlumno"],"estatus":{"$in":["Captura", "Revision", "Autorizada"]}})
                if count==0:
                    count=self.bd.opciones.count_documents({"_id":solicitud["idOpcion"], "estatus":True,
                                                            "carreras":{"$elemMatch":{"idCarrera":alumno.get("alumno").get("idCarrera"),"planes":{"$in":[alumno.get("alumno").get("carrera").get("plan")]}}}})
                    if count>0:
                        solicitud["fechaRegistro"] = str(date.today())
                        sumaF=date.today()+timedelta(days=5)
                        solicitud["fechaAtencion"]=str(sumaF)
                        solicitud["estatus"] = "Captura"
                        solicitud["idAdministrativo"] = carrera["jefePrograma"]
                        res=self.coleccion.insert_one(solicitud)
                        resp["estatus"] = "OK"
                        resp["mensaje"] = "Solicitud Agregada Con exito"+str(res.inserted_id)
                    else:
                        resp["estatus"] = "Error"
                        resp["mensaje"] = "La opcion no se encuentra vigente o no esta disponible para el alumno"
                else:
                    resp["estatus"]="Error"
                    resp["mensaje"] = "No se encontro "
            else:
                resp["estatus"] = "Error"
                resp["mensaje"] = "El Alummno no tiene los creditos sufivientes"
        else:
            resp["estatus"] = "Error"
            resp["mensaje"] = "No Existe el mono"


        resp["estatus"] = "ok"
        resp["mensaje"] = "Solicitud agregada en la BD"
        return resp


    def consultaGeneralSolicitudes(self):
        resp = {"estatus": "","mensaje":""}
        res = self.bd.vSolicitudes2.find_one({"id":ObjectId})
        if res:
            self.to_json_solicitud(res)
            resp["estatus"] = "ok"
            resp["mensaje"] = "listado de solicitudes"
            resp["solicitudes"] =res
        else:
            resp["estatus"] = "ok"
            resp["mensaje"] = "No hay solicitudes registradas con ese id"


    def to_json_solicitud(self,solicitud):
        solicitud["administrativo"]= {"id":solicitud.get("administrativo")[0].get("id"),
                                      "nombre":solicitud.get("administrativo")[0].get("nombre")[0]}
        solicitud["alumno"] = {"id":solicitud.get("alumno")[0].get("id"),
                               "NC":solicitud.get("alumno")[0].get("NC")[0],
                               "nombre":solicitud.get("alumno")[0].get("nombre")[0]}
        solicitud["carrera"] = {"id":solicitud.get("carrera")[0].get("id")[0],
                                "nombre" : solicitud.get("carrera")[0].get("id")[0]}
        solicitud["opcion"] = {"id": solicitud.get("opcion")[0].get("id"),
                                "nombre": solicitud.get("opcion")[0].get("nombre")[0]}
        solicitud["id"] =str(solicitud["id"])


    def eliminarSolicitud(self,id):
        resp = {"estatus": "", "mensale":""}
        res= self.bd.solicitudes.delete_one({"_id": ObjectId(id), "estatus":{"$in":["Captura", "Rechazada"]}})
        if res.deleted_count>0:
            resp["estatus"]= "ok"
            resp["mensaje"] ="la solicitus se elimino con exito"
        else:
            resp["estatus"] = "Error"
            resp["mensaje"] = "La solicitud no existe o no se encuentra en Captura/Rechazada"
            return resp

    def consultarSolicitudesPorAlumno(self,idAlumno):
        resp={"estatus":"","mensaje":""}
        res=self.bd.vSolicitudes2.find({"alumno.id":idAlumno})
        lista=[]
        for s in res:
            self.to_json_solicitud(s)
            lista.append(s)
            if len (lista)>0:
                resp["estatus"] = "ok"
                resp["mensaje"] = "Listado de solicitudes del alumno"
                resp["solicitudes"] = lista
            else:
                resp["estatus"] = "OK"
                resp["mensaje"]= "Alumno sin solicitudes"
                return  resp

