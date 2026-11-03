import { useState } from 'react'
const EMPTY = { name: '', description: '', price: '', quantity: ''}

export default function ProductForm ({onSubmit}){
    const [form, setForm] = useState(EMPTY)
    const [submitting, setSubmit] = useState(false)
    const [error, setError] = useState(null)


function handleChange(event){
    const {name, value} = event.target
    setForm((current) => ({...current, [name]: value}))
}

async function handleSubmit(event){
    event.preventDefault()
    setSubmit(true)
    setError(null)
    try{
        await onSubmit({
            name: form.name,
            description: form.description,
            price: Number(form.price),
            quantity: Number(form.quantity)
        })
        setForm(EMPTY)
    } catch (err) {
        setError(err.message)
    } finally  {
        setSubmit(false)
    }
}

return (
    <form onSubmit={handleSubmit} className="mb-6 flex flex-wrap gap-2">
        <input 
            name="name" value={form.name} onChange={handleChange}
            placeholder='Name' required
            className='rounded border px-2 py-1' />
        <input name="description" value={form.description} onChange={handleChange}
            placeholder='Description' required className="rounded border px-2 py-1"
        />
        <input name="price" value={form.price} onChange={handleChange} type="number"
            min="0" step="0.01" placeholder="Price" required className="w-24 rounded border px-2 py-1"
        />
        <input name="quantity" value={form.quantity} onChange={handleChange} type="number"
            min="0" placeholder="Quantity" required className="w-20 rounded border px-2 py-1" 
        />
        <button type="submit" disabled={submitting} className="rounded bg-black px-3 py-1 text-white disabled:opacity-50">
            {submitting ? 'Adding...' : 'Add'}
        </button>

        {error && <p className='w-full text-red-600'>{error}</p>}
    </form>
)
}