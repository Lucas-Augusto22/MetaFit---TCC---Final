import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import psycopg2
from database import get_db_connection
import os
import hashlib
from werkzeug.utils import secure_filename
import sys
print(sys.path)

usuario_bp = Blueprint('usuario', __name__)

# Configurações
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='MetaFit',
        user='postgres',
        password='senai'
    )
    return conn


def hash_senha(senha):
    """Gera hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()


@usuario_bp.route('/login')
def login():
    return render_template('login.html')

# @usuario_bp.route('/cadastrar_usuario', methods=['POST'])
# def cadastrar_usuario():
#     if request.method == 'POST':
#         nome = request.form.get('nome')
#         email = request.form.get('email')
#         senha = request.form.get('senha')  # SENHA SEM HASH
#         cpf = request.form.get('cpf')
#         cep = request.form.get('cep')
#         data_nascimento = request.form.get('data_nascimento')
#
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#
#             # Verificar se email já existe
#             cur.execute('SELECT * FROM cadastrousuarios WHERE email_usuario = %s', (email,))
#             if cur.fetchone():
#                 flash('Email já cadastrado!')
#                 return redirect('/login')
#
#             # Inserir novo usuário COM SENHA SEM HASH (para compatibilidade)
#             cur.execute(
#                 '''INSERT INTO cadastrousuarios
#                 (nome_usuario, email_usuario, senha_usuario, cpf_usuario, cep_usuario, data_nascimento, imagem_usuario)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)''',
#                 (nome, email, senha, cpf, cep, data_nascimento, 'default_avatar.png')  # Senha sem hash
#             )
#
#             conn.commit()
#
#             # Buscar o ID do usuário recém-criado
#             cur.execute('SELECT id_cadastro FROM cadastrousuarios WHERE email_usuario = %s', (email,))
#             resultado = cur.fetchone()
#             usuario_id = resultado[0] if resultado else None
#
#             cur.close()
#             conn.close()
#
#             if usuario_id:
#                 session['user_id'] = usuario_id
#                 session['user_email'] = email
#                 session['user_type'] = 'usuario'
#                 session['user_nome'] = nome
#                 session['user_imagem'] = 'default_avatar.png'
#
#                 flash('Cadastro realizado com sucesso!')
#                 return redirect('/perfil_foto')
#             else:
#                 flash('Erro ao recuperar ID do usuário')
#                 return redirect('/login')
#
#         except Exception as e:
#             print(f"Erro no cadastro: {str(e)}")
#             flash(f'Erro no cadastro: {str(e)}')
#             return redirect('/login')

# @usuario_bp.route('/cadastrar_usuario', methods=['POST'])
# def cadastrar_usuario():
#     if request.method == 'POST':
#         nome = request.form.get('nome')
#         email = request.form.get('email')
#         senha = request.form.get('senha')
#         cpf = request.form.get('cpf')
#         cep = request.form.get('cep')
#         data_nascimento = request.form.get('data_nascimento')
#
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#
#             # Verificar se email já existe
#             cur.execute('SELECT * FROM cadastrousuarios WHERE email_usuario = %s', (email,))
#             if cur.fetchone():
#                 flash('Email já cadastrado!')
#                 return redirect('/login')
#
#             # Inserir novo usuário SEM imagem (usa padrão)
#             cur.execute(
#                 '''INSERT INTO cadastrousuarios
#                 (nome_usuario, email_usuario, senha_usuario, cpf_usuario, cep_usuario, data_nascimento, imagem_usuario)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)''',
#                 (nome, email, senha, cpf, cep, data_nascimento, 'default_avatar.png')
#             )
#
#             conn.commit()
#
#             # Buscar o ID do usuário recém-criado
#             cur.execute('SELECT id_cadastro FROM cadastrousuarios WHERE email_usuario = %s', (email,))
#             resultado = cur.fetchone()
#             usuario_id = resultado[0] if resultado else None
#
#             cur.close()
#             conn.close()
#
#             if usuario_id:
#                 session['user_id'] = usuario_id
#                 session['user_email'] = email
#                 session['user_type'] = 'usuario'
#                 session['user_nome'] = nome
#                 session['user_imagem'] = 'default_avatar.png'
#
#                 flash('Cadastro realizado com sucesso! Complete seu perfil.')
#                 return redirect('/perfil_foto')  # SEMPRE redireciona para escolher foto
#
#             else:
#                 flash('Erro ao recuperar ID do usuário')
#                 return redirect('/login')
#
#         except Exception as e:
#             print(f"Erro no cadastro: {str(e)}")
#             flash(f'Erro no cadastro: {str(e)}')
#             return redirect('/login')

@usuario_bp.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        cpf = request.form.get('cpf')
        cep = request.form.get('cep')
        data_nascimento = request.form.get('data_nascimento')

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Verificar se email já existe
            cur.execute('SELECT * FROM cadastrousuarios WHERE email_usuario = %s', (email,))
            if cur.fetchone():
                flash('Email já cadastrado!')
                return redirect('/login')

            # **GARANTIR que é sempre string**
            nome_imagem = 'default_avatar.png'  # SEMPRE string

            # Inserir novo usuário COM imagem_usuario como STRING
            cur.execute(
                '''INSERT INTO cadastrousuarios 
                (nome_usuario, email_usuario, senha_usuario, cpf_usuario, cep_usuario, data_nascimento, imagem_usuario) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (nome, email, senha, cpf, cep, data_nascimento, nome_imagem)  # SEMPRE string
            )

            conn.commit()

            # Buscar o ID do usuário recém-criado
            cur.execute('SELECT id_cadastro FROM cadastrousuarios WHERE email_usuario = %s', (email,))
            resultado = cur.fetchone()
            usuario_id = resultado[0] if resultado else None

            cur.close()
            conn.close()

            if usuario_id:
                session['user_id'] = usuario_id
                session['user_email'] = email
                session['user_type'] = 'usuario'
                session['user_nome'] = nome
                session['user_imagem'] = nome_imagem  # SEMPRE string

                flash('Cadastro realizado com sucesso! Complete seu perfil.')
                return redirect('/perfil_foto')

            else:
                flash('Erro ao recuperar ID do usuário')
                return redirect('/login')

        except Exception as e:
            print(f"Erro no cadastro: {str(e)}")
            flash(f'Erro no cadastro: {str(e)}')
            return redirect('/login')


# @usuario_bp.route('/autenticar', methods=['POST'])
# def autenticar():
#     email = request.form.get('email')
#     senha = request.form.get('senha')
#
#     print(f"Tentativa de login: {email}")
#
#
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#
#         # Primeiro verificar se é administrador
#         cur.execute('SELECT * FROM adm WHERE email_adm = %s AND senha_adm = %s', (email, senha))
#         adm = cur.fetchone()
#
#         if adm:
#             print(f"Admin encontrado: {adm[1]}")
#             session['user_id'] = adm[0]  # id_adm
#             session['user_email'] = email
#             session['user_type'] = 'adm'
#             session['adm_nome'] = adm[1]  # nome_adm
#             # Para admin, usar imagem padrão ou vazio
#             session['user_imagem'] = 'default_avatar.png'
#             cur.close()
#             conn.close()
#             flash(f'Bem-vindo, Administrador {adm[1]}!', 'success')
#             return redirect('/index_adm')
#
#         # SE NÃO FOR ADMIN: Verifica se é usuário comum
#         cur.execute(
#             '''SELECT id_cadastro, nome_usuario, email_usuario, senha_usuario, imagem_usuario
#             FROM cadastrousuarios
#             WHERE email_usuario = %s''',
#             (email,)
#         )
#         usuario = cur.fetchone()
#
#         if usuario:
#             id_cadastro, nome_usuario, email_usuario, senha_bd, imagem_usuario = usuario
#
#             # Verificar senha - compatibilidade com cadastro antigo e novo
#             senha_correta = False
#
#             # Tentativa 1: Verificar sem hash (cadastro novo)
#             if senha == senha_bd:
#                 senha_correta = True
#                 print("Senha verificada sem hash")
#             # Tentativa 2: Verificar com hash (cadastro antigo)
#             else:
#                 senha_hash = hash_senha(senha)
#                 if senha_hash == senha_bd:
#                     senha_correta = True
#                     print("Senha verificada com hash")
#
#             if senha_correta:
#                 print(f"Usuario comum encontrado: {nome_usuario}")
#                 session['user_id'] = id_cadastro
#                 session['user_email'] = email
#                 session['user_type'] = 'usuario'
#                 session['user_nome'] = nome_usuario
#
#                 # CORREÇÃO CRÍTICA: Tratar a imagem_usuario que pode ser memoryview
#                 imagem_para_sessao = 'default_avatar.png'
#
#                 if imagem_usuario:
#                     if isinstance(imagem_usuario, memoryview):
#                         # Se é memoryview (BLOB), converter para string ou usar padrão
#                         try:
#                             # Tentar converter para string se possível
#                             imagem_str = str(imagem_usuario)
#                             if imagem_str and imagem_str != 'None':
#                                 imagem_para_sessao = imagem_str
#                             else:
#                                 imagem_para_sessao = 'default_avatar.png'
#                         except:
#                             imagem_para_sessao = 'default_avatar.png'
#                     elif isinstance(imagem_usuario, str) and imagem_usuario.strip() and imagem_usuario != 'None':
#                         # Já é uma string válida
#                         imagem_para_sessao = imagem_usuario.strip()
#
#                 session['user_imagem'] = imagem_para_sessao
#                 print(f"Imagem definida na sessão: {imagem_para_sessao}")
#
#                 cur.close()
#                 conn.close()
#
#                 # Verificar se tem foto de perfil real (não é a padrão)
#                 if imagem_para_sessao and imagem_para_sessao != 'default_avatar.png':
#                     flash(f'Bem-vindo de volta, {nome_usuario}!', 'success')
#                     return redirect('/')
#                 else:
#                     flash(f'Bem-vindo, {nome_usuario}! Complete seu perfil.', 'info')
#                     return redirect('/perfil_foto')
#             else:
#                 print("Senha incorreta")
#                 flash('Email ou senha incorretos!', 'error')
#                 return redirect('/login')
#
#         # Se não encontrou em nenhuma tabela
#         print("Usuário não encontrado")
#         flash('Email ou senha incorretos!', 'error')
#         return redirect('/login')
#
#     except Exception as e:
#         print(f"Erro na autenticacao: {str(e)}")
#         flash(f'Erro na autenticação: {str(e)}', 'error')
#         return redirect('/login')

@usuario_bp.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form.get('email')
    senha = request.form.get('senha')

    print(f"Tentativa de login: {email}")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Primeiro verificar se é administrador
        cur.execute('SELECT * FROM adm WHERE email_adm = %s AND senha_adm = %s', (email, senha))
        adm = cur.fetchone()

        if adm:
            print(f"Admin encontrado: {adm[1]}")
            session['user_id'] = adm[0]  # id_adm
            session['user_email'] = email
            session['user_type'] = 'adm'
            session['adm_nome'] = adm[1]  # nome_adm
            # Para admin, usar imagem padrão ou vazio
            session['user_imagem'] = 'default_avatar.png'
            cur.close()
            conn.close()
            flash(f'Bem-vindo, Administrador {adm[1]}!', 'success')
            return redirect('/index_adm')

        # SE NÃO FOR ADMIN: Verifica se é usuário comum
        cur.execute(
            '''SELECT id_cadastro, nome_usuario, email_usuario, senha_usuario, imagem_usuario 
            FROM cadastrousuarios 
            WHERE email_usuario = %s''',
            (email,)
        )
        usuario = cur.fetchone()

        if usuario:
            id_cadastro, nome_usuario, email_usuario, senha_bd, imagem_usuario = usuario

            # Verificar senha - compatibilidade com cadastro antigo e novo
            senha_correta = False

            # Tentativa 1: Verificar sem hash (cadastro novo)
            if senha == senha_bd:
                senha_correta = True
                print("Senha verificada sem hash")
            # Tentativa 2: Verificar com hash (cadastro antigo)
            else:
                senha_hash = hash_senha(senha)
                if senha_hash == senha_bd:
                    senha_correta = True
                    print("Senha verificada com hash")

            if senha_correta:
                print(f"Usuario comum encontrado: {nome_usuario}")
                session['user_id'] = id_cadastro
                session['user_email'] = email
                session['user_type'] = 'usuario'
                session['user_nome'] = nome_usuario

                # CORREÇÃO CRÍTICA: Tratar a imagem_usuario que pode ser memoryview
                imagem_para_sessao = 'default_avatar.png'

                if imagem_usuario:
                    if isinstance(imagem_usuario, memoryview):
                        # Se é memoryview (BLOB), converter para string ou usar padrão
                        try:
                            # Tentar converter para string se possível
                            imagem_str = str(imagem_usuario)
                            if imagem_str and imagem_str != 'None':
                                imagem_para_sessao = imagem_str
                            else:
                                imagem_para_sessao = 'default_avatar.png'
                        except:
                            imagem_para_sessao = 'default_avatar.png'
                    elif isinstance(imagem_usuario, str) and imagem_usuario.strip() and imagem_usuario != 'None':
                        # Já é uma string válida
                        imagem_para_sessao = imagem_usuario.strip()

                session['user_imagem'] = imagem_para_sessao
                print(f"Imagem definida na sessão: {imagem_para_sessao}")

                cur.close()
                conn.close()

                # VERIFICAÇÃO CORRIGIDA AQUI ↓
                if imagem_para_sessao and imagem_para_sessao != 'default_avatar.png':
                    flash(f'Bem-vindo de volta, {nome_usuario}!', 'success')
                    return redirect('/')  # ← MUDEI PARA '/index'
                else:
                    flash(f'Bem-vindo, {nome_usuario}! Complete seu perfil.', 'info')
                    return redirect('/perfil_foto')
            else:
                print("Senha incorreta")
                flash('Email ou senha incorretos!', 'error')
                return redirect('/login')

        # Se não encontrou em nenhuma tabela
        print("Usuário não encontrado")
        flash('Email ou senha incorretos!', 'error')
        return redirect('/login')

    except Exception as e:
        print(f"Erro na autenticacao: {str(e)}")
        flash(f'Erro na autenticação: {str(e)}', 'error')
        return redirect('/login')


@usuario_bp.route('/migrar_todas_imagens')
def migrar_todas_imagens():
    """Migra TODAS as imagens de BLOB para nomes de arquivo definitivamente"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar todos os usuários
        cur.execute('SELECT id_cadastro, nome_usuario, imagem_usuario FROM cadastrousuarios')
        usuarios = cur.fetchall()

        upload_dir = os.path.join('static', 'images', 'uploads')
        todas_imagens = os.listdir(upload_dir) if os.path.exists(upload_dir) else []

        print("=== MIGRAÇÃO COMPLETA DE IMAGENS ===")

        usuarios_migrados = 0

        for usuario in usuarios:
            id_cadastro, nome, imagem_atual = usuario

            # Se a imagem atual é memoryview ou BLOB, precisamos migrar
            if isinstance(imagem_atual, memoryview):
                # Procurar imagem correspondente na pasta uploads
                imagem_encontrada = None

                for imagem in todas_imagens:
                    # Lógica de matching
                    if (str(id_cadastro) in imagem or
                            nome.lower().replace(' ', '') in imagem.lower() or
                            nome.lower().split()[0] in imagem.lower()):
                        imagem_encontrada = imagem
                        break

                if imagem_encontrada:
                    # Atualizar para usar o nome do arquivo
                    cur.execute(
                        'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
                        (imagem_encontrada, id_cadastro)
                    )
                    print(f"✓ {nome} (ID: {id_cadastro}) -> {imagem_encontrada}")
                    usuarios_migrados += 1
                else:
                    # Usar padrão se não encontrou
                    cur.execute(
                        'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
                        ('default_avatar.png', id_cadastro)
                    )
                    print(f"✗ {nome} (ID: {id_cadastro}) -> default_avatar.png")
                    usuarios_migrados += 1

        conn.commit()
        cur.close()
        conn.close()

        return f"Migração concluída! {usuarios_migrados} usuários migrados."

    except Exception as e:
        return f"Erro na migração: {str(e)}"

