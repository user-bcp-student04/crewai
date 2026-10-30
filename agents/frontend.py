"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """
Implementa el backend de la feature a partir de user_story.md, que ya fue aprobado por una persona y está en el contexto anterior. Usa solo las secciones que afectan al backend: Diseño propuesto para Backend, Modelo de datos, Contrato de API, Mapeo CA-xx y Pruebas. Ignora lo exclusivo de frontend.

Antes de codificar:
- Antes de comenzar, valida que el proyecto está estable compilando en local y ejecutando todos los unit test.
- Lista los endpoints, operaciones, modelos, reglas de negocio y flujos que te pide el user_story.md.
- Confirma que cada endpoint tiene su contrato (entradas, respuestas y errores). Si falta algo o hay contradicciones, no inventes: decláralo en backend_spec.md como pregunta pendiente y aplica solo supuestos mínimos y visibles.
- No cambies rutas, métodos, parámetros, esquemas ni códigos de respuesta de los contratos existentes sin una decisión explícita.

Entregable 1: backend_spec.md, con estas secciones en orden:
1. Resumen de decisiones y supuestos
2. Trazabilidad: requisito → CA-xx → endpoint/flujo → clases
3. Endpoints: entradas, validaciones (campos obligatorios, formatos y límites) y ejemplos
4. Errores: códigos HTTP, estructura de respuesta y tratamiento de errores de dominio, validación y recursos inexistentes
5. Diseño por capas (hexagonal): recursos/controladores, casos de uso, puertos, adaptadores de persistencia y DTOs
6. Transacciones, consistencia y efectos sobre los datos
7. Casos de prueba: al menos un caso válido y uno de error, con entradas y respuestas esperadas
8. Supuestos, dependencias y discrepancias pendientes

Entregable 2: código Java con Quarkus 3.x y Maven, según el stack del README:
- Implementa los endpoints, casos de uso, puertos y adaptadores descritos en el entregable 1.
- Valida en los límites de entrada y en las reglas de negocio. No expongas excepciones internas ni datos sensibles.
- Ejecuta las escrituras relacionadas dentro de las transacciones definidas.
- Genera pruebas unitarias con JUnit 5 y Mockito con cobertura mínima del 90% a todo código nuevo.
- Utilizar Spotbugs para validaciones de seguridad, no deben haber observaciones críticas y altas.
- No dupliques lógica, contratos ni migraciones que pertenezcan a otros componentes o al equipo de Datos.
- Compila y ejecuta los unit testing y validaciones de spotbugs, si no pasa vuelve a iterar hasta solucionar las observaciones.
- Crea un repositorio por cada contrato implementado.

Formato del código (lo usa el extractor):
- Cada archivo va en un bloque markdown cuya primera línea es un comentario con el nombre del archivo, por ejemplo // NombreClase.java.
- El package sigue la estructura de paquetes definida por el arquitecto. Si no está definida, declara el package como supuesto.

Límites:
- No modifiques frontend, pruebas de otros componentes, ni los entregables de otros agentes.
- Si el user_story.md no tiene la información necesaria, detente en la pregunta pendiente en lugar de inventar la solución.

Gate: backend_spec.md y el código quedan pendientes de validación humana. No declares la implementación como completa sin evidencia de las pruebas.
"""

agent = Agent(role='Desarrollador frontend Angular',
              goal="Entregar frontend_spec.md y el código Angular del recorrido de usuario, trazables al user_story.md aprobado y listos para validación humana.",
              backstory="Eres un desarrollador frontend senior con experiencia en Angular 17, Node.js, pruebas unitarias y accesibilidad web. "
                        "Integras la interfaz con el contrato de API aprobado y no inventas endpoints ni campos.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea de cada bloque con // nombre.service.ts (o el archivo correspondiente).', agent=agent)
