//Importación del esqueleto de la petición guardado en el archivo client.js
import {request} from "./client"

// Función que hace la llamada al endpoint manufacturers (@app.get(/manufacturers))
export function listManufacturers(){
    return request("/manufacturers")
}

