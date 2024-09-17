# FavoriteHub API

Esta é uma API para gerenciar listas de favoritos, clientes e produtos usando Django e Django REST Framework. O projeto fornece funcionalidades para criar e gerenciar listas de produtos favoritos para cada cliente.

## Tecnologias Utilizadas
- [Django Rest (DRF)](https://www.django-rest-framework.org/)
- [DRF Paginagion](https://www.django-rest-framework.org/api-guide/pagination/)
- [DRF JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
- [DRF Renderers](https://www.django-rest-framework.org/api-guide/renderers/)
- [DRF-YASG (Swagger)](https://drf-yasg.readthedocs.io/en/stable/readme.html)
- [Python Decouple](https://github.com/henriquebastos/python-decouple)
- [Django Cors Headers](https://pypi.org/project/django-cors-headers/)
- [Python 3.11](https://www.python.org)
- [History Analysis (django-simple-history)](https://django-simple-history.readthedocs.io/en/latest/)

## Autenticação e Proteção de Rotas
- Todas as rotas da API são protegidas por autenticação. Apenas usuários autenticados podem acessar os endpoints disponíveis.
- A API utiliza **JWT (JSON Web Tokens)** para autenticar os usuários. Antes de acessar qualquer rota, é necessário que o usuário obtenha um token de acesso, que será utilizado para realizar requisições autenticadas.
- Exemplo: `Bearer <token_de_acesso>`

## History Analysis
Este projeto contém um script Python para analisar e imprimir o histórico de alterações dos objetos em uma aplicação Django usando `django-simple-history`, arquivo com mais informações em /check_logs/script_base.py.

### Funções

- **Parâmetros:**
  - `obj` (instância do modelo): A instância do modelo Django com registros históricos.
  - `limit` (int, opcional): O número máximo de registros históricos a processar. Se não especificado, todos os registros disponíveis serão processados.

- `print_history_summary(obj, limit=None)`
  - Imprime um resumo das ações realizadas nos registros de histórico do objeto fornecido.

- `print_field_changes(obj, limit=None)`
  - Imprime as mudanças nos campos entre as versões dos registros históricos do objeto fornecido.

- `print_all_history(obj)`
  - Imprime o histórico completo de alterações para o objeto fornecido, incluindo um resumo do histórico e mudanças nos campos.

## Modelos

### Client
Representa um cliente da aplicação.
- `email`: Email do cliente (único).
- `name`: Nome do cliente.

### Product
Representa um produto que pode ser adicionado à lista de favoritos de um cliente.
- `title`: Nome do produto.
- `image`: URL da imagem do produto.
- `price`: Preço do produto.

### Favorite
Representa a lista de favoritos de um cliente.
- `client`: Relacionamento OneToOne com o cliente.
- `products`: Muitos-para-Muitos com os produtos.
- Métodos:
  - `add_product(product)`: Adiciona um produto à lista de favoritos.
  - `remove_product(product)`: Remove um produto da lista de favoritos.
    
## Endpoints

### Authenticação
- **POST /api/register/**: Registra um novo usuário.
  - Request: ```json {"email": "usuario@example.com","password": "senha123"}```
  - Response: ```json {"tokens": {"access": "token_de_acesso","refresh": "token_de_refresh"}}```
- **POST /api/login/**: Faz login e retorna tokens de acesso.
  - Request: ```json {"email": "usuario@example.com","password": "senha123"}```
  - Response: ```json {"id": 1,"email": "usuario@example.com","tokens": {"access": "token_de_acesso","refresh": "token_de_refresh"}}```
- **POST /api/logout/**: Faz logout invalidando o token de refresh.
  - Request: ```json {"refresh": "token_de_refresh"}```
  - Response: ```json {"detail": "Logout realizado com sucesso"}```
  - 
### ClientViewSet
Gerencia os clientes.
- **GET /api/clients/**: Retorna uma lista de todos os clientes.
- **POST /api/clients/**: Cria um novo cliente.
- **PATCH /api/clients/{id}/**: Atualiza os dados de um cliente específico.
- **DELETE /api/clients/{id}/**: Remove um cliente.

### ProductListCreateAPIView
Gerencia a criação e listagem de produtos.
- **GET /api/products/**: Retorna uma lista de todos os produtos.
- **POST /api/products/**: Cria um novo produto.

### FavoriteViewSet
Gerencia as listas de favoritos de cada cliente.
- **GET /api/favorites/**: Retorna todas as listas de favoritos.
- **POST /api/favorites/**: Cria uma nova lista de favoritos para um cliente.
- **POST /api/favorites/{id}/add_product/**: Adiciona um produto à lista de favoritos de um cliente em específico.
- **POST /api/favorites/{id}/remove_product/**: Remove um produto da lista de favoritos de um cliente em específico.

## Funcionalidades

### Criar Lista de Favoritos
- Um cliente pode ter apenas uma lista de favoritos. 
- Ao criar uma nova lista, é necessário fornecer o `client_id` para associá-la ao cliente.

### Adicionar Produto à Lista de Favoritos
- Um produto pode ser adicionado à lista de favoritos de um cliente por meio do endpoint `/api/favorites/{id}/add_product/`, passando o `id` da lista pela url e o `product_id` no corpo da requisição.

### Remover Produto da Lista de Favoritos
- Um produto pode ser removido da lista de favoritos do cliente através do endpoint `/api/favorites/{id}/remove_product/`, passando o `id` da lista pela url e o `product_id` no corpo da requisição.

### Restrições
- **Cliente com lista duplicada**: Um cliente não pode ter mais de uma lista de favoritos. Isso é controlado no método `save` do modelo `Favorite`.
- **Produto já na lista**: O produto não pode ser adicionado mais de uma vez à mesma lista.

## Documentação de API
Esta API é documentada com Swagger, usando o pacote `drf-yasg`. A documentação interativa pode ser acessada através do endpoint:
- **/**: Interface interativa para testar os endpoints da API.

## Setup e Execução com Docker
Este guia explica como configurar, iniciar os containers e executar os testes no ambiente Docker.

### Pré-requisitos
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Certifique-se de ter o Docker e Docker Compose instalados antes de continuar.

### Instruções para rodar o projeto
1. Clonar o repositório, na sua máquina local: `git clone https://github.com/LucasDiasTavares/FavoriteHub`

2. Configurar o arquivo .env
   - Crie um arquivo .env na raiz do projeto e adicione as variáveis de ambiente necessárias. Utilize o arquivo env_example.
   - Certifique-se de ajustar os valores conforme necessário.
3. Construir e iniciar os containers
  - Para construir e iniciar os containers Docker, execute o seguinte comando:
  - `docker-compose up --build`
  - Este comando irá: Construir as imagens Docker e iniciar os containers do Django, PostgreSQL e quaisquer outros serviços configurados
4. Acessar a aplicação
   - Uma vez que os containers estiverem em execução, você poderá acessar a aplicação Django em http://localhost:8000 ou http://127.0.0.0:8000 ou http://0.0.0.0:8000 dependendo da forma que está configurado no seu Docker.

### Executar os testes
Para rodar os testes automatizados do Django, siga as instruções abaixo.
1. Conectar-se ao container
  - `docker-compose exec web bash`
2. Uma vez dentro do container, execute o seguinte comando para rodar os testes da aplicação:
   - Executa todos os testes:
     - `python manage.py test favoritehub.tests`
   - Executa apenas os testes relacionados ao cliente:
     - `python manage.py test favoritehub.tests.test_client`
   - Executa apenas os testes relacionados a lista de favoritos:
     - `python manage.py test favoritehub.tests.test_favorite`

### Desligar o projeto
- Execute o comando: `docker-compose down`
