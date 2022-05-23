# CodeBooks

## Sobre
<p>O projeto produzido por fins de estudo. Que consiste em uma rede social simples onde será possivel conversas, postagem, grupos e fazer amigos.

# Documentação
## Arquitetura
O projeto foi feito com base em uma arquitetura monolítica com o padrão MVC.
A estrutura do projeto se dividi em 5 partes, views composta principalmente por HTML,CSS e Javascript, usando o framework Bootstrap5 responsavel pela inteface de usuario. 
  Routes que fica responsavel pela roteamento para o envio de requisições para os controllers. Os controllers são quem controla o fluxo da aplicação comunicando com dao e
  models e renderizando as views de acordo com a requisição. Por fim temos as camadas dos models e dataAcessObject(DAO) que é onde fica as entidades e regras de negocio
  (models), e a comunicação com banco de dados postgresql por meio do DAO.
  
## Views
  As views responsavel pelas as intefaces, estão disposta na pasta templetes onde contem os arquivos .html e na pasta static em que há arquivos .css, .js e os .svg e .img
  das imagens dos icones. os html pode ser a pagina completa, ou html que estende outros aquivos ou um html estendido de outro, para essa estender um html base com blocos de outros html, usasse o a tag do flask  <strong> {% block "nome do bloco" %} e {% endblock %} </strong>, no bloco que vai estender do base insere-se <strong> {% extends "nome do html base"%} e {% block "nome do bloco" %} fechando com {% endblock "nome do bloco" %} </strong>. Para inserção de css, javaScript e icones deve-se coloca dentro de uma tag de templete <strong> {{ url_for('static',filename='caminho/nome do arquivo')}} </strong>.
  
## Routes
  Routes endereça as requisições da aplicação está na pasta routes.py. Para declarar uma rota usa-se o objeto flask da aplicação, obtido pelo <code> server.app </code> importado dos arquivos do config.py. A estrutura das rotas é a seguinte: 
  <p><code> server.app.add_url_rule("endereço da rota", enpoint="nome da rota",view_func="controller da rota", methods=["metodos http"]) </code></p>
  O endereço da rota é obrigratorio e o nome é opicional, entretanto devido ou uso de um decorector loggin_required o nome se torna obrigatorio, a view também é obrigatoria se não a rota não fará nada, o methods é opcional, pois por padrão é o metodo GET.
  
### Rotas do sistema
  <h5>Index</h5>
  <p>Url para requisitar a pagina principal. Chama o controller feed.index que vai comunicar com o banco de dados e buscar lista de postagem e caso usuario logado a lista de amigos.</p>
  <p><code>server.app.add_url_rule('/',endpoint='index',
                               view_func=controllers.feed.index)</code></p>
                               
  <h5>login</h5>
  <p>Url requisita pagina de login.</p>
  <p><code>server.app.add_url_rule('/login',endpoint='login',
                                    view_func=controllers.login.login)</code></p>  
  
  <h5>Register</h5>
  <p>Url requisita pagina de registro de novo usuario</p>
  <p><code>server.app.add_url_rule('/register',endpoint='register',
                                    view_func=controllers.register.register)</code></p>  
  
  <h5>Autenticação</h5>
  <p>Url requisitada a partir de um form para autenticação de usuario. Usa o metodo post e espera um formulario com input com <code> name='email' </code> e input com <code>name='password'</code> </p>
  <p><code>server.app.add_url_rule('/authenticate',endpoint='authenticate',
                                    view_func=controllers.login.authenticate,methods=['POST'])</code></p>  
  
  <h5>Salva usuario </h5>
  <p>Url requisitada a partir de um form. Usa metodo post e espera um form com 3 input com os seguintes names: <code> name='name', name='email', name='password'</code></p>
  <p><code>server.app.add_url_rule('/sing_in',endpoint='sing_in',
                                    view_func=controllers.register.sing_in,methods=['POST'])</code></p>  
  
    <h5>Logout</h5>
  <p>Url requisita ao sevidor a exclusão da session do usuario</p>
  <p><code>server.app.add_url_rule('/logout', endpoint='logout',
                                    view_func=controllers.login.logout)</code></p>  
  
    <h5></h5>
  <p></p>
  <p><code></code></p>  
  
    <h5></h5>
  <p></p>
  <p><code></code></p>  
  
    <h5></h5>
  <p></p>
  <p><code></code></p>  
  
    <h5></h5>
  <p></p>
  <p><code></code></p>  
  
    <h5></h5>
  <p></p>
  <p><code></code></p>  
  
    <h5></h5>
  <p></p>
  <p><code></code></p>  
  
    <h5></h5>
  <p></p>
  <p><code></code></p>  
