# Web News Project!

## Descrição

O Web News Project é uma aplicação Django, que oferece os recursos e funcionalidades que um site jornalístico esportivo proporcionam ao usuário. Este projeto foca em utilizar boas práticas de configuração e implementação com integração ao banco de dados relacional (MySQL) e integração a Interface de programação de aplicações (API).

---

## Requisitos

- Python 3.10 ou superior
- Django 5.1.2
- MySQL para banco de dados

---

## Configuração

### 1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/web-news-project.git
cd web-news-project
```

### 2. Crie um ambiente virtual (opcional):

Se preferir isolar as dependências do projeto, crie um ambiente virtual com o comando abaixo:
```bash
python -m venv 'nome_do_ambiente_virtual'
```

### 3. Instale as dependências:

Certifique-se de estar no diretório do projeto e instale as dependências com o comando:
```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`:

Na raiz do projeto, crie um arquivo `.env` com as seguintes variáveis de ambiente:

```env
SECRET_KEY='sua-chave-secreta'
DEBUG=True
ALLOWED_HOSTS='hosts-permitidos'
DB_NAME='nome-do-banco'
DB_PASSWORD='sua-senha'
DB_HOST='nome-do-host'
DB_PORT='sua-porta'
```

### 5. Configure o banco de dados:

Certifique-se de que o MySQL está em execução e que as credenciais no arquivo `.env` estão configuradas corretamente. Para isso, verifique o arquivo `.env` e ajuste as informações de acesso ao banco de dados.

Depois, execute as migrações para criar as tabelas e estruturar o banco de dados de acordo com os modelos definidos no projeto Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Inicie o servidor local:

Para iniciar o servidor de desenvolvimento local, utilize o seguinte comando:

```bash
python manage.py runserver
```

## Tecnologias Utilizadas

- **Django**: Framework web principal utilizado para a construção da aplicação.
- **MySQL**: Banco de dados relacional utilizado para armazenar os dados.

## Licença

Este projeto está licenciado sob a **MIT License**.
