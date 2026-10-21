"""Normalização, validação de formato e leitura de URLs de um arquivo."""

# Só estes caracteres são aceitos (letras sem acento e números).
LETRAS_E_NUMEROS = "abcdefghijklmnopqrstuvwxyz0123456789"


def normalizar(url):
    """Tira espaços das pontas e deixa tudo em minúsculas.

    Toda url deve passar por aqui antes de ser comparada ou guardada.
    """
    return url.strip().lower()


def _so_tem_caracteres(texto, permitidos):
    """True se todos os caracteres de texto estão em permitidos."""
    for letra in texto:
        if letra not in permitidos:
            return False
    return True


def _rotulo_valido(rotulo):
    """Valida um pedaço do domínio (o que fica entre os pontos).

    Pode ter letras, números e hífen, mas não pode começar nem terminar com hífen.
    """
    if rotulo == "":
        return False
    if not _so_tem_caracteres(rotulo, LETRAS_E_NUMEROS + "-"):
        return False
    return rotulo[0] != "-" and rotulo[-1] != "-"


def _segmento_valido(segmento):
    """Valida um pedaço do caminho (o que fica entre as barras): letras, números, _ e -."""
    if segmento == "":
        return False
    return _so_tem_caracteres(segmento, LETRAS_E_NUMEROS + "_-")


def validar_formato(url):
    url = normalizar(url)

    if url.startswith("https://"):
        url = url[len("https://"):]
    elif url.startswith("http://"):
        url = url[len("http://"):]

    # "www.ifpb.edu.br/tsi/alunos" -> ["www.ifpb.edu.br", "tsi", "alunos"]
    partes = url.split("/")
    dominio = partes[0]
    segmentos = partes[1:]

    rotulos = dominio.split(".")
    if len(rotulos) < 2:      
        return False
    for rotulo in rotulos:
        if not _rotulo_valido(rotulo):
            return False

    for segmento in segmentos:
        if not _segmento_valido(segmento):
            return False

    return True


def carregar_urls(caminho):
    """Lê o arquivo de URLs (uma por linha) e devolve um set com as válidas.

    Linhas em branco são ignoradas. Linhas com formato inválido são
    ignoradas e um aviso é mostrado na tela.
    Levanta FileNotFoundError se o arquivo não existir.
    """
    urls = set()
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            texto = linha.strip()
            if texto == "":
                continue
            if validar_formato(texto):
                urls.add(normalizar(texto))
            else:
                print(f"Aviso: linha ignorada (formato inválido): {texto}")
    return urls