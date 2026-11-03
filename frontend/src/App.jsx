import { useProducts } from '../src/hooks/useProducts'
import ProductForm from '../src/components/ProductForm'

export default function App(){
  const {products, loading, error, addProduct} = useProducts()
  return(
    <div className='mx-auto max-w-3xl p-6'>
      <h1 className='mb-4 text-2xl font-bold'>
        gestock
      </h1>

      <ProductForm onSubmit={addProduct}/>

      {loading && <p>Loading…</p>}
      {error && <p className="text-red-600">Error: {error}</p>}
      
      {!loading && !error && (
        <table className="w-full border-collapse text-left">
          <thead>
            <tr className="border-b">
              <th className="py-2">ID</th>
              <th className="py-2">Name</th>
              <th className="py-2">Description</th>
              <th className="py-2">Price</th>
              <th className="py-2">Qty</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id} className="border-b">
                <td className="py-2">{product.id}</td>
                <td className="py-2">{product.name}</td>
                <td className="py-2">{product.description}</td>
                <td className="py-2">{product.price}</td>
                <td className="py-2">{product.quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}