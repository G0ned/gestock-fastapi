import ProductForm from "./ProductForm";
import { VStack } from "@chakra-ui/react";

const FullSreenSection = ({children, isDarkBackground, ...boxProps}) => {
    return (
        <VStack backgroundColor={boxProps.backgroundColor} color={isDarkBackground ? "white" : "black"}>
            <VStack maxWidth="1280px" minHeight="100vh" {...boxProps}>
                {children}
            </VStack>
        </VStack>
    );
};

const ProductSection = () => 
(
    <FullSreenSection>
        <ProductForm/>
    </FullSreenSection>
)

export default ProductSection;