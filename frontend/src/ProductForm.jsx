
function ProductForm({form, onChange, onSubmit}){
    return(
        <form onSubmit={onSubmit}>
            <input type="text" name="name" value={form.name} onChange={onChange} placeholder="Name" required/>
            <input type="text" name="description" value={form.description} onChange={onChange} placeholder="Description" required/>
            <input type="number" name="price" value={form.price} onChange={onChange} placeholder="Price" required/>
            <input type="number" name="quantity" value={form.quantity} onChange={onChange} placeholder="Quantity" required/>
            <button type="submit">Add Product</button>
        </form>
    )
}

export default ProductForm