''' **IMPORTAÇÕES DO DJANGO**  '''
# Importa a classe base `AppConfig`, usada para configurar aplicativos no Django.
from django.apps import AppConfig  

# Define a configuração para o aplicativo `trendfeeds`.
class TrendfeedsConfig(AppConfig):  

    # Especifica o tipo padrão de campo de chave primária automática para os modelos do aplicativo como `BigAutoField`.
    default_auto_field = 'django.db.models.BigAutoField'  
    name = 'trendfeeds'  
        # Define o nome do aplicativo, que deve corresponder ao diretório do aplicativo.

