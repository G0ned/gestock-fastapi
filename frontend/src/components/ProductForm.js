// useState es un hook de React que permite guardar datos dentro del componente.
// Cuando esos datos cambian, React vuelve a dibujar el componente con los nuevos valores
import { useState, useEffect } from "react";
// Componentes de Chakra UI v3 que se utilizan en el formulario:
// VStack: apila a sus hijos en vertical, Box: contenedor genérico (como un div con estilos),
// Input: campo de texto, Button: botón, Field: agrupa etiqueta + campo + mensajes de ayuda/error,
// NativeSelect: desplegable basado en el <select> nativo del navegador
import { VStack, Box, Input, Button, Field, NativeSelect } from "@chakra-ui/react";

import { listManufacturers } from "../api/manufacturers";

// Valores iniciales del formulario. Se usan tanto al cargar el componente como para
// vaciar los campos después de enviar. Todo es string porque los inputs siempre devuelven texto
const INITIAL_VALUES = {
  name: "",
  description: "",
  price: "",
  quantity: "",
  manufacturer_id: "",
};

// Función de validación: recibe los valores del formulario y devuelve un objeto con un error
// por cada campo incorrecto. Si el objeto devuelto está vacío, el formulario es válido.
// Las reglas son las mismas que las de ProductCreate en app/schemas.py
function validate(values) {
  // Objeto donde se irán guardando los errores encontrados (clave: nombre del campo)
  const errors = {};

  // trim() elimina los espacios del principio y del final, así "   " cuenta como vacío
  if (!values.name.trim()) errors.name = "El nombre es obligatorio";
  // La descripción es opcional pero no puede pasar de 500 caracteres (max_length=500 en el backend)
  if (values.description.length > 500) {
    errors.description = "La descripción no puede superar los 500 caracteres";
  }
  // Number("") vale 0, por eso se comprueba aparte que el campo no esté vacío.
  // El precio debe ser mayor que 0 (gt=0 en el backend)
  if (values.price === "" || Number(values.price) <= 0) {
    errors.price = "El precio debe ser mayor que 0";
  }
  // La cantidad debe ser un número entero y mayor o igual que 0 (ge=0 en el backend)
  if (values.quantity === "" || !Number.isInteger(Number(values.quantity)) || Number(values.quantity) < 0) {
    errors.quantity = "La cantidad debe ser un entero igual o mayor que 0";
  }
  // Si el valor sigue siendo "" es que no se ha elegido ninguna opción del desplegable
  if (!values.manufacturer_id) errors.manufacturer_id = "Selecciona un fabricante";

  return errors;
}

