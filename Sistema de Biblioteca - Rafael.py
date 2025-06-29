# Sistema de Gerenciamento de Biblioteca
# Trabalho apresentado para Disciplina de Lógica de Programação
# Nome: Rafael Dalavale Kaiser Pinto
# Cadeira/Turma: Lógica de Programação - 9587
# Professor: Victor Costa Melo

# =============================================================================
# Abaixo estão as estruturas de apoio: classes, variáveis de controle e funções
# =============================================================================

# As importações são necessárias para o funcionamento do sistema
# Dataclass: Para automatizar a criação de métodos especiais (__init__, __repr__, etc.)
# List: usado para indicar que vamos trabalhar com conjuntos (listas) de elementos do mesmo tipo
from dataclasses import dataclass
from typing import List

# Constante que definirá o valor da multa cobrada por cada dia de atraso
# Facilitando a manutenção do código caso seja necessário alterar o valor da multa
valor_multa_por_dia = 1

# Classe responsável por controlar o tempo no sistema da biblioteca, começando no dia 1
# Assim conseguimos simular a passagem de dias para testar prazos e multas
class Sistema:
    def __init__(self):
        self.dia_atual = 1

# Estrutura de dados que representa um livro na biblioteca
# A class Livro, contém todas as informações necessárias sobre cada livro
@dataclass
class Livro:
    codigo: str
    titulo: str
    autor: str
    ano: int
    genero: str
    total: int
    disponivel: int

# Estrutura que representará um usuário do sistema (aluno ou professor)
# Armazenando informações básicas que serão necessárias para identificação do usuário
# Tipo, foi usado para identificar "aluno" ou "professor", que também determinará prazo de empréstimo depois
@dataclass
class Usuario:
    identificador_usuario: str
    nome: str
    tipo: str

# Estrutura que registra cada empréstimo realizado no sistema
# Controla todo o ciclo de vida do empréstimo (desde a retirada até a devolução)
@dataclass
class Emprestimo:
    identificador_usuario: str
    codigo_livro: str
    dia_emprestimo: int
    dia_previsto: int
    status: str = "ativo"
    dia_efetivo: int = 0

# As Listas que funcionaram como "banco de dados" em memória
# E armazenam todos os dados do sistema durante a execução
lista_livros: List[Livro] = []
lista_usuarios: List[Usuario] = []
lista_emprestimos: List[Emprestimo] = []

# Função de busca que localiza um usuário pelo seu identificador
# Percorre a lista de usuários até encontrar o ID correspondente
# Retorna o objeto Usuario se encontrado, None caso contrário
def buscar_usuario(identificador):
    for usuario_atual in lista_usuarios:
        if usuario_atual.identificador_usuario == identificador:
            return usuario_atual
    return None

# Função de busca que localiza um livro pelo seu código
# Similar à busca de usuário, mas para livros
# Essencial para validar se um livro existe antes de operações
def buscar_livro(codigo):
    for livro_atual in lista_livros:
        if livro_atual.codigo == codigo:
            return livro_atual
    return None

# Função que irá verificar se existe um empréstimo ativo específico
# Importante para evitar múltiplos empréstimos do mesmo livro para o mesmo usuário
# Verifica três condições: usuário, livro e status ativo
def buscar_emprestimo_ativo(identificador_usuario, codigo_livro):
    for emprestimo_atual in lista_emprestimos:
        if (emprestimo_atual.identificador_usuario == identificador_usuario and
            emprestimo_atual.codigo_livro == codigo_livro and
            emprestimo_atual.status == "ativo"):
            return emprestimo_atual
    return None

# Função responsável pelo cadastro de novos livros no sistema
# Realiza validações para garantir a segurança dos dados
# Coleta informações do usuário e cria um novo objeto Livro
def cadastrar_livro():
    print("\n--------------------------------")
    print("------ Cadastro de Livro -------")
    print("--------------------------------")
    codigo = input("Código: ")

    # Verifica se o código já existe para evitar duplicações
    if buscar_livro(codigo):
        print("Código já existente!")
        return

    # Coleta as informações básicas do livro (titulo, autor e gênero)
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Gênero: ")

    # Tenta converter ano e quantidade para inteiros, com identificação de erros
    try:
        ano = int(input("Ano de publicação: "))
        quantidade = int(input("Quantidade total de exemplares: "))

        if quantidade <= 0:
            print("Quantidade deve ser positiva.")
            return
    except:
        print("Ano e quantidade devem ser números inteiros.")
        return

    # Criamos o livro com todos os exemplares disponíveis logo após o cadastro
    # Em seguida, adicionamos o livro à lista da biblioteca
    novo_livro = Livro(codigo, titulo, autor, ano, genero, quantidade, quantidade)
    lista_livros.append(novo_livro)
    print("Livro cadastrado com sucesso!")

