# **IMPORTAÇÕES DO DJANGO**
from django.apps import AppConfig  
    # Importa a classe base `AppConfig`, usada para configurar aplicativos no Django.

class TrendfeedsConfig(AppConfig):  
    # Define a configuração para o aplicativo `trendfeeds`.
    default_auto_field = 'django.db.models.BigAutoField'  
        # Especifica o tipo padrão de campo de chave primária automática para os modelos do aplicativo como `BigAutoField`.

    name = 'trendfeeds'  
        # Define o nome do aplicativo, que deve corresponder ao diretório do aplicativo.
