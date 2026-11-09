import { useEffect, useRef } from "react";
import { Box, HStack, Link } from "@chakra-ui/react";
// Se renombra a RouterLink para no confundirlo con el Link de Chakra
import { Link as RouterLink } from "react-router-dom";

const Header = () => {
  const headerRef = useRef(null);
  useEffect(() => {
    let prevScrollPos = window.scrollY;
    const handleScroll = () => {
      const currentScrollPos = window.scrollY;
      const headerElement = headerRef.current;
      console.log("scroll", currentScrollPos, headerElement);
      if (!headerElement) return;

      if (prevScrollPos > currentScrollPos) {
        headerElement.style.transform = "translateY(0)";
      } else {
        headerElement.style.transform = "translateY(-200)";
      }
      prevScrollPos = currentScrollPos;
    };
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <Box
      position="fixed"
      top={0}
      left={0}
      right={0}
      translateY={0}
      transitionProperty="transform"
      transitionDuration=".2s"
      transitionTimingFunction="ease-in-out"
      backgroundColor="#F0EBD8"
      ref={headerRef}
    >
      <Box color="black" maxWidth="1280px" marin="0 auto">
        <HStack
          px={16}
          py={4}
          justifyContent="space-between"
          alignItems="center"
        >
          <nav>
            <HStack spacing={8}>
                {/* asChild hace que Chakra aplique sus estilos al hijo (RouterLink) en vez de crear un <a> propio.
                    RouterLink navega a /products sin recargar la página (a diferencia de href) */}
                <Link asChild borderRadius="md" border="2px solid" borderColor="transparent" _hover={{bg: "#1D2D44", color:"white", borderColor:"#1D2D44"}} px={3} py={1.5} transition="all 0.2s ease-in-out">
                  <RouterLink to="/products">Products</RouterLink>
                </Link>
                <Link href="" borderRadius="md" border="2px solid" borderColor="transparent" _hover={{bg: "#1D2D44", color:"white", borderColor:"#1D2D44"}} px={3} py={1.5} transition="all 0.2s ease-in-out">Manufacturers</Link>
            </HStack>
          </nav>
        </HStack>
      </Box>
    </Box>
  );
};

export default Header;
