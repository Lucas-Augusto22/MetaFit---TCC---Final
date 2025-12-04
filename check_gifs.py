import os


def verificar_gifs():
    gifs_path = 'static/images/gifs'

    if not os.path.exists(gifs_path):
        print(f"❌ Pasta não existe: {gifs_path}")
        print("Crie a pasta e copie todos os GIFs para lá.")
        return

    gifs = os.listdir(gifs_path)
    print(f"✅ Pasta existe: {gifs_path}")
    print(f"📁 Total de GIFs encontrados: {len(gifs)}")

    if len(gifs) > 0:
        print("📋 Lista de GIFs:")
        for gif in gifs[:20]:  # Mostrar primeiros 20
            print(f"  - {gif}")

        if len(gifs) > 20:
            print(f"  ... e mais {len(gifs) - 20} arquivos")

    # Verificar GIFs importantes
    importantes = ['Agachamento_livre.gif', 'Flexão_tradicional.gif',
                   'Remada_curvada_com_barra.gif', 'default_exercise.gif']

    print("\n🔍 Verificando GIFs importantes:")
    for gif in importantes:
        path = os.path.join(gifs_path, gif)
        if os.path.exists(path):
            print(f"  ✅ {gif} - OK")
        else:
            print(f"  ❌ {gif} - FALTANDO")


if __name__ == "__main__":
    verificar_gifs()