from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import requests
from database import get_db_connection, get_db_cursor
import json
from datetime import datetime
import random
import os
import re

bp = Blueprint('treino', __name__)

GENDER_API_URL = "https://api.genderize.io"
PEXELS_API_KEY = "xd2Cdf7h2R46Ye7yIJoDm5smxa4HNF0wcu4VaVeHRx3da0xbu5etPnK5"


# ========== FUNÇÃO PARA MAPEAR EXERCÍCIOS PARA GIFs ==========

# def get_exercise_gif_url(exercise_name):
#     """Retorna URL do GIF do exercício baseado no nome"""
#     try:
#         exercise_lower = exercise_name.lower().strip()
#
#         if exercise_lower.startswith('http'):
#             return exercise_lower
#
#         gif_mapping = {
#             # ... (mantenha o mapeamento existente completo)
#             'agachamento': 'Agachamento_livre.gif',
#             'squat': 'Agachamento_livre.gif',
#             'flexão': 'Flexão_tradicional.gif',
#             'push-up': 'Flexão_tradicional.gif',
#             # ... resto do mapeamento
#         }
#
#         for key, gif_filename in gif_mapping.items():
#             if key in exercise_lower:
#                 gif_path = os.path.join('static', 'images', 'gifs', gif_filename)
#                 if os.path.exists(gif_path):
#                     return f"images/gifs/{gif_filename}"
#                 else:
#                     print(f"GIF não encontrado: {gif_filename}")
#
#         # Fallback por grupos musculares
#         if any(word in exercise_lower for word in ['peito', 'chest', 'supino', 'flexão']):
#             return 'images/gifs/Flexão_tradicional.gif'
#         elif any(word in exercise_lower for word in ['costas', 'back', 'remada', 'puxada']):
#             return 'images/gifs/Remada_curvada_com_barra.gif'
#         # ... resto dos fallbacks
#
#         return 'images/gifs/default_exercise.gif'
#
#     except Exception as e:
#         print(f"Erro ao buscar GIF do exercício '{exercise_name}': {e}")
#         return 'images/gifs/default_exercise.gif'

def get_exercise_gif_url(exercise_name):
    """Retorna URL do GIF do exercício baseado no nome"""
    try:
        exercise_lower = exercise_name.lower().strip()

        # Primeiro, verificar se é uma URL completa
        if exercise_lower.startswith('http'):
            return exercise_lower

        # MAPEAMENTO COMPLETO DE EXERCÍCIOS PARA GIFs
        gif_mapping = {
            # Agachamentos
            'agachamento': 'Agachamento_livre.gif',
            'squat': 'Agachamento_livre.gif',
            'agachamento livre': 'Agachamento_livre.gif',
            'agachamento com mochila': 'Agachamento_livre.gif',
            'agachamento frontal': 'agachamento-frontal-com-barra.gif',
            'agachamento sumo': 'agachamento-sumo-sem-halter.gif',
            'agachamento búlgaro': 'agachamento-bulgaro.gif',
            'agachamento smith': 'Agachamento_no_smith.gif',
            'agachamento pistol': 'Agachamento_pistol_assistido.gif',
            'agachamento profundo': 'Agachamento_livre.gif',
            'agachamento hack': 'Agachamento_no_smith.gif',

            # Flexões
            'flexão': 'Flexão_tradicional.gif',
            'flexões': 'Flexão_tradicional.gif',
            'push-up': 'Flexão_tradicional.gif',
            'push up': 'Flexão_tradicional.gif',
            'flexão tradicional': 'Flexão_tradicional.gif',
            'flexão com pés elevados': 'Flexão_tradicional.gif',
            'flexão diamante': 'flexao-de-bracos-diamante.gif',
            'flexão inclinada': 'flexao-de-bracos-inclinada.gif',
            'flexão aberta': 'Flexão_aberta.gif',
            'pike push-up': 'Pike-Push-up.gif',
            'shoulder tap': 'Shoulder-Tap-Push-up.gif',
            'flexão hindu': 'Flexão_tradicional.gif',

            # Remadas
            'remada': 'Remada_curvada_com_barra.gif',
            'remada curvada': 'Remada_curvada_com_barra.gif',
            'remada alta': 'Remada_alta.gif',
            'remada baixa': 'Remada_baixa.gif',
            'remada unilateral': 'Remada_unilateral_com_halter.gif',
            'remada cavalinho': 'Remada_cavalinho.gif',
            'puxada': 'Puxada_na_frente_pulldown.gif',
            'puxada frente': 'Puxada_na_frente_pulldown.gif',
            'puxada atrás': 'Puxada_atras.gif',
            'remada com elástico': 'remada-de-costas-com-elastico-em-pe.gif',
            'remada invertida': 'remada-invertida-na-mesa.gif',
            'face pulls': 'Remada_alta.gif',

            # Supinos
            'supino': 'Supino_reto_com_barra.gif',
            'supino reto': 'Supino_reto_com_barra.gif',
            'supino inclinado': 'supino-inclinado-com-barra.gif',
            'supino declínio': 'Supino_decimalo.gif',
            'supino fechado': 'Supino_fechado.gif',
            'chest press': 'Chest_press_na_máquina.gif',
            'supino halteres': 'Supino_reto_com_barra.gif',

            # Desenvolvimento
            'desenvolvimento': 'Desenvolvimento_com_barra.gif',
            'shoulder press': 'Desenvolvimento_com_barra.gif',
            'arnold press': 'Arnold-Press.gif',
            'elevação lateral': 'Elevacao_lateral.gif',
            'elevação frontal': 'Elevacao_frontal.gif',
            'elevação lateral inclinada': 'Elevacao_lateral_inclinada.gif',
            'desenvolvimento militar': 'Desenvolvimento_com_barra.gif',

            # Rosca
            'rosca': 'Rosca_direta_barra.gif',
            'rosca direta': 'Rosca_direta_barra.gif',
            'rosca alternada': 'Rosca-Alternada-com-Halteres.gif',
            'rosca scott': 'Rosca_Scott_barra.gif',
            'rosca martelo': 'Rosca_martelo.gif',
            'rosca concentrada': 'Rosca_concentrada.gif',
            'rosca inversa': 'Rosca_inversa.gif',
            'bíceps': 'Rosca_direta_barra.gif',
            'rosca bíceps': 'Rosca_direta_barra.gif',
            'rosca spider': 'Rosca_concentrada.gif',

            # Tríceps
            'tríceps': 'Triceps_testa.gif',
            'tríceps testa': 'Triceps_testa.gif',
            'tríceps corda': 'Triceps_corda.gif',
            'tríceps pulley': 'Triceps_pulley.gif',
            'tríceps no banco': 'triceps-no-banco.gif',
            'tríceps kickback': 'Triceps_kickback.gif',
            'tríceps francês': 'Triceps_testa.gif',

            # Abdominais
            'abdominal': 'Abdominal_tradicional.gif',
            'abdominais': 'Abdominal_tradicional.gif',
            'crunch': 'Crunch_no_cabo.gif',
            'abdominal bicicleta': 'abdominal-bicicleta.gif',
            'abdominal infra': 'abdominal-infra-inferior.gif',
            'abdominal suspenso': 'Abdominal-infra-suspenso-na-barra.gif',
            'abdominal oblíquo': 'Abdominal_oblíquo_na_polia.gif',
            'hollow body': 'Hollow_body_hold.gif',
            'russian twist': 'Abdominal_oblíquo_na_polia.gif',
            'leg raises': 'abdominal-infra-inferior.gif',

            # Pranchas
            'prancha': 'prancha-frontal-tradicional-com-bracos-esticados.gif',
            'prancha frontal': 'prancha-frontal-tradicional-com-bracos-esticados.gif',
            'prancha lateral': 'prancha-lateral.gif',
            'prancha abdominal': 'Prancha-abdominal-Ponte-ventral.gif',
            'plank': 'prancha-frontal-tradicional-com-bracos-esticados.gif',

            # Pernas
            'leg press': 'Leg_press.gif',
            'cadeira extensora': 'cadeira-extensora.gif',
            'cadeira flexora': 'cadeira-flexora.gif',
            'mesa flexora': 'Mesa_flexora.gif',
            'stiff': 'Stiff_com_barra.gif',
            'levantamento terra': 'Levantamento_terra.gif',
            'levantamento terra romeno': 'Levantamento_terra_romeno.gif',
            'afundo': 'afundo-exercicio.gif',
            'avanço': 'Passada.gif',
            'passada': 'Passada.gif',
            'panturrilha': 'Elevacao_de_panturilha_em_pe.gif',
            'panturrilha sentado': 'Elevacao_de_panturilha_sentado.gif',
            'lunge': 'Passada.gif',
            'deadlift': 'Levantamento_terra.gif',

            # Glúteos
            'glúteo': 'ponte-para-gluteos.gif',
            'ponte glúteo': 'ponte-para-gluteos.gif',
            'ponte unilateral': 'Ponte_unilateral.gif',
            'coice': 'coice-no-cabo.gif',
            'glúteo no cabo': 'Glúteo_no_cabo.gif',
            'donkey kicks': 'Donkey-Kicks.gif',
            'fire hydrants': 'Fire_hydrants.gif',
            'glute bridge': 'ponte-para-gluteos.gif',

            # Costas
            'barra fixa': 'Barra_fixa_fechada.gif',
            'pull-up': 'barra_fixa_pegada_aberta.gif',
            'chin-up': 'Barra_fixa_fechada.gif',
            'pull over': 'Pull-over_na_maquina.gif',
            'crucifixo': 'Crucifixo_com_halteres_reto.gif',
            'crucifixo invertido': 'Crucifixo_invertido.gif',
            'lat pulldown': 'Puxada_na_frente_pulldown.gif',

            # Cardio
            'burpee': 'Burpees.gif',
            'burpees': 'Burpees.gif',
            'mountain climbers': 'Mountain_climbers.gif',
            'salto': 'Salto_vertical.gif',
            'corrida': 'corrida.gif',
            'polichinelo': 'Jumping-Jacks.gif',
            'jumping jacks': 'Jumping-Jacks.gif',
            'skipping': 'corrida.gif',
            'jump rope': 'corrida.gif',

            # Máquinas
            'peck deck': 'Peck_deck.gif',
            'kickback máquina': 'Kickback_na_máquina.gif',
            'cadeira adutora': 'Cadeira_adutora.gif',
            'abdução': 'abducao-de-pernas-na-maquina-com-cabos.gif',
            'mergulho': 'Mergulho_nas_paralelas.gif',
            'hip thrust': 'ponte-para-gluteos.gif',

            # Outros
            'superman': 'Superman-exercise.gif',
            'elevação de pernas': 'Elevacao_de_pernas.gif',
            'bird dog': 'Superman-exercise.gif',
            'good morning': 'Stiff_com_barra.gif',
            'calf raise': 'Elevacao_de_panturilha_em_pe.gif',
            'hip abduction': 'abducao-de-pernas-na-maquina-com-cabos.gif',
            'hip adduction': 'Cadeira_adutora.gif',
            'leg curl': 'cadeira-flexora.gif',
            'leg extension': 'cadeira-extensora.gif',
            'shrugs': 'Remada_alta.gif',
            'upright row': 'Remada_alta.gif',
            'clean and press': 'Desenvolvimento_com_barra.gif',
            'kettlebell swing': 'Levantamento_terra.gif',
            'battle ropes': 'corrida.gif',
            'box jump': 'Salto_vertical.gif',
        }

        # Procurar por correspondências exatas primeiro
        for key, gif_filename in gif_mapping.items():
            if key in exercise_lower:
                # Verificar se o GIF existe
                gif_path = os.path.join('static', 'images', 'gifs', gif_filename)
                if os.path.exists(gif_path):
                    return f"images/gifs/{gif_filename}"
                else:
                    print(f"GIF não encontrado: {gif_filename} em {gif_path}")
                    # Tentar fallback
                    break

        # Se não encontrar correspondência exata, buscar por grupos musculares
        if any(word in exercise_lower for word in ['peito', 'chest', 'supino', 'flexão', 'push', 'press']):
            return 'images/gifs/Flexão_tradicional.gif'
        elif any(word in exercise_lower for word in ['costas', 'back', 'remada', 'puxada', 'pull', 'row']):
            return 'images/gifs/Remada_curvada_com_barra.gif'
        elif any(word in exercise_lower for word in ['ombro', 'shoulder', 'desenvolvimento', 'press']):
            return 'images/gifs/Desenvolvimento_com_barra.gif'
        elif any(word in exercise_lower for word in ['braço', 'arm', 'rosca', 'bíceps', 'bicep', 'curl']):
            return 'images/gifs/Rosca_direta_barra.gif'
        elif any(word in exercise_lower for word in ['tríceps', 'tricep', 'extension']):
            return 'images/gifs/Triceps_testa.gif'
        elif any(word in exercise_lower for word in ['perna', 'leg', 'agachamento', 'squat', 'press', 'extension', 'curl']):
            return 'images/gifs/Agachamento_livre.gif'
        elif any(word in exercise_lower for word in ['glúteo', 'glute', 'quadril', 'hip', 'bridge']):
            return 'images/gifs/ponte-para-gluteos.gif'
        elif any(word in exercise_lower for word in ['abdomen', 'core', 'abdominal', 'crunch', 'prancha', 'plank']):
            return 'images/gifs/Abdominal_tradicional.gif'
        elif any(word in exercise_lower for word in ['cardio', 'aeróbico', 'corrida', 'run', 'jump', 'burpee']):
            return 'images/gifs/Burpees.gif'
        elif any(word in exercise_lower for word in ['terra', 'deadlift', 'stiff', 'levantamento']):
            return 'images/gifs/Levantamento_terra.gif'
        elif any(word in exercise_lower for word in ['barra', 'fixa', 'pull-up', 'chin-up']):
            return 'images/gifs/Barra_fixa_fechada.gif'

        # Fallback final
        return 'images/gifs/default_exercise.gif'

    except Exception as e:
        print(f"Erro ao buscar GIF do exercício '{exercise_name}': {e}")
        return 'images/gifs/default_exercise.gif'


# ========== FUNÇÕES AUXILIARES ATUALIZADAS ==========

def processar_resultado(resultado):
    """Processa resultado do banco, retornando dicionário"""
    if resultado is None:
        return None

    if isinstance(resultado, dict):
        return resultado
    elif isinstance(resultado, tuple):
        if len(resultado) >= 2:
            return {
                'data_nascimento': resultado[0],
                'nome_usuario': resultado[1]
            }
        else:
            return {f'coluna_{i}': valor for i, valor in enumerate(resultado)}
    else:
        return resultado


