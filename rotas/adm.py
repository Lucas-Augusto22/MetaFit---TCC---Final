
                                        # Tentativa 2


from flask import Blueprint, render_template, session, redirect, flash
import psycopg2
from database import get_db_connection
import os
import hashlib


adm_bp = Blueprint('adm', __name__)

# def get_db_connection():
#     conn = psycopg2.connect(
#         host='localhost',
#         database='MetaFit',
#         user='postgres',
#         password='senai'
#     )
#     return conn

# ========== ROTAS DO ADMINISTRADOR ==========

# @adm_bp.route('/index_adm')
# def index_adm():
#     print(f"🔍 Acessando index_adm - Sessão: {dict(session)}")
#
#     if 'user_id' not in session or session['user_type'] != 'adm':
#         flash('Acesso restrito a administradores!')
#         print("❌ Redirecionando para login - Sem permissão")
#         return redirect('/login')
#
#     print("✅ Admin autorizado, renderizando template")
#     return render_template('index_adm.html', adm_nome=session.get('adm_nome'))
#     # if 'user_id' not in session or session['user_type'] != 'adm':
#     #     flash('Acesso restrito a administradores!')
#     #     return redirect('/login')
#     # return render_template('index_adm.html', adm_nome=session.get('adm_nome'))

@adm_bp.route('/index_adm')
def index_adm():
    print(f"Acessando index_adm - Sessao: {dict(session)}")

    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        print("Redirecionando para login - Sem permissao")
        return redirect('/login')

    print("Admin autorizado, renderizando template")
    return render_template('index_adm.html', adm_nome=session.get('adm_nome'))

@adm_bp.route('/debug_sessao')
def debug_sessao():
    return f"""
    <h1>Debug da Sessão</h1>
    <pre>
    user_id: {session.get('user_id')}
    user_type: {session.get('user_type')}
    adm_nome: {session.get('adm_nome')}
    user_email: {session.get('user_email')}
    </pre>
    <a href="/index_adm">Tentar acessar index_adm</a>
    """

@adm_bp.route('/gallery_adm')
def gallery_adm():
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')
    return render_template('gallery_adm.html')

@adm_bp.route('/gallery_person_control')
def gallery_person_control():
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')
    return render_template('gallery_person_control.html')


