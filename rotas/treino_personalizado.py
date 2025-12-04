# treino_personalizado.py - VERSÃO ATUALIZADA
def gerar_treino_completo(idade, peso, altura, experiencia, objetivo, acesso, genero):
    """Gera treino PERSONALIZADO e COMPLETO baseado nas características do usuário"""

    # Determinar nível
    niveis = {
        "nunca pratiquei antes": "iniciante",
        "a menos de 1 ano": "iniciante",
        "a mais de 1 ano": "intermediario",
        "a 4 anos": "avancado",
        "a mais de 5 anos": "avancado"
    }
    nivel = niveis.get(experiencia.lower(), "intermediario")

    # Determinar foco
    objetivo_lower = objetivo.lower()
    if any(palavra in objetivo_lower for palavra in ['perder', 'emagrecer', 'queimar']):
        foco = "emagrecimento"
        intensidade = "moderada-alta"
        repeticoes = "12-15"
    elif any(palavra in objetivo_lower for palavra in ['ganhar', 'músculo', 'massa', 'hipertrofia']):
        foco = "hipertrofia"
        intensidade = "alta"
        repeticoes = "8-12"
    elif any(palavra in objetivo_lower for palavra in ['definir', 'definição', 'tonificar']):
        foco = "definicao"
        intensidade = "moderada-alta"
        repeticoes = "10-12"
    elif any(palavra in objetivo_lower for palavra in ['força', 'forca']):
        foco = "forca"
        intensidade = "muito alta"
        repeticoes = "4-6"
    else:
        foco = "saude"
        intensidade = "moderada"
        repeticoes = "10-12"

    # Ajustar para idade
    if idade < 18:
        foco = "adolescente"
        intensidade = "moderada"
        repeticoes = "10-15"
    elif idade > 50:
        foco = "maduro"
        intensidade = "moderada"
        repeticoes = "12-15"

    # ========== TREINO PARA CASA - COMPLETO ==========
    if acesso.lower() in ['casa', 'parque', 'ar livre', 'home']:
        treinos_casa = {
            "Upper A (Peito, Tríceps & Ombros)": [
                {"exercise": "Flexões tradicionais", "series": 4, "reps": repeticoes, "descricao": "Peitoral completo"},
                {"exercise": "Flexões inclinadas", "series": 3, "reps": "10-12",
                 "descricao": "Parte superior do peito"},
                {"exercise": "Flexões diamante", "series": 3, "reps": "8-12", "descricao": "Tríceps focalizado"},
                {"exercise": "Pike Push-ups", "series": 3, "reps": "8-10", "descricao": "Ombros e tríceps"},
                {"exercise": "Tríceps no banco", "series": 3, "reps": "12-15", "descricao": "Tríceps isolado"},
                {"exercise": "Elevação lateral com garrafas", "series": 3, "reps": "12-15",
                 "descricao": "Ombros laterais"}
            ],
            "Upper B (Costas, Bíceps & Posterior)": [
                {"exercise": "Remada curvada com mochila", "series": 4, "reps": "10-12",
                 "descricao": "Costas completas"},
                {"exercise": "Pull-ups assistidos (porta)", "series": 3, "reps": "6-8",
                 "descricao": "Latíssimos do dorso"},
                {"exercise": "Rosca bíceps com mochila", "series": 3, "reps": "12-15", "descricao": "Bíceps completo"},
                {"exercise": "Rosca martelo", "series": 3, "reps": "12-15", "descricao": "Braquial e antebraço"},
                {"exercise": "Remada invertida na mesa", "series": 3, "reps": "10-12", "descricao": "Costas médias"},
                {"exercise": "Face pulls com elástico", "series": 3, "reps": "12-15", "descricao": "Deltóide posterior"}
            ],
            "Lower A (Pernas & Glúteos)": [
                {"exercise": "Agachamento livre", "series": 4, "reps": "15-20", "descricao": "Quadríceps e glúteos"},
                {"exercise": "Agachamento sumo", "series": 3, "reps": "12-15", "descricao": "Adutores e glúteos"},
                {"exercise": "Afundo estático", "series": 3, "reps": "10-12 por perna",
                 "descricao": "Quadríceps unilateral"},
                {"exercise": "Elevação pélvica", "series": 4, "reps": "15-20", "descricao": "Glúteos máximo"},
                {"exercise": "Panturrilha em degrau", "series": 4, "reps": "20-25", "descricao": "Panturrilhas"},
                {"exercise": "Agachamento búlgaro", "series": 3, "reps": "10-12 por perna",
                 "descricao": "Perna unilateral"}
            ],
            "Core & Cardio Intenso": [
                {"exercise": "Prancha abdominal", "series": 3, "reps": "45-60 segundos", "descricao": "Core total"},
                {"exercise": "Prancha lateral", "series": 3, "reps": "30-45s por lado", "descricao": "Oblíquos"},
                {"exercise": "Abdominal bicicleta", "series": 4, "reps": "20 por lado",
                 "descricao": "Oblíquos superiores"},
                {"exercise": "Mountain climbers", "series": 4, "reps": "20-30", "descricao": "Cardio e core"},
                {"exercise": "Burpees", "series": 3, "reps": "10-12", "descricao": "Cardio total"},
                {"exercise": "Russian twists", "series": 3, "reps": "15 por lado", "descricao": "Rotação do core"}
            ],
            "Full Body (Corpo Inteiro)": [
                {"exercise": "Burpees com flexão", "series": 4, "reps": "8-10", "descricao": "Exercício completo"},
                {"exercise": "Agachamento com salto", "series": 3, "reps": "12-15", "descricao": "Potência de pernas"},
                {"exercise": "Flexões", "series": 3, "reps": "12-15", "descricao": "Peito e tríceps"},
                {"exercise": "Remada com mochila", "series": 3, "reps": "10-12", "descricao": "Costas"},
                {"exercise": "Prancha com elevação de braço", "series": 3, "reps": "30s",
                 "descricao": "Core e estabilidade"},
                {"exercise": "Lunges caminhando", "series": 3, "reps": "10 por perna", "descricao": "Pernas dinâmico"}
            ],
            "Mobilidade & Recuperação": [
                {"exercise": "Alongamento dinâmico completo", "series": 1, "reps": "10-15min",
                 "descricao": "Aquecimento total"},
                {"exercise": "Mobilidade de quadril", "series": 3, "reps": "10 por perna",
                 "descricao": "Flexibilidade"},
                {"exercise": "Mobilidade de ombros", "series": 3, "reps": "10-12", "descricao": "Amplitude articular"},
                {"exercise": "Alongamento estático", "series": 1, "reps": "30s cada",
                 "descricao": "Recuperação muscular"},
                {"exercise": "Respiração diafragmática", "series": 1, "reps": "5min",
                 "descricao": "Controle e relaxamento"},
                {"exercise": "Foam rolling", "series": 1, "reps": "10min", "descricao": "Liberação miofascial"}
            ]
        }

        # Selecionar treinos baseado no foco - MAIS TREINOS
        if foco == "emagrecimento":
            planos_selecionados = ["Full Body", "Core & Cardio Intenso", "Lower A", "Upper A"]
        elif foco == "hipertrofia":
            planos_selecionados = ["Upper A", "Upper B", "Lower A", "Full Body"]
        elif foco == "forca":
            planos_selecionados = ["Full Body", "Lower A", "Upper A", "Upper B"]
        elif foco == "adolescente":
            planos_selecionados = ["Full Body", "Core & Cardio Intenso", "Mobilidade & Recuperação"]
        elif foco == "maduro":
            planos_selecionados = ["Full Body", "Mobilidade & Recuperação", "Lower A", "Core & Cardio Intenso"]
        else:
            planos_selecionados = ["Upper A", "Lower A", "Core & Cardio Intenso", "Full Body"]

        # Ajustar para iniciantes
        if nivel == "iniciante":
            for plano in planos_selecionados:
                if plano in treinos_casa:
                    for exercicio in treinos_casa[plano]:
                        exercicio["series"] = max(2, exercicio["series"] - 1)
                        if "reps" in exercicio and isinstance(exercicio["reps"], str):
                            if "-" in exercicio["reps"]:
                                min_rep, max_rep = exercicio["reps"].split("-")
                                exercicio["reps"] = f"{int(min_rep) + 2}-{int(max_rep) + 2}"

        return {k: treinos_casa[k] for k in planos_selecionados if k in treinos_casa}

    # ========== TREINO PARA ACADEMIA - COMPLETO ==========
    else:  # academia
        treinos_academia = {
            "Peito & Tríceps": [
                {"exercise": "Supino reto com barra", "series": 4, "reps": repeticoes, "descricao": "Peitoral maior"},
                {"exercise": "Supino inclinado com halteres", "series": 3, "reps": "10-12",
                 "descricao": "Porção clavicular"},
                {"exercise": "Crucifixo reto", "series": 3, "reps": "12-15", "descricao": "Alongamento peitoral"},
                {"exercise": "Tríceps testa", "series": 3, "reps": "10-12", "descricao": "Tríceps longo"},
                {"exercise": "Tríceps corda", "series": 3, "reps": "12-15", "descricao": "Cabeça lateral"},
                {"exercise": "Push-ups com peso", "series": 3, "reps": "8-12", "descricao": "Força funcional"}
            ],
            "Costas & Bíceps": [
                {"exercise": "Remada curvada", "series": 4, "reps": repeticoes, "descricao": "Espessura das costas"},
                {"exercise": "Puxada frente", "series": 3, "reps": "10-12", "descricao": "Largura das costas"},
                {"exercise": "Remada unilateral", "series": 3, "reps": "10-12 por lado", "descricao": "Simetria"},
                {"exercise": "Rosca direta barra", "series": 3, "reps": "10-12", "descricao": "Bíceps completo"},
                {"exercise": "Rosca martelo", "series": 3, "reps": "12-15", "descricao": "Braquial e antebraço"},
                {"exercise": "Rosca concentrada", "series": 3, "reps": "10-12", "descricao": "Pico do bíceps"}
            ],
            "Pernas & Glúteos": [
                {"exercise": "Agachamento livre", "series": 4, "reps": "8-12", "descricao": "Exercício rei"},
                {"exercise": "Leg press 45°", "series": 3, "reps": "12-15", "descricao": "Quadríceps seguro"},
                {"exercise": "Mesa flexora", "series": 3, "reps": "12-15", "descricao": "Isquiotibiais"},
                {"exercise": "Cadeira extensora", "series": 3, "reps": "15-20", "descricao": "Quadríceps isolado"},
                {"exercise": "Elevação pélvica", "series": 4, "reps": "12-15", "descricao": "Glúteos máximo"},
                {"exercise": "Cadeira adutora/abdutora", "series": 3, "reps": "15-20",
                 "descricao": "Adutores/abdutores"}
            ],
            "Ombros & Trapézio": [
                {"exercise": "Desenvolvimento militar", "series": 4, "reps": repeticoes,
                 "descricao": "Deltóides completos"},
                {"exercise": "Elevação lateral", "series": 3, "reps": "12-15", "descricao": "Deltóide medial"},
                {"exercise": "Elevação frontal", "series": 3, "reps": "12-15", "descricao": "Deltóide anterior"},
                {"exercise": "Encolhimento com barra", "series": 3, "reps": "12-15", "descricao": "Trapézio superior"},
                {"exercise": "Crucifixo invertido", "series": 3, "reps": "12-15", "descricao": "Deltóide posterior"},
                {"exercise": "Arnold press", "series": 3, "reps": "10-12", "descricao": "Rotação completa"}
            ],
            "Abdômen & Core Avançado": [
                {"exercise": "Crunch na máquina", "series": 3, "reps": "15-20", "descricao": "Reto abdominal"},
                {"exercise": "Prancha abdominal", "series": 3, "reps": "60-90s", "descricao": "Core total"},
                {"exercise": "Elevação de pernas suspenso", "series": 3, "reps": "12-15", "descricao": "Inferiores"},
                {"exercise": "Rotação russa com peso", "series": 3, "reps": "15 por lado", "descricao": "Oblíquos"},
                {"exercise": "Abdominal infra", "series": 3, "reps": "15-20", "descricao": "Porção inferior"},
                {"exercise": "Hollow body hold", "series": 3, "reps": "30-45s", "descricao": "Core isométrico"}
            ],
            "Cardio & HIIT": [
                {"exercise": "Esteira (intervalado)", "series": 1, "reps": "20-30min", "descricao": "Cardio HIIT"},
                {"exercise": "Transport", "series": 1, "reps": "15-20min", "descricao": "Cardio de impacto"},
                {"exercise": "Bicicleta ergométrica", "series": 1, "reps": "25-35min", "descricao": "Cardio leve"},
                {"exercise": "Remo ergométrico", "series": 1, "reps": "15-20min", "descricao": "Cardio completo"},
                {"exercise": "Escada", "series": 1, "reps": "10-15min", "descricao": "Cardio intenso"},
                {"exercise": "Elliptical", "series": 1, "reps": "20-30min", "descricao": "Cardio sem impacto"}
            ],
            "Força & Potência": [
                {"exercise": "Power clean", "series": 4, "reps": "3-5", "descricao": "Potência total"},
                {"exercise": "Snatch grip deadlift", "series": 3, "reps": "4-6", "descricao": "Força de costas"},
                {"exercise": "Push press", "series": 3, "reps": "5-8", "descricao": "Potência de ombros"},
                {"exercise": "Box jumps", "series": 4, "reps": "5-8", "descricao": "Potência de pernas"},
                {"exercise": "Medicine ball slams", "series": 3, "reps": "8-10", "descricao": "Potência core"},
                {"exercise": "Kettlebell swings", "series": 3, "reps": "12-15", "descricao": "Força posterior"}
            ]
        }

        # Selecionar treinos baseado no foco - MAIS VARIEDADE
        if foco == "emagrecimento":
            planos_selecionados = ["Pernas & Glúteos", "Cardio & HIIT", "Abdômen & Core Avançado", "Costas & Bíceps",
                                   "Peito & Tríceps"]
        elif foco == "hipertrofia":
            planos_selecionados = ["Peito & Tríceps", "Costas & Bíceps", "Pernas & Glúteos", "Ombros & Trapézio",
                                   "Força & Potência"]
        elif foco == "definicao":
            planos_selecionados = ["Peito & Tríceps", "Costas & Bíceps", "Pernas & Glúteos", "Abdômen & Core Avançado",
                                   "Cardio & HIIT"]
        elif foco == "forca":
            planos_selecionados = ["Pernas & Glúteos", "Costas & Bíceps", "Peito & Tríceps", "Ombros & Trapézio",
                                   "Força & Potência"]
        elif foco == "adolescente":
            planos_selecionados = ["Pernas & Glúteos", "Peito & Tríceps", "Costas & Bíceps", "Abdômen & Core Avançado"]
        elif foco == "maduro":
            planos_selecionados = ["Pernas & Glúteos", "Costas & Bíceps", "Ombros & Trapézio", "Cardio & HIIT"]
        else:
            planos_selecionados = ["Peito & Tríceps", "Costas & Bíceps", "Pernas & Glúteos", "Ombros & Trapézio",
                                   "Abdômen & Core Avançado"]

        # Ajustar para iniciantes
        if nivel == "iniciante":
            for plano in planos_selecionados:
                if plano in treinos_academia:
                    for exercicio in treinos_academia[plano]:
                        exercicio["series"] = max(2, exercicio["series"] - 1)
                        if "reps" in exercicio and isinstance(exercicio["reps"], str):
                            if "-" in exercicio["reps"]:
                                min_rep, max_rep = exercicio["reps"].split("-")
                                exercicio["reps"] = f"{int(min_rep) + 2}-{int(max_rep) + 2}"

        return {k: treinos_academia[k] for k in planos_selecionados if k in treinos_academia}


