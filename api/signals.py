from django.db.models.signals import post_migrate
from django.dispatch import receiver
from api.models import Time, Jogador, Presidente, Tecnico, Estadio
from trendfeeds.models import Categoria
from unidecode import unidecode

@receiver(post_migrate)
def popular_banco(sender, **kwargs):
    
    if not Time.objects.exists():
        times = [
        
        # << Série A >>
        
        {
            "nome": "Atlético-MG",
            "ano_fundacao": 1908,
            "presidente": "Sérgio Coelho",
            "tecnico": "Gabriel Milito",
            "estadio": "Arena MRV",
            "jogadores": [
                ("Hulk", "Atacante"),
                ("Gustavo Scarpa", "Meia"),
                ("Éverson", "Goleiro")]
        },
        {
            "nome": "Athletico-PR",
            "ano_fundacao": 1924,
            "presidente": "Mario Celso Petraglia",
            "tecnico": "Lucho Gonzalez",
            "estadio": "Ligga Arena",
            "jogadores": [
                ("Agustín Canobbio", "Atacante"),
                ("Fernandinho", "Meia"),
                ("Thiago Heleno", "Defensor")]
        },
        {
            "nome": "Bahia",
            "ano_fundacao": 1931,
            "estadio": "Arena Fonte Nova",
            "cidade": "Salvador",
            "presidente": "Guilherme Bellintani",
            "tecnico": "Rogério Ceni",
            "jogadores": [
                ("Thaciano", "Atacante"),
                ("Everton Ribeiro", "Meia"),
                ("Cauly", "Meia")]
        },
        {
            "nome": "Botafogo",
            "ano_fundacao": 1894,
            "estadio": "Estádio Nilton Santos",
            "cidade": "Rio de Janeiro",
            "presidente": "Durcesio Mello",
            "tecnico": "Artur Jorge",
            "jogadores": [
                ("Luiz Henrique", "Atacante"),
                ("Thiago Almada", "Meia"),
                ("John", "Goleiro")]
        },
        {
            "nome": "Red Bull Bragantino",
            "ano_fundacao": 1928,
            "estadio": "Estádio Nabi Abi Chedid",
            "cidade": "Bragança Paulista",
            "presidente": "Marquinho Chedid",
            "tecnico": "Fernando Seabra",
            "jogadores": [
                ("Eduardo Sasha", "Atacante"),
                ("Lincoln", "Meia"),
                ("Juninho Capixaba", "Defensor")]
        },
        {
            "nome": "Corinthians",
            "ano_fundacao": 1910,
            "estadio": "Neo Química Arena",
            "cidade": "São Paulo",
            "presidente": "Augusto Melo",
            "tecnico": "Ramón Díaz",
            "jogadores": [
                ("Memphis Depay", "Atacante"),
                ("Yuri Alberto", "Atacante"),
                ("Rodrigo Garro", "Meia"),]
        },
        {
            "nome": "Cruzeiro",
            "ano_fundacao": 1921,
            "estadio": "Mineirão",
            "cidade": "Belo Horizonte",
            "presidente": "Lidson Potsch",
            "tecnico": "Fernando Diniz",
            "jogadores": [
                ("Kaio Jorge", "Atacante"),
                ("Matheus Pereira", "Meia"),
                ("Cássio", "Goleiro")]
        },
        {
            "nome": "Cuiabá",
            "ano_fundacao": 2001,
            "estadio": "Arena Pantanal",
            "cidade": "Cuiabá",
            "presidente": "Cristiano Dresch",
            "tecnico": "Bernardo Franco",
            "jogadores": [
                ("Isidro Pitta", "Atacante"),
                ("Fernando Sobral", "Meia"),
                ("Walter", "Goleiro")]
        },
        {
            "nome": "Flamengo",
            "ano_fundacao": 1895,
            "estadio": "Maracanã",
            "cidade": "Rio de Janeiro",
            "presidente": "Rodolfo Landim",
            "tecnico": "Filipe Luís",
            "jogadores": [
                ("Pedro", "Atacante"),
                ("Giorgian De Arrascaeta", "Meia"),
                ("Agustín Rossi", "Goleiro")]
        },
        {
            "nome": "Fluminense",
            "ano_fundacao": 1902,
            "estadio": "Maracanã",
            "cidade": "Rio de Janeiro",
            "presidente": "Mário Bittencourt",
            "tecnico": "Mano Menezes",
            "jogadores": [
                ("Germán Cano", "Atacante"),
                ("Paulo Henrique Ganso", "Meia"),
                ("Fábio", "Goleiro")]
        },
        {
            "nome": "Fortaleza",
            "ano_fundacao": 1918,
            "estadio": "Arena Castelão",
            "cidade": "Fortaleza",
            "presidente": "Alex Santiago",
            "tecnico": "Juan Pablo Vojvoda",
            "jogadores": [
                ("Juan Martín Lucero", "Atacante"),
                ("Marinho", "Atacante"),
                ("Titi", "Defensor")]
        },
        {
            "nome": "Grêmio",
            "ano_fundacao": 1903,
            "estadio": "Arena do Grêmio",
            "cidade": "Porto Alegre",
            "presidente": "Alberto Guerra",
            "tecnico": "Renato Gaúcho",
            "jogadores": [
                ("Martín Braithwaite", "Atacante"),
                ("Yeferson Soteldo", "Atacante"),
                ("Agustín Marchesín", "Goleiro")]
        },
        {
            "nome": "Internacional",
            "ano_fundacao": 1909,
            "estadio": "Beira-Rio",
            "cidade": "Porto Alegre",
            "presidente": "Alessandro Barcellos",
            "tecnico": "Roger Machado",
            "jogadores": [
                ("Rafael Borré", "Atacante"),
                ("Alan Patrick", "Meia"),
                ("Sergio Rochet", "Goleiro")]
        },
        {
            "nome": "Palmeiras",
            "ano_fundacao": 1914,
            "estadio": "Allianz Parque",
            "cidade": "São Paulo",
            "presidente": "Leila Pereira",
            "tecnico": "Abel Ferreira",
            "jogadores": [
                ("Raphael Veiga", "Meia"),
                ("Richard Ríos", "Volante"),
                ("Gustavo Gómez", "Defensor")]
        },
        {
            "nome": "São Paulo",
            "ano_fundacao": 1930,
            "estadio": "Morumbis",
            "cidade": "São Paulo",
            "presidente": "Júlio Casares",
            "tecnico": "Luis Zubeldia",
            "jogadores": [
                ("Jonathan Calleri", "Atacante"),
                ("Lucas", "Meia"),
                ("Robert Arboleda", "Defensor")]
        },
        {
            "nome": "Vasco",
            "ano_fundacao": 1898,
            "estadio": "São Januário",
            "cidade": "Rio de Janeiro",
            "presidente": "Pedrinho",
            "tecnico": "Rafael Paiva",
            "jogadores": [
                ("Pablo Vegetti", "Atacante"),
                ("Dimitri Payet", "Meia"),
                ("Philippe Coutinho", "Meia")]
        },
        {
            "nome": "Juventude",
            "ano_fundacao": 1913,
            "estadio": "Estádio Alfredo Jaconi",
            "cidade": "Caxias do Sul",
            "presidente": "Fábio Pizzamiglio",
            "tecnico": "Fábio Matias",
            "jogadores": [
                ("Gilberto", "Atacante"),
                ("Lucas Barbosa", "Atacante"),
                ("Nenê", "Meia")]
        },
        {
            "nome": "Criciúma",
            "ano_fundacao": 1947,
            "estadio": "Estádio Heriberto Hülse",
            "cidade": "Criciúma",
            "presidente": "Vilmar Guedes",
            "tecnico": "Cláudio Tencati",
            "jogadores": [
                ("Yannick Bolasie", "Atacante"),
                ("Felipe Vizeu", "Atacante"),
                ("Gustavo", "Goleiro")]
        },
        {
            "nome": "Vitória",
            "ano_fundacao": 1899,
            "estadio": "Estadio Manoel Barradas",
            "cidade": "Salvador",
            "presidente": "Fábio Mota",
            "tecnico": "Thiago Carpini",
            "jogadores": [
                ("Alerrandro", "Atacante"),
                ("Matheuzinho", "Meia"),
                ("Lucas Arcanjo", "Goleiro")]
        },
        {
            "nome": "Atlético-GO",
            "ano_fundacao": 1937,
            "estadio": "Estádio Antônio Accioly",
            "cidade": "Goiânia",
            "presidente": "Adson Batista",
            "tecnico": "Anderson Gomes",
            "jogadores": [
                ("Luiz Fernando", "Atacante"),
                ("Alejo Cruz", "Meia"),
                ("Ronaldo", "Goleiro")]
        },
        
        # << Seleção Brasileira >>
        
        {
            "nome": "Seleção Brasileira",
            "ano_fundacao": 1914,
            "estadio": "Maracanã",
            "cidade": "Rio de Janeiro",
            "presidente": "Ednaldo Rodrigues",
            "tecnico": "Dorival Júnior",
            "jogadores": [
                ("Vinícius Júnior", "Atacante"),
                ("Raphinha", "Meia"),
                ("Rodrigo", "Meia")]
        },
        
        # << Série B >>
        
        {
            "nome": "Ceará",
            "ano_fundacao": 1914,
            "estadio": "Arena Castelão",
            "cidade": "Fortaleza",
            "presidente": "João Paulo Silva",
            "tecnico": "Léo Condé",
            "jogadores": [
                ("Saulo Mineiro", "Atacante"),
                ("Erick Pulga", "Meia"),
                ("Fernando Miguel", "Goleiro")]
        },
        {
            "nome": "CRB",
            "ano_fundacao": 1912,
            "estadio": "Estádio Rei Pelé",
            "cidade": "Maceió",
            "presidente": "Mário Marroquim",
            "tecnico": "Helio Dos Anjos",
            "jogadores": [
                ("Rafael Bilú", "Atacante"),
                ("Chay", "Meia"),
                ("Luis Segovia", "Goleiro")]
        },
        {
            "nome": "Amazonas",
            "ano_fundacao": 2000,
            "estadio": "Estádio da Colina",
            "cidade": "Manaus",
            "presidente": "Wesley Couto dos Santos",
            "tecnico": "Ibson",
            "jogadores": [
                ("Sassá", "Atacante"),
                ("Dentinho", "Atacante"),
                ("Matheus Serafim", "Meia")]
        },
        {
            "nome": "Operário-PR",
            "ano_fundacao": 1912,
            "estadio": "Estádio Germano Krüger",
            "cidade": "Ponta Grossa",
            "presidente": "Álvaro Góes",
            "tecnico": "Rafael Guanaes",
            "jogadores": [
                ("Vinicius Mingotti", "Atacante"),
                ("Gabriel Boschilia", "Meia"),
                ("Rodrigo Lindoso", "Meia")]
        },
        {
            "nome": "Brusque",
            "ano_fundacao": 1989,
            "estadio": "Estádio Augusto Bauer",
            "cidade": "Brusque",
            "presidente": "Danilo Rezini",
            "tecnico": "Marcelo Cabo",
            "jogadores": [
                ("Keké", "Atacante"),
                ("Rodolfo Potiguar", "Meia"),
                ("Wallace Reis", "Defensor")]
        },
        {
            "nome": "Paysandu",
            "ano_fundacao": 1914,
            "estadio": "Estádio da Curuzu",
            "cidade": "Belém",
            "presidente": "Roger Aguilera",
            "tecnico": "Márcio Fernandes",
            "jogadores": [
                ("Nicolas", "Atacante"),
                ("Jean Dias", "Atacante"),
                ("Robinho", "Meia")]
        },
        {
            "nome": "Chapecoense",
            "ano_fundacao": 1973,
            "estadio": "Arena Condá",
            "cidade": "Chapecó",
            "presidente": "Alex Passos",
            "tecnico": "Gilmar Dal Pozzo",
            "jogadores": [
                ("Neílton", "Meia"),
                ("Rodrigo Moledo", "Defensor"),
                ("Matheus Cavichioli", "Goleiro")]
        },
        {
            "nome": "Ituano",
            "ano_fundacao": 1947,
            "estadio": "Estádio Novelli Júnior",
            "cidade": "Itu",
            "presidente": "João Paulo Ruiz",
            "tecnico": "Alberto Valentim",
            "jogadores": [
                ("Thonny Anderson", "Atacante"),
                ("Marcinho", "Defensor"),
                ("Saulo", "Goleiro")]
        },
        {
            "nome": "Mirassol",
            "ano_fundacao": 1925,
            "estadio": "Estádio José Maria de Campos Maia",
            "cidade": "Mirassol",
            "presidente": "Edson Antonio Ermenegildo",
            "tecnico": "Mozart Santos",
            "jogadores": [
                ("Léo Gamalho", "Atacante"),
                ("Chico Kim", "Meia"),
                ("Alex Muralha", "Goleiro")]
        },
        {
            "nome": "Novorizontino",
            "ano_fundacao": 1990,
            "estadio": "Estádio Jorge Ismael de Biasi",
            "cidade": "Novo Horizonte",
            "presidente": "Genilson Rocha Santos",
            "tecnico": "Eduardo Baptista",
            "jogadores": [
                ("Lucca", "Atacante"),
                ("Neto Pessoa", "Atacante"),
                ("Dudu", "Meia")]
        }, 
        {
            "nome": "Ponte Preta",
            "ano_fundacao": 1900,
            "estadio": "Estádio Moisés Lucarelli",
            "cidade": "Campinas",
            "presidente": "Marco Antonio Eberlin",
            "tecnico": "Joao Brigatti",
            "jogadores": [
                ("Jeh", "Atacante"),
                ("Emerson Santos", "Meia"),
                ("Dodô", "Meia")]
        },
        {
            "nome": "Sport",
            "ano_fundacao": 1905,
            "estadio": "Arena Pernambuco",
            "cidade": "Recife",
            "presidente": "Yuri Romão",
            "tecnico": "Pepa",
            "jogadores": [
                ("Zé Roberto", "Atacante"),
                ("Lucas Lima", "Meia"),
                ("Dalbert", "Defensor")]
        },
        {
            "nome": "Vila Nova",
            "ano_fundacao": 1943,
            "estadio": "Estádio Serra Dourada",
            "cidade": "Goiânia",
            "presidente": "Hugo Jorge Bravo",
            "tecnico": "Thiago Carvalho",
            "jogadores": [
                ("Apodi", "Atacante"),
                ("Ralf", "Meia"),
                ("Juan Quintero", "Defensor")]
        },
        {
            "nome": "Avaí",
            "ano_fundacao": 1923,
            "estadio": "Estádio da Ressacada",
            "cidade": "Florianópolis",
            "presidente": "Júlio Heerdt",
            "tecnico": "Enderson Moreira",
            "jogadores": [
                ("Vágner Love", "Atacante"),
                ("William Pottker", "Atacante"),
                ("Douglas Friedrich", "Goleiro")]
        },
        {
            "nome": "Botafogo-SP",
            "ano_fundacao": 1918,
            "estadio": "Estádio Santa Cruz",
            "cidade": "Ribeirão Preto",
            "presidente": "Eduardo Esteves",
            "tecnico": "Márcio Zanardi",
            "jogadores": [
                ("Jonas Toró", "Atacante"),
                ("Victor Andrade", "Meia"),
                ("Michael", "Goleiro")]
        },
        {
            "nome": "Guarani",
            "ano_fundacao": 1911,
            "estadio": "Estádio Brinco de Ouro",
            "cidade": "Campinas",
            "presidente": "Rômulo Amaro",
            "tecnico": "Allan Rodrigo Aal",
            "jogadores": [
                ("Bruno Mendes", "Atacante"),
                ("Estêvão", "Meia"),
                ("Heitor", "Defensor")]
        },
        {
            "nome": "Goiás",
            "ano_fundacao": 1943,
            "estadio": "Estádio de Hailé Pinheiro",
            "cidade": "Goiânia",
            "presidente": "Aroldo Guidão Filho",
            "tecnico": "Vagner Mancini",
            "jogadores": [
                ("Thiago Galhardo", "Atacante"),
                ("Paulo Baya", "Meia"),
                ("David Braz", "Defensor")]
        },
        {
            "nome": "Santos",
            "ano_fundacao": 1912,
            "estadio": "Arena Santos",
            "cidade": "Santos",
            "presidente": "Marcelo Pirilo Teixeira",
            "tecnico": "Leandro Zago",
            "jogadores": [
                ("Rómulo Otero", "Meia"),
                ("Giuliano", "Meia"),
                ("João Paulo", "Goleiro")]
        },
        {
            "nome": "Coritiba",
            "ano_fundacao": 1909,
            "estadio": "Estádio Couto Pereira",
            "cidade": "Curitiba",
            "presidente": "Glenn Stenger",
            "tecnico": "Guilherme Dalzotto Bossle",
            "jogadores": [
                ("Erick Castillo", "Atacante"),
                ("Alef Manga", "Meia"),
                ("Figueiredo", "Meia")]
        },
        {
            "nome": "América-MG",
            "ano_fundacao": 1912,
            "estadio": "Independência",
            "cidade": "Belo Horizonte",
            "presidente": "Marcus Salum",
            "tecnico": "Diogo Giacomini",
            "jogadores": [
                ("Brenner", "Atacante"),
                ("Martín Benítez", "Meia"),
                ("Juninho", "Meia")]
        }
        ]
    
    if not Categoria.objects.exists():
        times_data = [
            
        # Times Série A
        ("atletico_mg", "Atlético-MG", "#000000", "Conhecido como Galo, é um dos maiores clubes de Minas Gerais, famoso por sua torcida apaixonada e conquistas históricas.", "A"),
        ("athletico_pr", "Athletico-PR", "#D81E05", "O Furacão de Curitiba, reconhecido por sua gestão moderna e seu estádio inovador, a Arena da Baixada.", "A"),
        ("bahia", "Bahia", "#003E92", "O Esquadrão de Aço, símbolo de orgulho do futebol nordestino, com duas conquistas do Campeonato Brasileiro.", "A"),
        ("botafogo", "Botafogo", "#000000", "O Fogão, clube do Rio de Janeiro com uma rica história e grande tradição no futebol brasileiro.", "A"),
        ("bragantino", "Red Bull Bragantino", "#E30613", "Clube paulista patrocinado pela Red Bull, o Massa Bruta é conhecido por seu futebol jovem e dinâmico.", "A"),
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
        
        for time_data in times:
            if nome == time_data["nome"]:
            
                nome_formatado_presidente = unidecode(time_data["presidente"]).replace(" ", "_").lower()
                nome_formatado_tecnico = unidecode(time_data["tecnico"]).replace(" ", "_").lower()
                nome_formatado_estadio = unidecode(time_data["estadio"]).replace(" ", "_").lower()
                
                time, created = Time.objects.get_or_create(
                    nome=time_data["nome"],
                    ano_fundacao=time_data["ano_fundacao"]
                )
                
                Presidente.objects.get_or_create(
                    time=time,
                    nome=time_data["presidente"],
                    foto=f"presidentes/{nome_formatado_presidente}.png"
                )

                Tecnico.objects.get_or_create(
                    time=time,
                    nome=time_data["tecnico"],
                    foto=f"tecnicos/{nome_formatado_tecnico}.png"
                )

                Estadio.objects.get_or_create(
                    time=time,
                    nome=time_data["estadio"],
                    foto=f"estadios/{nome_formatado_estadio}.png"
                )

                for jogador_nome, jogador_posicao in time_data["jogadores"]:
                    
                    nome_formatado_jogador = unidecode(jogador_nome).replace(" ", "_").lower()
                    
                    Jogador.objects.get_or_create(
                        time=time,
                        nome=jogador_nome,
                        posicao=jogador_posicao,
                        foto=f"jogadores/{nome_formatado_jogador}.png"
                    )
                
        Categoria.objects.create(nome_categoria=categoria, nome=nome, cor=cor, descricao=descricao, serie=serie, time=time)
    
    Categoria.objects.create(nome_categoria="outros", nome="Outros", cor=None, descricao=None, serie=None, time=None)