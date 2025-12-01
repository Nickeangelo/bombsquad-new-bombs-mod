import urllib.request
import _babase
import os

# LINK RAW do mod no GitHub
url = "URL_RAW_DO_ARQUIVO_AQUI"

# Diretório do BombSquad Pro
user_dir = _babase.env().get("python_directory")
mods_path = os.path.join(user_dir, "mods")
mod_file_path = os.path.join(mods_path, "new_bombs_plus.py")

# Criar pasta mods se não existir
if not os.path.isdir(mods_path):
    os.makedirs(mods_path)

# Baixar arquivo temporário
temp_file, _ = urllib.request.urlretrieve(url)

# Ler e copiar para o local final
with open(temp_file, "r", encoding="utf-8") as downloaded:
    code = downloaded.read()

with open(mod_file_path, "w", encoding="utf-8") as modfile:
    modfile.write(code)

print("SUCCESS — Mod instalado!")
