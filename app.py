from flask import Flask, render_template, url_for, session, redirect, request, jsonify, send_file
import psycopg2
from PIL import Image
import os
import imageio
import io
import time

from rotas import treino, usuario, galeria, contato, agenda, adm

app = Flask(__name__)
app.secret_key = 'Lucas'

app.register_blueprint(treino.bp)
app.register_blueprint(usuario.usuario_bp)
app.register_blueprint(galeria.galeria_bp)
app.register_blueprint(contato.bp)
app.register_blueprint(agenda.bp)
app.register_blueprint(adm.adm_bp)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    if 'user_id' in session:
        if session['user_type'] == 'usuario':
            return render_template('index.html',
                                   user_nome=session.get('user_nome'),
                                   user_imagem=session.get('user_imagem'))
        elif session['user_type'] == 'adm':
            return redirect('/index_adm')
    return render_template('index.html')


@app.route('/my_level')
def my_level():
    """Rota corrigida para evitar o erro 127.0.0.1 - - [02/Dec/2025 19:34:05] "GET /my_level?dia_semana=Domingo&dia_semana=Segunda-feira"""
    if 'user_id' not in session:
        return redirect('/login')

    # Limpar parâmetros da URL se vierem duplicados
    dia_semana = request.args.get('dia_semana')

    # Se vier múltiplos parâmetros, pegar apenas o primeiro
    if isinstance(dia_semana, list):
        dia_semana = dia_semana[0] if dia_semana else None

    # Renderizar normalmente
    return render_template('my_level.html')


@app.route('/experts')
def experts():
    return render_template('experts.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/feeding')
def feeding():
    return render_template('feeding.html')


@app.route("/api/fitness", methods=["POST"])
def fitness_api():
    data = request.get_json()

    required_fields = ["name", "age", "sex", "height_cm", "weight_kg", "experience", "goal"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo obrigatório ausente: {field}"}), 400

    name = data["name"]
    age = int(data["age"])
    sex = data["sex"].lower()
    height_cm = float(data["height_cm"])
    weight_kg = float(data["weight_kg"])
    experience = data["experience"].lower()
    goal = data["goal"].lower()
    access = data.get("access", "casa")

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

    if sex == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    factors = {
        "nunca pratiquei antes": 1.375,
        "a menos de 1 ano": 1.375,
        "a mais de 1 ano": 1.55,
        "a 4 anos": 1.6,
        "a mais de 5 anos": 1.725
    }
    factor = factors.get(experience, 1.55)
    tdee = bmr * factor

    if "perder" in goal:
        target_calories = tdee * 0.85
    elif "ganhar" in goal:
        target_calories = tdee * 1.1
    else:
        target_calories = tdee
    target_calories = round(target_calories)

    protein_g = round(2.0 * weight_kg)
    fat_g = round(0.9 * weight_kg)
    carbs_g = round((target_calories - (protein_g * 4 + fat_g * 9)) / 4)

    # ATUALIZADO: Treino mais completo
    home_exercises = {
        "Upper A (Peito & Tríceps)": [
            {"exercise": "Flexões tradicionais", "series": 4, "reps": "12-15", "descricao": "Peitoral completo"},
            {"exercise": "Flexões inclinadas", "series": 3, "reps": "10-12", "descricao": "Parte superior do peito"},
            {"exercise": "Flexões diamante", "series": 3, "reps": "8-12", "descricao": "Tríceps focalizado"},
            {"exercise": "Tríceps no banco", "series": 3, "reps": "12-15", "descricao": "Tríceps isolado"},
            {"exercise": "Pike Push-ups", "series": 3, "reps": "8-10", "descricao": "Ombros e tríceps"}
        ],
        "Upper B (Costas & Bíceps)": [
            {"exercise": "Remada curvada com mochila", "series": 4, "reps": "10-12", "descricao": "Costas completas"},
            {"exercise": "Pull-ups assistidos (com elástico)", "series": 3, "reps": "6-8", "descricao": "Latíssimos"},
            {"exercise": "Rosca bíceps com mochila", "series": 3, "reps": "12-15", "descricao": "Bíceps completo"},
            {"exercise": "Rosca martelo", "series": 3, "reps": "12-15", "descricao": "Braquial e antebraço"},
            {"exercise": "Remada invertida na mesa", "series": 3, "reps": "10-12", "descricao": "Costas médias"}
        ],
        "Lower A (Pernas & Glúteos)": [
            {"exercise": "Agachamento livre", "series": 4, "reps": "15-20", "descricao": "Quadríceps e glúteos"},
            {"exercise": "Agachamento sumo", "series": 3, "reps": "12-15", "descricao": "Adutores e glúteos"},
            {"exercise": "Afundo estático", "series": 3, "reps": "10-12 por perna",
             "descricao": "Quadríceps unilateral"},
            {"exercise": "Elevação pélvica", "series": 4, "reps": "15-20", "descricao": "Glúteos máximo"},
            {"exercise": "Panturrilha em degrau", "series": 4, "reps": "20-25", "descricao": "Panturrilhas"}
        ],
        "Core & Cardio": [
            {"exercise": "Prancha abdominal", "series": 3, "reps": "45-60 segundos", "descricao": "Core total"},
            {"exercise": "Prancha lateral", "series": 3, "reps": "30-45s por lado", "descricao": "Oblíquos"},
            {"exercise": "Abdominal bicicleta", "series": 4, "reps": "20 por lado", "descricao": "Oblíquos superiores"},
            {"exercise": "Mountain climbers", "series": 4, "reps": "20-30", "descricao": "Cardio e core"},
            {"exercise": "Burpees", "series": 3, "reps": "10-12", "descricao": "Cardio total"}
        ],
        "Full Body (Corpo Inteiro)": [
            {"exercise": "Burpees com flexão", "series": 4, "reps": "8-10", "descricao": "Exercício completo"},
            {"exercise": "Agachamento com salto", "series": 3, "reps": "12-15", "descricao": "Potência de pernas"},
            {"exercise": "Flexões", "series": 3, "reps": "12-15", "descricao": "Peito e tríceps"},
            {"exercise": "Remada com mochila", "series": 3, "reps": "10-12", "descricao": "Costas"},
            {"exercise": "Prancha com elevação de braço", "series": 3, "reps": "30s",
             "descricao": "Core e estabilidade"}
        ]
    }

    frequency = 5 if "ganhar" in goal else 4 if "manter" in goal else 3

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
            "type": "Treino Completo - 5 tipos diferentes",
            "plan": home_exercises,
            "progression": "Aumentar carga ou repetições semanalmente. Alterar exercícios a cada 6-8 semanas.",
            "total_exercises": sum(len(exercises) for exercises in home_exercises.values())
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
        "notes": "Plano automático gerado com base em suas informações. Ajuste conforme evolução e consulte um profissional se necessário."
    }

    return jsonify(result), 200


