import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import ProductForm from './ProductForm'

function App() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({name: '', description:'', price: '', quantity: ''})

  function handleChange(e){
    const value = e.target.type === 'number' ? e.target.valueAsNumber : e.target.value
    setForm({...form, [e.target.name]: value})
  }

  function handleSubmit(e){
    e.preventDefault()
    fetch('http://localhost:8000/product', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(form)
    })
    .then(response => response.json())
    .then(newProduct=>{
      setProducts([...products, newProduct])
      setForm({name: '', description: '', price:'', quantity:''})
    })
  }

  useEffect(()=> {
    fetch('http://localhost:8000/products')
    .then(response => response.json())
    .then(data => setProducts(data))
  }, [])

  return (
    <>
    <ProductForm form={form} onChange={handleChange} onSubmit={handleSubmit}></ProductForm>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>Price</th>
          <th>Quantity</th>
        </tr>
      </thead>
      {products.map(product=>(
        <tr key={product.id}>
          <td>{product.id}</td>
          <td>{product.name}</td>
          <td>{product.description}</td>
          <td>{product.price}</td>
          <td>{product.quantity}</td>
        </tr>
      ))}
    </table>
  </>
  ) 
}

export default App