# Função que exibe todos os livros cadastrados no sistema
# E mostrará todas informações completas, incluindo disponibilidade
def listar_livros():
    print("\n----------------------------------")
    print("----- Catálogo da Biblioteca -----")
    print("----------------------------------")

    # Verifica se existem livros cadastrados
    if not lista_livros:
        print("Nenhum livro cadastrado.")
        return

    # Percorre e exibe cada livro com suas informações
    # Determina a situação baseada na disponibilidade
    for livro_atual in lista_livros:
        situacao = "Disponível" if livro_atual.disponivel > 0 else "Indisponível"

        # Aqui mostrará os dados principais do livro em uma linha só
        # E abaixo exibirá o gênero, quantidade disponível e status (Disponível ou Indisponível)
        print(f"{livro_atual.codigo} | {livro_atual.titulo} - {livro_atual.autor} ({livro_atual.ano})")
        print(f"Gênero: {livro_atual.genero} | {livro_atual.disponivel}/{livro_atual.total} - {situacao}")

# Função que permitirá buscar um livro por código, título ou autor
def buscar_livro_por_criterio():
    print("\n--------------------------------")
    print("------- Buscar Livro ---------")
    print("--------------------------------")
    criterio = input("Digite o código, título ou autor do livro: ").strip().lower()
    
    livros_encontrados = []
    for livro_atual in lista_livros:
        if criterio == livro_atual.codigo.lower() or \
           criterio in livro_atual.titulo.lower() or \
           criterio in livro_atual.autor.lower():
            livros_encontrados.append(livro_atual)
            
    if not livros_encontrados:
        print("Nenhum livro encontrado com o critério informado.")
        return
        
    print("\n--- Livros Encontrados ---")
    for livro_atual in livros_encontrados:
        situacao = "Disponível" if livro_atual.disponivel > 0 else "Indisponível"
        print(f"{livro_atual.codigo} | {livro_atual.titulo} - {livro_atual.autor} ({livro_atual.ano})")
        print(f"Gênero: {livro_atual.genero} | {livro_atual.disponivel}/{livro_atual.total} - {situacao}")
    print("-" * 30)


# Função para cadastro de novos usuários (alunos ou professores)
# Valida tipo de usuário e evita IDs duplicados
def cadastrar_usuario():
    print("\n---------------------------------")
    print("------ Cadastro de Usuário ------")
    print("---------------------------------")
    identificador = input("ID do usuário: ")

    # Verifica se o ID já existe, e depois validará se o tipo é válido
    # E por fim cria e adiciona o novo usuário
    if buscar_usuario(identificador):
        print("Usuário já cadastrado.")
        return

    nome = input("Nome: ")
    tipo = input("Tipo (aluno ou professor): ")

    if tipo != "aluno" and tipo != "professor":
        print("Tipo inválido.")
        return

    novo_usuario = Usuario(identificador, nome, tipo)
    lista_usuarios.append(novo_usuario)
    print("\n")
    print("Usuário cadastrado com sucesso!")

# Função que lista todos os usuários cadastrados
# Exibe ID, nome e tipo de cada usuário
def listar_usuarios():
    print("\n--------------------------------")
    print("------ Lista de Usuários -------")
    print("--------------------------------")

    if not lista_usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario_atual in lista_usuarios:
        print(f"{usuario_atual.identificador_usuario} | {usuario_atual.nome} ({usuario_atual.tipo})")

# Função principal para realizar empréstimos de livros
# Realiza múltiplas validações e define prazos diferentes por tipo de usuário
# Ela irá buscar e validar o usuário e o livro
# Verificará a disponibilidade do livro e se o usuário já possui ele emprestado
def realizar_emprestimo(sistema):
    print("\n--------------------------------")
    print("------ Empréstimo de Livro ------")
    print("---------------------------------")

    identificador = input("ID do usuário: ")
    usuario = buscar_usuario(identificador)
    if not usuario:
        print("Usuário não encontrado.")
        return

    codigo = input("Código do livro: ")
    livro = buscar_livro(codigo)
    if not livro:
        print("Livro não encontrado.")
        return

    if livro.disponivel == 0:
        print("Livro indisponível.")
        return

    if buscar_emprestimo_ativo(identificador, codigo):
        print("Este usuário já possui este livro emprestado.")
        return

    # É definido um prazo baseado no tipo de usuário (aluno: 7 dias, professor: 10 dias)
    # Logo é feito o registro do empréstimo e ao final é realizada a redução de um livro da lista
    prazo = 7 if usuario.tipo == "aluno" else 10
    dia_previsto = sistema.dia_atual + prazo

    novo_emprestimo = Emprestimo(identificador, codigo, sistema.dia_atual, dia_previsto)
    lista_emprestimos.append(novo_emprestimo)

    livro.disponivel -= 1

    print("\n")
    print("Empréstimo registrado com sucesso!")
    print(f"Devolução prevista para o dia {dia_previsto}")