@usuario_bp.route('/verificar_imagens_banco')
def verificar_imagens_banco():
    """Verifica como as imagens estão armazenadas no banco"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT id_cadastro, nome_usuario, imagem_usuario, pg_typeof(imagem_usuario) FROM cadastrousuarios')
        usuarios = cur.fetchall()

        resultado = "<h1>Estado das Imagens no Banco</h1>"
        for usuario in usuarios:
            id_cad, nome, imagem, tipo = usuario
            resultado += f"""
            <div style='border: 1px solid #ccc; margin: 10px; padding: 10px;'>
                <p><strong>{nome}</strong> (ID: {id_cad})</p>
                <p>Tipo: {tipo}</p>
                <p>Valor: {imagem}</p>
                <p>Tipo Python: {type(imagem)}</p>
                <p>É memoryview: {isinstance(imagem, memoryview)}</p>
            </div>
            """

        cur.close()
        conn.close()
        return resultado

    except Exception as e:
        return f"Erro: {e}"




@usuario_bp.route('/perfil_foto')
def perfil_foto():
    if 'user_id' not in session or session['user_type'] != 'usuario':
        flash('Acesso não autorizado!', 'error')
        return redirect('/login')
    return render_template('perfil_foto.html')



# @usuario_bp.route('/upload_foto', methods=['POST'])
# def upload_foto():
#     if 'user_id' not in session or session['user_type'] != 'usuario':
#         return redirect('/login')
#
#     if 'meuArquivo' not in request.files:
#         flash('Nenhum arquivo selecionado')
#         return redirect('/perfil_foto')
#
#     file = request.files['meuArquivo']
#
#     if file.filename == '':
#         flash('Nenhum arquivo selecionado')
#         return redirect('/perfil_foto')
#
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         import uuid
#         unique_filename = str(uuid.uuid4()) + '_' + filename
#
#         UPLOAD_FOLDER = 'static/images/uploads'
#         filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
#
#         # Garantir que a pasta existe
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#
#         file.save(filepath)
#
#         # Atualizar banco de dados - AGORA FUNCIONA CORRETAMENTE
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#
#             # session['user_id'] agora é o ID numérico, não o email
#             cur.execute(
#                 'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
#                 (unique_filename, session['user_id'])  # ← AGORA ESTÁ CORRETO
#             )
#
#             conn.commit()
#             cur.close()
#             conn.close()
#
#             # Atualizar a sessão com a nova imagem
#             session['user_imagem'] = unique_filename
#
#             print(f"DEBUG: Foto atualizada para usuário ID {session['user_id']} -> {unique_filename}")
#             flash('Foto de perfil atualizada com sucesso!')
#
#             return redirect('/')  # Redireciona para a página principal
#
#         except Exception as e:
#             print(f"ERRO ao atualizar foto: {str(e)}")
#             flash(f'Erro ao salvar foto: {str(e)}')
#             return redirect('/perfil_foto')
#
#     else:
#         flash('Tipo de arquivo não permitido')
#         return redirect('/perfil_foto')


# @usuario_bp.route('/upload_foto', methods=['POST'])
# def upload_foto():
#     if 'user_id' not in session or session['user_type'] != 'usuario':
#         return redirect('/login')
#
#     if 'meuArquivo' not in request.files:
#         flash('Nenhum arquivo selecionado')
#         return redirect('/perfil_foto')
#
#     file = request.files['meuArquivo']
#
#     if file.filename == '':
#         flash('Nenhum arquivo selecionado')
#         return redirect('/perfil_foto')
#
#     if file and allowed_file(file.filename):
#         # Gerar nome baseado no usuário logado
#         extensao = os.path.splitext(file.filename)[1].lower()
#         nome_usuario = session.get('user_nome', 'usuario')
#
#         # Limpar o nome do usuário para usar no arquivo
#         nome_limpo = "".join(c for c in nome_usuario if c.isalnum() or c in (' ', '-', '_')).rstrip()
#         nome_limpo = nome_limpo.replace(' ', '_').lower()
#
#         # Adicionar UUID para garantir unicidade
#         import uuid
#         unique_id = str(uuid.uuid4())[:8]
#
#         unique_filename = f"{nome_limpo}_{unique_id}{extensao}"
#
#         UPLOAD_FOLDER = 'static/images/uploads'
#         filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
#
#         # Garantir que a pasta existe
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#
#         file.save(filepath)
#
#         # Atualizar banco de dados
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#
#             cur.execute(
#                 'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
#                 (unique_filename, session['user_id'])
#             )
#
#             conn.commit()
#             cur.close()
#             conn.close()
#
#             # Atualizar a sessão com a nova imagem
#             session['user_imagem'] = unique_filename
#
#             print(f"DEBUG: Foto salva como: {unique_filename}")
#             flash('Foto de perfil atualizada com sucesso!')
#
#             return redirect('/')
#
#         except Exception as e:
#             print(f"ERRO ao atualizar foto: {str(e)}")
#             flash(f'Erro ao salvar foto: {str(e)}')
#             return redirect('/perfil_foto')
#
#     else:
#         flash('Tipo de arquivo não permitido')
#         return redirect('/perfil_foto')

@usuario_bp.route('/upload_foto', methods=['POST'])
def upload_foto():
    if 'user_id' not in session or session['user_type'] != 'usuario':
        return redirect('/login')

    if 'meuArquivo' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect('/perfil_foto')

    file = request.files['meuArquivo']

    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect('/perfil_foto')

    if file and allowed_file(file.filename):
        # Gerar nome baseado no usuário logado (SEMPRE string)
        extensao = os.path.splitext(file.filename)[1].lower()
        nome_usuario = session.get('user_nome', 'usuario')

        # Limpar o nome do usuário
        nome_limpo = "".join(c for c in nome_usuario if c.isalnum() or c in (' ', '-', '_')).rstrip()
        nome_limpo = nome_limpo.replace(' ', '_').lower()

        # Adicionar UUID
        import uuid
        unique_id = str(uuid.uuid4())[:8]

        # **NOME DA IMAGEM COMO STRING**
        nome_arquivo = f"{nome_limpo}_{unique_id}{extensao}"

        UPLOAD_FOLDER = 'static/images/uploads'
        filepath = os.path.join(UPLOAD_FOLDER, nome_arquivo)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)

        # **ATUALIZAR BANCO COM STRING**
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
                (nome_arquivo, session['user_id'])  # **SEMPRE string**
            )

            conn.commit()
            cur.close()
            conn.close()

            # Atualizar sessão
            session['user_imagem'] = nome_arquivo

            print(f"DEBUG: Foto salva como STRING: {nome_arquivo}")
            flash('Foto de perfil atualizada com sucesso!')

            return redirect('/')

        except Exception as e:
            print(f"ERRO ao atualizar foto: {str(e)}")
            flash(f'Erro ao salvar foto: {str(e)}')
            return redirect('/perfil_foto')

    else:
        flash('Tipo de arquivo não permitido')
        return redirect('/perfil_foto')


@usuario_bp.route('/debug_usuario')
def debug_usuario():
    if 'user_id' not in session:
        return "Não logado"

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM cadastrousuarios WHERE id_cadastro = %s', (session['user_id'],))
        usuario = cur.fetchone()
        cur.close()
        conn.close()

        if usuario:
            return f"""
            <h1>Debug Usuário</h1>
            <p>ID: {usuario[0]}</p>
            <p>Nome: {usuario[1]}</p>
            <p>Email: {usuario[4]}</p>
            <p>Imagem: {usuario[7]}</p>
            <p>Sessão user_id: {session['user_id']}</p>
            <p>Sessão user_email: {session.get('user_email')}</p>
            """
        else:
            return "Usuário não encontrado"
    except Exception as e:
        return f"Erro: {e}"


@usuario_bp.route('/pular_foto')
def pular_foto():
    if 'user_id' not in session or session['user_type'] != 'usuario':
        return redirect('/login')

    flash('Você pode adicionar uma foto de perfil depois!', 'info')
    return redirect('/')


@usuario_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect('/')


@usuario_bp.route('/teste_rota')
def teste_rota():
    return "✅ Rota de teste funcionando!"

@usuario_bp.route('/teste_banco')
def teste_banco():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return f"✅ Banco conectado: {result[0]}"
    except Exception as e:
        return f"❌ Erro banco: {str(e)}"

@usuario_bp.route('/teste_tabela')
def teste_tabela():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM cadastrousuarios;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"✅ Tabela existe! {count} usuários cadastrados"
    except Exception as e:
        return f"❌ Erro tabela: {str(e)}"


@usuario_bp.route('/mapear_usuarios_imagens')
def mapear_usuarios_imagens():
    """Mostra todos os usuários e imagens disponíveis para fazer o mapeamento"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar todos os usuários
        cur.execute(
            'SELECT id_cadastro, nome_usuario, email_usuario, imagem_usuario FROM cadastrousuarios ORDER BY nome_usuario')
        usuarios = cur.fetchall()

        # Buscar todas as imagens na pasta uploads
        upload_dir = os.path.join('static', 'images', 'uploads')
        todas_imagens = sorted(os.listdir(upload_dir)) if os.path.exists(upload_dir) else []

        resultado = """
        <h1>Mapeamento Usuários ↔ Imagens</h1>
        <style>
            .usuario { border: 1px solid #ccc; margin: 10px; padding: 10px; }
            .imagem-associada { color: green; font-weight: bold; }
            .sem-imagem { color: red; }
            .opcoes-imagem { background: #f0f0f0; padding: 5px; margin: 5px 0; }
        </style>
        """

        resultado += f"<h3>Total de usuários: {len(usuarios)}</h3>"
        resultado += f"<h3>Total de imagens na pasta: {len(todas_imagens)}</h3>"

        for usuario in usuarios:
            id_cadastro, nome, email, imagem_atual = usuario

            resultado += f"""
            <div class="usuario">
                <h3>{nome} (ID: {id_cadastro})</h3>
                <p>Email: {email}</p>
                <p>Imagem atual: <span class="{'imagem-associada' if imagem_atual and imagem_atual != 'default_avatar.png' else 'sem-imagem'}">{imagem_atual or 'Nenhuma'}</span></p>
            """

            # Mostrar possíveis imagens para este usuário
            imagens_candidatas = []
            for imagem in todas_imagens:
                # Lógica de matching - ajuste conforme necessário
                nome_limpo = nome.lower().replace(' ', '').replace('-', '')
                email_prefixo = email.split('@')[0].lower()

                if (nome_limpo in imagem.lower() or
                        email_prefixo in imagem.lower() or
                        str(id_cadastro) in imagem):
                    imagens_candidatas.append(imagem)

            if imagens_candidatas:
                resultado += "<div class='opcoes-imagem'>"
                resultado += "<strong>Possíveis imagens:</strong><br>"
                for img in imagens_candidatas:
                    resultado += f"""
                    <div style="display: inline-block; margin: 5px; text-align: center;">
                        <img src="/static/images/uploads/{img}" style="width: 80px; height: 80px; object-fit: cover; border: 2px solid blue;">
                        <br>
                        <small>{img}</small>
                        <br>
                        <a href="/associar_imagem/{id_cadastro}/{img}">[ASSOCIAR]</a>
                    </div>
                    """
                resultado += "</div>"
            else:
                resultado += "<p style='color: orange;'>Nenhuma imagem candidata encontrada</p>"

            resultado += "</div>"

        cur.close()
        conn.close()
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"


