from flask import Blueprint, render_template, session, redirect, flash, request
import psycopg2
from database import get_db_connection
import requests
import re
import os

import sys
import io

# Configurar encoding para evitar problemas com caracteres
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

galeria_bp = Blueprint('galeria', __name__)

# def get_db_connection():
#     # Use a mesma função de conexão do seu projeto
#     conn = psycopg2.connect(
#         host='localhost',
#         database='MetaFit',
#         user='postgres',
#         password='senai'
#     )
#     return conn

# Funções de geolocalização
# import requests
# import re


def codigo_postal_para_endereco(codigo_postal, pais=None):
    """
    Converte código postal para endereço usando OpenStreetMap Nominatim
    Funciona mundialmente
    """
    try:
        # Limpar o código postal
        codigo_limpo = codigo_postal.strip()

        # Se for um CEP brasileiro, usar API específica
        if re.match(r'^\d{5}-?\d{3}$', codigo_limpo):
            return cep_brasileiro(codigo_limpo)

        # Para outros países, usar OpenStreetMap Nominatim
        return consulta_global(codigo_limpo, pais)

    except Exception as e:
        print(f"Erro na consulta do código postal: {e}")
        return "Localização não encontrada"


def cep_brasileiro(cep):
    """Consulta específica para CEP brasileiro"""
    try:
        cep_limpo = cep.replace('-', '')
        url = f'https://viacep.com.br/ws/{cep_limpo}/json/'
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()
            if 'erro' not in dados:
                cidade = dados.get('localidade', '')
                estado = dados.get('uf', '')
                return f"{cidade}, {estado}" if cidade and estado else cidade

        return "CEP não encontrado"
    except:
        return "Erro na consulta"


