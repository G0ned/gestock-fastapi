import { request } from './client'

export function listProducts(){
    return request('/products')
}

export function createProduct(data){
    return request('/products', {method: 'POST', body: JSON.stringify(data)})
}

export function updateProduct(id, data) {
    return request(`/products/${id}`, {method: 'PUT', body: JSON.stringify(data)})
}

export function deleteProduct(id){
    return request(`/products/${id}`, {method: 'DELETE'})
}