@adm_bp.route('/teste_conexao')
def teste_conexao():
    """Rota para testar a conexão e ver os dados reais"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Teste 1: Contar usuários
        cur.execute('SELECT COUNT(*) FROM cadastrousuarios')
        total_usuarios = cur.fetchone()[0]

        # Teste 2: Ver todos os dados
        cur.execute('SELECT * FROM cadastrousuarios')
        todos_usuarios = cur.fetchall()

        # Teste 3: Ver estrutura da tabela
        cur.execute('''
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'cadastrousuarios'
            ORDER BY ordinal_position
        ''')
        colunas = cur.fetchall()

        cur.close()
        conn.close()

        # Montar resultado para debug
        resultado = f"""
        <h1>DEBUG - Teste de Conexão</h1>
        <h3>Total de usuários: {total_usuarios}</h3>
        <h3>Estrutura da tabela:</h3>
        <ul>
        """
        for coluna in colunas:
            resultado += f"<li>{coluna[0]} - {coluna[1]}</li>"

        resultado += "</ul><h3>Dados dos usuários:</h3>"

        for usuario in todos_usuarios:
            resultado += f"""
            <div style='border: 1px solid #ccc; margin: 10px; padding: 10px;'>
                <p><strong>ID:</strong> {usuario[0]}</p>
                <p><strong>Nome:</strong> {usuario[1]}</p>
                <p><strong>CPF:</strong> {usuario[2]}</p>
                <p><strong>Senha:</strong> {usuario[3]}</p>
                <p><strong>Email:</strong> {usuario[4]}</p>
                <p><strong>CEP:</strong> {usuario[5]}</p>
                <p><strong>Data Nasc:</strong> {usuario[6]}</p>
                <p><strong>Imagem:</strong> {usuario[7]}</p>
            </div>
            """

        return resultado

    except Exception as e:
        return f"ERRO NA CONEXÃO: {str(e)}"


# @adm_bp.route('/usuarios_cadastrados')
# def usuarios_cadastrados():
#     print("=== ACESSANDO ROTA usuarios_cadastrados ===")
#
#     if 'user_id' not in session or session['user_type'] != 'adm':
#         flash('Acesso restrito a administradores!')
#         return redirect('/login')
#     # return render_template('register_control.html')
#
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#
#         # Tente esta query alternativa - mais explícita
#         cur.execute('''
#             SELECT
#                 id_cadastro::text,
#                 nome_usuario::text,
#                 email_usuario::text,
#                 cep_usuario::text,
#                 COALESCE(imagem_usuario::text, '')
#             FROM cadastrousuarios
#             WHERE nome_usuario IS NOT NULL
#             ORDER BY nome_usuario
#         ''')
#
#         usuarios = cur.fetchall()
#         cur.close()
#         conn.close()
#
#         print(f"DEBUG: Query executada com sucesso!")
#         print(f"DEBUG: {len(usuarios)} usuários encontrados")
#
#         # Converter para lista para garantir que não é None
#         usuarios_list = list(usuarios) if usuarios else []
#
#         print(f"DEBUG: Enviando {len(usuarios_list)} usuários para o template")
#
#         return render_template('register_control.html', usuarios=usuarios_list)
#
#     except Exception as e:
#         print(f"ERRO NA CONSULTA: {str(e)}")
#         # Em caso de erro, retorna lista vazia
#         return render_template('register_control.html', usuarios=[])

# import base64
#
# @adm_bp.route('/usuarios_cadastrados')
# def usuarios_cadastrados():
#     if 'user_id' not in session or session['user_type'] != 'adm':
#         flash('Acesso restrito a administradores!')
#         return redirect('/login')
#
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#
#         cur.execute('''
#             SELECT
#                 id_cadastro,
#                 nome_usuario,
#                 email_usuario,
#                 cep_usuario,
#                 imagem_usuario
#             FROM cadastrousuarios
#             ORDER BY nome_usuario
#         ''')
#         usuarios_brutos = cur.fetchall()
#
#         cur.close()
#         conn.close()
#
#                 # Converter BLOB para arquivos de imagem
#         usuarios = []
#         for usuario in usuarios_brutos:
#             id_cadastro, nome, email, cep, imagem_binaria = usuario
#
#             nome_imagem = None
#
#             if imagem_binaria and isinstance(imagem_binaria, memoryview):
#                 try:
#                             # Converter memoryview para bytes
#                     imagem_bytes = bytes(imagem_binaria)
#                     if imagem_bytes:
#                                 # Salvar como arquivo
#                         nome_imagem = f"usuario_{id_cadastro}.jpg"
#                         caminho_arquivo = os.path.join('static', 'images', 'uploads', nome_imagem)
#
#                         with open(caminho_arquivo, 'wb') as f:
#                             f.write(imagem_bytes)
#
#                 except Exception as img_error:
#                     print(f"Erro ao processar imagem do usuário {id_cadastro}: {img_error}")
#                     nome_imagem = None
#
#             usuarios.append((id_cadastro, nome, email, cep, nome_imagem))
#
#         return render_template('register_control.html', usuarios=usuarios)
#
#     except Exception as e:
#         print(f"ERRO: {str(e)}")
#         flash(f'Erro ao carregar usuários: {str(e)}')
#         return redirect('/index_adm')

# import os

        # import os

@adm_bp.route('/debug_imagens')
def debug_imagens():
            """Rota para verificar quais imagens existem na pasta uploads"""
            upload_dir = os.path.join('static', 'images', 'uploads')

            if not os.path.exists(upload_dir):
                return f"Pasta {upload_dir} não existe!"

            imagens = os.listdir(upload_dir)

            resultado = f"<h1>Imagens na pasta uploads</h1>"
            resultado += f"<p>Total: {len(imagens)} imagens</p>"
            resultado += "<ul>"

            for imagem in sorted(imagens):
                caminho_completo = os.path.join(upload_dir, imagem)
                tamanho = os.path.getsize(caminho_completo) if os.path.isfile(caminho_completo) else 0
                resultado += f"<li>{imagem} ({tamanho} bytes)</li>"

            resultado += "</ul>"

            # Verificar também o que está no banco
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    'SELECT id_cadastro, nome_usuario, imagem_usuario, pg_typeof(imagem_usuario) FROM cadastrousuarios')
                usuarios = cur.fetchall()
                cur.close()
                conn.close()

                resultado += "<h1>Dados do Banco</h1>"
                for usuario in usuarios:
                    id_cad, nome, imagem, tipo = usuario
                    resultado += f"<p>ID: {id_cad}, Nome: {nome}, Tipo: {tipo}, Imagem: {type(imagem)}</p>"

            except Exception as e:
                resultado += f"<p>Erro no banco: {e}</p>"

            return resultado

@adm_bp.route('/usuarios_cadastrados')
def usuarios_cadastrados():
            if 'user_id' not in session or session['user_type'] != 'adm':
                flash('Acesso restrito a administradores!')
                return redirect('/login')

            try:
                conn = get_db_connection()
                cur = conn.cursor()

                # PRIMEIRO: Buscar apenas os dados básicos
                cur.execute('''
            SELECT 
                id_cadastro,
                nome_usuario,  
                email_usuario,
                cep_usuario
            FROM cadastrousuarios 
            ORDER BY nome_usuario
        ''')
                usuarios_basicos = cur.fetchall()
                cur.close()
                conn.close()

                # SEGUNDO: Encontrar as imagens correspondentes na pasta uploads
                upload_dir = os.path.join('static', 'images', 'uploads')
                todas_imagens = os.listdir(upload_dir) if os.path.exists(upload_dir) else []

                usuarios_com_imagens = []

                for usuario in usuarios_basicos:
                    id_cadastro, nome, email, cep = usuario

                    # Procurar imagem que corresponda a este usuário
                    imagem_encontrada = None

                    # Estratégia 1: Procurar por padrão no nome do arquivo
                    for imagem in todas_imagens:
                        # Se o arquivo contém o ID do usuário ou nome
                        if str(id_cadastro) in imagem or nome.lower().replace(' ', '_') in imagem.lower():
                            imagem_encontrada = imagem
                            break

                    # Estratégia 2: Se não encontrou, usar a primeira imagem que não foi usada
                    if not imagem_encontrada and todas_imagens:
                        # Remover imagens já usadas
                        imagens_usadas = [u[4] for u in usuarios_com_imagens if u[4]]
                        imagens_disponiveis = [img for img in todas_imagens if img not in imagens_usadas]

                        if imagens_disponiveis:
                            imagem_encontrada = imagens_disponiveis[0]

                    usuarios_com_imagens.append((id_cadastro, nome, email, cep, imagem_encontrada))

                # DEBUG
                print("=== USUÁRIOS COM IMAGENS ===")
                for usuario in usuarios_com_imagens:
                    print(f"{usuario[1]} -> {usuario[4]}")

                return render_template('register_control.html', usuarios=usuarios_com_imagens)

            except Exception as e:
                print(f"ERRO: {str(e)}")
                flash(f'Erro ao carregar usuários: {str(e)}')
                return redirect('/index_adm')


@adm_bp.route('/usuarios_cadastrados_test')
def usuarios_cadastrados_test():
    """Rota de teste com dados fictícios"""
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')

    # Dados de teste
    usuarios_teste = [
        (1, 'João Silva', 'joao@email.com', '12345678', 'joao.jpg'),
        (2, 'Maria Santos', 'maria@email.com', '87654321', 'maria.jpg'),
        (3, 'Lucas Teste', 'lucas@email.com', '16301500', None)
    ]

    print(f"DEBUG TESTE: Enviando {len(usuarios_teste)} usuários para o template")

    return render_template('register_control.html', usuarios=usuarios_teste)


@adm_bp.route('/excluir_usuario/<int:id_usuario>', methods=['POST'])
def excluir_usuario(id_usuario):
    if 'user_id' not in session or session['user_type'] != 'adm':
        flash('Acesso restrito a administradores!')
        return redirect('/login')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Excluir usuário
        cur.execute('DELETE FROM cadastrousuarios WHERE id_cadastro = %s', (id_usuario,))

        conn.commit()
        cur.close()
        conn.close()

        flash('Usuário excluído com sucesso!')

    except Exception as e:
        flash(f'Erro ao excluir usuário: {str(e)}')

    return redirect('/usuarios_cadastrados')


@adm_bp.route('/debug_usuarios')
def debug_usuarios():
    if 'user_id' not in session or session['user_type'] != 'adm':
        return "Acesso negado"

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar quantos usuários existem
        cur.execute('SELECT COUNT(*) FROM cadastrousuarios')
        total = cur.fetchone()[0]

        # Verificar estrutura da tabela
        cur.execute('''
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'cadastrousuarios'
        ''')
        colunas = cur.fetchall()

        cur.close()
        conn.close()

        return f"""
        Total de usuários: {total}<br>
        Colunas: {colunas}<br>
        <a href="/usuarios_cadastrados">Voltar</a>
        """

    except Exception as e:
        return f"Erro: {str(e)}"


# @bp.route('/gallery_adm')
# def gallery_adm():
#     return render_template('gallery_adm.html')
#
# @bp.route('/register_control')
# def register_control():
#     return render_template('register_control.html')