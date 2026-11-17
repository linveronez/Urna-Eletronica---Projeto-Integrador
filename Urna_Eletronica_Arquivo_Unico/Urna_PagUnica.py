"""Urna eletronica didatica em um unico arquivo, executada pelo terminal."""

# Cadastro: numero, nome, sigla, partido e cargo.
candidatos = [
    ["11", "Ana Silva", "PE", "Partido da Esperanca", "prefeito"],
    ["22", "Carlos Souza", "PP", "Partido do Progresso", "prefeito"],
    ["33", "Mariana Costa", "PM", "Partido da Mudanca", "prefeito"],
    ["11111", "Joao Lima", "PE", "Partido da Esperanca", "vereador"],
    ["11222", "Beatriz Rocha", "PE", "Partido da Esperanca", "vereador"],
    ["11333", "Fernando Dias", "PE", "Partido da Esperanca", "vereador"],
    ["11444", "Renata Castro", "PE", "Partido da Esperanca", "vereador"],
    ["22111", "Maria Oliveira", "PP", "Partido do Progresso", "vereador"],
    ["22222", "Lucas Martins", "PP", "Partido do Progresso", "vereador"],
    ["22333", "Juliana Alves", "PP", "Partido do Progresso", "vereador"],
    ["22444", "Roberto Mendes", "PP", "Partido do Progresso", "vereador"],
    ["33111", "Camila Pereira", "PM", "Partido da Mudanca", "vereador"],
    ["33222", "Gabriel Santos", "PM", "Partido da Mudanca", "vereador"],
    ["33333", "Patricia Barbosa", "PM", "Partido da Mudanca", "vereador"],
    ["33444", "Ricardo Gomes", "PM", "Partido da Mudanca", "vereador"],
]

votos = {c[0]: 0 for c in candidatos}
brancos = {"prefeito": 0, "vereador": 0}
nulos = {"prefeito": 0, "vereador": 0}
finalizada = False


def zeresima():
    """Zera a apuracao e imprime a relacao inicial de candidatos."""
    global finalizada
    for numero in votos:
        votos[numero] = 0
    for cargo in brancos:
        brancos[cargo] = 0
        nulos[cargo] = 0
    finalizada = False
    print("\nZERESIMA - contagem reiniciada")
    for cargo in ("prefeito", "vereador"):
        print("\n" + cargo.upper())
        for c in candidatos:
            if c[4] == cargo:
                print(f"{c[0]} - {c[1]} ({c[2]}) - 0 votos")


def votar(cargo, digitos):
    """Confirma a escolha antes de somar voto valido, branco ou nulo."""
    while True:
        numero = input(f"\nVoto para {cargo} ({digitos} digitos; B = branco): ").strip()
        escolhido = next((c for c in candidatos if c[0] == numero and c[4] == cargo), None)
        if numero.upper() == "B":
            tipo = "branco"
            print("Voto em branco.")
        elif escolhido:
            tipo = "candidato"
            print(f"Candidato: {escolhido[1]} | Partido: {escolhido[2]} - {escolhido[3]}")
        else:
            tipo = "nulo"
            print("Numero invalido ou nao cadastrado para este cargo. O voto sera NULO.")

        while True:
            resposta = input("Confirma a escolha? (S = confirmar, N = corrigir): ").strip().upper()
            if resposta in ("S", "N"):
                break
            print("Digite S para confirmar ou N para corrigir.")
        if resposta == "N":
            print("Escolha cancelada. Digite novamente.")
            continue

        if tipo == "candidato":
            votos[escolhido[0]] += 1
        elif tipo == "branco":
            brancos[cargo] += 1
        else:
            nulos[cargo] += 1
        print("Voto registrado.")
        return


def totalizar():
    """Exibe totais, resultado para prefeito e os tres mais votados a vereador."""
    print("\nTOTALIZACAO")
    for cargo in ("prefeito", "vereador"):
        print("\n" + cargo.upper())
        for c in candidatos:
            if c[4] == cargo:
                print(f"{c[0]} - {c[1]} ({c[2]}) - {votos[c[0]]} votos")
        print(f"Brancos: {brancos[cargo]} | Nulos: {nulos[cargo]}")

    prefeitos = [c for c in candidatos if c[4] == "prefeito"]
    maior = max(votos[c[0]] for c in prefeitos)
    lideres = [c for c in prefeitos if votos[c[0]] == maior and maior > 0]
    if not lideres:
        print("Nao houve votos validos para prefeito.")
    elif len(lideres) > 1:
        print("Empate na primeira colocacao: ocorrera segundo turno.")
    else:
        print(f"Prefeito vencedor: {lideres[0][1]} ({lideres[0][2]}).")

    vereadores = [c for c in candidatos if c[4] == "vereador" and votos[c[0]] > 0]
    # Ordena por votos; em empate, mantem a ordem original do cadastro.
    for i in range(len(vereadores)):
        for j in range(i + 1, len(vereadores)):
            if votos[vereadores[j][0]] > votos[vereadores[i][0]]:
                vereadores[i], vereadores[j] = vereadores[j], vereadores[i]
    print("Melhores colocados para vereador:")
    for posicao, c in enumerate(vereadores[:3], start=1):
        print(f"{posicao}o - {c[1]} ({c[2]}): {votos[c[0]]} votos")
    if len(vereadores) < 3:
        print(f"Vagas nao preenchidas: {3 - len(vereadores)}.")


def executar_votacao():
    global finalizada
    if finalizada:
        print("Votacao encerrada. Use a Zerésima para iniciar nova sessao.")
        return
    while True:
        votar("vereador", 5)
        votar("prefeito", 2)
        while True:
            proximo = input("Continuar com outro eleitor ou finalizar? (C/F): ").strip().upper()
            if proximo in ("C", "F"):
                break
            print("Digite C para continuar ou F para finalizar.")
        if proximo == "F":
            totalizar()
            finalizada = True
            return


def principal():
    print("URNA ELETRONICA DIDATICA - simulacao academica")
    while True:
        print("\n1 - Zerésima | 2 - Iniciar votacao | 3 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            zeresima()
        elif opcao == "2":
            executar_votacao()
        elif opcao == "3":
            print("Sessao encerrada.")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    principal()
