#Projeto básico de Flask - 'Jogoteca'  na versão 2 implanto o banco de dados...

from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo("Tetris", "Puzzle", "Atari")
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo("Mortal Combat", "Luta", "PS2")
lista = [jogo1, jogo2, jogo3] # lista global

app = Flask(__name__) # cria uma aplicação/objeto da classe Flask
app.secret_key = 'bressar' # Depois de instanciar a classe Flask,
# pegar a instância e definir o atributo secret_key com um valor string
# que será usado para encriptar os dados da sessão.

@app.route('/') # abre a rota para o html # precisa ser um código em html para ser exibido
def index(): # é preciso uma função para exibir a página
    #titulo = 'Jogos'
    print("Página /inicio acessada")
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo') # página html do formulário
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None: # se não tiver usuario em session direciona para a pagina de login
        return redirect(url_for('login', proxima=url_for('novo'))) # query string: ?proxima=novo
    return render_template('novo.html', titulo="Novo Jogo")

@app.route('/criar', methods=['POST',]) # precisa determinar o método na rota
def criar():
    # busca as informações do formulário html
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console) # cria um novo objeto jogo
    lista.append(jogo) # adiciona na lista
    return redirect(url_for('index')) # função quue instancia o index


@app.route('/login')
def login():
    proxima = request.args.get('proxima') # pega o nome definido na query string e passa para a variável 'proxima'
    return render_template('login.html', proxima=proxima) # envia para a proxima pagina html


@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'alohomora' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        # Session é um recurso do Flask que permite um armazenamento temporário de dados que persiste as informações
        # coletadas por mais de um ciclo de request.
        # A session consegue persistir os dados através de cryptographically-signed cookies
        # (cookies assinados criptograficamente). Esses cookies são enviados a cada ciclo de request para o servidor,
        # onde são processados da forma que a aplicação demanda.
        # É necessária a configuração de uma secret_key no servidor para a utilização da session.
        # Isso é essencial para garantir uma maior segurança dos dados guardados nos cookies,
        # já que uma pessoa má intencionada poderia acessar os cookies do navegador e mudar os seus dados armazenados.
        # A secret_key fornece um nível de assinatura criptográfica aos cookies.
        # Isso significa que seu conteúdo não pode ser alterado. Porém, é importante ressaltar que a
        # natureza criptográfica dos cookies não necessariamente impede a visualização dos dados.
        # Portanto, apesar de não ser recomendada a utilização de sessions para armazenamento
        # de dados sensíveis e dependerem do tamanho máximo de armazenamento dos cookies (por volta de 4 KB),
        # sessions se apresentam como um recurso poderoso do Flask, sendo rápidas de instanciar e fáceis de escalar..
        flash(session['usuario_logado'] + ' logado com sucesso!')# mostra uma mensagem rápida para o user
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) # o debug faz o hot reload

# app.run(debug=True) # Dessa maneira sem epecificar a porta não rodava no meu pc com windows...

#app.run() # http://127.0.0.1:5000 + '/inicio' "@app.route('/inicio')"
# roda a aplicação na porta 5000 e o endereço como 127.0.0.1.

# app.run(host='0.0.0.0', port=8080)
# Se quiser usar a porta 8080 para aplicação ou até mesmo
# permitir acessos externos à aplicação definindo o host como 0.0.0.0,
