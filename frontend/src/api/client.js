//Creación de una constante que toma el valor de la variable de entorno REACT_APP_API_URL que es la URL de la API
const BASE_URL = process.env.REACT_APP_API_URL

//Creación de una función asíncrona llamada request que toma como parámetros el path y las opciones correspondientes
export async function request(path, options = {}) {
    const response = await fetch(`${BASE_URL}${path}`,{
        headers: {'Content-Type': 'application/json'},
        ...options
    })
    
    if(!response.ok){
        const body = await response.json().catch(() => ({}))
        throw new Error(body.detail || `Request failed (${response.status})`)
    }

     if (response.status === 204) return null
    return response.json()
}