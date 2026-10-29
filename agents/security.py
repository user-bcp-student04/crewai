"""Agente de revisión de seguridad para los repositorios backend y frontend."""
from pathlib import Path

from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILES = ('backend.md', 'frontend.md')

INSTRUCTIONS = """Eres especialista en seguridad de la información bancaria. Revisa de
forma defensiva y sin modificar código los repositorios backend y frontend descritos en
backend.md y frontend.md. Usa las URL, criterios funcionales y pruebas recomendadas que
contengan. No te limites a resumir esas descripciones: inspecciona el código fuente y
los manifiestos/lockfiles de dependencias de ambos repositorios mediante GitHub MCP.

Realiza dos revisiones diferenciadas:
1. Dependencias: identifica librerías y versiones efectivamente utilizadas y contrástalas
   con registros CVE y NVD. Confirma que el rango de versiones afectadas aplica; no
   reportes una dependencia solo por tener una versión antigua.
2. Código: busca evidencia de vulnerabilidades conocidas de OWASP y CWE, incluyendo
   autorización por cuenta/objeto, autenticación y sesiones, flujos de transferencia,
   replay e idempotencia, validación de montos y límites, exposición de datos personales
   o financieros, secretos, criptografía, inyección, configuración y registros de
   auditoría. Prioriza el impacto en confidencialidad, integridad y disponibilidad de
   servicios financieros.

Usa OWASP y CWE para clasificar el tipo de debilidad y las entradas oficiales de NVD/CVE
para confirmar vulnerabilidades de dependencias. Incluye enlaces a las fuentes
autoritativas y evidencia localizable (repositorio, ruta y línea; paquete y versión,
cuando aplique). Revisa las pruebas recomendadas en backend.md y frontend.md y ejecútalas
si existe un runner seguro y autorizado; registra el comando y resultado. No ejecutes
código de explotación, no alteres datos ni modifiques código, dependencias o configuración.

No inventes hallazgos ni declares un repositorio libre de vulnerabilidades sin haber
inspeccionado su código y dependencias. Si falta un archivo de entrada, una URL, el
acceso a GitHub MCP, evidencia o capacidad para ejecutar una prueba recomendada, deja
constancia explícita de la limitación. No presentes una revisión incompleta como un
resultado sin vulnerabilidades.

Produce security_report.md en output/specs/ en español como tabla Markdown con estas cuatro columnas y
este orden exacto: hallazgo | criticidad | repositorio donde se halló la vulnerabilidad | fuente.
Usa criticidad Crítica, Alta, Media o Baja para vulnerabilidades confirmadas. Incluye
identificadores OWASP/CWE/CVE y evidencia en el hallazgo cuando corresponda. Si no se
identifican vulnerabilidades en una revisión completa, deja la tabla sin filas de
hallazgos y escribe CONFORME. Escribe NO CONFORME si se confirma al menos una
vulnerabilidad o si la revisión/pruebas quedan incompletas; agrega una razón breve.
"""
agent = Agent(role='Especialista en seguridad bancaria',
              goal="Detectar y documentar vulnerabilidades verificables en los repositorios bancarios backend y frontend.",
              backstory="Eres especialista en ciberseguridad de aplicaciones financieras. "
                        "Proteges la confidencialidad e integridad de los datos y las "
                        "transacciones, y basas cada conclusión en evidencia verificable.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    repository_context = []
    for filename in INPUT_FILES:
        path = ROOT / filename
        if path.is_file():
            contents = path.read_text(encoding='utf-8')
            repository_context.append(f"\n--- {filename} ---\n{contents}")
        else:
            repository_context.append(f"\n--- {filename} ---\n[No encontrado: {path}]")

    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", []))
                + "\n\nEntradas para identificar repositorios y pruebas:\n"
                + "".join(repository_context),
                expected_output='Informe output/specs/security_report.md en español con la tabla solicitada, '
                                'hallazgos basados en evidencia y limitaciones explícitas. '
                                'No modificar los repositorios revisados.',
                agent=agent)
