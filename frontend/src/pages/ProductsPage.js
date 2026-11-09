// Componentes de Chakra UI usados en la página:
// Box: contenedor, Heading: título, Table: tabla de datos, Text: párrafo de texto
import { Box, Heading, Table, Text } from "@chakra-ui/react";
// Hook propio que se encarga de pedir los productos a la API y guardarlos en un estado
import { useProducts } from "../hooks/useProducts";
// Formulario para crear productos
import ProductForm from "../components/ProductForm";

function ProductsPage() {
  // El hook devuelve la lista de productos, si se está cargando y el error (si lo hay)
  const { products, loading, error } = useProducts();

  return (
    // pt (padding-top) grande para que el header, que es fixed, no tape el contenido.
    // maxWidth y margin="0 auto" centran el contenido con un ancho máximo
    <Box pt={24} px={8} maxWidth="1280px" margin="0 auto">
      <Heading mb={6}>Products</Heading>

      {/* Renderizado condicional: según el estado de la petición se muestra una cosa u otra */}
      {loading && <Text>Cargando productos...</Text>}
      {error && <Text color="red.500">{error}</Text>}

      {/* Solo se pinta la tabla cuando ya terminó la carga y no hubo error */}
      {!loading && !error && (
        <Table.Root>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>Name</Table.ColumnHeader>
              <Table.ColumnHeader>Description</Table.ColumnHeader>
              <Table.ColumnHeader>Price</Table.ColumnHeader>
              <Table.ColumnHeader>Quantity</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {/* Una fila por producto. key permite a React identificar cada fila de la lista */}
            {products.map((product) => (
              <Table.Row key={product.id}>
                <Table.Cell>{product.name}</Table.Cell>
                <Table.Cell>{product.description}</Table.Cell>
                <Table.Cell>{product.price}</Table.Cell>
                <Table.Cell>{product.quantity}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      )}

      {/* El formulario de creación va debajo de la tabla */}
      <ProductForm />
    </Box>
  );
}

export default ProductsPage;
