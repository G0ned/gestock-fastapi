import {useState, useEffect} from 'react'
import {
    listProducts,
    createProduct,
    updateProduct,
    deleteProduct,
} from '../api/products'

export function useProducts(){
    const [products, setProducts] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)


useEffect(() => {
    listProducts()
        .then((data) => setProducts(data))
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false))
}, [])

async function addProduct(data){
    const created = await createProduct(data)
    setProducts((current) => [...current, created])
}

async function editProduct(id, data){
    const updated = await updateProduct(id, data)
    setProducts((current) =>
        current.map((p) => (p.id === id ? updated : p))
    )
}

async function removeProduct(id){
    await deleteProduct(id)
    setProducts((current) => current.filter((p) => p.id !== id))
}

return {products, loading, error, addProduct, editProduct, removeProduct}

}