const BASE_URL = import.meta.env.VITE_API_URL

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