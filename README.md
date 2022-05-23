# CodeBooks

## Sobre
<p>O projeto produzido por fins de estudo. Que consiste em uma rede social simples onde será possivel conversas, postagem, grupos e fazer amigos. O foco da rede social seria para programação e tecnologia, sendo possivel compartilhar codigos de qualquer linguagem.

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

#### Obs: para evitar erros com o decorector de login_required use sempre a função do flask url_for('nome da url','paramentros e argumentos'). Exemplo: <code> url_for('user_profile', id='id do usuario', pag='view')</code>
  <h5>Index</h5>
  <p>Url para requisitar a pagina principal. Chama o controller feed.index que vai comunicar com o banco de dados e buscar lista de postagem e caso usuario logado a lista de amigos.</p>
  <p><code>server.app.add_url_rule('/',endpoint='index',
                               view_func=controllers.feed.index)</code></p>
  <p>pelo url_for: </p>
                               
  <h5>login</h5>
  <p>Url requisita pagina de login.</p>
  <p><code>server.app.add_url_rule('/login',endpoint='login',
                                    view_func=controllers.login.login)</code></p>  
    <p>pelo url_for: <code> url_for('index') </code></p>

  
  <h5>Register</h5>
  <p>Url requisita pagina de registro de novo usuario</p>
  <p><code>server.app.add_url_rule('/register',endpoint='register',
                                    view_func=controllers.register.register)</code></p>  
  <p>pelo url_for: <code> url_for('register')</code></p>
  
  <h5>Autenticação</h5>
  <p>Url requisitada a partir de um form para autenticação de usuario. Usa o metodo post e requisição feita por um formulario com input com <code> name='email' </code> e input com <code>name='password'</code> </p>
  <p><code>server.app.add_url_rule('/authenticate',endpoint='authenticate',
                                    view_func=controllers.login.authenticate,methods=['POST'])</code></p>  
  <p>pelo url_for: <code> url_for('authenticate') </code></p>
  
  <h5>Salva usuario </h5>
  <p>Url requisitada a partir de um form. Usa metodo post e requisição feita por um form com 3 input com os seguintes names: <code> name='name', name='email', name='password'</code></p>
  <p><code>server.app.add_url_rule('/sing_in',endpoint='sing_in',
                                    view_func=controllers.register.sing_in,methods=['POST'])</code></p>  
  <p>pelo url_for: <code> url_for('sing_in')</code></p>
  
  <h5>Logout -> loggin_required</h5>
  <p>Url requisita ao sevidor a exclusão da session do usuario</p>
  <p><code>server.app.add_url_rule('/logout', endpoint='logout',
                                    view_func=controllers.login.logout)</code></p>  
  <p>pelo url_for: <code> url_for('logout')</code></p>
  
  <h5>Procura um usuario -> loggin_required</h5>
  <p>Url com metodo get e post, espera requisição com um json com um registro com key 'user', que irá procurar todos os usuario no banco com nomes parecido e retornar uma lista de usuraio por meio de um json.</p>
  <p><code>server.app.add_url_rule('/search_user', endpoint='search_user', 
                                    view_func=controllers.friend.seach_user, methods=['POST','GET'])</code></p>  
  <p>pelo url_for: <code> url_for('search_user')</code></p>
  
   <h5>Adiciona amigo -> loggin_required</h5>
  <p>Url para adcionar usuario a lista de amigos. Espera um inteiro com o id do usuario que vai ser adcionado, inteiro passado através da url. Exemplo: /add_friend/5, irá acionar o usuario de id 5 a lista de amigos, se já for amigo ou o proprio usuario retonara um mensagem.</p>
  <p><code>server.app.add_url_rule('/add_friend/<int:id>',endpoint='add_friend',
                                    view_func= controllers.friend.add_friend, methods=['GET'])</code></p>  
  <p>pelo url_for: <code> url_for('add_friend', id='id do usuario')</code></p>
  
  <h5>Remove amigo -> loggin_required</h5>
  <p>Url para excluir amigo da lista. Espera o id do amigo passado na url como o "add_friend" e caso seja amigo será excluido da lista e retonara um mensagem, se não for ou for o proprio usuario retonara uma mensagem.</p>
  <p><code>server.app.add_url_rule('/remove_friend/<int:id>', endpoint='remove_friend',
                                    view_func= controllers.friend.remove_friend)</code></p>  
  <p>pelo url_for: <code> url_for('remove_friend', id='id do usuario')</code></p>
  
  <h5>Fazer um post -> loggin_required</h5>
  <p>Url para salvar postagem e compartilhar. Espera requisição feita por  um formulario com enctype="multipart/form-data". Espera receber 4 input <code>input name='tilte', textarea name='description', textare name='code', input file name='files[]' accept=".jpg, .mp4" multiple="true"</code> </p>
  <p><code>server.app.add_url_rule('/create_post', endpoint='create_post', 
                                    view_func= controllers.post.create_post,methods = ['POST'])</code></p>  
  <p>pelo url_for: <code> url_for('create_post')</code></p>
  
  <h5>Ver perfil de usuario -> loggin_required</h5>
  <p>Url para visualizar perfil e caso o usuario logado seja o dono edita-lo também. Espera um junto a url e um argumeto pag='edit' ou pag='view'. Exemplos:
  <code>/user_profile/7?pag=view</code> abre perfil do usuario 7 no modo de visulização.
  <code>/user_profile/7?pag=edit</code> abre perfil do usuario 7 no modo edição.
  Se o usuario tentar colocar edit em um perfil alheio ou não for colocado nenhum argumento, ele será redirecionado para a pagina do perfil colocado na url</p>
  <p><code>server.app.add_url_rule('/user_profile/<int:id>',endpoint='user_profile', 
                                    view_func =  controllers.user.user_profile)</code></p>  
  <p>pelo url_for: <code> url_for('user_profile', id='id do usuario', pag='view')</code></p>
  <p>pelo url_for: <code> url_for('user_profile', id='id do usuario', pag='edit')</code></p>
  
  <h5>Salva edição do usauario -> loggin_required</h5>
  <p>Url para salvar as alterações do uruario. Espera requisição feita por um form com os inputs com os seguintes nomes: <code>name = 'name', name='email', name='job', name='age', name='password', input type='file' name='image'</code> na url deve conter um argumento com o id do usuario. Exemplo: <code>/user_edit_save?id=3</code> requistar o servidor editar o registro de usuario com id = 3, essa rota não tem proteção.</p>
  <p><code>server.app.add_url_rule('/user_edit_save', endpoint='user_save',
                                    view_func = controllers.user.user_edit_save,methods = ['POST'])</code></p>  
  <p>pelo url_for: <code>url_for('user_save', id='id do usuario')</code> </p>
  
  <h5>Rota de arquivos</h5>
  <p>Url para servir ao sistema, ela deve ser usada caso precise requisitar um aquivo que foi feito upload pelo usario. Exemplo:
  <code>img src='{{url_for('uploads', filename='user_image4.jpg')}}'</code></p>
  <p><code>server.app.add_url_rule('/uploads/<filename>',endpoint='uploads',
                                    view_func =  controllers.uploads.upload_folder)</code></p>  
  <p>pelo url_for: <code>url_for('uploads',filename='nome do arquivo')</code> </p>
    
  <h5>Visuslizar post</h5>
  <p>URl para visualizar um postagem com mais detalhes. Espera um requisição com o id do post passado na url. Exemplo: <code>/post/16</code> mostra os comentarios e os tropicos compartilhado da postagem</p>
  <p><code>server.app.add_url_rule('/post/<int:id>', endpoint='post', 
                      view_func =  controllers.code.code_list,methods = ['GET']  )</code></p>  
  <p>pelo url_for: <code>url_for('post', id='id do post')</code> </p>

  
  <h5>Adicionar codigo -> loggin_required</h5>
  <p>Url para adcionar codigo a um postagem. Espera receber uma requisição por um form, o form deve 1 textare com <code>name='code'</code>, e deve ser passado no paramentro o id do post. Exemplo: <code>/add_code/8</code> adciona um novo codigo na postagem com id = 8 </p>
  <p><code>server.app.add_url_rule('/add_code/<int:id>', endpoint='add_code', 
                                    view_func =  controllers.code.add_code,methods=['POST'])</code></p>  
  <p>pelo url_for: <code>url_for('add_code', id='id da postagem')</code> </p>

  
  <h5>Deletar codigo -> loggin_required</h5>
  <p>Url para deletar um codigo pulicado em um postagem. Espera receber o id do codigo como paramentro e o id da postagem como argumento, se o usuario logado não for autor vai aparecer um mensagem de erro. Exemplo: <code>/delete_code/8?post_id=3</code> deleta o codigo com id 8 da postagem de id 3.</p>
  <p><code>server.app.add_url_rule('/delete_code/<int:id>', endpoint='delete_code', 
                                    view_func = controllers.code.delete_code)</code></p>  
  <p>pelo url_for: <code>url_for('delete_code', id = 'id do codigo', post_id='id do post')</code> </p>

  
  <h5>Deleta conta -> loggin_required</h5>
  <p>Url para deletar conta do usuario. Espera requisição com id do usuario como paramentro. Exemplo: <code>/delete_account/35</code> deleta usuario 35. Url não protegida.</p>
  <p><code>server.app.add_url_rule('/delete_account/<int:id>',endpoint='delete_account',
                    view_func=controllers.user.delete_account)</code></p>  
  <p>pelo url_for: <code>url_for('delete_account', id='id do usuario')</code> </p>

  
  <h5>Chat  -> loggin_required</h5>
  <p>Url para mostrar o chat. Espera id do usuario que deseja conversar como paramentro da rota e rederiza o chat de conversa. Exemplo: <code>chat/8</code> conversar com usuario de id = 8</p>
  <p><code></code>server.app.add_url_rule('/chat/<int:id>', endpoint='chat', 
                                    view_func=controllers.chat.chat)</p>  
    <p>pelo url_for: <code>url_for('chat', id='id do usuario')</code> </p>


  
  <h5>Deleta o Post -> loggin_required</h5>
  <p>Url para deletar o post. Espera um requisição com o id do post como parametro. Exemplo: <code>/delte_post/9</code> deleta a postagem com id 9. Url sem proteção</p>
  <p><code>server.app.add_url_rule('/delte_post/<int:id>', endpoint='delete_post',
                                    view_func=controllers.post.delete_post)</code></p>  
  <p>pelo url_for: <code>url_for('delete_post', id='id do post')</code> </p>

  
  <h5>Editar post -> loggin_required</h5>
  <p>Url para salvar edição do post. Espera um requisição de um form com os 3 inputs com o seguintes nome: <code> name='title', name='description', name='idPost' -> hidden input </code></p>
  <p><code>server.app.add_url_rule('/edit_post', endpoint='edit_post', 
                                    view_func=controllers.post.edit_post, methods=['POST'])</code></p>  
  <p>pelo url_for: <code>url_for('edit_post')</code> </p>
  
  <h5>Fazer comentario -> loggin_required</h5>
  <p>Url para inserir comentario. Espera uma requisição como o id do post como argumento e venha de um formulario. Com um textarea com o name='comment'. Exemplo: <code> /insert_comment?idPost=5</code> faz um comentario na postagem com id 5</p>
  <p><code>server.app.add_url_rule('/insert_comment', endpoint='insert_comment', view_func=controllers.comment.insertComment, methods=['POST'])</code></p>  
  <p>pelo url_for: <code>url_for('insert_comment', idPost='id da postagem')</code> </p>
  
  
  
 ## Estrutura do sistema
![diagrama drawio](https://user-images.githubusercontent.com/76654459/169879941-f180681c-95ca-4764-ae62-9403df4833bd.png)

