import {Heading, VStack, Tag, HStack} from "@chakra-ui/react";

const greeting = "Welcome to the gestock App HomePage!"

const FullSreenSection = ({children, isDarkBackground, ...boxProps}) => {
    return (
        <VStack backgroundColor={boxProps.backgroundColor} color={isDarkBackground ? "white" : "black"}>
            <VStack maxWidth="1280px" minHeight="100vh" {...boxProps}>
                {children}
            </VStack>
        </VStack>
    );
};

const LandingSection = () => (
    <FullSreenSection
        justifyContent="center"
        alignItems="center"
        isDarkBackground
        backgroundColor="#221e22"
    >
        <VStack>
            <Heading>{greeting}</Heading>
        </VStack>
    </FullSreenSection>
)

export default LandingSection;