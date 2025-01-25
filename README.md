# SAUCE Agua Eureka Service

Servidor de descubrimiento de servicios (Eureka Server) para la arquitectura de microservicios de SAUCE Agua.

## Documentación

La documentación completa del proyecto está disponible en: [SAUCE Agua Eureka Service Documentation](https://sauce-services.github.io/SAUCE.agua.eureka-service/)

## Estado del Proyecto

[![Deploy GitHub Pages](https://github.com/SAUCE-services/SAUCE.agua.eureka-service/actions/workflows/pages.yml/badge.svg)](https://github.com/SAUCE-services/SAUCE.agua.eureka-service/actions/workflows/pages.yml)

## Descripción

Este servicio actúa como servidor de registro y descubrimiento para los microservicios de SAUCE Agua, permitiendo:
- Registro automático de servicios
- Descubrimiento dinámico de endpoints
- Balanceo de carga
- Alta disponibilidad

## Tecnologías

- Spring Boot 3
- Spring Cloud Netflix Eureka Server
- Java 21

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