@usuario_bp.route('/associacao_automatica')
def associacao_automatica():
    """Tenta associar automaticamente as imagens aos usuários"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar todos os usuários
        cur.execute('SELECT id_cadastro, nome_usuario, email_usuario FROM cadastrousuarios')
        usuarios = cur.fetchall()

        # Buscar todas as imagens
        upload_dir = os.path.join('static', 'images', 'uploads')
        todas_imagens = os.listdir(upload_dir) if os.path.exists(upload_dir) else []

        resultados = []
        associacoes_feitas = 0

        for usuario in usuarios:
            id_cadastro, nome, email = usuario

            # Lógica de matching automático
            nome_limpo = nome.lower().replace(' ', '_').replace('-', '')
            email_prefixo = email.split('@')[0].lower()

            imagem_encontrada = None

            # Tentar diferentes estratégias de matching
            for imagem in todas_imagens:
                imagem_lower = imagem.lower()

                # Estratégia 1: Nome do usuário no nome da imagem
                if nome_limpo in imagem_lower:
                    imagem_encontrada = imagem
                    break

                # Estratégia 2: Prefixo do email no nome da imagem
                if email_prefixo in imagem_lower:
                    imagem_encontrada = imagem
                    break

                # Estratégia 3: ID do usuário no nome da imagem
                if str(id_cadastro) in imagem:
                    imagem_encontrada = imagem
                    break

            if imagem_encontrada:
                # Atualizar o banco
                cur.execute(
                    'UPDATE cadastrousuarios SET imagem_usuario = %s WHERE id_cadastro = %s',
                    (imagem_encontrada, id_cadastro)
                )
                resultados.append(f"✓ {nome} -> {imagem_encontrada}")
                associacoes_feitas += 1
            else:
                resultados.append(f"✗ {nome} -> Nenhuma imagem encontrada")

        conn.commit()
        cur.close()
        conn.close()

        return f"""
        <h1>Associação Automática Concluída</h1>
        <p>Associações feitas: {associacoes_feitas} de {len(usuarios)}</p>
        <pre>{chr(10).join(resultados)}</pre>
        <br>
        <a href="/mapear_usuarios_imagens">Ver mapeamento detalhado</a>
        """

    except Exception as e:
        return f"Erro na associação automática: {str(e)}"


@usuario_bp.route('/debug_estrutura_tabela')
def debug_estrutura_tabela():
    """Verifica a estrutura da tabela cadastrousuarios"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar estrutura da coluna imagem_usuario
        cur.execute('''
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = 'cadastrousuarios' AND column_name = 'imagem_usuario'
        ''')
        coluna = cur.fetchone()

        # Verificar alguns registros
        cur.execute(
            'SELECT id_cadastro, nome_usuario, imagem_usuario, pg_typeof(imagem_usuario) FROM cadastrousuarios LIMIT 5')
        registros = cur.fetchall()

        resultado = "<h1>Debug - Estrutura da Tabela</h1>"

        if coluna:
            resultado += f"""
            <h3>Coluna imagem_usuario:</h3>
            <p>Nome: {coluna[0]}</p>
            <p>Tipo: {coluna[1]}</p>
            <p>Tamanho máximo: {coluna[2]}</p>
            """

        resultado += "<h3>Primeiros 5 registros:</h3>"
        for reg in registros:
            id_cad, nome, imagem, tipo_db = reg
            resultado += f"""
            <div style='border: 1px solid #ccc; margin: 10px; padding: 10px;'>
                <p><strong>{nome}</strong> (ID: {id_cad})</p>
                <p>Tipo no PostgreSQL: <strong>{tipo_db}</strong></p>
                <p>Tipo no Python: <strong>{type(imagem)}</strong></p>
                <p>Valor: <code>{imagem}</code></p>
            </div>
            """

        cur.close()
        conn.close()
        return resultado

    except Exception as e:
        return f"Erro: {e}"