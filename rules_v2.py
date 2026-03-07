from urllib.parse import urlparse


def infer_section_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        return "general"

    first = path.split("/")[0].lower()

    mapping = {
        "local": "general",
        "region": "general",
        "el-pais": "general",
        "mundo": "general",
        "motor": "general",
        "tecnologia": "general",
        "educacion": "general",
        "negocios": "general",
        "salud": "general",
        "deportes": "deportes",
        "policiales": "policiales",
        "espectaculos": "general_b",
    }

    return mapping.get(first, "general")


def choose_family(section: str, title: str, description: str) -> str:
    title = (title or "").strip()
    description = (description or "").strip().lower()

    if section == "deportes":
        return "deportes"

    if section == "policiales":
        return "policiales"

    if section == "general_b":
        return "general_b"

    # General B solo a cuentagotas, con reglas mecánicas.
    keywords = [
        "invitan",
        "charla",
        "curso",
        "capacitación",
        "capacitacion",
        "cortes",
        "cronograma",
        "inscripciones",
        "gratuita",
        "gratuito",
        "requisitos",
        "agenda",
    ]

    title_long = len(title) >= 95
    desc_present = len(description) >= 80
    has_keyword = any(k in description or k in title.lower() for k in keywords)

    if (title_long and has_keyword) or (has_keyword and desc_present):
        return "general_b"

    return "general_a"