# Função que irá processar a devolução de livros emprestados
# Calculando multas em caso de atraso, atualizando a disponibilidade e status
# Começa coletando informações para localizar o empréstimo
def realizar_devolucao(sistema):
    print("\n--------------------------------")
    print("------ Devolução do Livro ------")
    print("--------------------------------")

    identificador = input("ID do usuário: ")
    codigo = input("Código do livro: ")

    emprestimo = buscar_emprestimo_ativo(identificador, codigo)
    if not emprestimo:
        print("Empréstimo não encontrado ou já devolvido.")
        return

    emprestimo.status = "devolvido"
    emprestimo.dia_efetivo = sistema.dia_atual

    livro = buscar_livro(codigo)
    livro.disponivel += 1

    atraso = sistema.dia_atual - emprestimo.dia_previsto
    if atraso > 0:
        multa = atraso * valor_multa_por_dia
        print(f"Devolução com {atraso} dia(s) de atraso. Multa: R$ {multa}")
    else:
        print("Devolução dentro do prazo. Obrigado!")

# Função que gera o relatório de todos os empréstimos ativos
# Mostra informações detalhadas incluindo dias restantes ou atraso
# Percorrerá todos os empréstimos buscando os ativos, e logo busca usuário e livro
# Por fim, calculará os dias restantes ou em atraso e exibirá as informações formatadas
def relatorio_emprestimos(sistema):
    print("\n--------------------------------")
    print("------ Livros Emprestados ------")
    print("--------------------------------")

    tem_emprestimo = False

    for emprestimo in lista_emprestimos:
        if emprestimo.status == "ativo":
            usuario = buscar_usuario(emprestimo.identificador_usuario)
            livro = buscar_livro(emprestimo.codigo_livro)

            dias = emprestimo.dia_previsto - sistema.dia_atual
            situacao = f"{dias} dias restantes" if dias >= 0 else f"{-dias} dias em atraso"

            print(f"Livro: {livro.titulo} | Usuário: {usuario.nome} | Situação: {situacao}")
            tem_emprestimo = True

    if not tem_emprestimo:
        print("Nenhum empréstimo esta ativo.")

# Função que gera o relatório de livros com devolução em atraso
def relatorio_livros_em_atraso(sistema):
    print("\n-------------------------------------")
    print("----- Livros com Devolução em Atraso -----")
    print("-------------------------------------")

    tem_atraso = False
    for emprestimo in lista_emprestimos:
        if emprestimo.status == "ativo" and emprestimo.dia_previsto < sistema.dia_atual:
            usuario = buscar_usuario(emprestimo.identificador_usuario)
            livro = buscar_livro(emprestimo.codigo_livro)

            dias_atraso = sistema.dia_atual - emprestimo.dia_previsto
            multa_estimada = dias_atraso * valor_multa_por_dia

            print(f"Livro: {livro.titulo} (Cód: {livro.codigo}) | "
                  f"Usuário: {usuario.nome} (ID: {usuario.identificador_usuario}) | "
                  f"Previsto: Dia {emprestimo.dia_previsto} | "
                  f"Atraso: {dias_atraso} dias | "
                  f"Multa Estimada: R$ {multa_estimada:.2f}")
            tem_atraso = True

    if not tem_atraso:
        print("Nenhum livro com devolução em atraso no momento.")
    print("-" * 30)

