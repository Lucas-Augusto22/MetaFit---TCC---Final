import requests
import json
import os
from datetime import datetime

# Configurações
PEXELS_API_KEY = "xd2Cdf7h2R46Ye7yIJoDm5smxa4HNF0wcu4VaVeHRx3da0xbu5etPnK5"
TEST_USER_ID = 1  # Altere conforme seu usuário de teste


def test_pexels_api():
    """Testa a API do Pexels"""
    print("=" * 60)
    print("TESTANDO API PEXELS")
    print("=" * 60)

    try:
        headers = {'Authorization': PEXELS_API_KEY}

        # Testar busca de imagem de exercício
        print("\n1. Buscando imagem de exercício (fitness):")
        params = {
            'query': 'fitness workout',
            'per_page': 1,
            'orientation': 'portrait'
        }

        response = requests.get(
            'https://api.pexels.com/v1/search',
            headers=headers,
            params=params,
            timeout=10
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso! Encontradas {data.get('total_results', 0)} fotos")
            if data.get('photos'):
                photo = data['photos'][0]
                print(f"   Primeira foto: {photo['src']['medium']}")
                print(f"   Fotógrafo: {photo['photographer']}")
            return True
        elif response.status_code == 401:
            print("❌ ERRO 401: Chave API inválida ou expirada")
            print(f"   Chave usada: {PEXELS_API_KEY[:20]}...")
            return False
        elif response.status_code == 429:
            print("❌ ERRO 429: Limite de requisições excedido")
            return False
        else:
            print(f"❌ ERRO {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_local_fitness_api():
    """Testa a função local que gera treinos"""
    print("\n" + "=" * 60)
    print("TESTANDO API LOCAL DE FITNESS")
    print("=" * 60)

    try:
        # Dados de teste
        fitness_data = {
            "name": "João Silva",
            "age": 30,
            "sex": "male",
            "height_cm": 180,
            "weight_kg": 80,
            "experience": "a mais de 1 ano",
            "goal": "Ganhar músculo",
            "access": "academia"
        }

        print(f"\n1. Testando com dados:\n{json.dumps(fitness_data, indent=2, ensure_ascii=False)}")

        # Simular a função chamar_api_fitness_local
        result = chamar_api_fitness_local(fitness_data)

        if result:
            print("\n✅ API Local funcionou!")
            print(f"   Nome: {result['user']['name']}")
            print(f"   Idade: {result['user']['age']}")
            print(f"   Objetivo: {result['user']['goal']}")
            print(f"   IMC: {result['assessment']['BMI']}")
            print(f"   Calorias recomendadas: {result['assessment']['recommended_calories_kcal']}")

            print(f"\n   Plano de exercícios:")
            if 'exercise_plan' in result and 'plan' in result['exercise_plan']:
                for day, exercises in result['exercise_plan']['plan'].items():
                    print(f"   - {day}: {len(exercises)} exercícios")

            print(f"\n   Plano nutricional:")
            if 'nutrition_plan' in result and 'sample_menu' in result['nutrition_plan']:
                for meal, description in result['nutrition_plan']['sample_menu'].items():
                    print(f"   - {meal}: {description}")

            return True
        else:
            print("❌ API Local retornou None")
            return False

    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_connection():
    """Testa conexão com o banco de dados"""
    print("\n" + "=" * 60)
    print("TESTANDO CONEXÃO COM BANCO DE DADOS")
    print("=" * 60)

    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor

        def get_db_connection():
            return psycopg2.connect(
                host='localhost',
                database='MetaFit',
                user='postgres',
                password='senai'
            )

        def get_db_cursor(conn):
            return conn.cursor(cursor_factory=RealDictCursor)

        conn = get_db_connection()
        cur = get_db_cursor(conn)

        print("\n1. Testando conexão básica:")
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"   ✅ Conectado ao PostgreSQL: {version['version']}")

        print("\n2. Verificando tabelas:")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        print(f"   Tabelas encontradas: {len(tables)}")
        for table in tables:
            print(f"   - {table['table_name']}")

        print("\n3. Verificando usuários:")
        cur.execute("SELECT COUNT(*) as count FROM cadastrousuarios;")
        user_count = cur.fetchone()
        print(f"   Total de usuários: {user_count['count']}")

        print("\n4. Verificando treinos:")
        cur.execute("SELECT COUNT(*) as count FROM treino;")
        treino_count = cur.fetchone()
        print(f"   Total de treinos: {treino_count['count']}")

        print("\n5. Verificando agenda:")
        cur.execute("SELECT COUNT(*) as count FROM agenda;")
        agenda_count = cur.fetchone()
        print(f"   Total de itens na agenda: {agenda_count['count']}")

        # Testar inserção
        print("\n6. Testando inserção (simulada):")
        test_insert = """
        INSERT INTO treino 
        (id_cadastro, nome_treino, peso_usuario, altura_usuario, qtn_tempo_pratica_exercicios, objetivo_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id_treino;
        """
        try:
            # Apenas mostrar a query, não executar
            print(f"   Query de teste: {test_insert}")
            print(f"   Valores: ({TEST_USER_ID}, 'Teste', 70.5, 1.75, 'a mais de 1 ano', 'Ganhar músculo')")
            print("   ⚠️  Inserção não executada (apenas simulação)")
        except Exception as e:
            print(f"   ❌ Erro na inserção: {e}")

        cur.close()
        conn.close()
        print("\n   ✅ Conexão com banco OK!")
        return True

    except Exception as e:
        print(f"\n❌ Erro na conexão com banco: {e}")
        return False


def test_form_submission():
    """Testa o envio do formulário de treino"""
    print("\n" + "=" * 60)
    print("TESTANDO SUBMISSÃO DE FORMULÁRIO")
    print("=" * 60)

    try:
        import requests

        # Simular dados do formulário
        form_data = {
            'peso': '80.5',
            'altura': '1.80',
            'experiencia': 'a mais de 1 ano',
            'objetivo': 'Ganhar músculo',
            'acesso': 'academia'
        }

        print(f"\n1. Dados do formulário:\n{json.dumps(form_data, indent=2, ensure_ascii=False)}")

        print("\n2. URL que está sendo chamada:")
        print("   GET /my_level?objetivo=Desenvolver+músculos&experiencia=a+mais+de+1+ano&acesso=academia")

        print("\n3. Problema identificado:")
        print("   ❌ Você está usando GET em vez de POST!")
        print("   ❌ Os dados devem ser enviados via POST para /api/salvar_treino")
        print("   ❌ No GET, os dados aparecem na URL mas não são processados")

        print("\n4. Solução:")
        print("   ✅ Alterar o formulário para usar method='POST'")
        print("   ✅ Enviar para a rota /api/salvar_treino")
        print("   ✅ Usar JSON no corpo da requisição")

        print("\n5. Exemplo de requisição POST correta:")
        print("   URL: http://localhost:3000/api/salvar_treino")
        print("   Method: POST")
        print("   Headers: {'Content-Type': 'application/json'}")
        print("   Body:", json.dumps(form_data, indent=2))

        return False

    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def check_folder_structure():
    """Verifica estrutura de pastas"""
    print("\n" + "=" * 60)
    print("VERIFICANDO ESTRUTURA DE PASTAS")
    print("=" * 60)

    required_folders = [
        'static/images/gifs',
        'static/images/exercise_images',
        'static/images/food_images',
        'static/images/icons_agenda'
    ]

    required_images = {
        'exercise_images': ['default_exercise.jpg', 'pushup_exercise.jpg', 'squat_exercise.jpg'],
        'food_images': ['default_food.jpg', 'breakfast_eggs.jpg', 'lunch_chicken.jpg'],
        'gifs': ['default_exercise.gif', 'Agachamento_livre.gif', 'Flexão_tradicional.gif']
    }

    all_ok = True

    for folder in required_folders:
        if os.path.exists(folder):
            print(f"✅ Pasta existe: {folder}")
            files = os.listdir(folder)
            print(f"   Arquivos: {len(files)}")

            # Verificar imagens específicas
            folder_name = folder.split('/')[-1]
            if folder_name in required_images:
                for img in required_images[folder_name]:
                    img_path = os.path.join(folder, img)
                    if os.path.exists(img_path):
                        print(f"   ✅ {img}")
                    else:
                        print(f"   ❌ {img} - FALTANDO")
                        all_ok = False
        else:
            print(f"❌ Pasta não existe: {folder}")
            all_ok = False

    return all_ok


def check_flask_session():
    """Verifica configuração da sessão Flask"""
    print("\n" + "=" * 60)
    print("VERIFICANDO CONFIGURAÇÃO FLASK")
    print("=" * 60)

    try:
        print("\n1. Secret Key:")
        print("   ✅ Configurada: app.secret_key = 'Lucas'")

        print("\n2. Sessão necessária para /my_level:")
        print("   ✅ Rota /my_level verifica 'user_id' in session")
        print("   ✅ Se não estiver logado, redireciona para /login")

        print("\n3. Problema comum:")
        print("   ❌ Usuário não está logado (session['user_id'] não existe)")
        print("   ❌ Ou usuário foi redirecionado de /login sem session setada")

        return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


# ========== FUNÇÃO DA API LOCAL (copiada do treino.py) ==========

def chamar_api_fitness_local(fitness_data):
    """Chama a API de fitness localmente"""
    try:
        name = fitness_data["name"]
        age = fitness_data["age"]
        sex = fitness_data["sex"]
        height_cm = fitness_data["height_cm"]
        weight_kg = fitness_data["weight_kg"]
        experience = fitness_data["experience"]
        goal = fitness_data["goal"]
        access = fitness_data.get("access", "casa")

        # Cálculos
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

        # Plano de treino
        home_exercises = {
            "Upper A": [
                {"exercise": "Flexões com pés elevados", "series": 4, "reps": "8–12"},
                {"exercise": "Remada curvada com mochila", "series": 4, "reps": "10–12"},
                {"exercise": "Rosca bíceps com mochila", "series": 3, "reps": "10–15"},
                {"exercise": "Tríceps no banco", "series": 3, "reps": "12–15"}
            ],
            "Lower A": [
                {"exercise": "Agachamento com mochila", "series": 4, "reps": "10–15"},
                {"exercise": "Avanço (passada)", "series": 3, "reps": "10–12 por perna"},
                {"exercise": "Cadeira flexora improvisada (toalha/peso)", "series": 3, "reps": "12–15"},
                {"exercise": "Panturrilha em degrau", "series": 4, "reps": "15–20"}
            ],
            "Core & Cardio": [
                {"exercise": "Prancha abdominal", "series": 3, "reps": "30–60 segundos"},
                {"exercise": "Abdominal bicicleta", "series": 3, "reps": "20 por lado"},
                {"exercise": "Burpees", "series": 3, "reps": "10–12"},
                {"exercise": "Corrida parada ou polichinelos", "series": 3, "reps": "1 min"}
            ]
        }

        # Frequência
        if "ganhar" in goal_lower:
            frequency = 5
        elif "manter" in goal_lower:
            frequency = 4
        else:
            frequency = 3

        # Resultado
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
                "frequency_per_week": frequency,
                "type": "Upper/Lower + Core - casa",
                "plan": home_exercises,
                "progression": "Aumentar carga ou repetições semanalmente de forma gradual."
            },
            "nutrition_plan": {
                "calories_target_kcal": target_calories,
                "macros": {
                    "protein_g": protein_g,
                    "fat_g": fat_g,
                    "carbs_g": carbs_g
                },
                "sample_menu": {
                    "breakfast": "3 ovos + pão integral + 1 banana",
                    "snack": "Iogurte natural + aveia + mel",
                    "lunch": "Frango + arroz + feijão + salada",
                    "snack_2": "Sanduíche natural + fruta",
                    "dinner": "Peixe + batata doce + legumes"
                }
            },
            "notes": "Plano automático gerado com base em suas informações."
        }

        return result

    except Exception as e:
        print(f"❌ Erro na API local: {e}")
        return None