@app.route('/api/fitness/generate-gif', methods=['POST'])
def generate_gif():
    try:
        speed = float(request.form.get('speed', 1.0))
        frame_delay_ms = int(request.form.get('frame_delay_ms', 80))
        final_delay = max(1, int(frame_delay_ms / speed))
        width = int(request.form.get('width', 320))
        loop = int(request.form.get('loop', 0))

        frames_files = request.files.getlist('frames[]')
        template = request.files.get('template_gif', None)
        overlay_file = request.files.get('overlay', None)

        if template and not frames_files:
            buf = io.BytesIO()
            template.save(buf)
            buf.seek(0)
            return send_file(buf, mimetype='image/gif')

        if not frames_files:
            return jsonify({'error': 'Envie frames[] ou template_gif'}), 400

        overlay_img = None
        if overlay_file:
            overlay_img = Image.open(overlay_file.stream).convert('RGBA')

        processed_frames = []
        for f in frames_files:
            img = Image.open(f.stream).convert('RGBA')
            w, h = img.size
            new_h = int(width * (h / w))
            img = img.resize((width, new_h), Image.LANCZOS)

            if overlay_img:
                overlay_resized = overlay_img.resize((width, new_h), Image.LANCZOS)
                img = Image.alpha_composite(img, overlay_resized)

            img_rgb = img.convert('RGB')
            processed_frames.append(img_rgb)

        buf_out = io.BytesIO()

        if len(processed_frames) > 1:
            processed_frames[0].save(
                buf_out,
                format='GIF',
                save_all=True,
                append_images=processed_frames[1:],
                duration=final_delay,
                loop=loop,
                optimize=True
            )
        else:
            processed_frames[0].save(buf_out, format='GIF')

        buf_out.seek(0)
        return send_file(buf_out, mimetype='image/gif', as_attachment=False, download_name='animation.gif')

    except Exception as e:
        return jsonify({'error': f'Erro ao gerar GIF: {str(e)}'}), 500


