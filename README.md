# SAUCE Agua Eureka Service

Servidor de descubrimiento de servicios (Eureka Server) para la arquitectura de microservicios de SAUCE Agua.

## Documentación

- **Documentación Técnica**: [SAUCE Agua Eureka Service Documentation](https://sauce-services.github.io/SAUCE.agua.eureka-service/)
- **Wiki del Proyecto**: [SAUCE Agua Eureka Service Wiki](https://github.com/SAUCE-services/SAUCE.agua.eureka-service/wiki)

## Estado del Proyecto

[![Deploy GitHub Pages](https://github.com/SAUCE-services/SAUCE.agua.eureka-service/actions/workflows/pages.yml/badge.svg)](https://github.com/SAUCE-services/SAUCE.agua.eureka-service/actions/workflows/pages.yml)

## Descripción

Este servicio actúa como servidor de registro y descubrimiento para los microservicios de SAUCE Agua, permitiendo:
- Registro automático de servicios
- Descubrimiento dinámico de endpoints
- Balanceo de carga
- Alta disponibilidad

## Tecnologías

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?logo=springboot&logoColor=white)](https://spring.io/projects/spring-boot)
[![Spring Cloud](https://img.shields.io/badge/Spring%20Cloud-6DB33F?logo=spring&logoColor=white)](https://spring.io/projects/spring-cloud)
[![Java](https://img.shields.io/badge/Java-21-007396?logo=java&logoColor=white)](https://www.oracle.com/java/technologies/javase/)

## Estado de Integración Continua

[![SAUCE.agua.eureka-service CI](https://github.com/SAUCE-services/SAUCE.agua.eureka-service/actions/workflows/maven.yml/badge.svg)](https://github.com/SAUCE-services/SAUCE.agua.eureka-service/actions/workflows/maven.yml)

## Configuración

### Permisos Necesarios
Para que la generación automática de la wiki funcione, asegúrate de que:

1. El token tiene los siguientes permisos:
   - `repo` (acceso completo al repositorio)
   - `workflow` (para GitHub Actions)
   - `write:packages` (para operaciones de escritura)

2. La wiki está habilitada en la configuración del repositorio

3. El workflow tiene los permisos necesarios configurados
