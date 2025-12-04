# Crie um arquivo check_images.py na raiz do projeto:
import os


def verificar_imagens():
    base_path = 'static/images'

    # Imagens de exercícios
    exercise_images = [
        'exercise_images/pushup_exercise.jpg',
        'exercise_images/squat_exercise.jpg',
        'exercise_images/pullup_exercise.jpg',
        'exercise_images/crunch_exercise.jpg',
        'exercise_images/plank_exercise.jpg',
        'exercise_images/running_exercise.jpg',
        'exercise_images/burpees_exercise.jpg',
        'exercise_images/rowing_exercise.jpg',
        'exercise_images/default_exercise.jpg'
    ]

    # Imagens de alimentos
    food_images = [
        'food_images/breakfast_eggs.jpg',
        'food_images/lunch_chicken.jpg',
        'food_images/dinner_fish.jpg',
        'food_images/snack_yogurt.jpg',
        'food_images/snack_sandwich.jpg',
        'food_images/supper_shake.jpg',
        'food_images/default_food.jpg'
    ]

    # GIFs
    gifs = [
        'pushup.gif',
        'squat.gif',
        'pullup.gif',
        'crunch.gif',
        'running.gif',
        'jumping_jacks.gif',
        'burpees.gif',
        'plank.gif',
        'rowing.gif',
        'curl.gif',
        'tricep.gif',
        'calf_raise.gif',
        'lunge.gif',
        'default_exercise.gif'
    ]

    print("=== VERIFICAÇÃO DE IMAGENS ===")

    print("\n1. Imagens de exercícios:")
    for img in exercise_images:
        path = os.path.join(base_path, img)
        if os.path.exists(path):
            print(f" {img}")
        else:
            print(f" {img} - FALTANDO!")

    print("\n2. Imagens de alimentos:")
    for img in food_images:
        path = os.path.join(base_path, img)
        if os.path.exists(path):
            print(f" {img}")
        else:
            print(f" {img} - FALTANDO!")

    print("\n3. GIFs:")
    for gif in gifs:
        path = os.path.join(base_path, gif)
        if os.path.exists(path):
            print(f" {gif}")
        else:
            print(f" {gif} - FALTANDO!")


if __name__ == "__main__":
    verificar_imagens()