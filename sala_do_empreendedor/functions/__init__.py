import unicodedata
import os
from django.utils.text import slugify
from datetime import datetime

def remove_accentuation(filename):
    # Remove acentuações da string
    normalized_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('utf-8')

    # Substitui espaços em branco por underscores
    normalized_filename = normalized_filename.replace(' ', '_')

    # Usa o Django's slugify para remover caracteres especiais e criar um nome de arquivo amigável
    return slugify(os.path.splitext(normalized_filename)[0]) + os.path.splitext(filename)[1]
