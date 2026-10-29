"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa el backend de la feature usando como fuente los entregables aprobados del 
Arquitecto incluidos en el contexto anterior: user_story.md considerar solo información de relevante para 
la implementación del backend.

Antes de escribir código, identifica los endpoints, operaciones, modelos, reglas de negocio, 
dependencias y flujos. Mantén trazabilidad entre cada requisito, operación OpenAPI, diagrama y componente implementado. 
Respeta los nombres, rutas, métodos HTTP, parámetros, esquemas, códigos de respuesta y semántica del contrato.
 No inventes ni cambies el contrato para facilitar la implementación. Si hay contradicciones o faltan decisiones 
 necesarias, indícalas explícitamente en backend_spec.md y aplica solo supuestos mínimos, visibles y coherentes 
 con la arquitectura.

Entrega backend_spec.md con:
- Resumen de decisiones y trazabilidad requisito → endpoint/flujo → clases.
- Endpoints y validaciones de entrada, incluyendo campos obligatorios, formatos y límites relevantes.
- Errores coherentes con OpenAPI: códigos HTTP, estructura de respuesta y tratamiento de errores de dominio, 
validación y recursos inexistentes.
- Diseño de recursos/controladores, servicios, modelos/DTOs y repositorios/acceso a datos.
- Límites de transacción, consistencia y efectos sobre los datos.
- Al menos un caso válido y uno de error, con entradas y respuestas esperadas.
- Supuestos, dependencias y discrepancias pendientes, si las hubiera.

Implementa los endpoints y servicios en Java con el framework indicado por el arquitecto. Valida en los límites de 
entrada y en las reglas de negocio; no expongas excepciones internas ni datos sensibles. Mantén la persistencia detrás 
de la abstracción adecuada y ejecuta las escrituras relacionadas dentro de las transacciones definidas. No dupliques 
lógica, contratos ni migraciones que pertenezcan a otros componentes o al equipo de Datos. Crea los repositorios 
respectivos por cada contrato implementado.

Devuelve el contenido de backend_spec.md la ruta de los repositorios creados."""
agent = Agent(role='Desarrollador backend de microservicios', goal="Completar la tarea asignada.",
              backstory="Eres un integrante del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