def gerar_dieta_personalizada(peso, altura, idade, objetivo, genero, nivel_atividade):
    """Gera dieta PERSONALIZADA"""

    # Calcular necessidades calóricas
    if genero.lower() == "male":
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161

    # Fator de atividade
    fatores = {
        "sedentario": 1.2,
        "leve": 1.375,
        "moderado": 1.55,
        "ativo": 1.725,
        "muito_ativo": 1.9
    }

    # Mapear experiência para nível de atividade
    experiencia_map = {
        "nunca pratiquei antes": "leve",
        "a menos de 1 ano": "moderado",
        "a mais de 1 ano": "ativo",
        "a 4 anos": "ativo",
        "a mais de 5 anos": "muito_ativo"
    }

    nivel = experiencia_map.get(nivel_atividade.lower(), "moderado")
    fator = fatores.get(nivel, 1.55)

    tdee = tmb * fator

    # Ajustar baseado no objetivo
    objetivo_lower = objetivo.lower()
    if any(palavra in objetivo_lower for palavra in ['perder', 'emagrecer']):
        calorias = tdee * 0.85
        enfase = "Déficit calórico para perda de gordura"
    elif any(palavra in objetivo_lower for palavra in ['ganhar', 'músculo', 'massa']):
        calorias = tdee * 1.15
        enfase = "Superávit calórico para ganho muscular"
    else:
        calorias = tdee
        enfase = "Manutenção corporal"

    # Arredondar
    calorias = round(calorias / 50) * 50

    # Distribuição de macros PERSONALIZADA
    if "perder" in objetivo_lower:
        proteinas = round(2.2 * peso)  # Mais proteína para preservar músculo
        gorduras = round(0.8 * peso)
    elif "ganhar" in objetivo_lower:
        proteinas = round(1.8 * peso)
        gorduras = round(1.0 * peso)
    else:
        proteinas = round(2.0 * peso)
        gorduras = round(0.9 * peso)

    carboidratos = round((calorias - (proteinas * 4 + gorduras * 9)) / 4)

    # Dietas PERSONALIZADAS
    dietas = {
        "emagrecimento": {
            "cafe_manha": "Omelete de 3 claras + 1 gema com espinafre + 1 fatia pão integral + 1/2 abacate",
            "lanche_manha": "Iogurte grego natural + 1 colher chia + 5 morangos + 5 amêndoas",
            "almoco": "150g peito de frango grelhado + 100g arroz integral + 100g feijão + salada verde à vontade",
            "lanche_tarde": "Whey protein com água + 1 maçã verde + 1 colher pasta amendoim",
            "jantar": "150g filé de peixe (salmão/truta) + 150g batata doce + brócolis no vapor",
            "ceia": "Chá verde + 1 fatia queijo cottage",
            "hidratacao": f"{round(peso * 0.035, 1)}L de água ao longo do dia",
            "suplementos": "Omega-3, vitamina D, creatina (opcional)"
        },
        "hipertrofia": {
            "cafe_manha": "4 ovos mexidos + 2 fatias pão integral + 1 banana + 1 colher pasta amendoim + 1 copo leite",
            "lanche_manha": "Shake: Whey protein + 50g aveia + 200ml leite + 1 banana + 1 colher mel",
            "almoco": "200g carne moída magra + 150g arroz integral + feijão + legumes variados + 1 porção abacate",
            "lanche_tarde": "Sanduíche: 2 fatias pão integral + 150g frango desfiado + queijo cottage + alface + tomate",
            "jantar": "200g bife bovino (patinho/alcatra) + 200g batata inglesa + salada colorida com azeite",
            "ceia": "Caseína ou 200g iogurte grego + 10g pasta amendoim + 1 colher chia",
            "hidratacao": f"{round(peso * 0.04, 1)}L de água ao longo do dia",
            "suplementos": "Whey protein, creatina, BCAA (pós-treino), multivitamínico"
        },
        "definicao": {
            "cafe_manha": "3 ovos pochê + 1 fatia pão integral + 1/2 abacate pequeno + 1 xícara chá verde",
            "lanche_manha": "Iogurte natural + 20g granola sem açúcar + 5 amêndoas + 1 colher linhaça",
            "almoco": "180g filé de tilápia ou frango + 100g quinoa + salada de folhas verdes com limão",
            "lanche_tarde": "Whey protein isolado com água + 1 pera ou kiwi",
            "jantar": "180g patinho grelhado + abóbora assada + aspargos + 1 porção cogumelos",
            "ceia": "Chá de gengibre ou 1 copo leite desnatado + 1 colher proteína vegetal",
            "hidratacao": f"{round(peso * 0.038, 1)}L de água ao longo do dia",
            "suplementos": "Whey isolado, CLA, L-carnitina, chá verde em cápsulas"
        },
        "manutencao": {
            "cafe_manha": "2 ovos mexidos + 2 fatias pão integral + 1 fatia queijo minas + 1 fruta + 1 xícara café",
            "lanche_manha": "1 potinho iogurte + 1 colher mel + 1 punhado castanhas + 1 fruta seca",
            "almoco": "150g frango ou peixe + 120g arroz integral + lentilha + salada mista com azeite",
            "lanche_tarde": "1 sanduíche natural com pão integral + suco verde (couve, limão, gengibre)",
            "jantar": "150g peixe assado + 150g batata doce + legumes refogados no azeite",
            "ceia": "Chá de ervas ou 1 copo leite + 1 banana pequena",
            "hidratacao": f"{round(peso * 0.03, 1)}L de água ao longo do dia",
            "suplementos": "Multivitamínico, probiótico, vitamina C"
        },
        "vegetariano": {
            "cafe_manha": "Tofu mexido + 2 fatias pão integral + 1/2 abacate + 1 xícara chá",
            "lanche_manha": "Shake de proteína vegetal + 1 banana + 1 colher chia",
            "almoco": "Lentilha ou grão de bico + quinoa + legumes assados + salada",
            "lanche_tarde": "Hummus + palitos de vegetais + 1 punhado nozes",
            "jantar": "Omelete de claras com vegetais + batata doce + brócolis",
            "ceia": "Leite vegetal fortificado + 1 colher proteína em pó",
            "hidratacao": f"{round(peso * 0.035, 1)}L de água ao longo do dia",
            "suplementos": "Vitamina B12, ferro, proteína vegetal, omega-3 de algas"
        }
    }

    # Selecionar dieta baseada no objetivo
    if any(palavra in objetivo_lower for palavra in ['perder', 'emagrecer']):
        dieta_tipo = "emagrecimento"
    elif any(palavra in objetivo_lower for palavra in ['ganhar', 'músculo', 'massa']):
        dieta_tipo = "hipertrofia"
    elif any(palavra in objetivo_lower for palavra in ['definir', 'definição']):
        dieta_tipo = "definicao"
    elif any(palavra in objetivo_lower for palavra in ['vegetariano', 'vegano']):
        dieta_tipo = "vegetariano"
    else:
        dieta_tipo = "manutencao"

    dieta_base = dietas.get(dieta_tipo, dietas["manutencao"])

    return {
        "calorias_diarias": calorias,
        "macros": {
            "proteinas_g": proteinas,
            "carboidratos_g": carboidratos,
            "gorduras_g": gorduras
        },
        "refeicoes": dieta_base,
        "enfase": enfase,
        "observacoes": f"Dieta ajustada para {objetivo}. Baseada em: {peso}kg, {altura}cm, {idade} anos. Ajustar quantidades conforme evolução.",
        "recomendacoes": [
            "Comer a cada 3-4 horas",
            "Priorizar alimentos integrais e naturais",
            "Controlar porções",
            "Manter hidratação constante",
            "Ajustar conforme resposta corporal"
        ]
    }

