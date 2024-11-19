from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria

@receiver(post_migrate)
def populate_initial_data(sender, **kwargs):
    # Verifique se já existem dados para evitar duplicação
    if not Categoria.objects.exists():
        # Dados dos times
        times_data = [
            
        # Times Série A
        ("atletico_mg", "Atlético-MG", "#000000", "Conhecido como Galo, é um dos maiores clubes de Minas Gerais, famoso por sua torcida apaixonada e conquistas históricas.", "A"),
        ("athletico_pr", "Athletico-PR", "#D81E05", "O Furacão de Curitiba, reconhecido por sua gestão moderna e seu estádio inovador, a Arena da Baixada.", "A"),
        ("bahia", "Bahia", "#003E92", "O Esquadrão de Aço, símbolo de orgulho do futebol nordestino, com duas conquistas do Campeonato Brasileiro.", "A"),
        ("botafogo", "Botafogo", "#000000", "O Fogão, clube do Rio de Janeiro com uma rica história e grande tradição no futebol brasileiro.", "A"),
        ("bragantino", "Bragantino", "#E30613", "Clube paulista patrocinado pela Red Bull, o Massa Bruta é conhecido por seu futebol jovem e dinâmico.", "A"),
        ("corinthians", "Corinthians", "#000000", "O Timão é uma das maiores potências do futebol brasileiro, com uma torcida enorme e conquistas memoráveis.", "A"),
        ("cruzeiro", "Cruzeiro", "#003DA5", "A Raposa é uma gigante mineira, conhecida por suas conquistas nacionais e internacionais.", "A"),
        ("cuiaba", "Cuiabá", "#00843D", "O Dourado representa Mato Grosso e tem se destacado no cenário nacional com seu crescimento recente.", "A"),
        ("flamengo", "Flamengo", "#E30613", "O Rubro-Negro carioca é o clube mais popular do Brasil, com uma história repleta de títulos e jogadores lendários.", "A"),
        ("fluminense", "Fluminense", "#880016", "O Tricolor das Laranjeiras, clube tradicional do Rio de Janeiro, famoso por seu estilo de jogo elegante.", "A"),
        ("fortaleza", "Fortaleza", "#0033A0", "O Leão do Pici é um dos grandes representantes do Nordeste, com uma torcida vibrante e crescente protagonismo no cenário nacional.", "A"),
        ("gremio", "Grêmio", "#6CABDD", "O Imortal Tricolor do Rio Grande do Sul é conhecido por sua força, raça e conquistas históricas.", "A"),
        ("internacional", "Internacional", "#E30613", "O Colorado de Porto Alegre, com uma história rica e títulos internacionais memoráveis.", "A"),
        ("palmeiras", "Palmeiras", "#009739", "O Verdão, clube paulista de grande tradição, conhecido por suas conquistas e estrutura moderna.", "A"),
        ("sao_paulo", "São Paulo", "#E30613", "O Tricolor Paulista, famoso por sua hegemonia internacional e grandeza histórica.", "A"),
        ("vasco", "Vasco", "#000000", "O Gigante da Colina, um dos clubes mais tradicionais do Rio de Janeiro, com uma rica história e torcida apaixonada.", "A"),
        ("juventude", "Juventude", "#00843D", "O clube de Caxias do Sul, conhecido como Juve, tem história marcante no futebol gaúcho.", "A"),
        ("criciuma", "Criciúma", "#FFD700", "O Tigre de Santa Catarina é famoso por sua conquista da Copa do Brasil em 1991.", "A"),
        ("vitoria", "Vitória", "#E30613", "O Leão da Barra, clube baiano com uma torcida fiel e tradição no futebol nordestino.", "A"),
        ("atletico_go", "Atlético-GO", "#D81E05", "O Dragão de Goiás, com força crescente no cenário nacional e estadual.", "A"),
        
        # Seleção Brasileira
        ("selecao", "Seleção Brasileira", "#FFCC00", "Conhecida como Canarinho, é a seleção mais bem-sucedida da história do futebol mundial, com cinco títulos de Copa do Mundo.", None),
        
        # Times Série B
        ("ceara", "Ceará", "#000000", "O Vozão é um dos grandes clubes do Nordeste, com uma torcida fiel e tradição regional.", "B"),
        ("crb", "CRB", "#E30613", "O clube alagoano é conhecido por sua consistência no cenário regional e nacional.", "B"),
        ("amazonas", "Amazonas", "#FFD700", "A Onça Pintada é um clube emergente da região Norte, representando o Amazonas no cenário nacional.", "B"),
        ("operario_pr", "Operário-PR", "#000000", "O Fantasma é um clube tradicional do Paraná, conhecido por sua história e resistência no futebol.", "B"),
        ("brusque", "Brusque", "#FFCC00", "O maior do Vale do Itajaí, Brusque é reconhecido por sua tradição no futebol catarinense.", "B"),
        ("paysandu", "Paysandu", "#009FDA", "O Papão da Curuzu é uma lenda da região Norte, com grande torcida e tradição histórica.", "B"),
        ("chapecoense", "Chapecoense", "#00843D", "A Chape é um clube que emocionou o mundo com sua história de superação e união.", "B"),
        ("ituano", "Ituano", "#D81E05", "O Galo de Itu é um clube paulista conhecido por sua regularidade e revelação de talentos.", "B"),
        ("mirassol", "Mirassol", "#FFD700", "O Leão do interior paulista é conhecido por sua gestão estável e futebol competitivo.", "B"),
        ("novorizontino", "Novorizontino", "#FFD700", "O Tigre do Vale é um clube emergente, com destaque no futebol do interior paulista.", "B"),
        ("ponte_preta", "Ponte Preta", "#000000", "A Macaca é um dos clubes mais tradicionais do Brasil, com história rica no futebol paulista.", "B"),
        ("sport", "Sport", "#E30613", "O Leão da Ilha é um dos maiores clubes do Nordeste, com conquistas importantes e torcida apaixonada.", "B"),
        ("vila_nova", "Vila Nova", "#D81E05", "O Tigre de Goiás é reconhecido por sua torcida fiel e tradição regional.", "B"),
        ("avai", "Avaí", "#003DA5", "O Leão da Ilha catarinense tem uma história rica e grande torcida.", "B"),
        ("botafogo_sp", "Botafogo-SP", "#000000", "A Pantera é um clube tradicional do interior paulista, com destaque no cenário regional.", "B"),
        ("guarani", "Guarani", "#00843D", "O Bugre é o único clube do interior paulista a conquistar o Campeonato Brasileiro.", "B"),
        ("goias", "Goiás", "#00843D", "O Esmeraldino é um dos grandes clubes do Centro-Oeste, com história e conquistas relevantes.", "B"),
        ("santos", "Santos", "#000000", "O Peixe é um dos clubes mais vitoriosos do Brasil, com uma história gloriosa e grande revelador de talentos.", "B"),
        ("coritiba", "Coritiba", "#00843D", "O Coxa é um dos maiores clubes de Curitiba, com uma torcida apaixonada e uma história de títulos nacionais.", "B"),
        ("america_mg", "América-MG", "#00843D", "O Coelho é um clube tradicional de Minas Gerais, com uma trajetória sólida no futebol brasileiro.", "B")
        ]
        
        # Inserindo os dados na tabela
        for categoria, nome, cor, descricao, serie in times_data:
            Categoria.objects.create(nome_categoria=categoria, nome=nome, cor=cor, descricao=descricao, serie=serie)