# Função que permitirá avançar o tempo no sistema, agora com opções de submenu
# Útil para caso queira simular a passagem de dias e testar prazos/multas
# É feito a conversão da entrada para inteiro com identificação de erro
def menu_gerenciar_tempo(sistema):
    while True:
        print("\n--------------------------------")
        print("------- Gerenciar Tempo --------")
        print("--------------------------------")
        print(f"Dia atual do sistema: {sistema.dia_atual}")
        print("1. Avançar 1 dia")
        print("2. Avançar 7 dias (1 semana)")
        print("3. Avançar N dias")
        print("4. Consultar dia atual")
        print("5. Voltar ao Menu Principal")

        opcao_tempo = input("Escolha uma opção: ")

        if opcao_tempo == '1':
            sistema.dia_atual += 1
            print(f"Sistema avançado para o dia {sistema.dia_atual}.")
        elif opcao_tempo == '2':
            sistema.dia_atual += 7
            print(f"Sistema avançado 7 dias. Novo dia: {sistema.dia_atual}.")
        elif opcao_tempo == '3':
            try:
                n_dias = int(input("Quantos dias deseja avançar? "))
                if n_dias > 0:
                    sistema.dia_atual += n_dias
                    print(f"Sistema avançado {n_dias} dias. Novo dia: {sistema.dia_atual}.")
                else:
                    print("Por favor, insira um número positivo de dias.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número inteiro.")
        elif opcao_tempo == '4':
            print(f"O dia atual do sistema é: {sistema.dia_atual}.")
        elif opcao_tempo == '5':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Esta função cria e gerencia o submenu para operações relacionadas a livros.
# Ela permite ao usuário escolher entre cadastrar, listar ou buscar livros,
# e retorna ao menu principal quando a opção de saída é selecionada.
def menu_gerenciar_livros():
    while True:
        print("\n=============================")
        print("==== GERENCIAR LIVROS =======")
        print("=============================")
        print("1. Cadastrar Novo Livro")
        print("2. Listar Todos os Livros")
        print("3. Buscar Livro")
        print("4. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_livro()
        elif opcao == '2':
            listar_livros()
        elif opcao == '3':
            buscar_livro_por_criterio() # Função para buscar por código/titulo/autor
        elif opcao == '4':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Esta função cria e gerencia o submenu para operações relacionadas a usuários.
# Ela oferece opções para cadastrar novos usuários ou listar todos os usuários existentes,
# garantindo uma navegação organizada e clara para o gerenciamento de usuários.
def menu_gerenciar_usuarios():
    while True:
        print("\n=============================")
        print("==== GERENCIAR USUÁRIOS =====")
        print("=============================")
        print("1. Cadastrar Novo Usuário")
        print("2. Listar Todos os Usuários")
        print("3. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Esta função cria e gerencia o submenu para a geração de relatórios.
# Permite ao usuário escolher entre visualizar livros atualmente emprestados
# ou livros com devolução em atraso, facilitando o acompanhamento da biblioteca.
def menu_relatorios(sistema):
    while True:
        print("\n=============================")
        print("======== RELATÓRIOS =========")
        print("=============================")
        print("")
        print("1. Livros Emprestados Atualmente")
        print("2. Livros com Devolução em Atraso")
        print("3. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            relatorio_emprestimos(sistema)
        elif opcao == '2':
            relatorio_livros_em_atraso(sistema)
        elif opcao == '3':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Função principal que irá controlar o fluxo do programa
# Apresentando o menu de opções e direcionando para as funções correspondentes
# Logo damos incio ao loop principal do programa, aonde ixibirá todos as opções disponíveis
# Iniciamos o contador de dias do sistema
# Logo entra o escolha, para identificar o que o usuário quer e executar a função correspondente
# As opções 1,2 e 5 chamará os Submenus
def menu_principal():

    sistema = Sistema()

    while True:
        print("\n=============================")
        print("====== MENU PRINCIPAL =======")
        print("=============================")
        print(f"Dia atual: {sistema.dia_atual}")
        print("\n")
        print("1. Gerenciar Livros") 
        print("2. Gerenciar Usuários") 
        print("3. Realizar Empréstimo")
        print("4. Realizar Devolução")
        print("5. Relatórios") 
        print("6. Gerenciar Tempo (Avançar/Consultar Dias)") 
        print("7. Sair") 

        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            menu_gerenciar_livros()
        elif escolha == "2":
            menu_gerenciar_usuarios()
        elif escolha == "3":
            realizar_emprestimo(sistema)
        elif escolha == "4":
            realizar_devolucao(sistema)
        elif escolha == "5":
            menu_relatorios(sistema)
        elif escolha == "6":
            menu_gerenciar_tempo(sistema) # Chamando o submenu de tempo
        elif escolha == "7": # Opção de sair foi para 7
            print("Finalizando o sistema. Até a próxima amigo(a)!")
            break
        else:
            print("Opção inválida. Porfavor, tente novamente.")

# Quando este arquivo for executado, o sistema começará por aqui
# Chamamos o menu principal para iniciar a biblioteca e o usuário interagir com o sistema
if __name__ == "__main__":
    menu_principal()

