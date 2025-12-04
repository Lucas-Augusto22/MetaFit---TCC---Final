# organize_gifs.py
import os
import shutil
from pathlib import Path


def organize_gifs(source_folder, target_folder):
    """Organiza GIFs na pasta correta"""
    os.makedirs(target_folder, exist_ok=True)

    # Lista de extensões de GIF
    gif_extensions = ['.gif', '.GIF']

    # Encontrar todos os GIFs
    gif_files = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if any(file.endswith(ext) for ext in gif_extensions):
                gif_files.append(os.path.join(root, file))

    # Copiar para a pasta de destino
    for gif_path in gif_files:
        gif_name = os.path.basename(gif_path)
        target_path = os.path.join(target_folder, gif_name)

        try:
            shutil.copy2(gif_path, target_path)
            print(f"✓ Copiado: {gif_name}")
        except Exception as e:
            print(f"✗ Erro ao copiar {gif_name}: {e}")

    print(f"\nTotal de GIFs organizados: {len(gif_files)}")


if __name__ == "__main__":
    # Ajuste os caminhos conforme sua estrutura
    organize_gifs('.', 'static/images/gifs')