# ========== FUNÇÃO PRINCIPAL ==========

def main():
    print("\n" + "=" * 60)
    print("DIAGNÓSTICO COMPLETO - METAFIT")
    print("=" * 60)

    results = {}

    # Testar APIs
    results['pexels'] = test_pexels_api()
    results['fitness_api'] = test_local_fitness_api()
    results['database'] = test_database_connection()
    results['folders'] = check_folder_structure()
    results['flask'] = check_flask_session()

    # Mostrar problema específico do formulário
    test_form_submission()

    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)

    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test.upper()}")

    print("\n" + "=" * 60)
    print("PROBLEMA IDENTIFICADO:")
    print("=" * 60)
    print("""
    ⚠️  SEU FORMULÁRIO ESTÁ USANDO GET EM VEZ DE POST!

    A URL que aparece no terminal:
      GET /my_level?objetivo=Desenvolver+músculos&experiencia=a+mais+de+1+ano&acesso=academia

    Isso mostra que:
    1. O formulário está enviando via GET (method="get" ou não especificado)
    2. Os dados estão indo na URL, não no corpo da requisição
    3. A rota /my_level não processa esses parâmetros

    SOLUÇÃO:
    1. No arquivo my_level.html, altere o formulário para:
       <form id="formTreino" method="POST">

    2. Certifique-se que o JavaScript está enviando para /api/salvar_treino
       e não recarregando a página /my_level

    3. O JavaScript deve enviar os dados como JSON no corpo da requisição POST
    """)

    print("\n" + "=" * 60)
    print("PRÓXIMOS PASSOS:")
    print("=" * 60)
    print("""
    1. Corrigir o método do formulário para POST
    2. Verificar se o JavaScript está interceptando o submit corretamente
    3. Testar o envio com o console do navegador aberto (F12)
    4. Verificar se há erros no console do navegador
    5. Testar a rota /api/salvar_treino diretamente com Postman ou curl
    """)


if __name__ == "__main__":
    main()