function ProductForm() {
    const [manufacturers, setManufacturers ] = useState([]);

    useEffect(()=>{
        listManufacturers()
        .then((data) => setManufacturers(data))
        .catch((err) => console.error(err.message));
    }, [])

    const manufacturersOptions = manufacturers.map((m, index) => {
        return (
            <option key={m.id} value={m.id}>
                {m.name}
            </option>
        )
    })
  // Estado con los valores que el usuario va escribiendo.
  // inputs es el valor actual y setInputs la función para actualizarlo
  const [inputs, setInputs] = useState(INITIAL_VALUES);
  // Estado con los errores de validación que se muestran bajo cada campo
  const [errors, setErrors] = useState({});

  // Se ejecuta cada vez que el usuario escribe en un campo o cambia el desplegable.
  // "e" es el evento y e.target es el elemento que lo ha provocado
  function handleChange(e) {
    // Desestructuración: se sacan name y value del elemento.
    // name coincide con la clave del estado (name, price...) y value es lo escrito
    const { name, value } = e.target;
    // Se actualiza el estado copiando los valores anteriores (...values) y sustituyendo
    // solo el campo modificado. [name] usa el contenido de la variable como clave
    setInputs((values) => ({ ...values, [name]: value }));
  }

  // Se ejecuta al pulsar el botón de enviar
  function handleSubmit(e) {
    // Evita el comportamiento por defecto del formulario, que recargaría la página
    e.preventDefault();

    // Se validan los valores actuales y se guardan los errores para mostrarlos en pantalla
    const newErrors = validate(inputs);
    setErrors(newErrors);
    // Object.keys devuelve la lista de campos con error. Si hay alguno se corta aquí
    // con return y no se envía nada
    if (Object.keys(newErrors).length > 0) return;

    // De momento solo se muestra por consola lo que se enviaría a la API.
    // Los inputs devuelven texto, así que se pasan a número los campos que el backend espera numéricos
    console.log({
      ...inputs,
      price: Number(inputs.price),
      quantity: Number(inputs.quantity),
      manufacturer_id: Number(inputs.manufacturer_id),
    });
    // Se vacía el formulario volviendo a los valores iniciales
    setInputs(INITIAL_VALUES);
  }

  return (
    // Contenedor con padding (p), bordes redondeados (rounded) y todo el ancho disponible (w)
    <Box p={6} rounded="md" w="100%">
      {/* noValidate desactiva la validación del navegador para que se use solo la nuestra */}
      <form onSubmit={handleSubmit} noValidate>
        {/* gap: separación entre campos. align="stretch" hace que cada campo ocupe todo el ancho */}
        <VStack gap={4} align="stretch">
          {/* Field.Root agrupa todo lo de un campo. invalid activa el estilo de error
              (!! convierte el mensaje de error en true/false) y required marca el campo como obligatorio */}
          <Field.Root invalid={!!errors.name} required>
            {/* Field.Label es la etiqueta, y RequiredIndicator añade el asterisco de obligatorio */}
            <Field.Label>
              Name <Field.RequiredIndicator />
            </Field.Label>
            {/* Input controlado: su valor viene del estado y cada cambio llama a handleChange.
                El atributo name debe coincidir con la clave del estado */}
            <Input name="name" value={inputs.name} onChange={handleChange} placeholder="Name" />
            {/* ErrorText solo se ve cuando el Field.Root tiene invalid en true */}
            <Field.ErrorText>{errors.name}</Field.ErrorText>
          </Field.Root>

          {/* La descripción no es obligatoria, por eso no lleva required */}
          <Field.Root invalid={!!errors.description}>
            <Field.Label>Description</Field.Label>
            <Input
              name="description"
              value={inputs.description}
              onChange={handleChange}
              placeholder="Description"
            />
            {/* HelperText es un texto de ayuda que se muestra siempre bajo el campo */}
            <Field.HelperText>Máximo 500 caracteres</Field.HelperText>
            <Field.ErrorText>{errors.description}</Field.ErrorText>
          </Field.Root>

          <Field.Root invalid={!!errors.price} required>
            <Field.Label>
              Price <Field.RequiredIndicator />
            </Field.Label>
            {/* type="number" solo deja escribir números. step="0.01" permite dos decimales */}
            <Input
              type="number"
              step="0.01"
              name="price"
              value={inputs.price}
              onChange={handleChange}
              placeholder="99.99"
            />
            <Field.ErrorText>{errors.price}</Field.ErrorText>
          </Field.Root>

          <Field.Root invalid={!!errors.quantity} required>
            <Field.Label>
              Quantity <Field.RequiredIndicator />
            </Field.Label>
            {/* step="1" indica que la cantidad avanza de uno en uno (enteros) */}
            <Input
              type="number"
              step="1"
              name="quantity"
              value={inputs.quantity}
              onChange={handleChange}
              placeholder="Quantity"
            />
            <Field.ErrorText>{errors.quantity}</Field.ErrorText>
          </Field.Root>

          <Field.Root invalid={!!errors.manufacturer_id} required>
            <Field.Label>
              Manufacturer <Field.RequiredIndicator />
            </Field.Label>
            {/* NativeSelect se compone de Root (contenedor), Field (el select en sí)
                e Indicator (la flecha del desplegable) */}
            <NativeSelect.Root>
              <NativeSelect.Field
                name="manufacturer_id"
                value={inputs.manufacturer_id}
                onChange={handleChange}
              >
                {/* Opción vacía inicial: así el valor "" del estado coincide con una opción real
                    y el usuario tiene que elegir fabricante a propósito */}
                <option value="">Select manufacturer</option>
                {/* El value es el ID del fabricante, que es lo que espera el backend */}
                {manufacturersOptions}
              </NativeSelect.Field>
              <NativeSelect.Indicator />
            </NativeSelect.Root>
            <Field.ErrorText>{errors.manufacturer_id}</Field.ErrorText>
          </Field.Root>

          {/* type="submit" hace que al pulsarlo se dispare el onSubmit del formulario */}
          <Button type="submit">Send</Button>
        </VStack>
      </form>
    </Box>
  );
}

// Permite importar el componente desde otros archivos con: import ProductForm from "./ProductForm"
export default ProductForm;