def get_gender_by_name(nome):
    try:
        if not isinstance(nome, str):
            return 'male'
        primeiro_nome = nome.split()[0].lower()
        response = requests.get(f"{GENDER_API_URL}?name={primeiro_nome}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('probability', 0) > 0.6:
                return data.get('gender', 'male')
        return 'male'
    except:
        return 'male'


def generate_food_images(dieta):
    """Gera URLs de imagens para todas as refeições da dieta"""
    food_images = {}

    if isinstance(dieta, dict):
        meal_order = ['cafe_manha', 'lanche_manha', 'almoco', 'lanche_tarde', 'jantar', 'ceia']

        for meal_type in meal_order:
            if meal_type in dieta and isinstance(dieta[meal_type], str):
                food_images[meal_type] = get_food_image_url(dieta[meal_type])

    return food_images


# def get_food_image_url(meal_description):
#     """Busca imagem de comida na API do Pexels"""
#     try:
#         if not isinstance(meal_description, str):
#             return 'images/food_images/default_food.jpg'
#
#         meal_lower = meal_description.lower()
#         search_mapping = {
#             'ovo': 'egg breakfast healthy',
#             'pão': 'whole wheat bread breakfast',
#             # ... resto do mapeamento
#         }
#
#         search_term = 'healthy food nutrition'
#         for key, term in search_mapping.items():
#             if key in meal_lower:
#                 search_term = term
#                 break
#
#         headers = {'Authorization': PEXELS_API_KEY}
#         params = {
#             'query': search_term,
#             'per_page': 1,
#             'orientation': 'square'
#         }
#
#         response = requests.get(
#             'https://api.pexels.com/v1/search',
#             headers=headers,
#             params=params,
#             timeout=5
#         )
#
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('photos') and len(data['photos']) > 0:
#                 return data['photos'][0]['src']['medium']
#
#         return 'images/food_images/default_food.jpg'
#
#     except Exception as e:
#         print(f"Erro ao buscar imagem de comida: {e}")
#         return 'images/food_images/default_food.jpg'

def get_food_image_url(meal_description):
    """Busca imagem de comida na API do Pexels"""
    try:
        if not isinstance(meal_description, str):
            return 'images/food_images/default_food.jpg'

        meal_lower = meal_description.lower()

        # MAPEAMENTO COMPLETO PARA TERMOS DE BUSCA
        search_mapping = {
            # Café da manhã
            'ovo': 'egg breakfast healthy food',
            'ovos': 'egg breakfast healthy food',
            'omelete': 'omelette breakfast eggs',
            'pão': 'whole wheat bread breakfast healthy',
            'pão integral': 'whole wheat bread breakfast',
            'torrada': 'toast breakfast healthy',
            'aveia': 'oatmeal breakfast healthy',
            'granola': 'granola breakfast healthy',
            'iogurte': 'yogurt breakfast healthy',
            'iogurte grego': 'greek yogurt breakfast',
            'fruta': 'fresh fruits breakfast healthy',
            'banana': 'banana fruit healthy',
            'maçã': 'apple fruit healthy',
            'morangos': 'strawberries fruit healthy',
            'suco': 'fresh juice healthy',
            'vitamina': 'smoothie breakfast healthy',
            'smoothie': 'smoothie breakfast healthy',
            'whey': 'protein shake fitness',
            'proteína': 'protein food healthy',

            # Lanches
            'castanha': 'nuts healthy snack',
            'amêndoa': 'almonds healthy snack',
            'nozes': 'walnuts healthy snack',
            'fruta seca': 'dried fruits healthy snack',
            'barrinha': 'protein bar healthy snack',
            'cookies integral': 'healthy cookies snack',
            'bolo': 'healthy cake snack',

            # Almoço/Jantar
            'frango': 'grilled chicken healthy meal',
            'peito de frango': 'chicken breast healthy',
            'carne': 'lean meat healthy food',
            'bife': 'steak meat healthy',
            'peixe': 'grilled fish healthy meal',
            'salmão': 'salmon fish healthy',
            'tilápia': 'tilapia fish healthy',
            'atum': 'tuna fish healthy',
            'ovo cozido': 'boiled eggs healthy',

            # Carboidratos
            'arroz': 'rice healthy food',
            'arroz integral': 'brown rice healthy',
            'batata doce': 'sweet potato healthy food',
            'batata': 'potato healthy food',
            'batata inglesa': 'potato healthy',
            'macarrão': 'pasta healthy meal',
            'macarrão integral': 'whole wheat pasta healthy',
            'quinoa': 'quinoa healthy grain',
            'aveia': 'oats healthy grain',

            # Legumes/Verduras
            'feijão': 'beans healthy food',
            'lentilha': 'lentils healthy food',
            'grão de bico': 'chickpeas healthy food',
            'salada': 'fresh salad vegetables healthy',
            'alface': 'lettuce salad healthy',
            'tomate': 'tomato vegetable healthy',
            'cenoura': 'carrot vegetable healthy',
            'brócolis': 'broccoli vegetable healthy',
            'espinafre': 'spinach vegetable healthy',
            'couve': 'kale vegetable healthy',
            'abóbora': 'pumpkin vegetable healthy',
            'aspargos': 'asparagus vegetable healthy',

            # Gorduras saudáveis
            'abacate': 'avocado healthy fat',
            'azeite': 'olive oil healthy',
            'azeitona': 'olives healthy',
            'óleo de coco': 'coconut oil healthy',

            # Jantar/Ceia
            'sopa': 'soup healthy dinner',
            'creme': 'cream soup healthy',
            'shake': 'protein shake fitness',
            'proteico': 'protein food healthy',
            'caseína': 'protein powder fitness',
            'chá': 'tea healthy drink',
            'chá verde': 'green tea healthy',

            # Suplementos
            'whey protein': 'protein powder fitness',
            'creatina': 'fitness supplement',
            'bcaa': 'amino acids fitness',
            'multivitamínico': 'vitamins healthy',
            'omega': 'fish oil healthy',

            # Bebidas
            'água': 'water hydration healthy',
            'água de coco': 'coconut water healthy',
            'suco natural': 'fresh juice healthy',
            'suco verde': 'green juice healthy',
        }

        search_term = 'healthy food nutrition'
        for key, term in search_mapping.items():
            if key in meal_lower:
                search_term = term
                break

        headers = {'Authorization': PEXELS_API_KEY}
        params = {
            'query': search_term,
            'per_page': 1,
            'orientation': 'square',
            'size': 'medium'
        }

        response = requests.get(
            'https://api.pexels.com/v1/search',
            headers=headers,
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('photos') and len(data['photos']) > 0:
                return data['photos'][0]['src']['medium']

        # Fallback para imagem local
        return get_local_food_image(meal_description)

    except Exception as e:
        print(f"Erro ao buscar imagem de comida: {e}")
        return get_local_food_image(meal_description)


def get_local_food_image(meal_description):
    """Retorna imagem local como fallback"""
    try:
        if not isinstance(meal_description, str):
            return 'images/food_images/default_food.jpg'

        meal_lower = meal_description.lower()

        # Verificar se arquivos locais existem
        if any(word in meal_lower for word in ['ovo', 'pão', 'torrada', 'aveia', 'café']):
            return 'images/food_images/breakfast_eggs.jpg'
        elif any(word in meal_lower for word in ['iogurte', 'fruta', 'vitamina', 'smoothie']):
            return 'images/food_images/snack_yogurt.jpg'
        elif any(word in meal_lower for word in ['frango', 'carne', 'peixe', 'bife']):
            return 'images/food_images/lunch_chicken.jpg'
        elif any(word in meal_lower for word in ['arroz', 'feijão', 'macarrão', 'batata']):
            return 'images/food_images/lunch_rice.jpg'
        elif any(word in meal_lower for word in ['salada', 'legumes', 'verduras', 'vegetais']):
            return 'images/food_images/salad_vegetables.jpg'
        elif any(word in meal_lower for word in ['shake', 'proteico', 'whey', 'suplemento']):
            return 'images/food_images/supper_shake.jpg'
        elif any(word in meal_lower for word in ['sopa', 'creme']):
            return 'images/food_images/dinner_soup.jpg'
        elif any(word in meal_lower for word in ['sanduíche', 'lanche', 'tapioca']):
            return 'images/food_images/snack_sandwich.jpg'
        else:
            return 'images/food_images/default_food.jpg'
    except:
        return 'images/food_images/default_food.jpg'


# def get_training_image_url(exercise_name):
#     """Busca imagem de treino"""
#     try:
#         if isinstance(exercise_name, str) and exercise_name.startswith('http'):
#             return exercise_name
#
#         exercise_lower = exercise_name.lower() if isinstance(exercise_name, str) else ''
#
#         search_terms = {
#             'agachamento': 'squat exercise gym',
#             'flexão': 'push up workout',
#             # ... resto do mapeamento
#         }
#
#         search_term = 'fitness workout gym'
#         for key, term in search_terms.items():
#             if key in exercise_lower:
#                 search_term = term
#                 break
#
#         headers = {'Authorization': PEXELS_API_KEY}
#         params = {
#             'query': search_term,
#             'per_page': 1,
#             'orientation': 'portrait'
#         }
#
#         response = requests.get(
#             'https://api.pexels.com/v1/search',
#             headers=headers,
#             params=params,
#             timeout=5
#         )
#
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('photos') and len(data['photos']) > 0:
#                 return data['photos'][0]['src']['medium']
#
#         return get_local_exercise_image(exercise_name)
#
#     except Exception as e:
#         print(f"Erro ao buscar imagem Pexels para '{exercise_name}': {e}")
#         return get_local_exercise_image(exercise_name)

def get_training_image_url(exercise_name):
    """Busca imagem de treino"""
    try:
        # Se já é uma URL completa, retornar diretamente
        if isinstance(exercise_name, str) and exercise_name.startswith('http'):
            return exercise_name

        exercise_lower = exercise_name.lower() if isinstance(exercise_name, str) else ''

        # MAPEAMENTO COMPLETO DE TERMOS DE BUSCA
        search_terms = {
            # Agachamentos
            'agachamento': 'squat exercise gym fitness',
            'squat': 'squat weightlifting gym',
            'agachamento livre': 'barbell squat gym',
            'agachamento frontal': 'front squat exercise',
            'agachamento sumo': 'sumo squat exercise',

            # Flexões
            'flexão': 'push up workout fitness',
            'push-up': 'push up exercise chest',
            'flexão diamante': 'diamond push up triceps',
            'flexão inclinada': 'incline push up chest',

            # Supinos
            'supino': 'bench press chest workout',
            'bench press': 'bench press gym',
            'supino inclinado': 'incline bench press',
            'supino declínio': 'decline bench press',

            # Remadas
            'remada': 'rowing exercise back workout',
            'remada curvada': 'bent over row back',
            'puxada': 'pull up back exercise',
            'lat pulldown': 'lat pulldown machine',

            # Ombros
            'desenvolvimento': 'shoulder press gym',
            'shoulder press': 'military press shoulders',
            'elevação lateral': 'lateral raise shoulders',
            'elevação frontal': 'front raise shoulders',

            # Braços
            'rosca': 'bicep curl arm workout',
            'bíceps': 'bicep exercise arms',
            'tríceps': 'tricep exercise arms',
            'tríceps testa': 'skull crusher triceps',
            'tríceps corda': 'tricep pushdown cable',

            # Pernas
            'leg press': 'leg press machine gym',
            'cadeira extensora': 'leg extension machine',
            'cadeira flexora': 'leg curl machine',
            'stiff': 'stiff leg deadlift',
            'levantamento terra': 'deadlift weightlifting',
            'afundo': 'lunge exercise legs',
            'avanço': 'walking lunge exercise',
            'panturrilha': 'calf raise exercise',

            # Glúteos
            'glúteo': 'glute workout fitness',
            'ponte glúteo': 'glute bridge exercise',
            'hip thrust': 'barbell hip thrust',

            # Abdominais
            'abdominal': 'ab workout fitness',
            'crunch': 'abdominal crunch exercise',
            'prancha': 'plank exercise core',
            'prancha lateral': 'side plank exercise',

            # Cardio
            'burpee': 'burpee exercise cardio',
            'mountain climbers': 'mountain climber cardio',
            'corrida': 'running exercise cardio',
            'polichinelo': 'jumping jack cardio',
            'jumping jacks': 'jumping jack workout',

            # Máquinas
            'peck deck': 'pec deck machine chest',
            'cadeira adutora': 'hip adduction machine',
            'mergulho': 'dip exercise triceps',

            # Outros
            'barra fixa': 'pull up bar exercise',
            'pull-up': 'pull up back workout',
            'chin-up': 'chin up bicep exercise',
            'kettlebell': 'kettlebell workout fitness',
            'halteres': 'dumbbell workout fitness',
            'elástico': 'resistance band exercise',
        }

        search_term = 'fitness workout gym exercise'
        for key, term in search_terms.items():
            if key in exercise_lower:
                search_term = term
                break

        headers = {'Authorization': PEXELS_API_KEY}
        params = {
            'query': search_term,
            'per_page': 1,
            'orientation': 'portrait',
            'size': 'medium'
        }

        response = requests.get(
            'https://api.pexels.com/v1/search',
            headers=headers,
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('photos') and len(data['photos']) > 0:
                return data['photos'][0]['src']['medium']

        # Fallback para imagem local
        return get_local_exercise_image(exercise_name)

    except Exception as e:
        print(f"Erro ao buscar imagem Pexels para '{exercise_name}': {e}")
        return get_local_exercise_image(exercise_name)


def get_local_exercise_image(exercise_name):
    """Retorna imagem local como fallback"""
    try:
        if not isinstance(exercise_name, str):
            return 'images/exercise_images/default_exercise.jpg'

        exercise_lower = exercise_name.lower()

        # Verificar se arquivos locais existem
        if any(word in exercise_lower for word in ['flexão', 'push', 'peito', 'supino', 'chest']):
            return 'images/exercise_images/pushup_exercise.jpg'
        elif any(word in exercise_lower for word in ['agachamento', 'squat', 'perna', 'leg press', 'leg']):
            return 'images/exercise_images/squat_exercise.jpg'
        elif any(word in exercise_lower for word in ['barra fixa', 'pull', 'costas', 'remada', 'back']):
            return 'images/exercise_images/pullup_exercise.jpg'
        elif any(word in exercise_lower for word in ['abdominal', 'crunch', 'core', 'prancha', 'plank']):
            return 'images/exercise_images/crunch_exercise.jpg'
        elif any(word in exercise_lower for word in ['corrida', 'run', 'cardio', 'burpee', 'jump']):
            return 'images/exercise_images/running_exercise.jpg'
        elif any(word in exercise_lower for word in ['rosca', 'bíceps', 'curl', 'arm']):
            return 'images/exercise_images/curl_exercise.jpg'
        elif any(word in exercise_lower for word in ['tríceps', 'tricep', 'extension']):
            return 'images/exercise_images/tricep_exercise.jpg'
        elif any(word in exercise_lower for word in ['desenvolvimento', 'ombro', 'shoulder', 'press']):
            return 'images/exercise_images/shoulder_exercise.jpg'
        elif any(word in exercise_lower for word in ['terra', 'deadlift', 'stiff']):
            return 'images/exercise_images/deadlift_exercise.jpg'
        elif any(word in exercise_lower for word in ['glúteo', 'glute', 'hip', 'bridge']):
            return 'images/exercise_images/glute_exercise.jpg'
        else:
            return 'images/exercise_images/default_exercise.jpg'
    except:
        return 'images/exercise_images/default_exercise.jpg'


# ========== ROTA PRINCIPAL ALL_MY_TRAINING - ATUALIZADA ==========

# @bp.route('/all_my_training')
# def all_my_training():
#     """Rota principal corrigida - Cada usuário tem seu próprio treino"""
#     if 'user_id' not in session:
#         return redirect('/login')
#
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         # Buscar treino específico do usuário
#         cur.execute("""
#             SELECT t.*
#             FROM treino t
#             WHERE t.id_cadastro = %s
#             ORDER BY t.id_treino DESC
#             LIMIT 1
#         """, (user_id,))
#
#         treino_result = cur.fetchone()
#
#         if not treino_result:
#             # Se não tiver treino, redirecionar para criar
#             return redirect('/my_level')
#
#         treino_data = processar_resultado(treino_result)
#
#         # Buscar dados específicos do usuário
#         cur.execute("""
#             SELECT data_nascimento, nome_usuario, email_usuario
#             FROM cadastrousuarios
#             WHERE id_cadastro = %s
#         """, (user_id,))
#
#         usuario_result = cur.fetchone()
#
#         if not usuario_result:
#             cur.close()
#             conn.close()
#             return render_template('all_my_training.html',
#                                    error="Usuário não encontrado")
#
#         usuario_data = processar_resultado(usuario_result)
#
#         # Calcular idade específica do usuário
#         data_nascimento = usuario_data['data_nascimento']
#         hoje = datetime.now()
#         idade = hoje.year - data_nascimento.year
#
#         if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
#             idade -= 1
#
#         # Identificar gênero específico
#         genero = get_gender_by_name(usuario_data['nome_usuario'])
#
#         # Preparar dados PERSONALIZADOS para API
#         fitness_data = {
#             "name": usuario_data['nome_usuario'],
#             "age": idade,
#             "sex": genero,
#             "height_cm": float(treino_data['altura_usuario']) * 100,
#             "weight_kg": float(treino_data['peso_usuario']),
#             "experience": treino_data['qtn_tempo_pratica_exercicios'],
#             "goal": treino_data['objetivo_usuario'],
#             "access": "casa"  # ou buscar do banco se tiver campo
#         }
#
#         # Gerar treino PERSONALIZADO para este usuário
#         api_data = chamar_api_fitness_local(fitness_data)
#
#         # Buscar agenda específica do usuário
#         cur.execute("""
#             SELECT DISTINCT dia_semana
#             FROM agenda
#             WHERE id_cadastro = %s
#         """, (user_id,))
#
#         dias_result = cur.fetchall()
#         user_training_days_raw = [processar_resultado(dia)['dia_semana'] for dia in dias_result]
#
#         # Ordenar dias
#         day_order = {
#             'Domingo': 1, 'Segunda-feira': 2, 'Terça-feira': 3,
#             'Quarta-feira': 4, 'Quinta-feira': 5, 'Sexta-feira': 6, 'Sábado': 7
#         }
#         user_training_days = sorted(user_training_days_raw, key=lambda x: day_order.get(x, 99))
#
#         # Preparar exercícios PERSONALIZADOS
#         exercicios = []
#
#         if api_data and 'exercise_plan' in api_data and 'plan' in api_data['exercise_plan']:
#             treino_plan = api_data['exercise_plan']['plan']
#             day_counter = 0
#
#             # Garantir que cada usuário tenha treino completo
#             total_exercicios = sum(len(exercises) for exercises in treino_plan.values())
#             print(f"Usuário {user_id} - {usuario_data['nome_usuario']} tem {total_exercicios} exercícios")
#
#             for training_type, exercises in treino_plan.items():
#                 for exercise in exercises:
#                     # Obter recursos visuais
#                     gif_url = get_exercise_gif_url(exercise['exercise'])
#                     image_url = get_training_image_url(exercise['exercise'])
#
#                     # Determinar dia da semana
#                     if user_training_days and day_counter < len(user_training_days):
#                         dia_semana = user_training_days[day_counter]
#                         day_counter = (day_counter + 1) % len(user_training_days)
#                     else:
#                         # Distribuir pelos dias da semana
#                         dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira',
#                                        'Quinta-feira', 'Sexta-feira', 'Sábado']
#                         dia_semana = dias_semana[day_counter % len(dias_semana)]
#                         day_counter += 1
#
#                     exercicios.append({
#                         'nome': exercise['exercise'],
#                         'series': exercise.get('series', 3),
#                         'reps': exercise.get('reps', '10-12'),
#                         'dia': dia_semana,
#                         'tipo': training_type,
#                         'gif_url': gif_url,
#                         'imagem_exercicio': image_url,
#                         'descricao': exercise.get('descricao', '')
#                     })
#
#         # Buscar agenda completa
#         cur.execute("""
#             SELECT a.*, t.nome_treino, t.objetivo_usuario
#             FROM agenda a
#             JOIN treino t ON a.id_treino = t.id_treino
#             WHERE a.id_cadastro = %s
#             ORDER BY
#                 CASE dia_semana
#                     WHEN 'Domingo' THEN 1
#                     WHEN 'Segunda-feira' THEN 2
#                     WHEN 'Terça-feira' THEN 3
#                     WHEN 'Quarta-feira' THEN 4
#                     WHEN 'Quinta-feira' THEN 5
#                     WHEN 'Sexta-feira' THEN 6
#                     WHEN 'Sábado' THEN 7
#                 END,
#                 horario
#         """, (user_id,))
#
#         agenda_results = cur.fetchall()
#
#         # Organizar agenda
#         agenda_organizada = {
#             'Domingo': [], 'Segunda-feira': [], 'Terça-feira': [],
#             'Quarta-feira': [], 'Quinta-feira': [], 'Sexta-feira': [], 'Sábado': []
#         }
#
#         for item_result in agenda_results:
#             item = processar_resultado(item_result)
#             dia = item.get('dia_semana', '')
#
#             if dia in agenda_organizada:
#                 agenda_organizada[dia].append({
#                     'horario': item.get('horario', '--:--'),
#                     'treino': item.get('nome_treino', 'Treino'),
#                     'objetivo': item.get('objetivo_usuario', ''),
#                     'icone': f"images/icons_agenda/mdi_dumbbell.svg"
#                 })
#
#         # Preparar dieta PERSONALIZADA
#         dieta = {}
#         if api_data and 'nutrition_plan' in api_data and 'sample_menu' in api_data['nutrition_plan']:
#             menu = api_data['nutrition_plan']['sample_menu']
#             dieta = {
#                 'cafe_manha': menu.get('breakfast', '3 ovos + pão integral + 1 banana'),
#                 'lanche_manha': menu.get('snack', 'Iogurte natural + aveia + mel'),
#                 'almoco': menu.get('lunch', 'Frango + arroz + feijão + salada'),
#                 'lanche_tarde': menu.get('snack_2', 'Sanduíche natural + fruta'),
#                 'jantar': menu.get('dinner', 'Peixe + batata doce + legumes'),
#                 'ceia': 'Shake proteico ou chá'
#             }
#         else:
#             # Dieta padrão personalizada pelo objetivo
#             objetivo = treino_data.get('objetivo_usuario', 'Ganhar músculo').lower()
#
#             if 'perder' in objetivo or 'emagrecer' in objetivo:
#                 dieta = {
#                     'cafe_manha': 'Omelete de 2 ovos + 1 fatia pão integral',
#                     'lanche_manha': 'Iogurte grego natural + 5 morangos',
#                     'almoco': '150g frango grelhado + 100g arroz integral + salada',
#                     'lanche_tarde': '1 maçã + 10 amêndoas',
#                     'jantar': '150g peixe + legumes no vapor',
#                     'ceia': 'Chá verde'
#                 }
#             elif 'ganhar' in objetivo or 'músculo' in objetivo:
#                 dieta = {
#                     'cafe_manha': '4 ovos mexidos + 2 fatias pão + 1 banana',
#                     'lanche_manha': 'Whey protein + 50g aveia',
#                     'almoco': '200g carne + 150g arroz + feijão',
#                     'lanche_tarde': 'Sanduíche de frango + queijo',
#                     'jantar': '200g peixe + 200g batata doce',
#                     'ceia': 'Caseína ou iogurte grego'
#                 }
#             else:
#                 dieta = {
#                     'cafe_manha': '3 ovos + pão integral + 1 banana',
#                     'lanche_manha': 'Iogurte natural + aveia + mel',
#                     'almoco': 'Frango + arroz + feijão + salada',
#                     'lanche_tarde': 'Sanduíche natural + fruta',
#                     'jantar': 'Peixe + batata doce + legumes',
#                     'ceia': 'Shake proteico ou chá'
#                 }
#
#         # Gerar imagens de comida
#         food_images = generate_food_images(dieta)
#
#         # Calcular estatísticas
#         total_atividades = sum(len(atividades) for atividades in agenda_organizada.values())
#         dias_com_atividade = sum(1 for atividades in agenda_organizada.values() if len(atividades) > 0)
#
#         # Preparar dados para template
#         meal_types = {
#             'cafe_manha': 'Café da manhã',
#             'lanche_manha': 'Lanche da manhã',
#             'almoco': 'Almoço',
#             'lanche_tarde': 'Lanche da tarde',
#             'jantar': 'Jantar',
#             'ceia': 'Ceia'
#         }
#
#         meal_times = {
#             'cafe_manha': '6:00 AM',
#             'lanche_manha': '10:00 AM',
#             'almoco': '12:00 PM',
#             'lanche_tarde': '16:00 PM',
#             'jantar': '19:00 PM',
#             'ceia': '21:00 PM'
#         }
#
#         assessment_data = api_data.get('assessment', {}) if api_data else {}
#
#         cur.close()
#         conn.close()
#
#         return render_template('all_my_training.html',
#                                treino=treino_data,
#                                exercicios=exercicios,
#                                agenda=agenda_organizada,
#                                dieta=dieta,
#                                food_images=food_images,
#                                api_data=api_data,
#                                genero=genero,
#                                user_training_days=user_training_days,
#                                meal_types=meal_types,
#                                meal_times=meal_times,
#                                total_atividades=total_atividades,
#                                dias_com_atividade=dias_com_atividade,
#                                assessment_data=assessment_data,
#                                user_nome=usuario_data['nome_usuario'],
#                                user_id=user_id)
#
#     except Exception as e:
#         print(f"Erro em all_my_training para usuário {user_id}: {str(e)}")
#         import traceback
#         traceback.print_exc()
#
#         try:
#             cur.close()
#             conn.close()
#         except:
#             pass
#
#         return render_template('all_my_training.html',
#                                error=f"Erro ao carregar seus dados: {str(e)[:100]}")


# ========== API LOCAL ATUALIZADA ==========

def chamar_api_fitness_local(fitness_data):
    """API local aprimorada que gera treinos COMPLETOS e PERSONALIZADOS"""
    try:
        name = fitness_data["name"]
        age = fitness_data["age"]
        sex = fitness_data["sex"]
        height_cm = fitness_data["height_cm"]
        weight_kg = fitness_data["weight_kg"]
        experience = fitness_data["experience"]
        goal = fitness_data["goal"]
        access = fitness_data.get("access", "casa")

        # Gerar treino COMPLETO
        from . import treino_personalizado

        treino_completo = treino_personalizado.gerar_treino_completo(
            idade=age,
            peso=weight_kg,
            altura=height_cm / 100,
            experiencia=experience,
            objetivo=goal,
            acesso=access,
            genero=sex
        )

        # Gerar dieta PERSONALIZADA
        dieta_personalizada = treino_personalizado.gerar_dieta_personalizada(
            peso=weight_kg,
            altura=height_cm,
            idade=age,
            objetivo=goal,
            genero=sex,
            nivel_atividade=experience
        )

        # Cálculos metabólicos
        altura_m = height_cm / 100
        bmi = round(weight_kg / (altura_m ** 2), 2)

        if bmi < 18.5:
            bmi_category = "Abaixo do peso"
        elif bmi < 25:
            bmi_category = "Normal"
        elif bmi < 30:
            bmi_category = "Sobrepeso"
        else:
            bmi_category = "Obesidade"

        # Fórmula de Mifflin–St Jeor
        if sex == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        # Fator de atividade
        factors = {
            "nunca pratiquei antes": 1.375,
            "a menos de 1 ano": 1.375,
            "a mais de 1 ano": 1.55,
            "a 4 anos": 1.6,
            "a mais de 5 anos": 1.725
        }
        factor = factors.get(experience.lower(), 1.55)
        tdee = bmr * factor

        # Calorias alvo
        goal_lower = goal.lower()
        if "perder" in goal_lower:
            target_calories = tdee * 0.85
        elif "ganhar" in goal_lower:
            target_calories = tdee * 1.1
        else:
            target_calories = tdee
        target_calories = round(target_calories)

        # Macros
        protein_g = round(2.0 * weight_kg)
        fat_g = round(0.9 * weight_kg)
        carbs_g = round((target_calories - (protein_g * 4 + fat_g * 9)) / 4)

        # Montar resposta
        result = {
            "user": {
                "name": name,
                "age": age,
                "sex": sex,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "experience": experience,
                "goal": goal,
                "access": access
            },
            "assessment": {
                "BMI": bmi,
                "BMI_category": bmi_category,
                "BMR_kcal": round(bmr, 1),
                "TDEE_kcal": round(tdee, 1),
                "recommended_calories_kcal": target_calories,
                "macros": {
                    "protein_g": protein_g,
                    "fat_g": fat_g,
                    "carbs_g": carbs_g
                }
            },
            "exercise_plan": {
                "frequency_per_week": 5 if access.lower() == 'academia' else 4,
                "type": "Treino Personalizado Completo",
                "plan": treino_completo,
                "progression": "Aumentar carga semanalmente. Alterar exercícios a cada 6-8 semanas.",
                "total_exercises": sum(len(exercises) for exercises in treino_completo.values())
            },
            "nutrition_plan": {
                "calories_target_kcal": dieta_personalizada["calorias_diarias"],
                "macros": dieta_personalizada["macros"],
                "sample_menu": dieta_personalizada["refeicoes"],
                "emphasis": dieta_personalizada["enfase"]
            },
            "recommendations": {
                "descanso": "Dormir 7-9 horas por noite",
                "hidratacao": f"Beber {round(weight_kg * 0.035, 1)}L de água diariamente",
                "suplementacao": "Considerar creatina e whey protein se necessário",
                "consistencia": "Manter pelo menos 80% de aderência ao plano"
            },
            "notes": f"Plano gerado em {datetime.now().strftime('%d/%m/%Y')}. Personalizado para {name} ({age} anos)."
        }

        return result

    except Exception as e:
        print(f"Erro ao gerar treino local: {e}")
        import traceback
        traceback.print_exc()
        return None


# ========== ROTAS PARA AGENDA COM TREINOS DISPONÍVEIS ==========

@bp.route('/api/treinos_disponiveis')
def treinos_disponiveis():
    """Retorna treinos disponíveis para selecionar na agenda"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        # Buscar treino atual
        cur.execute("""
            SELECT * FROM treino 
            WHERE id_cadastro = %s 
            ORDER BY id_treino DESC 
            LIMIT 1
        """, (user_id,))

        treino_atual = cur.fetchone()

        if not treino_atual:
            return jsonify({'error': 'Crie um treino primeiro'}), 400

        # Buscar dados do usuário
        cur.execute("""
            SELECT nome_usuario, data_nascimento 
            FROM cadastrousuarios 
            WHERE id_cadastro = %s
        """, (user_id,))

        usuario = cur.fetchone()

        # Processar dados
        treino_data = processar_resultado(treino_atual)
        usuario_data = processar_resultado(usuario)

        # Calcular idade
        data_nascimento = usuario_data['data_nascimento']
        idade = datetime.now().year - data_nascimento.year
        hoje = datetime.now()
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1

        # Gerar múltiplas opções de treino
        from . import treino_personalizado

        treinos_opcoes = treino_personalizado.gerar_treino_completo(
            idade=idade,
            peso=float(treino_data['peso_usuario']),
            altura=float(treino_data['altura_usuario']),
            experiencia=treino_data['qtn_tempo_pratica_exercicios'],
            objetivo=treino_data['objetivo_usuario'],
            acesso='academia' if 'academia' in treino_data.get('acesso', '') else 'casa',
            genero=get_gender_by_name(usuario_data['nome_usuario'])
        )

        # Formatar opções para select
        opcoes_formatadas = []

        for tipo_treino, exercicios in treinos_opcoes.items():
            opcoes_formatadas.append({
                'id': f"treino_{tipo_treino.lower().replace(' ', '_').replace('&', 'e')}",
                'nome': f"{tipo_treino}",
                'tipo': 'treino',
                'descricao': f"Treino de {tipo_treino} com {len(exercicios)} exercícios",
                'exercicios': exercicios[:3],  # Preview de 3 exercícios
                'total_exercicios': len(exercicios)
            })

        # Adicionar opções de dieta
        dietas_opcoes = [
            {
                'id': 'dieta_emagrecimento',
                'nome': 'Refeição para Emagrecimento',
                'tipo': 'dieta',
                'descricao': 'Plano alimentar focado em perda de gordura',
                'refeicao': 'Frango grelhado + legumes'
            },
            {
                'id': 'dieta_hipertrofia',
                'nome': 'Refeição para Ganho Muscular',
                'tipo': 'dieta',
                'descricao': 'Plano alimentar focado em ganho de massa',
                'refeicao': 'Carne + batata doce + vegetais'
            },
            {
                'id': 'dieta_balanceada',
                'nome': 'Refeição Balanceada',
                'tipo': 'dieta',
                'descricao': 'Refeição equilibrada com todos nutrientes',
                'refeicao': 'Peixe + arroz integral + salada'
            }
        ]

        # Opções de descanso/recuperação
        recuperacao_opcoes = [
            {
                'id': 'descanso_ativo',
                'nome': 'Descanso Ativo',
                'tipo': 'recuperacao',
                'descricao': 'Atividades leves para recuperação',
                'sugestoes': 'Caminhada leve, alongamento, yoga'
            },
            {
                'id': 'descanso_total',
                'nome': 'Descanso Total',
                'tipo': 'recuperacao',
                'descricao': 'Dia completo de descanso',
                'sugestoes': 'Repouso, hidratação, sono de qualidade'
            }
        ]

        todas_opcoes = opcoes_formatadas + dietas_opcoes + recuperacao_opcoes

        return jsonify({
            'success': True,
            'opcoes': todas_opcoes,
            'total': len(todas_opcoes),
            'user_info': {
                'nome': usuario_data['nome_usuario'],
                'idade': idade,
                'objetivo': treino_data['objetivo_usuario'],
                'user_id': user_id
            }
        })

    except Exception as e:
        print(f"Erro ao buscar treinos disponíveis: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# @bp.route('/api/atualizar_treino', methods=['POST'])
# def atualizar_treino():
#     """Permite ao usuário atualizar seu treino quando quiser"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     try:
#         data = request.get_json()
#         user_id = session['user_id']
#
#         # Validar dados
#         required = ['peso', 'altura', 'experiencia', 'objetivo']
#         for field in required:
#             if field not in data:
#                 return jsonify({'error': f'Campo obrigatório: {field}'}), 400
#
#         # Converter valores
#         peso = float(str(data['peso']).replace(',', '.'))
#         altura = float(str(data['altura']).replace(',', '.'))
#         experiencia = data['experiencia']
#         objetivo = data['objetivo']
#         acesso = data.get('acesso', 'casa')
#
#         # Buscar dados do usuário
#         conn = get_db_connection()
#         cur = get_db_cursor(conn)
#
#         cur.execute("""
#             SELECT nome_usuario, data_nascimento
#             FROM cadastrousuarios
#             WHERE id_cadastro = %s
#         """, (user_id,))
#
#         usuario = cur.fetchone()
#         nome_usuario = usuario['nome_usuario']
#         data_nascimento = usuario['data_nascimento']
#
#         # Calcular idade
#         idade = datetime.now().year - data_nascimento.year
#         hoje = datetime.now()
#         if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
#             idade -= 1
#
#         # Gerar NOVO treino personalizado
#         fitness_data = {
#             "name": nome_usuario,
#             "age": idade,
#             "sex": get_gender_by_name(nome_usuario),
#             "height_cm": altura * 100,
#             "weight_kg": peso,
#             "experience": experiencia,
#             "goal": objetivo,
#             "access": acesso
#         }
#
#         # Gerar novo treino
#         novo_treino_info = chamar_api_fitness_local(fitness_data)
#
#         if not novo_treino_info:
#             cur.close()
#             conn.close()
#             return jsonify({'error': 'Falha ao gerar novo treino'}), 500
#
#         # Salvar NOVO treino no banco
#         nome_treino = f"Treino {objetivo} - Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
#
#         cur.execute("""
#             INSERT INTO treino
#             (id_cadastro, nome_treino, peso_usuario, altura_usuario,
#              qtn_tempo_pratica_exercicios, objetivo_usuario)
#             VALUES (%s, %s, %s, %s, %s, %s)
#             RETURNING id_treino
#         """, (
#             user_id,
#             nome_treino,
#             peso,
#             altura,
#             experiencia,
#             objetivo
#         ))
#
#         novo_treino_id = cur.fetchone()['id_treino']
#
#         # MANTER agenda antiga (usuário decide se quer atualizar)
#         # A agenda continua com os treinos antigos até o usuário reconfigurar
#
#         conn.commit()
#
#         return jsonify({
#             'success': True,
#             'message': 'Treino atualizado com sucesso! Você pode manter sua agenda atual ou reconfigurá-la.',
#             'treino_id': novo_treino_id,
#             'treino_info': novo_treino_info,
#             'recomendacao': 'Acesse "Meu Treino" para ver seu novo plano ou "Agenda" para reconfigurar seus horários.'
#         })
#
#     except Exception as e:
#         print(f"Erro ao atualizar treino: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         try:
#             if 'cur' in locals():
#                 cur.close()
#             if 'conn' in locals():
#                 conn.close()
#         except:
#             pass

@bp.route('/api/atualizar_treino', methods=['POST'])
def atualizar_treino():
    """Permite ao usuário atualizar seu treino quando quiser"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    try:
        data = request.get_json()
        print(f"Dados recebidos para atualização: {data}")  # DEBUG

        user_id = session['user_id']

        # Validar dados
        required = ['peso', 'altura', 'experiencia', 'objetivo']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400

        # Converter valores
        try:
            peso_str = str(data['peso']).replace(',', '.')
            peso = float(peso_str)
        except ValueError:
            return jsonify({'error': f'Peso inválido: {data["peso"]}. Use números (ex: 75.5 ou 75,5)'}), 400

        try:
            altura_str = str(data['altura']).replace(',', '.')
            altura = float(altura_str)
        except ValueError:
            return jsonify({'error': f'Altura inválida: {data["altura"]}. Use números (ex: 1.75 ou 1,75)'}), 400

        experiencia = data['experiencia']
        objetivo = data['objetivo']
        acesso = data.get('acesso', 'casa')

        print(f"Valores convertidos: peso={peso}, altura={altura}, exp={experiencia}, obj={objetivo}")  # DEBUG

        # Buscar dados do usuário
        conn = get_db_connection()
        cur = get_db_cursor(conn)

        try:
            cur.execute("""
                SELECT nome_usuario, data_nascimento 
                FROM cadastrousuarios 
                WHERE id_cadastro = %s
            """, (user_id,))

            usuario = cur.fetchone()
            if not usuario:
                return jsonify({'error': 'Usuário não encontrado'}), 404

            nome_usuario = usuario['nome_usuario']
            data_nascimento = usuario['data_nascimento']

            # Calcular idade
            idade = datetime.now().year - data_nascimento.year
            hoje = datetime.now()
            if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
                idade -= 1

            # Identificar gênero
            genero = get_gender_by_name(nome_usuario)

            # Gerar NOVO treino personalizado
            fitness_data = {
                "name": nome_usuario,
                "age": idade,
                "sex": genero,
                "height_cm": altura * 100,
                "weight_kg": peso,
                "experience": experiencia,
                "goal": objetivo,
                "access": acesso
            }

            print(f"Dados para API: {fitness_data}")  # DEBUG

            # Gerar novo treino
            novo_treino_info = chamar_api_fitness_local(fitness_data)

            if not novo_treino_info:
                print("API local retornou None")
                return jsonify({'error': 'Falha ao gerar novo treino. Tente novamente.'}), 500

            # Salvar NOVO treino no banco
            nome_treino = f"Treino {objetivo} - Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"

            cur.execute("""
                INSERT INTO treino 
                (id_cadastro, nome_treino, peso_usuario, altura_usuario, 
                 qtn_tempo_pratica_exercicios, objetivo_usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_treino
            """, (
                user_id,
                nome_treino,
                peso,
                altura,
                experiencia,
                objetivo
            ))

            resultado = cur.fetchone()
            if not resultado:
                return jsonify({'error': 'Falha ao inserir treino no banco'}), 500

            novo_treino_id = resultado['id_treino'] if isinstance(resultado, dict) else resultado[0]

            # MANTER agenda antiga (usuário decide se quer atualizar)
            # A agenda continua com os treinos antigos até o usuário reconfigurar

            conn.commit()

            print(f"Treino atualizado com sucesso! ID: {novo_treino_id}")

            # Calcular estatísticas do novo treino
            total_exercicios = 0
            if novo_treino_info and 'exercise_plan' in novo_treino_info:
                if 'plan' in novo_treino_info['exercise_plan']:
                    plan = novo_treino_info['exercise_plan']['plan']
                    if isinstance(plan, dict):
                        total_exercicios = sum(len(exercises) for exercises in plan.values())

            return jsonify({
                'success': True,
                'message': 'Treino atualizado com sucesso!',
                'treino_id': novo_treino_id,
                'nome_treino': nome_treino,
                'total_exercicios': total_exercicios,
                'user_info': {
                    'nome': nome_usuario,
                    'idade': idade,
                    'objetivo': objetivo,
                    'peso': peso,
                    'altura': altura
                },
                'recomendacao': 'Acesse "Meu Treino" para ver seu novo plano ou "Agenda" para reconfigurar seus horários.'
            })

        except Exception as e:
            conn.rollback()
            print(f"Erro no banco de dados durante atualização: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500

        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    except Exception as e:
        print(f"Erro geral em atualizar_treino: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


# ========== OUTRAS ROTAS ==========

@bp.route('/my_level')
def my_level():
    """Página para criar/atualizar treino"""
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('my_level.html')


@bp.route('/api/salvar_treino', methods=['POST'])
def salvar_treino():
    """Salva um novo treino no banco de dados - CORRIGIDA"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    try:
        data = request.get_json()
        user_id = session['user_id']

        # Validação
        required_fields = ['peso', 'altura', 'experiencia', 'objetivo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório faltando: {field}'}), 400

        # Converter valores
        try:
            peso = float(str(data['peso']).replace(',', '.'))
        except:
            return jsonify({'error': 'Peso inválido'}), 400

        try:
            altura = float(str(data['altura']).replace(',', '.'))
        except:
            return jsonify({'error': 'Altura inválida'}), 400

        experiencia = data['experiencia']
        objetivo = data['objetivo']
        acesso = data.get('acesso', 'casa')

        # Buscar dados do usuário
        conn = get_db_connection()
        cur = get_db_cursor(conn)

        cur.execute("""
            SELECT data_nascimento, nome_usuario 
            FROM cadastrousuarios 
            WHERE id_cadastro = %s
        """, (user_id,))

        resultado = cur.fetchone()
        if not resultado:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        usuario_data = processar_resultado(resultado)
        data_nascimento = usuario_data['data_nascimento']
        nome_usuario = usuario_data['nome_usuario']

        # Calcular idade
        idade = datetime.now().year - data_nascimento.year
        hoje = datetime.now()
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1

        # Identificar gênero
        genero = get_gender_by_name(nome_usuario)

        # Preparar dados para API
        fitness_data = {
            "name": nome_usuario,
            "age": idade,
            "sex": genero,
            "height_cm": altura * 100,
            "weight_kg": peso,
            "experience": experiencia,
            "goal": objetivo,
            "access": acesso
        }

        # Gerar treino PERSONALIZADO
        treino_info = chamar_api_fitness_local(fitness_data)

        # Salvar no banco
        nome_treino = f"Treino {objetivo} - {datetime.now().strftime('%d/%m/%Y')}"

        cur.execute("""
            INSERT INTO treino 
            (id_cadastro, nome_treino, peso_usuario, altura_usuario, 
             qtn_tempo_pratica_exercicios, objetivo_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_treino
        """, (
            user_id,
            nome_treino,
            peso,
            altura,
            experiencia,
            objetivo
        ))

        treino_id = cur.fetchone()['id_treino']
        conn.commit()

        return jsonify({
            'success': True,
            'treino_id': treino_id,
            'nome_treino': nome_treino,
            'treino_info': treino_info,
            'message': 'Treino personalizado criado com sucesso!'
        })

    except Exception as e:
        print(f"Erro em salvar_treino: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
        except:
            pass


@bp.route('/api/treinos_usuario')
def treinos_usuario():
    """API para buscar treinos do usuário"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        cur.execute("""
            SELECT id_treino, nome_treino, objetivo_usuario, 
                   peso_usuario, altura_usuario, qtn_tempo_pratica_exercicios
            FROM treino 
            WHERE id_cadastro = %s 
            ORDER BY id_treino DESC
        """, (user_id,))

        treinos = cur.fetchall()

        treinos_list = []
        for treino in treinos:
            treinos_list.append({
                'id_treino': treino['id_treino'],
                'nome_treino': treino['nome_treino'],
                'objetivo_usuario': treino['objetivo_usuario'],
                'peso_usuario': treino['peso_usuario'],
                'altura_usuario': treino['altura_usuario'],
                'experiencia': treino['qtn_tempo_pratica_exercicios']
            })

        return jsonify({
            'success': True,
            'treinos': treinos_list,
            'total': len(treinos_list)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# def melhorar_get_exercise_gif_url(exercise_name):
#     """Versão melhorada para associar melhor GIFs com exercícios"""
#     try:
#         exercise_lower = exercise_name.lower().strip()
#
#         # Log para debug
#         print(f"Buscando GIF para: {exercise_name} -> {exercise_lower}")
#
#         # Mapeamento otimizado
#         gif_map = {
#             # Agachamentos
#             'agachamento': 'Agachamento_livre.gif',
#             'squat': 'Agachamento_livre.gif',
#             'agachamento livre': 'Agachamento_livre.gif',
#
#             # Flexões
#             'flexão': 'Flexão_tradicional.gif',
#             'push-up': 'Flexão_tradicional.gif',
#             'push up': 'Flexão_tradicional.gif',
#
#             # Supinos
#             'supino': 'Supino_reto_com_barra.gif',
#             'bench press': 'Supino_reto_com_barra.gif',
#
#             # Remadas
#             'remada': 'Remada_curvada_com_barra.gif',
#             'row': 'Remada_curvada_com_barra.gif',
#
#             # Puxadas
#             'puxada': 'Puxada_na_frente_pulldown.gif',
#             'pull-up': 'barra_fixa_pegada_aberta.gif',
#
#             # Ombros
#             'desenvolvimento': 'Desenvolvimento_com_barra.gif',
#             'shoulder press': 'Desenvolvimento_com_barra.gif',
#
#             # Rosca
#             'rosca': 'Rosca_direta_barra.gif',
#             'bíceps': 'Rosca_direta_barra.gif',
#             'curl': 'Rosca_direta_barra.gif',
#
#             # Tríceps
#             'tríceps': 'Triceps_testa.gif',
#             'tricep': 'Triceps_testa.gif',
#
#             # Pernas
#             'leg press': 'Leg_press.gif',
#             'leg extension': 'cadeira-extensora.gif',
#             'leg curl': 'cadeira-flexora.gif',
#
#             # Abdominais
#             'abdominal': 'Abdominal_tradicional.gif',
#             'crunch': 'Crunch_no_cabo.gif',
#
#             # Pranchas
#             'prancha': 'prancha-frontal-tradicional-com-bracos-esticados.gif',
#             'plank': 'prancha-frontal-tradicional-com-bracos-esticados.gif',
#
#             # Cardio
#             'burpee': 'Burpees.gif',
#             'corrida': 'corrida.gif',
#             'running': 'corrida.gif',
#         }
#
#         # Buscar correspondência exata primeiro
#         for key, gif in gif_map.items():
#             if key in exercise_lower:
#                 gif_path = os.path.join('static', 'images', 'gifs', gif)
#                 if os.path.exists(gif_path):
#                     print(f"GIF encontrado: {gif} para {exercise_name}")
#                     return f"images/gifs/{gif}"
#                 else:
#                     print(f"GIF não encontrado no caminho: {gif_path}")
#
#         # Fallback por palavras-chave
#         keywords = {
#             'peito': 'Flexão_tradicional.gif',
#             'chest': 'Flexão_tradicional.gif',
#             'costas': 'Remada_curvada_com_barra.gif',
#             'back': 'Remada_curvada_com_barra.gif',
#             'ombro': 'Desenvolvimento_com_barra.gif',
#             'shoulder': 'Desenvolvimento_com_barra.gif',
#             'bíceps': 'Rosca_direta_barra.gif',
#             'bicep': 'Rosca_direta_barra.gif',
#             'tríceps': 'Triceps_testa.gif',
#             'tricep': 'Triceps_testa.gif',
#             'perna': 'Agachamento_livre.gif',
#             'leg': 'Agachamento_livre.gif',
#             'glúteo': 'ponte-para-gluteos.gif',
#             'glute': 'ponte-para-gluteos.gif',
#             'abdomen': 'Abdominal_tradicional.gif',
#             'core': 'Abdominal_tradicional.gif',
#             'cardio': 'Burpees.gif',
#             'aerobic': 'Burpees.gif',
#         }
#
#         for keyword, gif in keywords.items():
#             if keyword in exercise_lower:
#                 gif_path = os.path.join('static', 'images', 'gifs', gif)
#                 if os.path.exists(gif_path):
#                     print(f"GIF por keyword: {gif} para {exercise_name}")
#                     return f"images/gifs/{gif}"
#
#         # Fallback final
#         default_gif = 'default_exercise.gif'
#         default_path = os.path.join('static', 'images', 'gifs', default_gif)
#         if os.path.exists(default_path):
#             print(f"Usando GIF default para: {exercise_name}")
#             return f"images/gifs/{default_gif}"
#         else:
#             print(f"GIF default não encontrado: {default_path}")
#             return 'images/gifs/default_exercise.gif'
#
#     except Exception as e:
#         print(f"Erro crítico em get_exercise_gif_url: {e}")
#         return 'images/gifs/default_exercise.gif'
#
#
# def melhorar_get_food_image_url(meal_description):
#     """Versão melhorada para associar imagens de comida"""
#     try:
#         if not isinstance(meal_description, str):
#             return 'images/food_images/default_food.jpg'
#
#         meal_lower = meal_description.lower()
#         print(f"Buscando imagem de comida para: {meal_description}")
#
#         # Mapeamento direto de alimentos para imagens
#         food_map = {
#             # Café da manhã
#             'ovo': 'breakfast_eggs.jpg',
#             'ovos': 'breakfast_eggs.jpg',
#             'omelete': 'breakfast_eggs.jpg',
#             'pão': 'breakfast_bread.jpg',
#             'aveia': 'breakfast_oats.jpg',
#             'granola': 'breakfast_granola.jpg',
#             'iogurte': 'breakfast_yogurt.jpg',
#             'fruta': 'breakfast_fruit.jpg',
#             'banana': 'breakfast_fruit.jpg',
#             'maçã': 'breakfast_fruit.jpg',
#
#             # Almoço/Jantar
#             'frango': 'lunch_chicken.jpg',
#             'carne': 'lunch_meat.jpg',
#             'peixe': 'lunch_fish.jpg',
#             'salmão': 'lunch_fish.jpg',
#             'arroz': 'lunch_rice.jpg',
#             'feijão': 'lunch_beans.jpg',
#             'batata doce': 'lunch_sweet_potato.jpg',
#             'salada': 'lunch_salad.jpg',
#             'legumes': 'lunch_vegetables.jpg',
#
#             # Lanches
#             'sanduíche': 'snack_sandwich.jpg',
#             'castanha': 'snack_nuts.jpg',
#             'shake': 'snack_shake.jpg',
#             'whey': 'snack_shake.jpg',
#
#             # Jantar/Ceia
#             'sopa': 'dinner_soup.jpg',
#             'creme': 'dinner_soup.jpg',
#             'chá': 'dinner_tea.jpg',
#         }
#
#         # Buscar correspondência
#         for food, image in food_map.items():
#             if food in meal_lower:
#                 image_path = os.path.join('static', 'images', 'food_images', image)
#                 if os.path.exists(image_path):
#                     print(f"Imagem encontrada: {image} para {meal_description}")
#                     return f"images/food_images/{image}"
#                 else:
#                     # Tentar fallback local
#                     fallback = get_local_food_image_by_keyword(food)
#                     if fallback:
#                         return fallback
#
#         # Se não encontrou, usar Pexels como fallback
#         try:
#             headers = {'Authorization': PEXELS_API_KEY}
#             params = {
#                 'query': f'{meal_description} healthy food',
#                 'per_page': 1,
#                 'orientation': 'square'
#             }
#
#             response = requests.get(
#                 'https://api.pexels.com/v1/search',
#                 headers=headers,
#                 params=params,
#                 timeout=3
#             )
#
#             if response.status_code == 200:
#                 data = response.json()
#                 if data.get('photos') and len(data['photos']) > 0:
#                     return data['photos'][0]['src']['medium']
#         except:
#             pass
#
#         # Fallback final
#         return get_local_food_image_by_keyword('default')
#
#     except Exception as e:
#         print(f"Erro em get_food_image_url: {e}")
#         return 'images/food_images/default_food.jpg'


def get_local_food_image_by_keyword(keyword):
    """Busca imagem local por palavra-chave"""
    image_files = {
        'ovo': 'breakfast_eggs.jpg',
        'pão': 'breakfast_bread.jpg',
        'fruta': 'breakfast_fruit.jpg',
        'iogurte': 'breakfast_yogurt.jpg',
        'aveia': 'breakfast_oats.jpg',
        'frango': 'lunch_chicken.jpg',
        'carne': 'lunch_meat.jpg',
        'peixe': 'lunch_fish.jpg',
        'arroz': 'lunch_rice.jpg',
        'feijão': 'lunch_beans.jpg',
        'salada': 'lunch_salad.jpg',
        'sanduíche': 'snack_sandwich.jpg',
        'shake': 'snack_shake.jpg',
        'sopa': 'dinner_soup.jpg',
        'default': 'default_food.jpg'
    }

    for key, filename in image_files.items():
        if key in keyword.lower():
            filepath = os.path.join('static', 'images', 'food_images', filename)
            if os.path.exists(filepath):
                return f"images/food_images/{filename}"

    return 'images/food_images/default_food.jpg'


# ATUALIZE a rota all_my_training para usar as novas funções:

@bp.route('/all_my_training')
def all_my_training():
    """Rota principal SIMPLIFICADA - sem cache complexo"""
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        print(f"Carregando treino para usuário {user_id}")

        # Buscar treino mais recente
        cur.execute("""
            SELECT t.* 
            FROM treino t 
            WHERE t.id_cadastro = %s
            ORDER BY t.id_treino DESC
            LIMIT 1
        """, (user_id,))

        treino_result = cur.fetchone()

        if not treino_result:
            print(f"Usuário {user_id} não tem treino")
            cur.close()
            conn.close()
            return redirect('/my_level')

        treino_data = processar_resultado(treino_result)

        # Buscar dados do usuário
        cur.execute("""
            SELECT data_nascimento, nome_usuario 
            FROM cadastrousuarios 
            WHERE id_cadastro = %s
        """, (user_id,))

        usuario_result = cur.fetchone()
        usuario_data = processar_resultado(usuario_result)

        # Calcular idade
        data_nascimento = usuario_data['data_nascimento']
        hoje = datetime.now()
        idade = hoje.year - data_nascimento.year
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1

        # Preparar dados para API
        fitness_data = {
            "name": usuario_data['nome_usuario'],
            "age": idade,
            "sex": get_gender_by_name(usuario_data['nome_usuario']),
            "height_cm": float(treino_data.get('altura_usuario', 1.70)) * 100,
            "weight_kg": float(treino_data.get('peso_usuario', 70.0)),
            "experience": treino_data.get('qtn_tempo_pratica_exercicios', 'a mais de 1 ano'),
            "goal": treino_data.get('objetivo_usuario', 'Ganhar músculo'),
            "access": "casa"
        }

        # Gerar treino
        api_data = chamar_api_fitness_local(fitness_data)

        if not api_data:
            api_data = gerar_dados_padrao(fitness_data)

        # Buscar dias da agenda
        cur.execute("SELECT DISTINCT dia_semana FROM agenda WHERE id_cadastro = %s", (user_id,))
        dias_result = cur.fetchall()
        user_training_days = [processar_resultado(d)['dia_semana'] for d in dias_result if processar_resultado(d)]

        # Preparar exercícios
        exercicios = []

        if api_data and 'exercise_plan' in api_data and 'plan' in api_data['exercise_plan']:
            treino_plan = api_data['exercise_plan']['plan']
            day_counter = 0

            for training_type, exercises in treino_plan.items():
                if not isinstance(exercises, list):
                    continue

                for exercise in exercises:
                    if not isinstance(exercise, dict):
                        continue

                    exercise_name = exercise.get('exercise', 'Exercício')
                    gif_url = get_exercise_gif_url(exercise_name)  # Use a função ORIGINAL
                    image_url = get_training_image_url(exercise_name)  # Use a função ORIGINAL

                    # Determinar dia
                    if user_training_days and day_counter < len(user_training_days):
                        dia_semana = user_training_days[day_counter]
                        day_counter = (day_counter + 1) % len(user_training_days)
                    else:
                        dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira',
                                       'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
                        dia_semana = dias_semana[day_counter % len(dias_semana)] if dias_semana else 'Não definido'
                        day_counter += 1

                    exercicios.append({
                        'nome': exercise_name,
                        'series': exercise.get('series', 3),
                        'reps': exercise.get('reps', '10-12'),
                        'dia': dia_semana,
                        'tipo': training_type,
                        'gif_url': gif_url,
                        'imagem_exercicio': image_url,
                        'descricao': exercise.get('descricao', '')
                    })

        # Se não gerou exercícios, criar alguns
        if not exercicios:
            default_exercises = [
                {'exercise': 'Flexões', 'series': 4, 'reps': '12-15', 'descricao': 'Peitoral'},
                {'exercise': 'Agachamentos', 'series': 4, 'reps': '15-20', 'descricao': 'Pernas'},
                {'exercise': 'Prancha', 'series': 3, 'reps': '30-60s', 'descricao': 'Core'},
            ]

            for i, exercise in enumerate(default_exercises):
                exercise_name = exercise['exercise']
                gif_url = get_exercise_gif_url(exercise_name)
                image_url = get_training_image_url(exercise_name)

                if user_training_days and i < len(user_training_days):
                    dia = user_training_days[i]
                else:
                    dia = ['Segunda-feira', 'Terça-feira', 'Quarta-feira'][i % 3]

                exercicios.append({
                    'nome': exercise_name,
                    'series': exercise['series'],
                    'reps': exercise['reps'],
                    'dia': dia,
                    'tipo': 'Treino Completo',
                    'gif_url': gif_url,
                    'imagem_exercicio': image_url,
                    'descricao': exercise.get('descricao', '')
                })

        # Buscar agenda
        cur.execute("""
            SELECT a.*, t.nome_treino, t.objetivo_usuario
            FROM agenda a 
            JOIN treino t ON a.id_treino = t.id_treino 
            WHERE a.id_cadastro = %s
            ORDER BY 
                CASE dia_semana
                    WHEN 'Domingo' THEN 1
                    WHEN 'Segunda-feira' THEN 2
                    WHEN 'Terça-feira' THEN 3
                    WHEN 'Quarta-feira' THEN 4
                    WHEN 'Quinta-feira' THEN 5
                    WHEN 'Sexta-feira' THEN 6
                    WHEN 'Sábado' THEN 7
                END,
                horario
        """, (user_id,))

        agenda_results = cur.fetchall()

        # Organizar agenda
        agenda_organizada = {
            'Domingo': [], 'Segunda-feira': [], 'Terça-feira': [],
            'Quarta-feira': [], 'Quinta-feira': [], 'Sexta-feira': [], 'Sábado': []
        }

        for item_result in agenda_results:
            item = processar_resultado(item_result)
            dia = item.get('dia_semana', '')

            if dia in agenda_organizada:
                agenda_organizada[dia].append({
                    'horario': item.get('horario', '--:--'),
                    'treino': item.get('atividade_nome', item.get('nome_treino', 'Treino')),
                    'objetivo': item.get('objetivo_usuario', ''),
                    'icone': 'images/icons_agenda/mdi_dumbbell.svg'
                })

        # Preparar dieta
        dieta = {}
        if api_data and 'nutrition_plan' in api_data and 'sample_menu' in api_data['nutrition_plan']:
            menu = api_data['nutrition_plan']['sample_menu']
            dieta = {
                'cafe_manha': menu.get('breakfast', '3 ovos + pão integral + 1 banana'),
                'lanche_manha': menu.get('snack', 'Iogurte natural + aveia + mel'),
                'almoco': menu.get('lunch', 'Frango + arroz + feijão + salada'),
                'lanche_tarde': menu.get('snack_2', 'Sanduíche natural + fruta'),
                'jantar': menu.get('dinner', 'Peixe + batata doce + legumes'),
                'ceia': menu.get('supper', 'Shake proteico ou chá')
            }
        else:
            objetivo = treino_data.get('objetivo_usuario', 'Ganhar músculo').lower()

            if 'perder' in objetivo:
                dieta = {
                    'cafe_manha': 'Omelete de 2 ovos + 1 fatia pão integral',
                    'lanche_manha': 'Iogurte grego natural + 5 morangos',
                    'almoco': '150g frango grelhado + 100g arroz integral + salada',
                    'lanche_tarde': '1 maçã + 10 amêndoas',
                    'jantar': '150g peixe + legumes no vapor',
                    'ceia': 'Chá verde'
                }
            else:
                dieta = {
                    'cafe_manha': '3 ovos + pão integral + 1 banana',
                    'lanche_manha': 'Iogurte natural + aveia + mel',
                    'almoco': 'Frango + arroz + feijão + salada',
                    'lanche_tarde': 'Sanduíche natural + fruta',
                    'jantar': 'Peixe + batata doce + legumes',
                    'ceia': 'Shake proteico ou chá'
                }

        # Gerar imagens de comida
        food_images = {}
        for key, value in dieta.items():
            food_images[key] = get_food_image_url(value)  # Use a função ORIGINAL

        # Fechar conexões
        cur.close()
        conn.close()

        # Renderizar template
        return render_template('all_my_training.html',
                               treino=treino_data,
                               exercicios=exercicios,
                               agenda=agenda_organizada,
                               dieta=dieta,
                               food_images=food_images,
                               api_data=api_data,
                               user_nome=usuario_data.get('nome_usuario', 'Usuário')
                               )

    except Exception as e:
        print(f"Erro em all_my_training: {str(e)}")
        import traceback
        traceback.print_exc()

        try:
            cur.close()
            conn.close()
        except:
            pass

        return render_template('all_my_training.html',
                               error=f"Erro ao carregar dados: {str(e)[:100]}"
                               )


def get_icon_for_agenda(nome_atividade, objetivo):
    """Retorna ícone para agenda"""
    nome_lower = nome_atividade.lower() if nome_atividade else ''
    objetivo_lower = objetivo.lower() if objetivo else ''

    if any(word in nome_lower for word in ['dieta', 'refeição', 'alimentação', 'comida']):
        return 'images/icons_agenda/mdi_food.svg'
    elif any(word in nome_lower for word in ['descanso', 'recuperação', 'sono']):
        return 'images/icons_agenda/mdi_sleep.svg'
    elif any(word in nome_lower for word in ['cardio', 'corrida', 'aeróbico']):
        return 'images/icons_agenda/mdi_cardio.svg'
    else:
        return 'images/icons_agenda/mdi_dumbbell.svg'


def gerar_dados_padrao(fitness_data):
    """Gera dados padrão se a API falhar"""
    return {
        "user": fitness_data,
        "assessment": {
            "BMI": 22.5,
            "BMI_category": "Normal",
            "BMR_kcal": 1800,
            "TDEE_kcal": 2200,
            "recommended_calories_kcal": 2000,
            "macros": {
                "protein_g": 150,
                "fat_g": 67,
                "carbs_g": 200
            }
        },
        "exercise_plan": {
            "frequency_per_week": 4,
            "type": "Treino Padrão",
            "plan": {
                "Upper A": [
                    {"exercise": "Flexões tradicionais", "series": 4, "reps": "12-15", "descricao": "Peitoral"},
                    {"exercise": "Remada curvada", "series": 4, "reps": "10-12", "descricao": "Costas"},
                    {"exercise": "Rosca bíceps", "series": 3, "reps": "12-15", "descricao": "Braços"}
                ],
                "Lower A": [
                    {"exercise": "Agachamento livre", "series": 4, "reps": "15-20", "descricao": "Pernas"},
                    {"exercise": "Afundo", "series": 3, "reps": "10-12 por perna", "descricao": "Pernas unilateral"},
                    {"exercise": "Prancha", "series": 3, "reps": "30-60s", "descricao": "Core"}
                ]
            }
        },
        "nutrition_plan": {
            "calories_target_kcal": 2000,
            "macros": {
                "protein_g": 150,
                "fat_g": 67,
                "carbs_g": 200
            },
            "sample_menu": {
                "breakfast": "3 ovos + pão integral + 1 banana",
                "snack": "Iogurte natural + aveia + mel",
                "lunch": "Frango + arroz + feijão + salada",
                "snack_2": "Sanduíche natural + fruta",
                "dinner": "Peixe + batata doce + legumes"
            }
        }
    }

# from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
# import requests
# from database import get_db_connection, get_db_cursor
# import json
# from datetime import datetime
# import random
# import os
# import re
#
# bp = Blueprint('treino', __name__)
#
# GENDER_API_URL = "https://api.genderize.io"
# PEXELS_API_KEY = "xd2Cdf7h2R46Ye7yIJoDm5smxa4HNF0wcu4VaVeHRx3da0xbu5etPnK5"
#
#
# # ========== FUNÇÃO PARA MAPEAR EXERCÍCIOS PARA GIFs ==========
#
# def get_exercise_gif_url(exercise_name):
#     """Retorna URL do GIF do exercício baseado no nome - VERSÃO CORRIGIDA"""
#     try:
#         exercise_lower = exercise_name.lower().strip()
#
#         # Primeiro, verificar se é uma URL completa (do Pexels)
#         if exercise_lower.startswith('http'):
#             return exercise_lower
#
#         # Mapeamento detalhado de exercícios para GIFs disponíveis
#         gif_mapping = {
#             # Agachamentos
#             'agachamento': 'Agachamento_livre.gif',
#             'squat': 'Agachamento_livre.gif',
#             'agachamento livre': 'Agachamento_livre.gif',
#             'agachamento com mochila': 'Agachamento_livre.gif',
#             'agachamento frontal': 'agachamento-frontal-com-barra.gif',
#             'agachamento sumo': 'agachamento-sumo-sem-halter.gif',
#             'agachamento búlgaro': 'agachamento-bulgaro.gif',
#             'agachamento smith': 'Agachamento_no_smith.gif',
#             'agachamento pistol': 'Agachamento_pistol_assistido.gif',
#
#             # Flexões
#             'flexão': 'Flexão_tradicional.gif',
#             'flexões': 'Flexão_tradicional.gif',
#             'push-up': 'Flexão_tradicional.gif',
#             'push up': 'Flexão_tradicional.gif',
#             'flexão tradicional': 'Flexão_tradicional.gif',
#             'flexão com pés elevados': 'Flexão_tradicional.gif',
#             'flexão diamante': 'flexao-de-bracos-diamante.gif',
#             'flexão inclinada': 'flexao-de-bracos-inclinada.gif',
#             'flexão aberta': 'Flexão_aberta.gif',
#             'pike push-up': 'Pike-Push-up.gif',
#             'shoulder tap': 'Shoulder-Tap-Push-up.gif',
#
#             # Remadas
#             'remada': 'Remada_curvada_com_barra.gif',
#             'remada curvada': 'Remada_curvada_com_barra.gif',
#             'remada alta': 'Remada_alta.gif',
#             'remada baixa': 'Remada_baixa.gif',
#             'remada unilateral': 'Remada_unilateral_com_halter.gif',
#             'remada cavalinho': 'Remada_cavalinho.gif',
#             'puxada': 'Puxada_na_frente_pulldown.gif',
#             'puxada frente': 'Puxada_na_frente_pulldown.gif',
#             'puxada atrás': 'Puxada_atras.gif',
#             'remada com elástico': 'remada-de-costas-com-elastico-em-pe.gif',
#             'remada invertida': 'remada-invertida-na-mesa.gif',
#
#             # Supinos
#             'supino': 'Supino_reto_com_barra.gif',
#             'supino reto': 'Supino_reto_com_barra.gif',
#             'supino inclinado': 'supino-inclinado-com-barra.gif',
#             'supino declínio': 'Supino_decimalo.gif',
#             'supino fechado': 'Supino_fechado.gif',
#             'chest press': 'Chest_press_na_máquina.gif',
#
#             # Desenvolvimento
#             'desenvolvimento': 'Desenvolvimento_com_barra.gif',
#             'shoulder press': 'Desenvolvimento_com_barra.gif',
#             'arnold press': 'Arnold-Press.gif',
#             'elevação lateral': 'Elevacao_lateral.gif',
#             'elevação frontal': 'Elevacao_frontal.gif',
#             'elevação lateral inclinada': 'Elevacao_lateral_inclinada.gif',
#
#             # Rosca
#             'rosca': 'Rosca_direta_barra.gif',
#             'rosca direta': 'Rosca_direta_barra.gif',
#             'rosca alternada': 'Rosca-Alternada-com-Halteres.gif',
#             'rosca scott': 'Rosca_Scott_barra.gif',
#             'rosca martelo': 'Rosca_martelo.gif',
#             'rosca concentrada': 'Rosca_concentrada.gif',
#             'rosca inversa': 'Rosca_inversa.gif',
#             'bíceps': 'Rosca_direta_barra.gif',
#             'rosca bíceps': 'Rosca_direta_barra.gif',
#
#             # Tríceps
#             'tríceps': 'Triceps_testa.gif',
#             'tríceps testa': 'Triceps_testa.gif',
#             'tríceps corda': 'Triceps_corda.gif',
#             'tríceps pulley': 'Triceps_pulley.gif',
#             'tríceps no banco': 'triceps-no-banco.gif',
#             'tríceps kickback': 'Triceps_kickback.gif',
#
#             # Abdominais
#             'abdominal': 'Abdominal_tradicional.gif',
#             'abdominais': 'Abdominal_tradicional.gif',
#             'crunch': 'Crunch_no_cabo.gif',
#             'abdominal bicicleta': 'abdominal-bicicleta.gif',
#             'abdominal infra': 'abdominal-infra-inferior.gif',
#             'abdominal suspenso': 'Abdominal-infra-suspenso-na-barra.gif',
#             'abdominal oblíquo': 'Abdominal_oblíquo_na_polia.gif',
#             'hollow body': 'Hollow_body_hold.gif',
#
#             # Pranchas
#             'prancha': 'prancha-frontal-tradicional-com-bracos-esticados.gif',
#             'prancha frontal': 'prancha-frontal-tradicional-com-bracos-esticados.gif',
#             'prancha lateral': 'prancha-lateral.gif',
#             'prancha abdominal': 'Prancha-abdominal-Ponte-ventral.gif',
#
#             # Pernas
#             'leg press': 'Leg_press.gif',
#             'cadeira extensora': 'cadeira-extensora.gif',
#             'cadeira flexora': 'cadeira-flexora.gif',
#             'mesa flexora': 'Mesa_flexora.gif',
#             'stiff': 'Stiff_com_barra.gif',
#             'levantamento terra': 'Levantamento_terra.gif',
#             'levantamento terra romeno': 'Levantamento_terra_romeno.gif',
#             'afundo': 'afundo-exercicio.gif',
#             'avanço': 'Passada.gif',
#             'passada': 'Passada.gif',
#             'panturrilha': 'Elevacao_de_panturilha_em_pe.gif',
#             'panturrilha sentado': 'Elevacao_de_panturilha_sentado.gif',
#
#             # Glúteos
#             'glúteo': 'ponte-para-gluteos.gif',
#             'ponte glúteo': 'ponte-para-gluteos.gif',
#             'ponte unilateral': 'Ponte_unilateral.gif',
#             'coice': 'coice-no-cabo.gif',
#             'glúteo no cabo': 'Glúteo_no_cabo.gif',
#             'donkey kicks': 'Donkey-Kicks.gif',
#             'fire hydrants': 'Fire_hydrants.gif',
#
#             # Costas
#             'barra fixa': 'Barra_fixa_fechada.gif',
#             'pull-up': 'barra_fixa_pegada_aberta.gif',
#             'chin-up': 'Barra_fixa_fechada.gif',
#             'pull over': 'Pull-over_na_maquina.gif',
#             'crucifixo': 'Crucifixo_com_halteres_reto.gif',
#             'crucifixo invertido': 'Crucifixo_invertido.gif',
#
#             # Cardio
#             'burpee': 'Burpees.gif',
#             'burpees': 'Burpees.gif',
#             'mountain climbers': 'Mountain_climbers.gif',
#             'salto': 'Salto_vertical.gif',
#             'corrida': 'corrida.gif',
#             'polichinelo': 'Jumping-Jacks.gif',
#             'jumping jacks': 'Jumping-Jacks.gif',
#
#             # Máquinas
#             'peck deck': 'Peck_deck.gif',
#             'kickback máquina': 'Kickback_na_máquina.gif',
#             'cadeira adutora': 'Cadeira_adutora.gif',
#             'abdução': 'abducao-de-pernas-na-maquina-com-cabos.gif',
#             'mergulho': 'Mergulho_nas_paralelas.gif',
#
#             # Outros
#             'superman': 'Superman-exercise.gif',
#             'elevação de pernas': 'Elevacao_de_pernas.gif',
#         }
#
#         # Procurar por correspondências exatas primeiro
#         for key, gif_filename in gif_mapping.items():
#             if key in exercise_lower:
#                 # Verificar se o GIF existe
#                 gif_path = os.path.join('static', 'images', 'gifs', gif_filename)
#                 if os.path.exists(gif_path):
#                     return f"images/gifs/{gif_filename}"
#                 else:
#                     print(f"GIF não encontrado: {gif_filename} em {gif_path}")
#
#         # Se não encontrar correspondência exata, buscar por palavras-chave
#         if any(word in exercise_lower for word in ['peito', 'chest', 'supino', 'flexão']):
#             return 'images/gifs/Flexão_tradicional.gif'
#         elif any(word in exercise_lower for word in ['costas', 'back', 'remada', 'puxada']):
#             return 'images/gifs/Remada_curvada_com_barra.gif'
#         elif any(word in exercise_lower for word in ['ombro', 'shoulder', 'desenvolvimento']):
#             return 'images/gifs/Desenvolvimento_com_barra.gif'
#         elif any(word in exercise_lower for word in ['braço', 'arm', 'rosca', 'bíceps']):
#             return 'images/gifs/Rosca_direta_barra.gif'
#         elif any(word in exercise_lower for word in ['tríceps', 'tricep']):
#             return 'images/gifs/Triceps_testa.gif'
#         elif any(word in exercise_lower for word in ['perna', 'leg', 'agachamento', 'squat']):
#             return 'images/gifs/Agachamento_livre.gif'
#         elif any(word in exercise_lower for word in ['glúteo', 'glute', 'quadril']):
#             return 'images/gifs/ponte-para-gluteos.gif'
#         elif any(word in exercise_lower for word in ['abdomen', 'core', 'abdominal']):
#             return 'images/gifs/Abdominal_tradicional.gif'
#         elif any(word in exercise_lower for word in ['cardio', 'aeróbico']):
#             return 'images/gifs/Burpees.gif'
#
#         # Fallback
#         return 'images/gifs/default_exercise.gif'
#
#     except Exception as e:
#         print(f"Erro ao buscar GIF do exercício '{exercise_name}': {e}")
#         return 'images/gifs/default_exercise.gif'
#
#
# # ========== FUNÇÃO PARA IMAGENS DE EXERCÍCIOS NO PEXELS ==========
#
# def get_training_image_url(exercise_name):
#     """Busca imagem de treino na API do Pexels - VERSÃO CORRIGIDA"""
#     try:
#         # Se já é uma URL completa (do Pexels), retornar diretamente
#         if isinstance(exercise_name, str) and exercise_name.startswith('http'):
#             return exercise_name
#
#         exercise_lower = exercise_name.lower() if isinstance(exercise_name, str) else ''
#
#         # Mapeamento de termos de busca
#         search_terms = {
#             'agachamento': 'squat exercise gym',
#             'flexão': 'push up workout',
#             'supino': 'bench press weightlifting',
#             'remada': 'rowing exercise back',
#             'puxada': 'pull up bar',
#             'rosca': 'bicep curl arm',
#             'tríceps': 'tricep exercise',
#             'prancha': 'plank exercise',
#             'abdominal': 'abdominal crunch',
#             'leg press': 'leg press machine',
#             'desenvolvimento': 'shoulder press gym',
#             'barra fixa': 'pull up exercise',
#             'avanço': 'lunge exercise',
#             'panturrilha': 'calf raise',
#             'glúteo': 'glute workout',
#             'cardio': 'cardio workout',
#             'corrida': 'running exercise',
#             'burpee': 'burpee exercise'
#         }
#
#         search_term = 'fitness workout gym'
#         for key, term in search_terms.items():
#             if key in exercise_lower:
#                 search_term = term
#                 break
#
#         # Buscar no Pexels
#         headers = {'Authorization': PEXELS_API_KEY}
#         params = {
#             'query': search_term,
#             'per_page': 1,
#             'orientation': 'portrait'
#         }
#
#         response = requests.get(
#             'https://api.pexels.com/v1/search',
#             headers=headers,
#             params=params,
#             timeout=5
#         )
#
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('photos') and len(data['photos']) > 0:
#                 return data['photos'][0]['src']['medium']
#
#         # Fallback para imagem local
#         return get_local_exercise_image(exercise_name)
#
#     except Exception as e:
#         print(f"Erro ao buscar imagem Pexels para '{exercise_name}': {e}")
#         return get_local_exercise_image(exercise_name)
#
#
# def get_local_exercise_image(exercise_name):
#     """Retorna imagem local como fallback"""
#     try:
#         if not isinstance(exercise_name, str):
#             return 'images/exercise_images/default_exercise.jpg'
#
#         exercise_lower = exercise_name.lower()
#
#         if any(word in exercise_lower for word in ['flexão', 'push', 'peito', 'supino']):
#             return 'images/exercise_images/pushup_exercise.jpg'
#         elif any(word in exercise_lower for word in ['agachamento', 'squat', 'perna', 'leg press']):
#             return 'images/exercise_images/squat_exercise.jpg'
#         elif any(word in exercise_lower for word in ['barra fixa', 'pull', 'costas', 'remada']):
#             return 'images/exercise_images/pullup_exercise.jpg'
#         elif any(word in exercise_lower for word in ['abdominal', 'crunch', 'core', 'prancha']):
#             return 'images/exercise_images/crunch_exercise.jpg'
#         elif any(word in exercise_lower for word in ['corrida', 'run', 'cardio', 'burpee']):
#             return 'images/exercise_images/running_exercise.jpg'
#         elif any(word in exercise_lower for word in ['rosca', 'bíceps']):
#             return 'images/exercise_images/curl_exercise.jpg'
#         elif any(word in exercise_lower for word in ['tríceps']):
#             return 'images/exercise_images/tricep_exercise.jpg'
#         elif any(word in exercise_lower for word in ['desenvolvimento', 'ombro']):
#             return 'images/exercise_images/shoulder_exercise.jpg'
#         else:
#             return 'images/exercise_images/default_exercise.jpg'
#     except:
#         return 'images/exercise_images/default_exercise.jpg'
#
#
# # ========== FUNÇÃO PARA IMAGENS DE COMIDA NO PEXELS ==========
#
# def get_food_image_url(meal_description):
#     """Busca imagem de comida na API do Pexels - VERSÃO CORRIGIDA"""
#     try:
#         if not isinstance(meal_description, str):
#             return 'images/food_images/default_food.jpg'
#
#         meal_lower = meal_description.lower()
#
#         # Mapeamento para termos de busca
#         search_mapping = {
#             'ovo': 'egg breakfast healthy',
#             'pão': 'whole wheat bread breakfast',
#             'banana': 'banana fruit healthy',
#             'iogurte': 'yogurt with fruits',
#             'aveia': 'oatmeal breakfast',
#             'mel': 'honey natural',
#             'frango': 'grilled chicken healthy',
#             'arroz': 'rice healthy food',
#             'feijão': 'beans healthy',
#             'salada': 'fresh salad vegetables',
#             'sanduíche': 'healthy sandwich',
#             'fruta': 'fresh fruits healthy',
#             'peixe': 'grilled fish healthy',
#             'batata doce': 'sweet potato healthy',
#             'legumes': 'steamed vegetables',
#             'shake': 'protein shake fitness',
#             'proteico': 'protein food',
#             'carne': 'lean meat healthy',
#             'queijo': 'cheese healthy'
#         }
#
#         search_term = 'healthy food nutrition'
#         for key, term in search_mapping.items():
#             if key in meal_lower:
#                 search_term = term
#                 break
#
#         # Buscar no Pexels
#         headers = {'Authorization': PEXELS_API_KEY}
#         params = {
#             'query': search_term,
#             'per_page': 1,
#             'orientation': 'square'
#         }
#
#         response = requests.get(
#             'https://api.pexels.com/v1/search',
#             headers=headers,
#             params=params,
#             timeout=5
#         )
#
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('photos') and len(data['photos']) > 0:
#                 # Salvar a URL para uso futuro
#                 return data['photos'][0]['src']['medium']
#
#         # Fallback para imagem local
#         return get_local_food_image(meal_description)
#
#     except Exception as e:
#         print(f"Erro ao buscar imagem de comida: {e}")
#         return get_local_food_image(meal_description)
#
#
# def get_local_food_image(meal_description):
#     """Retorna imagem local como fallback"""
#     try:
#         if not isinstance(meal_description, str):
#             return 'images/food_images/default_food.jpg'
#
#         meal_lower = meal_description.lower()
#
#         # Verificar se arquivos locais existem
#         image_files = {
#             'ovo': 'breakfast_eggs.jpg',
#             'pão': 'breakfast_eggs.jpg',
#             'banana': 'breakfast_eggs.jpg',
#             'iogurte': 'snack_yogurt.jpg',
#             'aveia': 'snack_yogurt.jpg',
#             'frango': 'lunch_chicken.jpg',
#             'arroz': 'lunch_chicken.jpg',
#             'feijão': 'lunch_chicken.jpg',
#             'salada': 'lunch_chicken.jpg',
#             'sanduíche': 'snack_sandwich.jpg',
#             'fruta': 'snack_sandwich.jpg',
#             'peixe': 'dinner_fish.jpg',
#             'batata': 'dinner_fish.jpg',
#             'legumes': 'dinner_fish.jpg',
#             'shake': 'supper_shake.jpg',
#             'proteico': 'supper_shake.jpg'
#         }
#
#         for key, filename in image_files.items():
#             if key in meal_lower:
#                 # Verificar se o arquivo existe
#                 filepath = os.path.join('static', 'images', 'food_images', filename)
#                 if os.path.exists(filepath):
#                     return f"images/food_images/{filename}"
#
#         return 'images/food_images/default_food.jpg'
#     except:
#         return 'images/food_images/default_food.jpg'
#
#
# # ========== FUNÇÕES AUXILIARES ==========
#
# # def processar_resultado(resultado):
# #     """Processa resultado do banco, retornando dicionário"""
# #     if resultado is None:
# #         return None
# #
# #     if isinstance(resultado, dict):
# #         return resultado
# #     elif isinstance(resultado, tuple):
# #         if len(resultado) >= 2:
# #             return {
# #                 'data_nascimento': resultado[0],
# #                 'nome_usuario': resultado[1]
# #             }
# #         else:
# #             return {f'coluna_{i}': valor for i, valor in enumerate(resultado)}
# #     else:
# #         return resultado
#
#
# def get_gender_by_name(nome):
#     try:
#         if not isinstance(nome, str):
#             return 'male'
#         primeiro_nome = nome.split()[0].lower()
#         response = requests.get(f"{GENDER_API_URL}?name={primeiro_nome}", timeout=3)
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('probability', 0) > 0.6:
#                 return data.get('gender', 'male')
#         return 'male'
#     except:
#         return 'male'
#
#
# def generate_food_images(dieta):
#     """Gera URLs de imagens para todas as refeições da dieta"""
#     food_images = {}
#
#     if isinstance(dieta, dict):
#         meal_order = ['cafe_manha', 'lanche_manha', 'almoco', 'lanche_tarde', 'jantar', 'ceia']
#
#         for meal_type in meal_order:
#             if meal_type in dieta and isinstance(dieta[meal_type], str):
#                 food_images[meal_type] = get_food_image_url(dieta[meal_type])
#
#     return food_images
#
#
# # ========== ROTA PRINCIPAL ALL_MY_TRAINING - VERSÃO CORRIGIDA ==========
#
# @bp.route('/all_my_training')
# def all_my_training():
#     if 'user_id' not in session:
#         return redirect('/login')
#
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         # Buscar treino mais recente
#         cur.execute("""
#             SELECT t.*
#             FROM treino t
#             WHERE t.id_cadastro = %s
#             ORDER BY t.id_treino DESC
#             LIMIT 1
#         """, (user_id,))
#         treino_result = cur.fetchone()
#         treino_data = processar_resultado(treino_result)
#
#         if not treino_data:
#             return redirect('/my_level')
#
#         # Buscar dados do usuário
#         cur.execute("""
#             SELECT data_nascimento, nome_usuario
#             FROM cadastrousuarios
#             WHERE id_cadastro = %s
#         """, (user_id,))
#         usuario_result = cur.fetchone()
#         usuario_data = processar_resultado(usuario_result)
#
#         if not usuario_data:
#             return render_template('all_my_training.html',
#                                    treino=None,
#                                    exercicios=[],
#                                    agenda={},
#                                    dieta={},
#                                    food_images={},
#                                    genero='male',
#                                    error="Dados do usuário não encontrados")
#
#         # Buscar agenda
#         cur.execute("""
#             SELECT a.*, t.nome_treino, t.objetivo_usuario
#             FROM agenda a
#             JOIN treino t ON a.id_treino = t.id_treino
#             WHERE a.id_cadastro = %s
#             ORDER BY
#                 CASE dia_semana
#                     WHEN 'Domingo' THEN 1
#                     WHEN 'Segunda-feira' THEN 2
#                     WHEN 'Terça-feira' THEN 3
#                     WHEN 'Quarta-feira' THEN 4
#                     WHEN 'Quinta-feira' THEN 5
#                     WHEN 'Sexta-feira' THEN 6
#                     WHEN 'Sábado' THEN 7
#                 END,
#                 horario
#         """, (user_id,))
#         agenda_results = cur.fetchall()
#
#         # Buscar dias de treino
#         cur.execute("""
#             SELECT DISTINCT dia_semana
#             FROM agenda
#             WHERE id_cadastro = %s
#         """, (user_id,))
#         dias_result = cur.fetchall()
#
#         cur.close()
#         conn.close()
#
#         # Processar dias de treino
#         user_training_days_raw = []
#         for dia_result in dias_result:
#             dia_data = processar_resultado(dia_result)
#             if isinstance(dia_data, dict):
#                 user_training_days_raw.append(dia_data['dia_semana'])
#             else:
#                 user_training_days_raw.append(dia_data[0])
#
#         # Ordenar dias
#         day_order = {
#             'Domingo': 1, 'Segunda-feira': 2, 'Terça-feira': 3,
#             'Quarta-feira': 4, 'Quinta-feira': 5, 'Sexta-feira': 6, 'Sábado': 7
#         }
#         user_training_days = sorted(user_training_days_raw, key=lambda x: day_order.get(x, 99))
#
#         # Calcular idade
#         data_nascimento = usuario_data['data_nascimento']
#         idade = datetime.now().year - data_nascimento.year
#         hoje = datetime.now()
#         if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
#             idade -= 1
#
#         # Identificar gênero
#         genero = get_gender_by_name(usuario_data['nome_usuario'])
#
#         # Obter valores do treino
#         altura_usuario = treino_data.get('altura_usuario', 1.70)
#         peso_usuario = treino_data.get('peso_usuario', 70.0)
#         experiencia = treino_data.get('qtn_tempo_pratica_exercicios', 'a mais de 1 ano')
#         objetivo = treino_data.get('objetivo_usuario', 'Ganhar músculo')
#
#         # Converter valores
#         try:
#             altura_float = round(float(str(altura_usuario).replace(',', '.')), 2)
#         except:
#             altura_float = 1.70
#
#         try:
#             peso_float = round(float(str(peso_usuario).replace(',', '.')), 1)
#         except:
#             peso_float = 70.0
#
#         # Preparar dados para API local
#         fitness_data = {
#             "name": usuario_data['nome_usuario'],
#             "age": idade,
#             "sex": genero,
#             "height_cm": round(altura_float * 100, 2),
#             "weight_kg": peso_float,
#             "experience": experiencia,
#             "goal": objetivo,
#             "access": "casa"
#         }
#
#         # Chamar API local
#         api_data = chamar_api_fitness_local(fitness_data)
#
#         # Preparar exercícios
#         exercicios = []
#
#         if api_data and 'exercise_plan' in api_data and 'plan' in api_data['exercise_plan']:
#             treino_plan = api_data['exercise_plan']['plan']
#
#             # Contar total de exercícios
#             total_exercicios = sum(len(exercises) for exercises in treino_plan.values())
#
#             print(f"Total de exercícios no plano: {total_exercicios}")
#
#             # Mapear tipos de treino para dias da semana reais
#             training_types = list(treino_plan.keys())
#             day_counter = 0
#
#             for training_type in training_types:
#                 for exercise in treino_plan[training_type]:
#                     gif_url = get_exercise_gif_url(exercise['exercise'])
#                     image_url = get_training_image_url(exercise['exercise'])
#
#                     # Determinar dia da semana
#                     if user_training_days and day_counter < len(user_training_days):
#                         dia_semana = user_training_days[day_counter]
#                         day_counter += 1
#                     else:
#                         # Mapeamento padrão
#                         type_to_day = {
#                             'Upper A': 'Segunda-feira',
#                             'Lower A': 'Terça-feira',
#                             'Full Body': 'Quarta-feira',
#                             'Core & Cardio': 'Quinta-feira',
#                             'Pernas & Glúteos': 'Sexta-feira',
#                             'Peito & Tríceps': 'Segunda-feira',
#                             'Costas & Bíceps': 'Terça-feira',
#                             'Ombros & Trapézio': 'Quarta-feira'
#                         }
#                         dia_semana = type_to_day.get(training_type, training_type)
#
#                     exercicios.append({
#                         'nome': exercise['exercise'],
#                         'series': exercise.get('series', 3),
#                         'reps': exercise.get('reps', '10-12'),
#                         'dia': dia_semana,
#                         'tipo': training_type,
#                         'gif_url': gif_url,
#                         'imagem_exercicio': image_url,
#                         'descricao': exercise.get('descricao', '')
#                     })
#         # exercicios = []
#         #
#         # if api_data and 'exercise_plan' in api_data and 'plan' in api_data['exercise_plan']:
#         #     day_counter = 0
#         #     for training_type, exercises in api_data['exercise_plan']['plan'].items():
#         #         for exercise in exercises:
#         #             # Obter GIF e imagem
#         #             gif_url = get_exercise_gif_url(exercise['exercise'])
#         #             image_url = get_training_image_url(exercise['exercise'])
#         #
#         #             # Determinar dia
#         #             if user_training_days and day_counter < len(user_training_days):
#         #                 dia_semana = user_training_days[day_counter]
#         #                 day_counter += 1
#         #             else:
#         #                 training_type_to_day = {
#         #                     'Upper A': 'Segunda-feira',
#         #                     'Lower A': 'Terça-feira',
#         #                     'Upper B': 'Quarta-feira',
#         #                     'Lower B': 'Quinta-feira',
#         #                     'Core & Cardio': 'Sexta-feira'
#         #                 }
#         #                 dia_semana = training_type_to_day.get(training_type, 'Ainda não definido')
#         #
#         #             exercicios.append({
#         #                 'nome': exercise['exercise'],
#         #                 'series': exercise.get('series', 3),
#         #                 'reps': exercise.get('reps', '10-12'),
#         #                 'dia': dia_semana,
#         #                 'gif_url': gif_url,
#         #                 'imagem_exercicio': image_url
#         #             })
#         else:
#             # Exercícios padrão
#             default_exercises = [
#                 {'exercise': 'Flexões', 'series': 4, 'reps': '10-12'},
#                 {'exercise': 'Agachamentos', 'series': 4, 'reps': '12-15'},
#                 {'exercise': 'Prancha', 'series': 3, 'reps': '30-60 segundos'}
#             ]
#
#             for i, exercise in enumerate(default_exercises):
#                 if i < len(user_training_days):
#                     dia = user_training_days[i]
#                 else:
#                     dia = ['Segunda-feira', 'Quarta-feira', 'Sexta-feira'][i] if i < 3 else 'Ainda não definido'
#
#                 gif_url = get_exercise_gif_url(exercise['exercise'])
#                 image_url = get_training_image_url(exercise['exercise'])
#
#                 exercicios.append({
#                     'nome': exercise['exercise'],
#                     'series': exercise['series'],
#                     'reps': exercise['reps'],
#                     'dia': dia,
#                     'gif_url': gif_url,
#                     'imagem_exercicio': image_url
#                 })
#
#         # Organizar agenda
#         agenda_organizada = {
#             'Domingo': [], 'Segunda-feira': [], 'Terça-feira': [],
#             'Quarta-feira': [], 'Quinta-feira': [], 'Sexta-feira': [], 'Sábado': []
#         }
#
#         for item_result in agenda_results:
#             item = processar_resultado(item_result)
#             dia = item.get('dia_semana', '')
#
#             if dia in agenda_organizada:
#                 agenda_organizada[dia].append({
#                     'horario': item.get('horario', '--:--'),
#                     'treino': item.get('nome_treino', 'Treino'),
#                     'objetivo': item.get('objetivo_usuario', ''),
#                     'icone': f"images/icons_agenda/mdi_dumbbell.svg"
#                 })
#
#         # Preparar dieta
#         dieta = {}
#         if api_data and 'nutrition_plan' in api_data and 'sample_menu' in api_data['nutrition_plan']:
#             menu = api_data['nutrition_plan']['sample_menu']
#             dieta = {
#                 'cafe_manha': menu.get('breakfast', '3 ovos + pão integral + 1 banana'),
#                 'lanche_manha': menu.get('snack', 'Iogurte natural + aveia + mel'),
#                 'almoco': menu.get('lunch', 'Frango + arroz + feijão + salada'),
#                 'lanche_tarde': menu.get('snack_2', 'Sanduíche natural + fruta'),
#                 'jantar': menu.get('dinner', 'Peixe + batata doce + legumes'),
#                 'ceia': 'Shake proteico ou chá'
#             }
#         else:
#             dieta = {
#                 'cafe_manha': '3 ovos + pão integral + 1 banana',
#                 'lanche_manha': 'Iogurte natural + aveia + mel',
#                 'almoco': 'Frango + arroz + feijão + salada',
#                 'lanche_tarde': 'Sanduíche natural + fruta',
#                 'jantar': 'Peixe + batata doce + legumes',
#                 'ceia': 'Shake proteico ou chá'
#             }
#
#         # Gerar imagens de comida
#         food_images = generate_food_images(dieta)
#
#         # Calcular estatísticas
#         total_atividades = sum(len(atividades) for atividades in agenda_organizada.values())
#         dias_com_atividade = sum(1 for atividades in agenda_organizada.values() if len(atividades) > 0)
#
#         # Preparar dados para template
#         meal_types = {
#             'cafe_manha': 'Café da manhã',
#             'lanche_manha': 'Lanche da manhã',
#             'almoco': 'Almoço',
#             'lanche_tarde': 'Lanche da tarde',
#             'jantar': 'Jantar',
#             'ceia': 'Ceia'
#         }
#
#         meal_times = {
#             'cafe_manha': '6:00 AM',
#             'lanche_manha': '10:00 AM',
#             'almoco': '12:00 PM',
#             'lanche_tarde': '16:00 PM',
#             'jantar': '19:00 PM',
#             'ceia': '21:00 PM'
#         }
#
#         assessment_data = api_data.get('assessment', {}) if api_data else {}
#
#         return render_template('all_my_training.html',
#                                treino=treino_data,
#                                exercicios=exercicios,
#                                agenda=agenda_organizada,
#                                dieta=dieta,
#                                food_images=food_images,
#                                api_data=api_data,
#                                genero=genero,
#                                user_training_days=user_training_days,
#                                meal_types=meal_types,
#                                meal_times=meal_times,
#                                total_atividades=total_atividades,
#                                dias_com_atividade=dias_com_atividade,
#                                assessment_data=assessment_data)
#
#     except Exception as e:
#         print(f"Erro em all_my_training: {str(e)}")
#         import traceback
#         traceback.print_exc()
#
#         try:
#             cur.close()
#             conn.close()
#         except:
#             pass
#
#         return render_template('all_my_training.html',
#                                treino=None,
#                                exercicios=[],
#                                agenda={},
#                                dieta={},
#                                food_images={},
#                                genero='male',
#                                meal_types={},
#                                meal_times={},
#                                total_atividades=0,
#                                dias_com_atividade=0,
#                                error=f"Erro ao carregar dados: {str(e)[:100]}")
#
#
# # ========== OUTRAS FUNÇÕES ==========
#
# # def chamar_api_fitness_local(fitness_data):
# #     """Chama a API de fitness localmente"""
# #     try:
# #         # ... (mantenha o código existente da função chamar_api_fitness_local)
# #         # Esta função já está correta no seu arquivo original
# #         pass
# #     except Exception as e:
# #         print(f"Erro ao gerar treino local: {e}")
# #         return None
#
# # No treino.py, substitua a função chamar_api_fitness_local por:
#
# def chamar_api_fitness_local(fitness_data):
#     """API local aprimorada que gera treinos personalizados"""
#     try:
#         name = fitness_data["name"]
#         age = fitness_data["age"]
#         sex = fitness_data["sex"]
#         height_cm = fitness_data["height_cm"]
#         weight_kg = fitness_data["weight_kg"]
#         experience = fitness_data["experience"]
#         goal = fitness_data["goal"]
#         access = fitness_data.get("access", "casa")
#
#         # Importar a nova função de treino personalizado
#         from . import treino_personalizado
#
#         # Gerar treino personalizado
#         treino_completo = treino_personalizado.gerar_treino_completo(
#             idade=age,
#             peso=weight_kg,
#             altura=height_cm / 100,
#             experiencia=experience,
#             objetivo=goal,
#             acesso=access,
#             genero=sex
#         )
#
#         # Gerar dieta personalizada
#         dieta_personalizada = treino_personalizado.gerar_dieta_personalizada(
#             peso=weight_kg,
#             altura=height_cm,
#             idade=age,
#             objetivo=goal,
#             genero=sex,
#             nivel_atividade=experience
#         )
#
#         # ===== Cálculos metabólicos =====
#         altura_m = height_cm / 100
#         bmi = round(weight_kg / (altura_m ** 2), 2)
#
#         if bmi < 18.5:
#             bmi_category = "Abaixo do peso"
#         elif bmi < 25:
#             bmi_category = "Normal"
#         elif bmi < 30:
#             bmi_category = "Sobrepeso"
#         else:
#             bmi_category = "Obesidade"
#
#         # Fórmula de Mifflin–St Jeor
#         if sex == "male":
#             bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
#         else:
#             bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
#
#         # Fator de atividade baseado na experiência
#         factors = {
#             "nunca pratiquei antes": 1.375,
#             "a menos de 1 ano": 1.375,
#             "a mais de 1 ano": 1.55,
#             "a 4 anos": 1.6,
#             "a mais de 5 anos": 1.725
#         }
#         factor = factors.get(experience.lower(), 1.55)
#         tdee = bmr * factor
#
#         # Calorias alvo
#         goal_lower = goal.lower()
#         if "perder" in goal_lower:
#             target_calories = tdee * 0.85
#         elif "ganhar" in goal_lower:
#             target_calories = tdee * 1.1
#         else:
#             target_calories = tdee
#         target_calories = round(target_calories)
#
#         # Macros
#         protein_g = round(2.0 * weight_kg)
#         fat_g = round(0.9 * weight_kg)
#         carbs_g = round((target_calories - (protein_g * 4 + fat_g * 9)) / 4)
#
#         # ===== Montar resposta completa =====
#         result = {
#             "user": {
#                 "name": name,
#                 "age": age,
#                 "sex": sex,
#                 "height_cm": height_cm,
#                 "weight_kg": weight_kg,
#                 "experience": experience,
#                 "goal": goal,
#                 "access": access
#             },
#             "assessment": {
#                 "BMI": bmi,
#                 "BMI_category": bmi_category,
#                 "BMR_kcal": round(bmr, 1),
#                 "TDEE_kcal": round(tdee, 1),
#                 "recommended_calories_kcal": target_calories,
#                 "macros": {
#                     "protein_g": protein_g,
#                     "fat_g": fat_g,
#                     "carbs_g": carbs_g
#                 }
#             },
#             "exercise_plan": {
#                 "frequency_per_week": 4 if "casa" in access.lower() else 5,
#                 "type": "Treino Personalizado Completo",
#                 "plan": treino_completo,  # Agora com múltiplos treinos
#                 "progression": "Aumentar carga semanalmente. Alterar exercícios a cada 6-8 semanas.",
#                 "total_exercises": sum(len(exercises) for exercises in treino_completo.values())
#             },
#             "nutrition_plan": {
#                 "calories_target_kcal": dieta_personalizada["calorias_diarias"],
#                 "macros": dieta_personalizada["macros"],
#                 "sample_menu": dieta_personalizada["refeicoes"],
#                 "emphasis": dieta_personalizada["enfase"]
#             },
#             "recommendations": {
#                 "descanso": "Dormir 7-9 horas por noite",
#                 "hidratacao": "Beber 3-4L de água diariamente",
#                 "suplementacao": "Considerar creatina e whey protein se necessário",
#                 "consistencia": "Manter pelo menos 80% de aderência ao plano"
#             },
#             "notes": f"Plano gerado em {datetime.now().strftime('%d/%m/%Y')}. Personalizado para {name} ({age} anos)."
#         }
#
#         return result
#
#     except Exception as e:
#         print(f"Erro ao gerar treino local: {e}")
#         import traceback
#         traceback.print_exc()
#         return None
#
#
# @bp.route('/api/salvar_treino', methods=['POST'])
# def salvar_treino():
#     """Salva um novo treino no banco de dados"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     try:
#         data = request.get_json()
#         print(f"Dados recebidos: {data}")  # DEBUG
#
#         user_id = session['user_id']
#
#         # Validação dos campos obrigatórios
#         required_fields = ['peso', 'altura', 'experiencia', 'objetivo']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({'error': f'Campo obrigatório faltando: {field}'}), 400
#
#         # Converter valores
#         try:
#             peso_str = str(data['peso']).replace(',', '.')
#             peso_float = float(peso_str)
#         except ValueError:
#             return jsonify({'error': f'Peso inválido: {data["peso"]}. Use números (ex: 75.5 ou 75,5)'}), 400
#
#         try:
#             altura_str = str(data['altura']).replace(',', '.')
#             altura_float = float(altura_str)
#         except ValueError:
#             return jsonify({'error': f'Altura inválida: {data["altura"]}. Use números (ex: 1.75 ou 1,75)'}), 400
#
#         experiencia = data['experiencia']
#         objetivo = data['objetivo']
#         acesso = data.get('acesso', 'casa')
#
#         # Buscar dados do usuário
#         conn = get_db_connection()
#         cur = get_db_cursor(conn)
#
#         try:
#             cur.execute("""
#                 SELECT data_nascimento, nome_usuario
#                 FROM cadastrousuarios
#                 WHERE id_cadastro = %s
#             """, (user_id,))
#
#             resultado = cur.fetchone()
#             if not resultado:
#                 return jsonify({'error': 'Usuário não encontrado no banco de dados'}), 404
#
#             usuario_data = processar_resultado(resultado)
#             data_nascimento = usuario_data['data_nascimento']
#             nome_usuario = usuario_data['nome_usuario']
#
#             # Calcular idade
#             idade = datetime.now().year - data_nascimento.year
#             hoje = datetime.now()
#             if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
#                 idade -= 1
#
#             # Identificar gênero
#             genero = get_gender_by_name(nome_usuario)
#
#             # Preparar dados para a API local
#             fitness_data = {
#                 "name": nome_usuario,
#                 "age": idade,
#                 "sex": genero,
#                 "height_cm": altura_float * 100,
#                 "weight_kg": peso_float,
#                 "experience": experiencia,
#                 "goal": objetivo,
#                 "access": acesso
#             }
#
#             # Chamar API LOCALMENTE
#             treino_info = chamar_api_fitness_local(fitness_data)
#
#             if not treino_info:
#                 print("API local retornou None, usando dados básicos")
#                 # Criar dados básicos se a API falhar
#                 treino_info = {
#                     "exercise_plan": {
#                         "plan": {
#                             "Upper A": [
#                                 {"exercise": "Flexões com pés elevados", "series": 4, "reps": "8–12"},
#                                 {"exercise": "Remada curvada com mochila", "series": 4, "reps": "10–12"}
#                             ]
#                         }
#                     }
#                 }
#
#             # Salvar no banco de dados
#             nome_treino = f"Treino {objetivo} - {datetime.now().strftime('%d/%m/%Y')}"
#
#             cur.execute("""
#                 INSERT INTO treino
#                 (id_cadastro, nome_treino, peso_usuario, altura_usuario, qtn_tempo_pratica_exercicios, objetivo_usuario)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#                 RETURNING id_treino
#             """, (
#                 user_id,
#                 nome_treino,
#                 peso_float,
#                 altura_float,
#                 experiencia,
#                 objetivo
#             ))
#
#             treino_id_result = cur.fetchone()
#             treino_id = treino_id_result['id_treino'] if isinstance(treino_id_result, dict) else treino_id_result[0]
#
#             conn.commit()
#
#             # Log de sucesso
#             print(f"Treino salvo com sucesso! ID: {treino_id}, Usuário: {user_id}")
#
#             # Retornar resposta JSON
#             return jsonify({
#                 'success': True,
#                 'treino_id': treino_id,
#                 'nome_treino': nome_treino,
#                 'treino_info': treino_info,
#                 'genero_identificado': genero,
#                 'idade_calculada': idade,
#                 'dados_processados': {
#                     'altura': altura_float,
#                     'peso': peso_float,
#                     'altura_cm': altura_float * 100
#                 },
#                 'message': 'Treino gerado e salvo com sucesso!'
#             })
#
#         except Exception as e:
#             conn.rollback()
#             print(f"Erro no banco de dados: {str(e)}")
#             import traceback
#             traceback.print_exc()
#             return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500
#
#         finally:
#             try:
#                 cur.close()
#                 conn.close()
#             except:
#                 pass
#
#     except Exception as e:
#         print(f"Erro geral em salvar_treino: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Erro interno: {str(e)}'}), 500
#
#
# def processar_resultado(resultado):
#     """Processa resultado do banco, retornando dicionário"""
#     if resultado is None:
#         return None
#
#     if isinstance(resultado, dict):
#         return resultado
#     elif isinstance(resultado, tuple):
#         # Tentar identificar a estrutura
#         if len(resultado) == 2:
#             # Provavelmente (data_nascimento, nome_usuario)
#             return {
#                 'data_nascimento': resultado[0],
#                 'nome_usuario': resultado[1]
#             }
#         else:
#             # Converter para dicionário genérico
#             return {f'coluna_{i}': valor for i, valor in enumerate(resultado)}
#     else:
#         return resultado
#
#
# # ========== ROTAS ADICIONAIS ==========
#
# @bp.route('/my_level')
# def my_level():
#     if 'user_id' not in session:
#         return redirect('/login')
#     return render_template('my_level.html')
#
#
# @bp.route('/api/treinos_usuario')
# def treinos_usuario():
#     """API para buscar treinos do usuário para o select"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         cur.execute("""
#             SELECT id_treino, nome_treino, objetivo_usuario
#             FROM treino
#             WHERE id_cadastro = %s
#             ORDER BY id_treino DESC
#         """, (user_id,))
#
#         treinos = cur.fetchall()
#
#         treinos_list = []
#         for treino in treinos:
#             treinos_list.append({
#                 'id_treino': treino['id_treino'],
#                 'nome_treino': treino['nome_treino'],
#                 'objetivo_usuario': treino['objetivo_usuario']
#             })
#
#         return jsonify({
#             'success': True,
#             'treinos': treinos_list,
#             'total': len(treinos_list)
#         })
#
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
#     finally:
#         cur.close()
#         conn.close()
#
#
# # No treino.py, adicione estas rotas:
#
# @bp.route('/api/treinos_disponiveis')
# def treinos_disponiveis():
#     """Retorna todos os treinos disponíveis para o usuário selecionar na agenda"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         # Buscar treino atual do usuário
#         cur.execute("""
#             SELECT * FROM treino
#             WHERE id_cadastro = %s
#             ORDER BY id_treino DESC
#             LIMIT 1
#         """, (user_id,))
#
#         treino_atual = cur.fetchone()
#
#         if not treino_atual:
#             return jsonify({'error': 'Crie um treino primeiro'}), 400
#
#         # Buscar dados do usuário para personalização
#         cur.execute("""
#             SELECT nome_usuario, data_nascimento
#             FROM cadastrousuarios
#             WHERE id_cadastro = %s
#         """, (user_id,))
#
#         usuario = cur.fetchone()
#
#         # Processar dados
#         treino_data = processar_resultado(treino_atual)
#         usuario_data = processar_resultado(usuario)
#
#         # Calcular idade
#         data_nascimento = usuario_data['data_nascimento']
#         idade = datetime.now().year - data_nascimento.year
#         hoje = datetime.now()
#         if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
#             idade -= 1
#
#         # Gerar opções de treino baseadas no perfil
#         from . import treino_personalizado
#
#         treinos_opcoes = treino_personalizado.gerar_treino_completo(
#             idade=idade,
#             peso=float(treino_data['peso_usuario']),
#             altura=float(treino_data['altura_usuario']),
#             experiencia=treino_data['qtn_tempo_pratica_exercicios'],
#             objetivo=treino_data['objetivo_usuario'],
#             acesso='academia' if 'academia' in treino_data.get('acesso', '') else 'casa',
#             genero=get_gender_by_name(usuario_data['nome_usuario'])
#         )
#
#         # Formatar para o select da agenda
#         opcoes_formatadas = []
#
#         for tipo_treino, exercicios in treinos_opcoes.items():
#             opcoes_formatadas.append({
#                 'id': f"treino_{tipo_treino.lower().replace(' ', '_')}",
#                 'nome': f"{tipo_treino} - {len(exercicios)} exercícios",
#                 'tipo': tipo_treino,
#                 'descricao': f"Treino de {tipo_treino} com {len(exercicios)} exercícios",
#                 'exercicios': exercicios[:2]  # Mostrar apenas 2 para preview
#             })
#
#         # Adicionar opções de dieta também
#         dietas_opcoes = [
#             {
#                 'id': 'dieta_emagrecimento',
#                 'nome': 'Dieta para Emagrecimento',
#                 'tipo': 'dieta',
#                 'descricao': 'Plano alimentar focado em perda de gordura'
#             },
#             {
#                 'id': 'dieta_hipertrofia',
#                 'nome': 'Dieta para Ganho Muscular',
#                 'tipo': 'dieta',
#                 'descricao': 'Plano alimentar focado em ganho de massa'
#             },
#             {
#                 'id': 'dieta_definicao',
#                 'nome': 'Dieta para Definição',
#                 'tipo': 'dieta',
#                 'descricao': 'Plano alimentar para definição muscular'
#             },
#             {
#                 'id': 'descanso',
#                 'nome': 'Dia de Descanso',
#                 'tipo': 'descanso',
#                 'descricao': 'Dia de recuperação ativa ou total'
#             }
#         ]
#
#         todas_opcoes = opcoes_formatadas + dietas_opcoes
#
#         return jsonify({
#             'success': True,
#             'opcoes': todas_opcoes,
#             'total': len(todas_opcoes),
#             'user_info': {
#                 'nome': usuario_data['nome_usuario'],
#                 'idade': idade,
#                 'objetivo': treino_data['objetivo_usuario']
#             }
#         })
#
#     except Exception as e:
#         print(f"Erro ao buscar treinos disponíveis: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cur.close()
#         conn.close()
#
#
# @bp.route('/api/atualizar_treino', methods=['POST'])
# def atualizar_treino():
#     """Permite ao usuário atualizar seu treino"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     try:
#         data = request.get_json()
#         user_id = session['user_id']
#
#         # Validar dados
#         required = ['peso', 'altura', 'experiencia', 'objetivo']
#         for field in required:
#             if field not in data:
#                 return jsonify({'error': f'Campo obrigatório: {field}'}), 400
#
#         # Converter valores
#         peso = float(str(data['peso']).replace(',', '.'))
#         altura = float(str(data['altura']).replace(',', '.'))
#         experiencia = data['experiencia']
#         objetivo = data['objetivo']
#         acesso = data.get('acesso', 'casa')
#
#         # Buscar dados do usuário
#         conn = get_db_connection()
#         cur = get_db_cursor(conn)
#
#         cur.execute("""
#             SELECT nome_usuario, data_nascimento
#             FROM cadastrousuarios
#             WHERE id_cadastro = %s
#         """, (user_id,))
#
#         usuario = cur.fetchone()
#         nome_usuario = usuario['nome_usuario']
#         data_nascimento = usuario['data_nascimento']
#
#         # Calcular idade
#         idade = datetime.now().year - data_nascimento.year
#         hoje = datetime.now()
#         if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
#             idade -= 1
#
#         # Gerar novo treino personalizado
#         from . import treino_personalizado
#
#         # Preparar dados para API
#         fitness_data = {
#             "name": nome_usuario,
#             "age": idade,
#             "sex": get_gender_by_name(nome_usuario),
#             "height_cm": altura * 100,
#             "weight_kg": peso,
#             "experience": experiencia,
#             "goal": objetivo,
#             "access": acesso
#         }
#
#         # Gerar novo treino
#         novo_treino_info = chamar_api_fitness_local(fitness_data)
#
#         if not novo_treino_info:
#             return jsonify({'error': 'Falha ao gerar novo treino'}), 500
#
#         # Atualizar no banco
#         nome_treino = f"Treino {objetivo} - Atualizado em {datetime.now().strftime('%d/%m/%Y')}"
#
#         cur.execute("""
#             INSERT INTO treino
#             (id_cadastro, nome_treino, peso_usuario, altura_usuario,
#              qtn_tempo_pratica_exercicios, objetivo_usuario)
#             VALUES (%s, %s, %s, %s, %s, %s)
#             RETURNING id_treino
#         """, (
#             user_id,
#             nome_treino,
#             peso,
#             altura,
#             experiencia,
#             objetivo
#         ))
#
#         novo_treino_id = cur.fetchone()['id_treino']
#         conn.commit()
#
#         # Limpar agenda antiga associada a treinos antigos
#         cur.execute("""
#             DELETE FROM agenda
#             WHERE id_cadastro = %s
#             AND id_treino != %s
#         """, (user_id, novo_treino_id))
#         conn.commit()
#
#         return jsonify({
#             'success': True,
#             'message': 'Treino atualizado com sucesso!',
#             'treino_id': novo_treino_id,
#             'treino_info': novo_treino_info
#         })
#
#     except Exception as e:
#         print(f"Erro ao atualizar treino: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         try:
#             cur.close()
#             conn.close()
#         except:
#             pass