def consulta_global(codigo_postal, pais=None):
    """Consulta global usando OpenStreetMap Nominatim"""
    try:
        # Construir query base
        query = codigo_postal

        # Adicionar país se especificado
        if pais:
            query = f"{codigo_postal}, {pais}"

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1
        }

        headers = {
            'User-Agent': 'MetaFitAcademia/1.0 (contato@metafit.com)'
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            dados = response.json()

            if dados:
                endereco = dados[0].get('address', {})

                # Tentar diferentes níveis de detalhe
                cidade = (endereco.get('city') or
                          endereco.get('town') or
                          endereco.get('village') or
                          endereco.get('municipality'))

                estado = (endereco.get('state') or
                          endereco.get('region'))

                pais_nome = endereco.get('country')

                # Montar resposta
                partes = []
                if cidade:
                    partes.append(cidade)
                if estado:
                    partes.append(estado)
                if pais_nome and not pais:
                    partes.append(pais_nome)

                return ", ".join(partes) if partes else "Localização encontrada"

        return "Localização não encontrada"

    except Exception as e:
        print(f"Erro na consulta global: {e}")
        return "Erro na consulta"


def detectar_pais_por_codigo(codigo_postal):
    """
    Tenta detectar o país baseado no formato do código postal
    """
    codigo_limpo = codigo_postal.replace(' ', '').replace('-', '').upper()

    # Padrões por país
    padroes = {
        'BR': r'^\d{8}$',  # Brasil: 00000000
        'US': r'^\d{5}(?:\d{4})?$',  # EUA: 12345 ou 12345-6789
        'UK': r'^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$',  # UK: SW1A 1AA
        'CA': r'^[A-Z]\d[A-Z] ?\d[A-Z]\d$',  # Canadá: A1A 1A1
        'FR': r'^\d{5}$',  # França: 75007
        'DE': r'^\d{5}$',  # Alemanha: 10117
        'JP': r'^\d{3}-?\d{4}$',  # Japão: 160-0022
        'AU': r'^\d{4}$',  # Austrália: 2000
    }

    for pais, padrao in padroes.items():
        if re.match(padrao, codigo_limpo):
            return pais

    return None


def codigo_postal_global_melhorado(codigo_postal):
    """
    Versão melhorada com detecção automática de país
    """
    try:
        codigo_limpo = codigo_postal.strip()

        # Detectar país automaticamente
        pais_detectado = detectar_pais_por_codigo(codigo_limpo)

        # Se for Brasil, usar API específica
        if pais_detectado == 'BR':
            return cep_brasileiro(codigo_limpo)

        # Para outros países, consulta global
        resultado = consulta_global_melhorada(codigo_limpo, pais_detectado)

        return resultado if resultado else "Localização não encontrada"

    except Exception as e:
        print(f"Erro na consulta: {e}")
        return "Erro na consulta"


def consulta_global_melhorada(codigo_postal, pais=None):
    """Consulta global melhorada"""
    try:
        # Construir query
        if pais:
            query = f"{codigo_postal}, {pais}"
        else:
            query = codigo_postal

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'postalcode': codigo_postal,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1
        }

        if pais:
            params['countrycodes'] = pais.lower()

        headers = {
            'User-Agent': 'MetaFitAcademia/1.0'
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            dados = response.json()

            if dados:
                endereco = dados[0].get('address', {})

                # Extrair informações de localização
                localizacao = extrair_localizacao(endereco)
                return localizacao

        return None

    except Exception as e:
        print(f"Erro na consulta global: {e}")
        return None


def extrair_localizacao(endereco):
    """Extrai informações de localização do endereço"""
    componentes = []

    # Cidade/town/village
    cidade = (endereco.get('city') or
              endereco.get('town') or
              endereco.get('village') or
              endereco.get('municipality'))

    # Estado/região
    estado = (endereco.get('state') or
              endereco.get('region') or
              endereco.get('state_district'))

    # País
    pais = endereco.get('country')

    if cidade:
        componentes.append(cidade)
    if estado:
        componentes.append(estado)
    if pais and len(componentes) == 0:  # Só adiciona país se não tiver cidade/estado
        componentes.append(pais)

    return ", ".join(componentes) if componentes else "Localização encontrada"

# Teste da função
# testes = [
#     "01310-000",    # São Paulo, BR
#     "10001",        # Nova York, US
#     "SW1A 1AA",     # Londres, UK
#     "75007",        # Paris, FR
#     "10117",        # Berlim, DE
#     "160-0022",     # Tóquio, JP
#     "2000",         # Sydney, AU
#     "M5H 2N2",      # Toronto, CA
# ]
#
# for teste in testes:
#     resultado = codigo_postal_global_melhorado(teste)
#     print(f"{teste} → {resultado}")

@galeria_bp.route('/migrar_imagens_forcado')
def migrar_imagens_forcado():
    """Migra TODAS as imagens FORÇADAMENTE para nomes de arquivo"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar todos os usuários
        cur.execute('SELECT id_cadastro, nome_usuario, imagem_usuario FROM cadastrousuarios')
        usuarios = cur.fetchall()

        usuarios_migrados = 0
        usuarios_ja_string = 0

        for usuario in usuarios:
            id_cadastro, nome, imagem = usuario

            # Se é memoryview, converter para nome de arquivo
            if isinstance(imagem, memoryview):
                nome_imagem = f"usuario_{id_cadastro}.jpg"

                cur.execute(
                    'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
                    (nome_imagem, id_cadastro)
                )
                print(f"Migrado: {nome} (ID: {id_cadastro}) -> {nome_imagem}")
                usuarios_migrados += 1

            elif isinstance(imagem, str) and imagem:
                print(f" Já é string: {nome} -> {imagem}")
                usuarios_ja_string += 1

            else:  # None ou vazio
                cur.execute(
                    'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
                    ('default_avatar.png', id_cadastro)
                )
                print(f" Definido padrão: {nome} -> default_avatar.png")
                usuarios_migrados += 1

        conn.commit()
        cur.close()
        conn.close()

        return f"""
        <h1>Migração Forçada Concluída!</h1>
        <p>Usuários migrados: {usuarios_migrados}</p>
        <p>Já eram strings: {usuarios_ja_string}</p>
        <p><a href="/debug_imagens_detalhado">Verificar resultado</a></p>
        """

    except Exception as e:
        return f"Erro na migração: {str(e)}"


# Rotas da Galeria
# @galeria_bp.route('/gallery_adm')
# def gallery_adm():
#     if 'user_id' not in session or session['user_type'] != 'adm':
#         flash('Acesso restrito a administradores!')
#         return redirect('/login')
#
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#
#         # Buscar clientes da galeria com informações dos usuários
#         cur.execute('''
#             SELECT
#                 c.id_clientes,
#                 c.link_rede_social,
#                 u.id_cadastro,
#                 u.nome_usuario,
#                 u.cep_usuario,
#                 u.imagem_usuario
#             FROM clientes c
#             INNER JOIN cadastrousuarios u ON c.id_cadastro = u.id_cadastro
#             ORDER BY u.nome_usuario
#         ''')
#         clientes_galeria = cur.fetchall()
#
#         cur.close()
#         conn.close()
#
#         # Processar localizações
#         clientes_processados = []
#         for cliente in clientes_galeria:
#             id_clientes, link_rede_social, id_cadastro, nome, cep, imagem = cliente
#
#             # Converter CEP em localização
#             localizacao = codigo_postal_global_melhorado(cep) if cep else "Localização não informada"
#
#             # Usar imagem do usuário ou padrão
#             imagem_url = f"../static/images/uploads/{imagem}" if imagem and imagem != 'default_avatar.png' else "../static/images/gallery-1.jpg"
#
#             clientes_processados.append({
#                 'id': id_clientes,
#                 'nome': nome,
#                 'localizacao': localizacao,
#                 'imagem': imagem_url,
#                 'link_rede_social': link_rede_social,
#                 'id_cadastro': id_cadastro
#             })
#
#         return render_template('gallery_adm.html', clientes=clientes_processados)
#
#     except Exception as e:
#         print(f"Erro ao carregar galeria: {e}")
#         flash('Erro ao carregar galeria')
#         return render_template('gallery_adm.html', clientes=[])
#
#
# @galeria_bp.route('/gallery')
# def gallery():
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#
#         # Buscar clientes da galeria (mesma query)
#         cur.execute('''
#             SELECT
#                 u.nome_usuario,
#                 u.cep_usuario,
#                 u.imagem_usuario,
#                 c.link_rede_social
#             FROM clientes c
#             INNER JOIN cadastrousuarios u ON c.id_cadastro = u.id_cadastro
#             ORDER BY u.nome_usuario
#         ''')
#         clientes_galeria = cur.fetchall()
#
#         cur.close()
#         conn.close()
#
#         # Processar localizações
#         clientes_processados = []
#         for cliente in clientes_galeria:
#             nome, cep, imagem, link_rede_social = cliente
#
#             localizacao = codigo_postal_global_melhorado(cep) if cep else "Localização não informada"
#             imagem_url = f"../static/images/uploads/{imagem}" if imagem and imagem != 'default_avatar.png' else "../static/images/gallery-1.jpg"
#
#             clientes_processados.append({
#                 'nome': nome,
#                 'localizacao': localizacao,
#                 'imagem': imagem_url,
#                 'link_rede_social': link_rede_social
#             })
#
#         return render_template('gallery.html', clientes=clientes_processados)
#
#     except Exception as e:
#         print(f"Erro ao carregar galeria pública: {e}")
#         return render_template('gallery.html', clientes=[])

@galeria_bp.route('/gallery_adm')
def gallery_adm():
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            SELECT 
                c.id_clientes,
                c.link_rede_social,
                u.id_cadastro,
                u.nome_usuario,
                u.cep_usuario,
                u.imagem_usuario
            FROM clientes c
            INNER JOIN cadastrousuarios u ON c.id_cadastro = u.id_cadastro
            ORDER BY u.nome_usuario
        ''')
        clientes_galeria = cur.fetchall()

        cur.close()
        conn.close()

        # DEBUG (sem emojis)
        print("=== DEBUG GALLERY ADM ===")

        clientes_processados = []
        for cliente in clientes_galeria:
            id_clientes, link_rede_social, id_cadastro, nome, cep, imagem = cliente

            localizacao = codigo_postal_global_melhorado(cep) if cep else "Localização não informada"

            # CORREÇÃO: Verificar se a imagem existe antes de usar
            if imagem and imagem != 'default_avatar.png':
                caminho_imagem = f"static/images/uploads/{imagem}"
                if os.path.exists(caminho_imagem):
                    imagem_url = f"/static/images/uploads/{imagem}"
                    print(f"ENCONTRADO: {nome}: {imagem_url}")
                else:
                    imagem_url = "/static/images/gallery-1.jpg"
                    print(f"NAO ENCONTRADO: {nome}: Imagem não encontrada - {imagem}")
            else:
                imagem_url = "/static/images/gallery-1.jpg"
                print(f"PADRAO: {nome}: Usando imagem padrão")

            clientes_processados.append({
                'id': id_clientes,
                'nome': nome,
                'localizacao': localizacao,
                'imagem': imagem_url,
                'link_rede_social': link_rede_social,
                'id_cadastro': id_cadastro
            })

        return render_template('gallery_adm.html', clientes=clientes_processados)

    except Exception as e:
        print(f"Erro ao carregar galeria: {e}")
        flash('Erro ao carregar galeria')
        return render_template('gallery_adm.html', clientes=[])


@galeria_bp.route('/gallery')
def gallery():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar clientes da galeria
        cur.execute('''
            SELECT 
                u.nome_usuario,
                u.cep_usuario,
                u.imagem_usuario,
                c.link_rede_social
            FROM clientes c
            INNER JOIN cadastrousuarios u ON c.id_cadastro = u.id_cadastro
            ORDER BY u.nome_usuario
        ''')
        clientes_galeria = cur.fetchall()

        cur.close()
        conn.close()

        # Processar localizações
        clientes_processados = []
        for cliente in clientes_galeria:
            nome, cep, imagem, link_rede_social = cliente

            localizacao = codigo_postal_global_melhorado(cep) if cep else "Localização não informada"

            # SIMPLES: imagem já é string
            if imagem and imagem != 'default_avatar.png':
                imagem_url = f"/static/images/uploads/{imagem}"
            else:
                imagem_url = "/static/images/gallery-1.jpg"

            clientes_processados.append({
                'nome': nome,
                'localizacao': localizacao,
                'imagem': imagem_url,
                'link_rede_social': link_rede_social
            })

        return render_template('gallery.html', clientes=clientes_processados)

    except Exception as e:
        print(f"Erro ao carregar galeria pública: {e}")
        return render_template('gallery.html', clientes=[])


# @galeria_bp.route('/gallery_person_control')
# def gallery_person_control():
#     if 'user_id' not in session or session['user_type'] != 'adm':
#         flash('Acesso restrito a administradores!')
#         return redirect('/login')
#
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#
#         # Buscar todos os usuários cadastrados para o select
#         cur.execute('''
#             SELECT id_cadastro, nome_usuario, cep_usuario
#             FROM cadastrousuarios
#             ORDER BY nome_usuario
#         ''')
#         todos_usuarios = cur.fetchall()
#
#         # Buscar usuários que já estão na galeria
#         cur.execute('SELECT id_cadastro FROM clientes')
#         usuarios_na_galeria = [row[0] for row in cur.fetchall()]
#
#         cur.close()
#         conn.close()
#
#         # Preparar dados para o template
#         usuarios_select = []
#         for usuario in todos_usuarios:
#             id_cadastro, nome, cep = usuario
#             localizacao = codigo_postal_global_melhorado(cep) if cep else "Localização não informada"
#
#             usuarios_select.append({
#                 'id': id_cadastro,
#                 'nome': nome,
#                 'localizacao': localizacao,
#                 'ja_na_galeria': id_cadastro in usuarios_na_galeria
#             })
#
#         return render_template('gallery_person_control.html', usuarios=usuarios_select)
#
#     except Exception as e:
#         print(f"Erro ao carregar controle de galeria: {e}")
#         flash('Erro ao carregar dados')
#         return render_template('gallery_person_control.html', usuarios=[])

@galeria_bp.route('/gallery_person_control')
def gallery_person_control():
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar todos os usuários cadastrados para o select
        cur.execute('''
            SELECT id_cadastro, nome_usuario, cep_usuario, imagem_usuario 
            FROM cadastrousuarios 
            ORDER BY nome_usuario
        ''')
        todos_usuarios = cur.fetchall()

        # Buscar usuários que já estão na galeria
        cur.execute('SELECT id_cadastro FROM clientes')
        usuarios_na_galeria = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        # Preparar dados para o template
        usuarios_select = []
        for usuario in todos_usuarios:
            id_cadastro, nome, cep, imagem = usuario
            localizacao = codigo_postal_global_melhorado(cep) if cep else "Localização não informada"

            # TRATAMENTO PARA AMBOS OS FORMATOS
            imagem_url = "/static/images/gallery-1.jpg"  # Padrão

            if imagem:
                if isinstance(imagem, memoryview):
                    # Se é memoryview, usar imagem padrão
                    imagem_url = "/static/images/gallery-1.jpg"
                elif isinstance(imagem, str) and imagem != 'default_avatar.png':
                    # Se é string válida, usar a imagem
                    imagem_url = f"/static/images/uploads/{imagem}"

            usuarios_select.append({
                'id': id_cadastro,
                'nome': nome,
                'localizacao': localizacao,
                'imagem': imagem_url,
                'ja_na_galeria': id_cadastro in usuarios_na_galeria
            })

        return render_template('gallery_person_control.html', usuarios=usuarios_select)

    except Exception as e:
        print(f"Erro ao carregar controle de galeria: {e}")
        flash('Erro ao carregar dados')
        return render_template('gallery_person_control.html', usuarios=[])


@galeria_bp.route('/adicionar_galeria', methods=['POST'])
def adicionar_galeria():
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')

    id_cadastro = request.form.get('usuario_select')
    link_rede_social = request.form.get('link_rede_social')

    if not id_cadastro or not link_rede_social:
        flash('Preencha todos os campos!')
        return redirect('/gallery_person_control')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar se o usuário já está na galeria
        cur.execute('SELECT id_clientes FROM clientes WHERE id_cadastro = %s', (id_cadastro,))
        existe = cur.fetchone()

        if existe:
            # Atualizar
            cur.execute(
                'UPDATE clientes SET link_rede_social = %s WHERE id_cadastro = %s',
                (link_rede_social, id_cadastro)
            )
            flash('Cliente atualizado na galeria!')
            print(f"ATUALIZADO: Usuario ID {id_cadastro} na galeria")
        else:
            # Inserir novo
            cur.execute(
                'INSERT INTO clientes (link_rede_social, id_cadastro) VALUES (%s, %s)',
                (link_rede_social, id_cadastro)
            )
            flash('Cliente adicionado à galeria!')
            print(f"ADICIONADO: Usuario ID {id_cadastro} à galeria")

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/gallery_adm')

    except Exception as e:
        print(f"ERRO ao adicionar à galeria: {e}")
        flash('Erro ao adicionar cliente à galeria')
        return redirect('/gallery_person_control')


@galeria_bp.route('/debug_imagens')
def debug_imagens():
    """Debug para verificar o estado das imagens"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT id_cadastro, nome_usuario, imagem_usuario FROM cadastrousuarios LIMIT 10')
        usuarios = cur.fetchall()

        resultado = "<h1>Debug - Estado das Imagens</h1>"
        for usuario in usuarios:
            id_cad, nome, imagem = usuario
            resultado += f"""
            <div style='border: 1px solid #ccc; margin: 10px; padding: 10px;'>
                <p><strong>{nome}</strong> (ID: {id_cad})</p>
                <p>Imagem: <code>{imagem}</code></p>
                <p>Tipo: <strong>{type(imagem)}</strong></p>
                <p>É string: <strong>{isinstance(imagem, str)}</strong></p>
                <p>É memoryview: <strong>{isinstance(imagem, memoryview)}</strong></p>
            </div>
            """

        cur.close()
        conn.close()
        return resultado

    except Exception as e:
        return f"Erro: {e}"


@galeria_bp.route('/debug_imagens_detalhado')
def debug_imagens_detalhado():
    """Debug mais detalhado para verificar as imagens"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT id_cadastro, nome_usuario, imagem_usuario FROM cadastrousuarios')
        usuarios = cur.fetchall()

        resultado = "<h1>Debug Detalhado - Estado das Imagens</h1>"

        for usuario in usuarios:
            id_cad, nome, imagem = usuario
            resultado += f"""
            <div style='border: 1px solid #ccc; margin: 10px; padding: 10px;'>
                <p><strong>{nome}</strong> (ID: {id_cad})</p>
                <p>Tipo: <strong>{type(imagem)}</strong></p>
                <p>É string: <strong>{isinstance(imagem, str)}</strong></p>
                <p>É memoryview: <strong>{isinstance(imagem, memoryview)}</strong></p>
                <p>É None: <strong>{imagem is None}</strong></p>
            """

            if isinstance(imagem, memoryview):
                resultado += f"<p style='color: red;'><strong>PROBLEMA: É MEMORYVIEW (BLOB)</strong></p>"
                try:
                    # Tentar converter para ver o conteúdo
                    imagem_bytes = bytes(imagem)
                    resultado += f"<p>Tamanho em bytes: {len(imagem_bytes)}</p>"
                except Exception as e:
                    resultado += f"<p>Erro ao converter: {e}</p>"
            elif isinstance(imagem, str):
                resultado += f"<p style='color: green;'><strong>OK: É STRING</strong></p>"
                resultado += f"<p>Nome do arquivo: <code>{imagem}</code></p>"

            resultado += "</div>"

        cur.close()
        conn.close()
        return resultado

    except Exception as e:
        return f"Erro: {e}"


@galeria_bp.route('/verificar_imagens_uploads')
def verificar_imagens_uploads():
    """Verifica se as imagens existem na pasta uploads"""
    try:
        upload_dir = 'static/images/uploads'

        if not os.path.exists(upload_dir):
            return f"Pasta {upload_dir} não existe!"

        imagens = os.listdir(upload_dir)

        resultado = f"<h1>Imagens na pasta uploads</h1>"
        resultado += f"<p>Total: {len(imagens)} imagens</p>"
        resultado += "<ul>"

        for imagem in sorted(imagens):
            caminho_completo = os.path.join(upload_dir, imagem)
            tamanho = os.path.getsize(caminho_completo)
            resultado += f"<li>{imagem} ({tamanho} bytes)</li>"

        resultado += "</ul>"

        # Verificar se as imagens específicas existem
        imagens_procuradas = ['lucas_74406104.jpg', 'kimiko_1563738c.jpg', 'sonia_fe52dc87.jpg']
        resultado += "<h2>Imagens procuradas:</h2>"

        for img in imagens_procuradas:
            caminho = os.path.join(upload_dir, img)
            existe = os.path.exists(caminho)
            resultado += f"<p>{img}: <strong style='color: {'green' if existe else 'red'}'>{'EXISTE' if existe else 'NÃO ENCONTRADA'}</strong></p>"

        return resultado

    except Exception as e:
        return f"Erro: {e}"


@galeria_bp.route('/migrar_urgente')
def migrar_urgente():
    """Migração URGENTE - Converte memoryview para nomes de arquivo"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar TODOS os usuários
        cur.execute('SELECT id_cadastro, nome_usuario, imagem_usuario FROM cadastrousuarios')
        usuarios = cur.fetchall()

        print("=== MIGRAÇÃO URGENTE INICIADA ===")

        for usuario in usuarios:
            id_cadastro, nome, imagem = usuario

            print(f"Processando: {nome} (ID: {id_cadastro})")
            print(f"Tipo da imagem: {type(imagem)}")
            print(f"Valor: {imagem}")

            # Se é memoryview, CONVERTER para nome de arquivo
            if isinstance(imagem, memoryview):
                print(f" CONVERTENDO memoryview para string...")

                # Gerar nome baseado no usuário
                nome_limpo = "".join(c for c in nome if c.isalnum() or c in (' ', '-', '_')).rstrip()
                nome_limpo = nome_limpo.replace(' ', '_').lower()

                import uuid
                unique_id = str(uuid.uuid4())[:8]
                novo_nome = f"{nome_limpo}_{unique_id}.jpg"

                # ATUALIZAR BANCO
                cur.execute(
                    'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
                    (novo_nome, id_cadastro)  # AGORA É STRING!
                )

                print(f" CONVERTIDO: {nome} -> {novo_nome}")

            elif isinstance(imagem, str):
                print(f" JÁ É STRING: {nome} -> {imagem}")
            else:
                print(f" TIPO DESCONHECIDO: {type(imagem)}")

            print("---")

        conn.commit()
        cur.close()
        conn.close()

        return """
        <h1>Migração URGente Concluída!</h1>
        <p>Verifique o console para ver os detalhes.</p>
        <p><a href="/debug_imagens_detalhado">Verificar resultado</a></p>
        <p><a href="/gallery_adm">Testar galeria</a></p>
        """

    except Exception as e:
        return f"Erro na migração: {str(e)}"


@galeria_bp.route('/teste_imagem/<nome_imagem>')
def teste_imagem(nome_imagem):
    """Testa se uma imagem específica é acessível"""
    caminho = f"static/images/uploads/{nome_imagem}"

    if os.path.exists(caminho):
        return f"""
        <h1>Imagem Encontrada: {nome_imagem}</h1>
        <img src="/static/images/uploads/{nome_imagem}" style="max-width: 500px; border: 3px solid green;">
        <p>Caminho: {caminho}</p>
        <p>Tamanho: {os.path.getsize(caminho)} bytes</p>
        """
    else:
        return f"""
        <h1 style="color: red;">Imagem NÃO Encontrada: {nome_imagem}</h1>
        <p>Caminho procurado: {caminho}</p>
        <p>Pasta uploads existe: {os.path.exists('static/images/uploads')}</p>
        <p>Conteúdo da pasta: {os.listdir('static/images/uploads') if os.path.exists('static/images/uploads') else 'Pasta não existe'}</p>
        """


@galeria_bp.route('/estado_atual_banco')
def estado_atual_banco():
    """Mostra o estado atual de TODOS os usuários no banco"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT id_cadastro, nome_usuario, imagem_usuario FROM cadastrousuarios')
        usuarios = cur.fetchall()

        resultado = "<h1>Estado Atual do Banco</h1>"

        memoryviews = 0
        strings = 0
        outros = 0

        for usuario in usuarios:
            id_cad, nome, imagem = usuario

            if isinstance(imagem, memoryview):
                memoryviews += 1
                status = " MEMORYVIEW"
            elif isinstance(imagem, str):
                strings += 1
                status = "STRING"
            else:
                outros += 1
                status = " OUTRO"

            resultado += f"""
            <div style='border: 1px solid #ccc; margin: 5px; padding: 5px;'>
                <strong>{nome}</strong> (ID: {id_cad}) - {status}
                <br>Valor: {imagem}
            </div>
            """

        resultado += f"""
        <h2>Resumo:</h2>
        <p> Strings: {strings}</p>
        <p> Memoryviews: {memoryviews}</p>
        <p> Outros: {outros}</p>
        <p>Total: {len(usuarios)}</p>
        """

        cur.close()
        conn.close()
        return resultado

    except Exception as e:
        return f"Erro: {e}"


@galeria_bp.route('/solucao_extrema')
def solucao_extrema():
    """Solução extrema - Define TODOS como default_avatar.png"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # DEFINIR TODOS como default_avatar.png
        cur.execute('UPDATE cadastrousuarios SET imagem_usuario = %s', ('default_avatar.png',))

        conn.commit()
        cur.close()
        conn.close()

        return """
        <h1>Solução Extrema Aplicada!</h1>
        <p>TODOS os usuários foram definidos com default_avatar.png</p>
        <p><a href="/gallery_adm">Testar galeria</a></p>
        <p style="color: orange;">AVISO: Isso vai resetar todas as imagens dos usuários!</p>
        """

    except Exception as e:
        return f"Erro: {str(e)}"


@galeria_bp.route('/remover_galeria', methods=['POST'])
def remover_galeria():
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')

    id_cadastro = request.form.get('usuario_remover')

    if not id_cadastro:
        flash('Selecione um usuário para remover!')
        return redirect('/gallery_person_control')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar se o usuário está na galeria
        cur.execute('SELECT id_clientes FROM clientes WHERE id_cadastro = %s', (id_cadastro,))
        existe = cur.fetchone()

        if not existe:
            flash('Este usuário não está na galeria!')
            return redirect('/gallery_person_control')

        # Remover da galeria
        cur.execute('DELETE FROM clientes WHERE id_cadastro = %s', (id_cadastro,))

        conn.commit()
        cur.close()
        conn.close()

        flash('Cliente removido da galeria com sucesso!')
        print(f"REMOVIDO: Usuario ID {id_cadastro} da galeria")

        return redirect('/gallery_adm')

    except Exception as e:
        print(f"ERRO ao remover da galeria: {e}")
        flash('Erro ao remover cliente da galeria')
        return redirect('/gallery_person_control')


@galeria_bp.route('/excluir_diretamente/<int:id_cliente>')
def excluir_diretamente(id_cliente):
    """Exclui diretamente um cliente da galeria (para usar nos botões da gallery_adm.html)"""
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar se o cliente existe
        cur.execute(
            'SELECT nome_usuario FROM cadastrousuarios u INNER JOIN clientes c ON u.id_cadastro = c.id_cadastro WHERE c.id_clientes = %s',
            (id_cliente,))
        cliente = cur.fetchone()

        if cliente:
            nome_cliente = cliente[0]
            # Excluir da galeria
            cur.execute('DELETE FROM clientes WHERE id_clientes = %s', (id_cliente,))
            conn.commit()
            flash(f'Cliente {nome_cliente} removido da galeria!')
            print(f"EXCLUÍDO DIRETAMENTE: ID {id_cliente} - {nome_cliente}")
        else:
            flash('Cliente não encontrado!')

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao excluir diretamente: {e}")
        flash('Erro ao remover cliente')

    return redirect('/gallery_adm')