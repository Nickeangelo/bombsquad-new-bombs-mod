import urllib.request
import _babase
import os

# LINK RAW DO MOD → substitua pelo link RAW do GitHub
url = "https://raw.githubusercontent.com/Nickeangelo/bombsquad-new-bombs-mod/main/new_bombs_plus.py"

# Diretório do BombSquad Pro
user_dir = _babase.env().get("python_directory_user")
mods_path = os.path.join(user_dir, "mods")
mod_file_path = os.path.join(mods_path, "new_bombs_plus.py")

# Criar pasta mods se não existir
if not os.path.isdir(mods_path):
    os.makedirs(mods_path)

# Baixar arquivo temporário
temp_file = urllib.request.urlretrieve(url)[0]

# Ler e gravar no destino
with open(temp_file, "r") as downloaded:
    code = downloaded.read()

with open(mod_file_path, "w+") as modfile:
    modfile.write(code)

print("SUCCESS — Mod instalado!")