# # treino_personalizado.py
# def gerar_treino_completo(idade, peso, altura, experiencia, objetivo, acesso, genero):
#     """Gera treino personalizado baseado nas características do usuário"""
#
#     # Determinar nível baseado na experiência
#     niveis = {
#         "nunca pratiquei antes": "iniciante",
#         "a menos de 1 ano": "iniciante",
#         "a mais de 1 ano": "intermediario",
#         "a 4 anos": "avancado",
#         "a mais de 5 anos": "avancado"
#     }
#     nivel = niveis.get(experiencia.lower(), "intermediario")
#
#     # Determinar foco baseado no objetivo
#     objetivo_lower = objetivo.lower()
#     if any(palavra in objetivo_lower for palavra in ['perder', 'emagrecer', 'queimar']):
#         foco = "emagrecimento"
#         intensidade = "moderada"
#         repeticoes = "12-15"
#     elif any(palavra in objetivo_lower for palavra in ['ganhar', 'músculo', 'massa', 'hipertrofia']):
#         foco = "hipertrofia"
#         intensidade = "alta"
#         repeticoes = "8-12"
#     elif any(palavra in objetivo_lower for palavra in ['definir', 'definição', 'tonificar']):
#         foco = "definicao"
#         intensidade = "moderada-alta"
#         repeticoes = "10-12"
#     elif any(palavra in objetivo_lower for palavra in ['força', 'forca']):
#         foco = "forca"
#         intensidade = "alta"
#         repeticoes = "4-6"
#     else:
#         foco = "geral"
#         intensidade = "moderada"
#         repeticoes = "10-12"
#
#     # Ajustar baseado na idade
#     if idade < 18:
#         foco = "adolescente"
#         intensidade = "moderada"
#     elif idade > 50:
#         foco = "maduro"
#         intensidade = "moderada-baixa"
#         repeticoes = f"{repeticoes} (adaptado)"
#
#     # TREINOS COMPLETOS POR TIPO
#
#     # ========== TREINO PARA CASA ==========
#     if acesso.lower() in ['casa', 'parque', 'ar livre']:
#         treinos_casa = {
#             "Upper A (Superior)": [
#                 {"exercise": "Flexões tradicionais", "series": 4, "reps": repeticoes, "descricao": "Foco peitoral"},
#                 {"exercise": "Flexões diamante", "series": 3, "reps": "10-12", "descricao": "Foco tríceps"},
#                 {"exercise": "Prancha com elevação de braço", "series": 3, "reps": "30-45s",
#                  "descricao": "Core e estabilidade"},
#                 {"exercise": "Flexões inclinadas", "series": 3, "reps": repeticoes,
#                  "descricao": "Parte superior do peito"},
#                 {"exercise": "Burpees", "series": 4, "reps": "10-15", "descricao": "Cardio e força total"}
#             ],
#             "Lower A (Inferior)": [
#                 {"exercise": "Agachamento livre", "series": 4, "reps": "15-20", "descricao": "Quadríceps e glúteos"},
#                 {"exercise": "Afundo estático", "series": 3, "reps": "12-15 por perna",
#                  "descricao": "Quadríceps unilateral"},
#                 {"exercise": "Elevação pélvica", "series": 4, "reps": "15-20", "descricao": "Glúteos e posterior"},
#                 {"exercise": "Agachamento sumo", "series": 3, "reps": "12-15", "descricao": "Adutores e glúteos"},
#                 {"exercise": "Ponte unilateral", "series": 3, "reps": "10-12 por perna", "descricao": "Glúteo isolado"}
#             ],
#             "Full Body (Corpo Inteiro)": [
#                 {"exercise": "Flexões", "series": 4, "reps": repeticoes, "descricao": "Peito e tríceps"},
#                 {"exercise": "Agachamento com salto", "series": 4, "reps": "12-15", "descricao": "Potência de pernas"},
#                 {"exercise": "Prancha lateral", "series": 3, "reps": "30-45s por lado", "descricao": "Oblíquos"},
#                 {"exercise": "Mountain climbers", "series": 4, "reps": "20-30", "descricao": "Cardio e core"},
#                 {"exercise": "Superman", "series": 3, "reps": "12-15", "descricao": "Costas inferiores"}
#             ],
#             "Core & Cardio": [
#                 {"exercise": "Abdominal bicicleta", "series": 4, "reps": "20 por lado", "descricao": "Oblíquos"},
#                 {"exercise": "Prancha abdominal", "series": 3, "reps": "45-60s", "descricao": "Core total"},
#                 {"exercise": "Elevação de pernas", "series": 3, "reps": "15-20", "descricao": "Inferiores abdominais"},
#                 {"exercise": "Polichinelos", "series": 4, "reps": "30-40", "descricao": "Cardio"},
#                 {"exercise": "Corrida estacionária", "series": 3, "reps": "1 min", "descricao": "Cardio intenso"}
#             ],
#             "Mobilidade & Força": [
#                 {"exercise": "Alongamento dinâmico", "series": 1, "reps": "5-10min", "descricao": "Aquecimento"},
#                 {"exercise": "Flexão de quadril", "series": 3, "reps": "10 por perna", "descricao": "Mobilidade"},
#                 {"exercise": "Agachamento profundo", "series": 3, "reps": "8-10", "descricao": "Amplitude total"},
#                 {"exercise": "Flexão de braço assistida", "series": 3, "reps": "8-12", "descricao": "Progressão"},
#                 {"exercise": "Prancha com rotação", "series": 3, "reps": "10 por lado", "descricao": "Core rotacional"}
#             ]
#         }
#
#         # Selecionar treinos baseado no foco
#         if foco == "emagrecimento":
#             planos_selecionados = ["Full Body", "Core & Cardio", "Lower A"]
#         elif foco == "hipertrofia":
#             planos_selecionados = ["Upper A", "Lower A", "Full Body"]
#         elif foco == "forca":
#             planos_selecionados = ["Full Body", "Mobilidade & Força", "Upper A"]
#         else:
#             planos_selecionados = ["Upper A", "Lower A", "Core & Cardio"]
#
#         return {k: treinos_casa[k] for k in planos_selecionados if k in treinos_casa}
#
#     # ========== TREINO PARA ACADEMIA ==========
#     else:  # academia
#         treinos_academia = {
#             "Peito & Tríceps": [
#                 {"exercise": "Supino reto com barra", "series": 4, "reps": repeticoes, "descricao": "Peitoral maior"},
#                 {"exercise": "Supino inclinado com halteres", "series": 3, "reps": "10-12",
#                  "descricao": "Porção clavicular"},
#                 {"exercise": "Crucifixo reto", "series": 3, "reps": "12-15", "descricao": "Alongamento peitoral"},
#                 {"exercise": "Tríceps testa", "series": 3, "reps": "10-12", "descricao": "Tríceps longo"},
#                 {"exercise": "Tríceps corda", "series": 3, "reps": "12-15", "descricao": "Cabeça lateral"}
#             ],
#             "Costas & Bíceps": [
#                 {"exercise": "Remada curvada", "series": 4, "reps": repeticoes, "descricao": "Espessura das costas"},
#                 {"exercise": "Puxada frente", "series": 3, "reps": "10-12", "descricao": "Largura das costas"},
#                 {"exercise": "Remada unilateral", "series": 3, "reps": "10-12 por lado", "descricao": "Simetria"},
#                 {"exercise": "Rosca direta barra", "series": 3, "reps": "10-12", "descricao": "Bíceps completo"},
#                 {"exercise": "Rosca martelo", "series": 3, "reps": "12-15", "descricao": "Braquial e antebraço"}
#             ],
#             "Pernas & Glúteos": [
#                 {"exercise": "Agachamento livre", "series": 4, "reps": "8-12", "descricao": "Exercício rei"},
#                 {"exercise": "Leg press 45°", "series": 3, "reps": "12-15", "descricao": "Quadríceps seguro"},
#                 {"exercise": "Mesa flexora", "series": 3, "reps": "12-15", "descricao": "Isquiotibiais"},
#                 {"exercise": "Cadeira extensora", "series": 3, "reps": "15-20", "descricao": "Quadríceps isolado"},
#                 {"exercise": "Elevação pélvica", "series": 4, "reps": "12-15", "descricao": "Glúteos máximo"}
#             ],
#             "Ombros & Trapézio": [
#                 {"exercise": "Desenvolvimento militar", "series": 4, "reps": repeticoes,
#                  "descricao": "Deltóides completos"},
#                 {"exercise": "Elevação lateral", "series": 3, "reps": "12-15", "descricao": "Deltóide medial"},
#                 {"exercise": "Elevação frontal", "series": 3, "reps": "12-15", "descricao": "Deltóide anterior"},
#                 {"exercise": "Encolhimento com barra", "series": 3, "reps": "12-15", "descricao": "Trapézio superior"},
#                 {"exercise": "Crucifixo invertido", "series": 3, "reps": "12-15", "descricao": "Deltóide posterior"}
#             ],
#             "Abdômen & Core": [
#                 {"exercise": "Crunch na máquina", "series": 3, "reps": "15-20", "descricao": "Reto abdominal"},
#                 {"exercise": "Prancha abdominal", "series": 3, "reps": "60-90s", "descricao": "Core total"},
#                 {"exercise": "Elevação de pernas suspenso", "series": 3, "reps": "12-15", "descricao": "Inferiores"},
#                 {"exercise": "Rotação russa com peso", "series": 3, "reps": "15 por lado", "descricao": "Oblíquos"},
#                 {"exercise": "Abdominal infra", "series": 3, "reps": "15-20", "descricao": "Porção inferior"}
#             ],
#             "Cardio & Resistência": [
#                 {"exercise": "Esteira (intervalado)", "series": 1, "reps": "20-30min", "descricao": "Cardio HIIT"},
#                 {"exercise": "Transport", "series": 1, "reps": "15-20min", "descricao": "Cardio de impacto"},
#                 {"exercise": "Bicicleta ergométrica", "series": 1, "reps": "25-35min", "descricao": "Cardio leve"},
#                 {"exercise": "Remo ergométrico", "series": 1, "reps": "15-20min", "descricao": "Cardio completo"},
#                 {"exercise": "Escada", "series": 1, "reps": "10-15min", "descricao": "Cardio intenso"}
#             ]
#         }
#
#         # Selecionar treinos baseado no foco
#         if foco == "emagrecimento":
#             planos_selecionados = ["Pernas & Glúteos", "Cardio & Resistência", "Abdômen & Core", "Costas & Bíceps"]
#         elif foco == "hipertrofia":
#             planos_selecionados = ["Peito & Tríceps", "Costas & Bíceps", "Pernas & Glúteos", "Ombros & Trapézio"]
#         elif foco == "definicao":
#             planos_selecionados = ["Peito & Tríceps", "Costas & Bíceps", "Pernas & Glúteos", "Abdômen & Core"]
#         elif foco == "forca":
#             planos_selecionados = ["Pernas & Glúteos", "Costas & Bíceps", "Peito & Tríceps", "Ombros & Trapézio"]
#         else:
#             planos_selecionados = ["Peito & Tríceps", "Costas & Bíceps", "Pernas & Glúteos", "Abdômen & Core"]
#
#         # Ajustar para iniciantes
#         if nivel == "iniciante":
#             for plano in planos_selecionados:
#                 for exercicio in treinos_academia[plano]:
#                     exercicio["series"] = max(2, exercicio["series"] - 1)
#                     if "reps" in exercicio and isinstance(exercicio["reps"], str):
#                         if "-" in exercicio["reps"]:
#                             min_rep, max_rep = exercicio["reps"].split("-")
#                             exercicio["reps"] = f"{int(min_rep) + 2}-{int(max_rep) + 2}"
#
#         return {k: treinos_academia[k] for k in planos_selecionados if k in treinos_academia}
#
#
# def gerar_dieta_personalizada(peso, altura, idade, objetivo, genero, nivel_atividade):
#     """Gera dieta personalizada"""
#
#     # Calcular necessidades calóricas básicas
#     if genero.lower() == "male":
#         tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
#     else:
#         tmb = 10 * peso + 6.25 * altura - 5 * idade - 161
#
#     # Fator de atividade
#     fatores = {
#         "sedentario": 1.2,
#         "leve": 1.375,
#         "moderado": 1.55,
#         "ativo": 1.725,
#         "muito_ativo": 1.9
#     }
#     fator = fatores.get(nivel_atividade.lower(), 1.55)
#
#     tdee = tmb * fator
#
#     # Ajustar baseado no objetivo
#     objetivo_lower = objetivo.lower()
#     if any(palavra in objetivo_lower for palavra in ['perder', 'emagrecer']):
#         calorias = tdee * 0.85
#         enfase = "Deficit calórico para perda de gordura"
#     elif any(palavra in objetivo_lower for palavra in ['ganhar', 'músculo', 'massa']):
#         calorias = tdee * 1.15
#         enfase = "Superávit calórico para ganho muscular"
#     else:
#         calorias = tdee
#         enfase = "Manutenção corporal"
#
#     # Arredondar
#     calorias = round(calorias / 50) * 50
#
#     # Distribuição de macros
#     proteinas = round(2.0 * peso)
#     gorduras = round(0.9 * peso)
#     carboidratos = round((calorias - (proteinas * 4 + gorduras * 9)) / 4)
#
#     # Dietas por objetivo
#     dietas = {
#         "emagrecimento": {
#             "cafe_manha": "Omelete de 3 claras + 1 gema com espinafre + 1 fatia pão integral",
#             "lanche_manha": "Iogurte grego natural + 1 colher chia + 5 morangos",
#             "almoco": "150g peito de frango grelhado + 100g arroz integral + salada verde à vontade",
#             "lanche_tarde": "Whey protein com água + 1 maçã",
#             "jantar": "150g filé de peixe + 150g batata doce + brócolis no vapor",
#             "ceia": "Chá verde ou chá de camomila",
#             "hidratacao": "3L de água ao longo do dia"
#         },
#         "hipertrofia": {
#             "cafe_manha": "4 ovos mexidos + 2 fatias pão integral + 1 banana + 1 colher pasta amendoim",
#             "lanche_manha": "Shake: Whey protein + 50g aveia + 200ml leite + 1 banana",
#             "almoco": "200g carne moída magra + 150g arroz + feijão + legumes variados",
#             "lanche_tarde": "Sanduíche: Pão integral + frango desfiado + queijo cottage + alface",
#             "jantar": "200g bife bovino + 200g batata inglesa + salada colorida",
#             "ceia": "Caseína ou iogurte grego + 10g pasta amendoim",
#             "hidratacao": "4L de água ao longo do dia"
#         },
#         "definicao": {
#             "cafe_manha": "3 ovos pochê + 1 fatia pão integral + 1/2 abacate pequeno",
#             "lanche_manha": "Iogurte natural + 20g granola sem açúcar + 5 amêndoas",
#             "almoco": "180g filé de tilápia + 100g quinoa + salada de folhas verdes",
#             "lanche_tarde": "Whey protein com água + 1 pera",
#             "jantar": "180g patinho grelhado + abóbora assada + aspargos",
#             "ceia": "Chá de gengibre ou 1 copo leite desnatado",
#             "hidratacao": "3.5L de água ao longo do dia"
#         },
#         "manutencao": {
#             "cafe_manha": "2 ovos mexidos + 2 fatias pão integral + 1 fatia queijo + 1 fruta",
#             "lanche_manha": "1 potinho iogurte + 1 colher mel + 1 punhado castanhas",
#             "almoco": "150g frango + 120g arroz + lentilha + salada mista",
#             "lanche_tarde": "1 sanduíche natural + suco verde",
#             "jantar": "150g peixe + 150g batata doce + legumes refogados",
#             "ceia": "Chá de ervas ou 1 copo leite",
#             "hidratacao": "2.5L de água ao longo do dia"
#         }
#     }
#
#     # Selecionar dieta baseada no objetivo
#     if any(palavra in objetivo_lower for palavra in ['perder', 'emagrecer']):
#         dieta_tipo = "emagrecimento"
#     elif any(palavra in objetivo_lower for palavra in ['ganhar', 'músculo', 'massa']):
#         dieta_tipo = "hipertrofia"
#     elif any(palavra in objetivo_lower for palavra in ['definir', 'definição']):
#         dieta_tipo = "definicao"
#     else:
#         dieta_tipo = "manutencao"
#
#     dieta_base = dietas[dieta_tipo]
#
#     return {
#         "calorias_diarias": calorias,
#         "macros": {
#             "proteinas_g": proteinas,
#             "carboidratos_g": carboidratos,
#             "gorduras_g": gorduras
#         },
#         "refeicoes": dieta_base,
#         "enfase": enfase,
#         "observacoes": f"Dieta ajustada para {objetivo}. Ajustar quantidades conforme evolução."
#     }