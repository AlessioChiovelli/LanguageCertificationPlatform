from . import re

def parse_command(text: str) -> str | None:
    """
    Cerca un comando nel testo che inizi con '/' seguito da lettere, numeri o underscore/camelCase.
    Restituisce il nome del comando senza lo slash, oppure None se non trovato.
    """
    match = re.match(r"/([a-zA-Z_][a-zA-Z0-9_]*)", text.strip())
    if match:
        return match.group(1)
    return None