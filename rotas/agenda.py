from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from database import get_db_connection, get_db_cursor
import json
import os

bp = Blueprint('agenda', __name__)


@bp.route('/agenda')
def agenda_page():
    """Página principal da agenda"""
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('all_my_training.html')


@bp.route('/api/atividades_disponiveis')
def atividades_disponiveis():
    """Retorna atividades disponíveis para agenda"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    atividades = [
        {
            'id': 'treino_superior',
            'nome': 'Treino Superior (Peito/Tríceps)',
            'tipo': 'treino',
            'descricao': 'Treino focado em peito e tríceps'
        },
        {
            'id': 'treino_inferior',
            'nome': 'Treino Inferior (Pernas/Glúteos)',
            'tipo': 'treino',
            'descricao': 'Treino focado em pernas e glúteos'
        },
        {
            'id': 'treino_core',
            'nome': 'Treino Core (Abdômen)',
            'tipo': 'treino',
            'descricao': 'Treino focado em abdômen e core'
        },
        {
            'id': 'dieta_manha',
            'nome': 'Refeição da Manhã',
            'tipo': 'dieta',
            'descricao': 'Café da manhã balanceado'
        },
        {
            'id': 'dieta_tarde',
            'nome': 'Refeição da Tarde',
            'tipo': 'dieta',
            'descricao': 'Almoço nutritivo'
        },
        {
            'id': 'descanso',
            'nome': 'Dia de Descanso',
            'tipo': 'descanso',
            'descricao': 'Recuperação ativa'
        }
    ]

    return jsonify({
        'success': True,
        'atividades': atividades
    })


@bp.route('/api/salvar_agenda', methods=['POST'])
def salvar_agenda():
    """Salva agenda CORRIGIDA - sem problemas de array"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    try:
        data = request.get_json()
        user_id = session['user_id']

        print(f"Dados recebidos para agenda: {data}")

        # Validação
        if 'itens_agenda' not in data or not data['itens_agenda']:
            return jsonify({'error': 'Nenhum item de agenda enviado'}), 400

        atividade_nome = data.get('atividade_nome', 'Treino Personalizado')
        atividade_tipo = data.get('tipo_atividade', 'treino')  # string simples, não array

        # Buscar treino atual do usuário
        conn = get_db_connection()
        cur = get_db_cursor(conn)

        # Buscar o treino mais recente
        cur.execute("""
            SELECT id_treino 
            FROM treino 
            WHERE id_cadastro = %s 
            ORDER BY id_treino DESC 
            LIMIT 1
        """, (user_id,))

        treino_result = cur.fetchone()

        if not treino_result:
            cur.close()
            conn.close()
            return jsonify({'error': 'Crie um treino primeiro'}), 400

        treino_id = treino_result['id_treino']

        # Limpar agenda existente para este usuário/treino
        cur.execute("""
            DELETE FROM agenda 
            WHERE id_cadastro = %s AND id_treino = %s
        """, (user_id, treino_id))

        # Salvar novos itens da agenda
        itens_salvos = 0
        for item in data['itens_agenda']:
            horario = item.get('horario')
            dia_semana = item.get('dia_semana')

            if not horario or not dia_semana:
                continue

            # INSERÇÃO CORRIGIDA - atividade_tipo como string simples
            cur.execute("""
                INSERT INTO agenda 
                (id_treino, id_cadastro, horario, dia_semana, atividade_tipo, atividade_nome)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                treino_id,
                user_id,
                horario,
                dia_semana,
                atividade_tipo,  # string simples
                atividade_nome
            ))
            itens_salvos += 1

        conn.commit()

        return jsonify({
            'success': True,
            'message': f'Agenda salva com sucesso! {itens_salvos} dias programados.',
            'treino_id': treino_id,
            'itens_salvos': itens_salvos,
            'atividade': atividade_nome
        })

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Erro ao salvar agenda: {e}")
        return jsonify({'error': f'Erro ao salvar agenda: {str(e)}'}), 500
    finally:
        try:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
        except:
            pass


@bp.route('/api/carregar_agenda')
def carregar_agenda():
    """Carrega a agenda do usuário - VERSÃO SIMPLIFICADA"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        # Consulta SIMPLIFICADA - sem join complexo
        cur.execute("""
            SELECT a.horario, a.dia_semana, a.atividade_nome, t.objetivo_usuario
            FROM agenda a 
            LEFT JOIN treino t ON a.id_treino = t.id_treino 
            WHERE a.id_cadastro = %s
            ORDER BY 
                CASE a.dia_semana
                    WHEN 'Domingo' THEN 1
                    WHEN 'Segunda-feira' THEN 2
                    WHEN 'Terça-feira' THEN 3
                    WHEN 'Quarta-feira' THEN 4
                    WHEN 'Quinta-feira' THEN 5
                    WHEN 'Sexta-feira' THEN 6
                    WHEN 'Sábado' THEN 7
                END,
                a.horario
        """, (user_id,))

        agenda_data = cur.fetchall()

        agenda_organizada = {
            'Domingo': [], 'Segunda-feira': [], 'Terça-feira': [],
            'Quarta-feira': [], 'Quinta-feira': [], 'Sexta-feira': [], 'Sábado': []
        }

        for item in agenda_data:
            dia = item['dia_semana']
            if dia in agenda_organizada:
                agenda_organizada[dia].append({
                    'horario': item['horario'] or '--:--',
                    'treino': item['atividade_nome'] or 'Treino',
                    'objetivo': item['objetivo_usuario'] or 'Treino personalizado',
                    'icone': 'images/icons_agenda/mdi_dumbbell.svg'
                })

        # Calcular estatísticas
        total_atividades = sum(len(atividades) for atividades in agenda_organizada.values())
        dias_com_atividade = sum(1 for atividades in agenda_organizada.values() if len(atividades) > 0)

        return jsonify({
            'success': True,
            'agenda': agenda_organizada,
            'total_atividades': total_atividades,
            'dias_com_atividade': dias_com_atividade
        })

    except Exception as e:
        print(f"Erro ao carregar agenda: {e}")
        return jsonify({'error': f'Erro ao carregar agenda: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()


@bp.route('/api/limpar_agenda', methods=['POST'])
def limpar_agenda():
    """Limpa toda a agenda do usuário"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        cur.execute("DELETE FROM agenda WHERE id_cadastro = %s", (user_id,))
        conn.commit()

        return jsonify({
            'success': True,
            'message': 'Agenda limpa com sucesso!'
        })

    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao limpar agenda: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()


# from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
# from database import get_db_connection, get_db_cursor
# import json
# import requests
# import os
#
# bp = Blueprint('agenda', __name__)
#
# ICONS_BASE_PATH = 'static/images/icons_agenda'
# os.makedirs(ICONS_BASE_PATH, exist_ok=True)
#
#
# @bp.route('/agenda')
# def agenda_page():
#     """Página principal da agenda"""
#     if 'user_id' not in session:
#         return redirect('/login')
#     return render_template('all_my_training.html')
#
#
# @bp.route('/api/meus_treinos')
# def meus_treinos():
#     """Retorna os treinos do usuário para o select da agenda"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         # Buscar o treino mais recente do usuário
#         cur.execute("""
#             SELECT id_treino, nome_treino, objetivo_usuario
#             FROM treino
#             WHERE id_cadastro = %s
#             ORDER BY id_treino DESC
#             LIMIT 1
#         """, (user_id,))
#
#         treino = cur.fetchone()
#
#         if not treino:
#             return jsonify({
#                 'success': True,
#                 'treinos': [],
#                 'message': 'Nenhum treino encontrado. Crie um treino primeiro.'
#             })
#
#         # Formatar resultado
#         treinos_list = [{
#             'id': treino['id_treino'],
#             'nome': treino['nome_treino'],
#             'objetivo': treino['objetivo_usuario']
#         }]
#
#         return jsonify({
#             'success': True,
#             'treinos': treinos_list,
#             'default_treino_id': treino['id_treino']
#         })
#
#     except Exception as e:
#         print(f"Erro ao buscar treinos: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cur.close()
#         conn.close()
#
#
# @bp.route('/api/treinos_disponiveis_agenda')
# def treinos_disponiveis_agenda():
#     """Retorna atividades disponíveis para agenda"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     user_id = session['user_id']
#
#     try:
#         # Dados de exemplo - você pode substituir por dados reais do banco
#         atividades = [
#             {
#                 'id': 'treino_upper_a',
#                 'nome': 'Treino Superior A (Peito/Tríceps)',
#                 'tipo': 'treino',
#                 'descricao': 'Treino focado em peito e tríceps',
#                 'icone': 'mdi:dumbbell'
#             },
#             {
#                 'id': 'treino_lower_a',
#                 'nome': 'Treino Inferior A (Pernas/Glúteos)',
#                 'tipo': 'treino',
#                 'descricao': 'Treino focado em pernas e glúteos',
#                 'icone': 'mdi:run'
#             },
#             {
#                 'id': 'treino_core',
#                 'nome': 'Treino Core (Abdômen)',
#                 'tipo': 'treino',
#                 'descricao': 'Treino focado em abdômen e core',
#                 'icone': 'mdi:yoga'
#             },
#             {
#                 'id': 'dieta_manha',
#                 'nome': 'Refeição da Manhã',
#                 'tipo': 'dieta',
#                 'descricao': 'Café da manhã balanceado',
#                 'icone': 'mdi:food-apple'
#             },
#             {
#                 'id': 'dieta_tarde',
#                 'nome': 'Refeição da Tarde',
#                 'tipo': 'dieta',
#                 'descricao': 'Almoço nutritivo',
#                 'icone': 'mdi:food'
#             },
#             {
#                 'id': 'descanso',
#                 'nome': 'Dia de Descanso',
#                 'tipo': 'descanso',
#                 'descricao': 'Recuperação ativa',
#                 'icone': 'mdi:sleep'
#             }
#         ]
#
#         return jsonify({
#             'success': True,
#             'atividades': atividades,
#             'user_id': user_id
#         })
#
#     except Exception as e:
#         print(f"Erro ao buscar atividades: {e}")
#         return jsonify({'error': str(e)}), 500
#
#
# @bp.route('/api/salvar_agenda', methods=['POST'])
# def salvar_agenda():
#     """Salva agenda com atividades selecionadas - VERSÃO CORRIGIDA"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     try:
#         data = request.get_json()
#         user_id = session['user_id']
#
#         print(f"Dados recebidos para agenda: {data}")
#
#         # Validação dos dados
#         if 'itens_agenda' not in data:
#             return jsonify({'error': 'Nenhum item de agenda enviado'}), 400
#
#         # Buscar treino atual do usuário
#         conn = get_db_connection()
#         cur = get_db_cursor(conn)
#
#         cur.execute("""
#             SELECT id_treino FROM treino
#             WHERE id_cadastro = %s
#             ORDER BY id_treino DESC
#             LIMIT 1
#         """, (user_id,))
#
#         treino_result = cur.fetchone()
#
#         if not treino_result:
#             cur.close()
#             conn.close()
#             return jsonify({'error': 'Crie um treino primeiro'}), 400
#
#         treino_id = treino_result['id_treino']
#         atividade_nome = data.get('atividade_nome', 'Treino Personalizado')
#         atividade_tipo = data.get('tipo_atividade', 'treino')
#
#         # Limpar agenda existente para este usuário/treino
#         cur.execute("""
#             DELETE FROM agenda
#             WHERE id_cadastro = %s AND id_treino = %s
#         """, (user_id, treino_id))
#
#         # Salvar novos itens da agenda
#         itens_salvos = 0
#         for item in data['itens_agenda']:
#             horario = item.get('horario')
#             dia_semana = item.get('dia_semana')
#
#             if not horario or not dia_semana:
#                 continue
#
#             cur.execute("""
#                 INSERT INTO agenda
#                 (id_treino, id_cadastro, horario, dia_semana, atividade_tipo, atividade_nome)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             """, (
#                 treino_id,
#                 user_id,
#                 horario,
#                 dia_semana,
#                 atividade_tipo,
#                 atividade_nome
#             ))
#             itens_salvos += 1
#
#         conn.commit()
#
#         return jsonify({
#             'success': True,
#             'message': f'Agenda salva com sucesso! {itens_salvos} dias programados.',
#             'treino_id': treino_id,
#             'itens_salvos': itens_salvos,
#             'atividade': atividade_nome
#         })
#
#     except Exception as e:
#         if 'conn' in locals():
#             conn.rollback()
#         print(f"Erro ao salvar agenda: {e}")
#         return jsonify({'error': f'Erro ao salvar agenda: {str(e)}'}), 500
#     finally:
#         try:
#             if 'cur' in locals():
#                 cur.close()
#             if 'conn' in locals():
#                 conn.close()
#         except:
#             pass
#
#
# @bp.route('/api/carregar_agenda')
# def carregar_agenda():
#     """Carrega a agenda do usuário"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         cur.execute("""
#             SELECT a.*, t.objetivo_usuario, t.nome_treino
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
#         agenda_data = cur.fetchall()
#
#         agenda_organizada = {
#             'Domingo': [], 'Segunda-feira': [], 'Terça-feira': [],
#             'Quarta-feira': [], 'Quinta-feira': [], 'Sexta-feira': [], 'Sábado': []
#         }
#
#         for item in agenda_data:
#             dia = item['dia_semana']
#             if dia in agenda_organizada:
#                 agenda_organizada[dia].append({
#                     'horario': item['horario'],
#                     'treino': item.get('atividade_nome', item['nome_treino']),
#                     'objetivo': item['objetivo_usuario'],
#                     'id_treino': item['id_treino'],
#                     'tipo': item.get('atividade_tipo', 'treino'),
#                     'icone': get_icon_for_activity(
#                         item.get('atividade_nome', item['nome_treino']),
#                         item['objetivo_usuario']
#                     )
#                 })
#
#         # Calcular estatísticas
#         total_atividades = sum(len(atividades) for atividades in agenda_organizada.values())
#         dias_com_atividade = sum(1 for atividades in agenda_organizada.values() if len(atividades) > 0)
#
#         return jsonify({
#             'success': True,
#             'agenda': agenda_organizada,
#             'total_atividades': total_atividades,
#             'dias_com_atividade': dias_com_atividade,
#             'user_id': user_id
#         })
#
#     except Exception as e:
#         print(f"Erro ao carregar agenda: {e}")
#         return jsonify({'error': f'Erro ao carregar agenda: {str(e)}'}), 500
#     finally:
#         cur.close()
#         conn.close()
#
#
# def get_icon_for_activity(nome_atividade, objetivo):
#     """Retorna o ícone apropriado para a atividade"""
#     nome_lower = nome_atividade.lower() if nome_atividade else ''
#     objetivo_lower = objetivo.lower() if objetivo else ''
#
#     # Mapeamento de ícones
#     if any(word in nome_lower for word in ['peito', 'tríceps', 'supino', 'flexão', 'push']):
#         return 'images/icons_agenda/mdi_chest.svg'
#     elif any(word in nome_lower for word in ['costas', 'bíceps', 'remada', 'puxada', 'pull']):
#         return 'images/icons_agenda/mdi_back.svg'
#     elif any(word in nome_lower for word in ['perna', 'glúteo', 'agachamento', 'squat', 'leg']):
#         return 'images/icons_agenda/mdi_leg.svg'
#     elif any(word in nome_lower for word in ['ombro', 'shoulder', 'desenvolvimento']):
#         return 'images/icons_agenda/mdi_shoulder.svg'
#     elif any(word in nome_lower for word in ['abdômen', 'core', 'abdominal', 'prancha']):
#         return 'images/icons_agenda/mdi_abs.svg'
#     elif any(word in nome_lower for word in ['cardio', 'corrida', 'burpee', 'jump']):
#         return 'images/icons_agenda/mdi_cardio.svg'
#     elif any(word in nome_lower for word in ['dieta', 'refeição', 'alimentação', 'comida']):
#         return 'images/icons_agenda/mdi_food.svg'
#     elif any(word in nome_lower for word in ['descanso', 'recuperação']):
#         return 'images/icons_agenda/mdi_sleep.svg'
#     else:
#         return 'images/icons_agenda/mdi_dumbbell.svg'


# from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
# from database import get_db_connection, get_db_cursor
# import json
# import requests
# import os
# 
# bp = Blueprint('agenda', __name__)
# 
# ICONS_BASE_PATH = 'static/images/icons_agenda'
# ICONS_API_URL = "https://api.iconify.design"
# 
# os.makedirs(ICONS_BASE_PATH, exist_ok=True)
# 
# 
# @bp.route('/agenda')
# def agenda_page():
#     """Página principal da agenda"""
#     if 'user_id' not in session:
#         return redirect('/login')
#     return render_template('all_my_training.html')
# 
# 
# @bp.route('/api/meus_treinos')
# def meus_treinos():
#     """Retorna os treinos do usuário para o select da agenda - VERSÃO CORRIGIDA"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
# 
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
# 
#     try:
#         # Buscar todos os treinos do usuário
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
#                 'id': treino['id_treino'],
#                 'nome': treino['nome_treino'],
#                 'objetivo': treino['objetivo_usuario']
#             })
# 
#         return jsonify({
#             'success': True,
#             'treinos': treinos_list,
#             'total': len(treinos_list)
#         })
# 
#     except Exception as e:
#         print(f"Erro ao buscar treinos: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cur.close()
#         conn.close()
# 
# 
# @bp.route('/api/salvar_agenda', methods=['POST'])
# def salvar_agenda():
#     """Salva agenda com múltiplas opções de treino - VERSÃO CORRIGIDA"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
# 
#     try:
#         data = request.get_json()
#         user_id = session['user_id']
# 
#         print(f"Dados recebidos para agenda: {data}")  # DEBUG
# 
#         # Validação dos dados
#         if 'itens_agenda' not in data:
#             return jsonify({'error': 'Nenhum item de agenda enviado'}), 400
# 
#         treino_id = data.get('treino_id')
#         if not treino_id:
#             return jsonify({'error': 'Treino não selecionado'}), 400
# 
#         conn = get_db_connection()
#         cur = get_db_cursor(conn)
# 
#         # Verificar se o treino pertence ao usuário
#         cur.execute("""
#             SELECT id_treino FROM treino
#             WHERE id_treino = %s AND id_cadastro = %s
#         """, (treino_id, user_id))
# 
#         if not cur.fetchone():
#             cur.close()
#             conn.close()
#             return jsonify({'error': 'Treino não pertence ao usuário'}), 403
# 
#         # Limpar agenda existente para este treino
#         cur.execute("""
#             DELETE FROM agenda 
#             WHERE id_treino = %s AND id_cadastro = %s
#         """, (treino_id, user_id))
# 
#         # Salvar novos itens da agenda
#         itens_salvos = 0
#         for item in data['itens_agenda']:
#             horario = item.get('horario')
#             dia_semana = item.get('dia_semana')
# 
#             if not horario or not dia_semana:
#                 continue  # Pular itens incompletos
# 
#             # Verificar se já existe um agendamento para este horário/dia
#             cur.execute("""
#                 SELECT id_agenda FROM agenda
#                 WHERE id_cadastro = %s 
#                 AND dia_semana = %s 
#                 AND horario = %s
#             """, (user_id, dia_semana, horario))
# 
#             if cur.fetchone():
#                 # Atualizar existente
#                 cur.execute("""
#                     UPDATE agenda 
#                     SET id_treino = %s
#                     WHERE id_cadastro = %s 
#                     AND dia_semana = %s 
#                     AND horario = %s
#                 """, (treino_id, user_id, dia_semana, horario))
#             else:
#                 # Inserir novo
#                 cur.execute("""
#                     INSERT INTO agenda 
#                     (id_treino, id_cadastro, horario, dia_semana)
#                     VALUES (%s, %s, %s, %s)
#                 """, (treino_id, user_id, horario, dia_semana))
# 
#             itens_salvos += 1
# 
#         conn.commit()
# 
#         return jsonify({
#             'success': True,
#             'message': f'Agenda salva com sucesso! {itens_salvos} itens salvos.',
#             'treino_id': treino_id,
#             'itens_salvos': itens_salvos
#         })
# 
#     except Exception as e:
#         if 'conn' in locals():
#             conn.rollback()
#         print(f"Erro ao salvar agenda: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Erro ao salvar agenda: {str(e)}'}), 500
#     finally:
#         try:
#             if 'cur' in locals():
#                 cur.close()
#             if 'conn' in locals():
#                 conn.close()
#         except:
#             pass
# 
# 
# @bp.route('/api/carregar_agenda')
# def carregar_agenda():
#     """Carrega a agenda do usuário - VERSÃO CORRIGIDA"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
# 
#     user_id = session['user_id']
# 
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
# 
#     try:
#         cur.execute("""
#             SELECT a.*, t.objetivo_usuario, t.nome_treino
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
#         agenda_data = cur.fetchall()
# 
#         agenda_organizada = {
#             'Domingo': [], 'Segunda-feira': [], 'Terça-feira': [],
#             'Quarta-feira': [], 'Quinta-feira': [], 'Sexta-feira': [], 'Sábado': []
#         }
# 
#         for item in agenda_data:
#             dia = item['dia_semana']
#             if dia in agenda_organizada:
#                 agenda_organizada[dia].append({
#                     'horario': item['horario'],
#                     'treino': item['nome_treino'],
#                     'objetivo': item['objetivo_usuario'],
#                     'id_treino': item['id_treino'],
#                     'icone': f"images/icons_agenda/mdi_dumbbell.svg"
#                 })
# 
#         # Calcular estatísticas
#         total_atividades = sum(len(atividades) for atividades in agenda_organizada.values())
#         dias_com_atividade = sum(1 for atividades in agenda_organizada.values() if len(atividades) > 0)
# 
#         return jsonify({
#             'success': True,
#             'agenda': agenda_organizada,
#             'total_atividades': total_atividades,
#             'dias_com_atividade': dias_com_atividade,
#             'user_id': user_id
#         })
# 
#     except Exception as e:
#         print(f"Erro ao carregar agenda: {e}")
#         return jsonify({'error': f'Erro ao carregar agenda: {str(e)}'}), 500
#     finally:
#         cur.close()
#         conn.close()
# 
# 
# @bp.route('/api/limpar_agenda', methods=['POST'])
# def limpar_agenda():
#     """Limpa toda a agenda do usuário"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
# 
#     user_id = session['user_id']
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
# 
#     try:
#         cur.execute("DELETE FROM agenda WHERE id_cadastro = %s", (user_id,))
#         conn.commit()
# 
#         return jsonify({
#             'success': True,
#             'message': 'Agenda limpa com sucesso!'
#         })
# 
#     except Exception as e:
#         conn.rollback()
#         return jsonify({'error': f'Erro ao limpar agenda: {str(e)}'}), 500
#     finally:
#         cur.close()
#         conn.close()
# 
# 
# def get_icon_for_activity(nome_treino, objetivo):
#     nome_lower = nome_treino.lower() if nome_treino else ''
#     objetivo_lower = objetivo.lower() if objetivo else ''
# 
#     if any(word in nome_lower for word in ['corrida', 'cardio', 'aerobico']):
#         return 'mdi:run'
#     elif any(word in nome_lower for word in ['musculação', 'força', 'peso']):
#         return 'mdi:dumbbell'
#     elif any(word in nome_lower for word in ['yoga', 'meditação']):
#         return 'mdi:yoga'
#     elif any(word in nome_lower for word in ['boxe', 'luta']):
#         return 'mdi:boxing-glove'
#     elif any(word in nome_lower for word in ['alimentação', 'dieta']):
#         return 'mdi:food-apple'
#     elif any(word in nome_lower for word in ['descanso']):
#         return 'mdi:sleep'
#     else:
#         return 'mdi:exercise'

# from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
# from database import get_db_connection, get_db_cursor
# import json
# import requests
# import os
#
# bp = Blueprint('agenda', __name__)
#
# ICONS_BASE_PATH = 'static/images/icons_agenda'
# ICONS_API_URL = "https://api.iconify.design"
#
# os.makedirs(ICONS_BASE_PATH, exist_ok=True)
#
#
# @bp.route('/api/meus_treinos')
# def meus_treinos():
#     """Retorna os treinos do usuário para o select da agenda"""
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
#             ORDER BY nome_treino
#         """, (user_id,))
#
#         treinos = cur.fetchall()
#
#         treinos_list = []
#         for treino in treinos:
#             treinos_list.append({
#                 'id': treino['id_treino'],
#                 'nome': treino['nome_treino'],
#                 'objetivo': treino['objetivo_usuario']
#             })
#
#         return jsonify({
#             'success': True,
#             'treinos': treinos_list
#         })
#
#     except Exception as e:
#         print(f"Erro ao buscar treinos: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cur.close()
#         conn.close()
#
#
# @bp.route('/api/salvar_agenda', methods=['POST'])
# def salvar_agenda():
#     """Salva agenda com múltiplas opções de treino"""
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     data = request.get_json()
#     user_id = session['user_id']
#
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         # Agora podemos receber tanto id_treino quanto tipo_atividade
#         tipo_atividade = data.get('tipo_atividade')
#         atividade_nome = data.get('atividade_nome', 'Treino')
#         atividade_desc = data.get('atividade_desc', '')
#
#         # Buscar o treino mais recente do usuário
#         cur.execute("""
#             SELECT id_treino FROM treino
#             WHERE id_cadastro = %s
#             ORDER BY id_treino DESC LIMIT 1
#         """, (user_id,))
#
#         treino_result = cur.fetchone()
#
#         if not treino_result:
#             return jsonify({'error': 'Crie um treino primeiro'}), 400
#
#         treino_id = treino_result['id_treino']
#
#         # Limpar agenda existente para este treino
#         cur.execute("DELETE FROM agenda WHERE id_treino = %s", (treino_id,))
#
#         # Salvar novos itens da agenda
#         itens_salvos = 0
#         for item in data.get('itens_agenda', []):
#             cur.execute("""
#                 INSERT INTO agenda
#                 (id_treino, id_cadastro, horario, dia_semana, atividade_tipo, atividade_nome)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             """, (
#                 treino_id,
#                 user_id,
#                 item.get('horario', '08:00'),
#                 item.get('dia_semana', 'Segunda-feira'),
#                 tipo_atividade or 'treino',
#                 atividade_nome
#             ))
#             itens_salvos += 1
#
#         conn.commit()
#
#         return jsonify({
#             'success': True,
#             'message': 'Agenda salva com sucesso',
#             'treino_id': treino_id,
#             'itens_salvos': itens_salvos,
#             'atividade': atividade_nome
#         })
#
#     except Exception as e:
#         conn.rollback()
#         print(f"Erro ao salvar agenda: {e}")
#         return jsonify({'error': f'Erro ao salvar agenda: {str(e)}'}), 500
#     finally:
#         cur.close()
#         conn.close()
#
#
# # @bp.route('/api/salvar_agenda', methods=['POST'])
# # def salvar_agenda():
# #     if 'user_id' not in session:
# #         return jsonify({'error': 'Usuário não logado'}), 401
# #
# #     data = request.get_json()
# #     user_id = session['user_id']
# #
# #     conn = get_db_connection()
# #     cur = get_db_cursor(conn)
# #
# #     try:
# #         treino_id = data.get('treino_id')
# #         if not treino_id:
# #             return jsonify({'error': 'Treino não selecionado'}), 400
# #
# #         # Verificar se o treino pertence ao usuário
# #         cur.execute("""
# #             SELECT id_treino FROM treino
# #             WHERE id_treino = %s AND id_cadastro = %s
# #         """, (treino_id, user_id))
# #
# #         if not cur.fetchone():
# #             return jsonify({'error': 'Treino não pertence ao usuário'}), 403
# #
# #         # Limpar agenda existente para este treino
# #         cur.execute("DELETE FROM agenda WHERE id_treino = %s", (treino_id,))
# #
# #         # Salvar novos itens
# #         itens_salvos = 0
# #         for item in data.get('itens_agenda', []):
# #             cur.execute("""
# #                 INSERT INTO agenda
# #                 (id_treino, id_cadastro, horario, dia_semana)
# #                 VALUES (%s, %s, %s, %s)
# #             """, (
# #                 treino_id,
# #                 user_id,
# #                 item.get('horario', '08:00'),
# #                 item.get('dia_semana', 'Segunda-feira')
# #             ))
# #             itens_salvos += 1
# #
# #         conn.commit()
# #
# #         return jsonify({
# #             'success': True,
# #             'message': 'Agenda salva com sucesso',
# #             'treino_id': treino_id,
# #             'itens_salvos': itens_salvos
# #         })
# #
# #     except Exception as e:
# #         conn.rollback()
# #         return jsonify({'error': f'Erro ao salvar agenda: {str(e)}'}), 500
# #     finally:
# #         cur.close()
# #         conn.close()
#
# @bp.route('/api/carregar_agenda')
# def carregar_agenda():
#     if 'user_id' not in session:
#         return jsonify({'error': 'Usuário não logado'}), 401
#
#     user_id = session['user_id']
#
#     conn = get_db_connection()
#     cur = get_db_cursor(conn)
#
#     try:
#         cur.execute("""
#             SELECT a.*, t.objetivo_usuario, t.nome_treino
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
#         agenda_data = cur.fetchall()
#
#         agenda_organizada = {
#             'Domingo': [], 'Segunda-feira': [], 'Terça-feira': [],
#             'Quarta-feira': [], 'Quinta-feira': [], 'Sexta-feira': [], 'Sábado': []
#         }
#
#         for item in agenda_data:
#             dia = item['dia_semana']
#             agenda_organizada[dia].append({
#                 'horario': item['horario'],
#                 'treino': item['nome_treino'],
#                 'objetivo': item['objetivo_usuario'],
#                 'icone': f"images/icons_agenda/mdi_dumbbell.svg"
#             })
#
#         return jsonify({
#             'success': True,
#             'agenda': agenda_organizada,
#             'total_atividades': len(agenda_data)
#         })
#
#     except Exception as e:
#         return jsonify({'error': f'Erro ao carregar agenda: {str(e)}'}), 500
#     finally:
#         cur.close()
#         conn.close()
#
#
# def get_icon_for_activity(nome_treino, objetivo):
#     nome_lower = nome_treino.lower() if nome_treino else ''
#     objetivo_lower = objetivo.lower() if objetivo else ''
#
#     if any(word in nome_lower for word in ['corrida', 'cardio', 'aerobico']):
#         return 'mdi:run'
#     elif any(word in nome_lower for word in ['musculação', 'força', 'peso']):
#         return 'mdi:dumbbell'
#     elif any(word in nome_lower for word in ['yoga', 'meditação']):
#         return 'mdi:yoga'
#     elif any(word in nome_lower for word in ['boxe', 'luta']):
#         return 'mdi:boxing-glove'
#     elif any(word in nome_lower for word in ['alimentação', 'dieta']):
#         return 'mdi:food-apple'
#     elif any(word in nome_lower for word in ['descanso']):
#         return 'mdi:sleep'
#     else:
#         return 'mdi:exercise'
