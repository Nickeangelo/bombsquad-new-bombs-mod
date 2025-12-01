# Installer for New Bombs Plus mod

import os
import shutil
import _babase


def install():
    print("[New Bombs Plus] Instalando mod...")

    # Pasta destino onde o BombSquad guarda scripts do usuário
    user_path = _babase.env().get("python_directory_user")

    if not user_path:
        raise RuntimeError("Não foi possível localizar python_directory_user")

    # Caminho final do mod
    mod_dir = os.path.join(user_path, "new_bombs_plus")

    # Pasta onde o GitHub armazena os arquivos deste plugin
    src_dir = os.path.join(os.path.dirname(__file__), "new_bombs_plus")

    # Verifica se a pasta existe no plugin
    if not os.path.isdir(src_dir):
        raise RuntimeError("Pasta 'new_bombs_plus' não encontrada no plugin.")

    # Remove instalação anterior
    if os.path.exists(mod_dir):
        shutil.rmtree(mod_dir)

    # Copia nova versão
    shutil.copytree(src_dir, mod_dir)

    print("[New Bombs Plus] Mod instalado com sucesso!")


def on_app_launch():
    install()