@app.context_processor
def utility_processor():
    def file_exists(filename):
        return os.path.exists(filename)

    return dict(file_exists=file_exists)


if __name__ == "__main__":
    app.run(debug=True, port=3000)

# from flask import Flask, render_template, url_for, session, redirect, request, jsonify, send_file
# import psycopg2
# from PIL import Image
# import os
# import imageio
# import io
# import time
#
# from rotas import treino, usuario, galeria, contato, agenda, adm
#
# app = Flask(__name__)
# app.secret_key = 'Lucas'
#
# app.register_blueprint(treino.bp)
# app.register_blueprint(usuario.usuario_bp)
# app.register_blueprint(galeria.galeria_bp)
# app.register_blueprint(contato.bp)
# app.register_blueprint(agenda.bp)
# app.register_blueprint(adm.adm_bp)
#
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#
#
# @app.route('/')
# def index():
#     if 'user_id' in session:
#         if session['user_type'] == 'usuario':
#             return render_template('index.html',
#                                    user_nome=session.get('user_nome'),
#                                    user_imagem=session.get('user_imagem'))
#         elif session['user_type'] == 'adm':
#             return redirect('/index_adm')
#     return render_template('index.html')
#
#
# @app.route('/experts')
# def experts():
#     return render_template('experts.html')
#
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
#
# @app.route('/feeding')
# def feeding():
#     return render_template('feeding.html')
#
#
# @app.route("/api/fitness", methods=["POST"])
# def fitness_api():
#     data = request.get_json()
#
#     required_fields = ["name", "age", "sex", "height_cm", "weight_kg", "experience", "goal"]
#     for field in required_fields:
#         if field not in data:
#             return jsonify({"error": f"Campo obrigatório ausente: {field}"}), 400
#
#     name = data["name"]
#     age = int(data["age"])
#     sex = data["sex"].lower()
#     height_cm = float(data["height_cm"])
#     weight_kg = float(data["weight_kg"])
#     experience = data["experience"].lower()
#     goal = data["goal"].lower()
#     access = data.get("access", "casa")
#
#     altura_m = height_cm / 100
#     bmi = round(weight_kg / (altura_m ** 2), 2)
#
#     if bmi < 18.5:
#         bmi_category = "Abaixo do peso"
#     elif bmi < 25:
#         bmi_category = "Normal"
#     elif bmi < 30:
#         bmi_category = "Sobrepeso"
#     else:
#         bmi_category = "Obesidade"
#
#     if sex == "male":
#         bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
#     else:
#         bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
#
#     factors = {
#         "nunca pratiquei antes": 1.375,
#         "a menos de 1 ano": 1.375,
#         "a mais de 1 ano": 1.55,
#         "a 4 anos": 1.6,
#         "a mais de 5 anos": 1.725
#     }
#     factor = factors.get(experience, 1.55)
#     tdee = bmr * factor
#
#     if "perder" in goal:
#         target_calories = tdee * 0.85
#     elif "ganhar" in goal:
#         target_calories = tdee * 1.1
#     else:
#         target_calories = tdee
#     target_calories = round(target_calories)
#
#     protein_g = round(2.0 * weight_kg)
#     fat_g = round(0.9 * weight_kg)
#     carbs_g = round((target_calories - (protein_g * 4 + fat_g * 9)) / 4)
#
#     home_exercises = {
#         "Upper A": [
#             {"exercise": "Flexões com pés elevados", "series": 4, "reps": "8–12"},
#             {"exercise": "Remada curvada com mochila", "series": 4, "reps": "10–12"},
#             {"exercise": "Rosca bíceps com mochila", "series": 3, "reps": "10–15"},
#             {"exercise": "Tríceps no banco", "series": 3, "reps": "12–15"}
#         ],
#         "Lower A": [
#             {"exercise": "Agachamento com mochila", "series": 4, "reps": "10–15"},
#             {"exercise": "Avanço (passada)", "series": 3, "reps": "10–12 por perna"},
#             {"exercise": "Cadeira flexora improvisada (toalha/peso)", "series": 3, "reps": "12–15"},
#             {"exercise": "Panturrilha em degrau", "series": 4, "reps": "15–20"}
#         ],
#         "Core & Cardio": [
#             {"exercise": "Prancha abdominal", "series": 3, "reps": "30–60 segundos"},
#             {"exercise": "Abdominal bicicleta", "series": 3, "reps": "20 por lado"},
#             {"exercise": "Burpees", "series": 3, "reps": "10–12"},
#             {"exercise": "Corrida parada ou polichinelos", "series": 3, "reps": "1 min"}
#         ]
#     }
#
#     frequency = 5 if "ganhar" in goal else 4 if "manter" in goal else 3
#
#     result = {
#         "user": {
#             "name": name,
#             "age": age,
#             "sex": sex,
#             "height_cm": height_cm,
#             "weight_kg": weight_kg,
#             "experience": experience,
#             "goal": goal,
#             "access": access
#         },
#         "assessment": {
#             "BMI": bmi,
#             "BMI_category": bmi_category,
#             "BMR_kcal": round(bmr, 1),
#             "TDEE_kcal": round(tdee, 1),
#             "recommended_calories_kcal": target_calories,
#             "macros": {
#                 "protein_g": protein_g,
#                 "fat_g": fat_g,
#                 "carbs_g": carbs_g
#             }
#         },
#         "exercise_plan": {
#             "frequency_per_week": frequency,
#             "type": "Upper/Lower + Core - casa",
#             "plan": home_exercises,
#             "progression": "Aumentar carga ou repetições semanalmente de forma gradual."
#         },
#         "nutrition_plan": {
#             "calories_target_kcal": target_calories,
#             "macros": {
#                 "protein_g": protein_g,
#                 "fat_g": fat_g,
#                 "carbs_g": carbs_g
#             },
#             "sample_menu": {
#                 "breakfast": "3 ovos + pão integral + 1 banana",
#                 "snack": "Iogurte natural + aveia + mel",
#                 "lunch": "Frango + arroz + feijão + salada",
#                 "snack_2": "Sanduíche natural + fruta",
#                 "dinner": "Peixe + batata doce + legumes"
#             }
#         },
#         "notes": "Plano automático gerado com base em suas informações. Ajuste conforme evolução e consulte um profissional se necessário."
#     }
#
#     return jsonify(result), 200
#
#
# @app.route('/api/fitness/generate-gif', methods=['POST'])
# def generate_gif():
#     try:
#         speed = float(request.form.get('speed', 1.0))
#         frame_delay_ms = int(request.form.get('frame_delay_ms', 80))
#         final_delay = max(1, int(frame_delay_ms / speed))
#         width = int(request.form.get('width', 320))
#         loop = int(request.form.get('loop', 0))
#
#         frames_files = request.files.getlist('frames[]')
#         template = request.files.get('template_gif', None)
#         overlay_file = request.files.get('overlay', None)
#
#         if template and not frames_files:
#             buf = io.BytesIO()
#             template.save(buf)
#             buf.seek(0)
#             return send_file(buf, mimetype='image/gif')
#
#         if not frames_files:
#             return jsonify({'error': 'Envie frames[] ou template_gif'}), 400
#
#         overlay_img = None
#         if overlay_file:
#             overlay_img = Image.open(overlay_file.stream).convert('RGBA')
#
#         processed_frames = []
#         for f in frames_files:
#             img = Image.open(f.stream).convert('RGBA')
#             w, h = img.size
#             new_h = int(width * (h / w))
#             img = img.resize((width, new_h), Image.LANCZOS)
#
#             if overlay_img:
#                 overlay_resized = overlay_img.resize((width, new_h), Image.LANCZOS)
#                 img = Image.alpha_composite(img, overlay_resized)
#
#             img_rgb = img.convert('RGB')
#             processed_frames.append(img_rgb)
#
#         buf_out = io.BytesIO()
#
#         if len(processed_frames) > 1:
#             processed_frames[0].save(
#                 buf_out,
#                 format='GIF',
#                 save_all=True,
#                 append_images=processed_frames[1:],
#                 duration=final_delay,
#                 loop=loop,
#                 optimize=True
#             )
#         else:
#             processed_frames[0].save(buf_out, format='GIF')
#
#         buf_out.seek(0)
#         return send_file(buf_out, mimetype='image/gif', as_attachment=False, download_name='animation.gif')
#
#     except Exception as e:
#         return jsonify({'error': f'Erro ao gerar GIF: {str(e)}'}), 500
#
#
# @app.context_processor
# def utility_processor():
#     def file_exists(filename):
#         return os.path.exists(filename)
#
#     return dict(file_exists=file_exists)
#
#
# if __name__ == "__main__":
#     app.run(debug=True, port=3000)
#
