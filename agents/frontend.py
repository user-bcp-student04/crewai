"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa el recorrido del usuario según el diseño de figma aprobado.
Realiza la integracion con el contrato de API aprobado por el backend.
Define campos, validaciones de estructura, acciones y mensajes.
Cubre estados de carga, vacío, éxito y error, y evita envíos duplicados.
Conserva etiquetas accesibles, navegación por teclado y foco visible.
Incluye cómo comprobar el recorrido mediante los test unitarios basandote en mantener una cobertura de 90%.
Entrega frontend_spec.md y código Angular con el formato de extracción que ya exige build_task."""
agent = Agent(role='Desarrollador frontend web', goal="Completar la tarea asignada.",
              backstory="Eres un integrante del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // nombre.service.ts.', agent=agent)
