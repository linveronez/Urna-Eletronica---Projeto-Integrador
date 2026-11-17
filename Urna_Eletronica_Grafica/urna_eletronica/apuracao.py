"""Contagem dos votos e apresentação dos resultados."""


class Apuracao:
    def __init__(self, candidatos):
        # A apuração usa a lista já criada pelo catálogo.
        self.candidatos = candidatos
        # Os votos brancos e nulos são separados por cargo.
        self.brancos = {"prefeito": 0, "vereador": 0}
        self.nulos = {"prefeito": 0, "vereador": 0}

    def zerar_votos(self):
        # Reinicia os votos dos candidatos e os totais de branco/nulo.
        for candidato in self.candidatos:
            candidato.votos = 0
        self.brancos = {"prefeito": 0, "vereador": 0}
        self.nulos = {"prefeito": 0, "vereador": 0}

    def registrar_voto(self, cargo, tipo, candidato=None):
        # Só soma voto depois que a interface recebe a confirmação.
        if tipo == "candidato":
            candidato.votos += 1
        elif tipo == "branco":
            self.brancos[cargo] += 1
        else:
            self.nulos[cargo] += 1

    def criar_zeresima(self):
        # Monta as linhas que serão exibidas no relatório inicial.
        linhas = ["ZERÉSIMA - TODOS OS CANDIDATOS COMEÇAM COM ZERO VOTOS", ""]
        for cargo in ["prefeito", "vereador"]:
            linhas.append(cargo.upper())
            for candidato in self.candidatos:
                if candidato.cargo == cargo:
                    linhas.append(
                        f"{candidato.numero} - {candidato.nome} - "
                        f"{candidato.sigla} ({candidato.partido}) - 0 votos"
                    )
            linhas.append("")
        linhas.append("Votos brancos: 0 | Votos nulos: 0")
        return "\n".join(linhas)

    def criar_totalizacao(self):
        # Mostra todos os candidatos, mesmo quem recebeu zero votos.
        linhas = ["TOTALIZAÇÃO DA VOTAÇÃO", ""]
        for cargo in ["prefeito", "vereador"]:
            linhas.append(cargo.upper())
            lista_cargo = []
            for candidato in self.candidatos:
                if candidato.cargo == cargo:
                    lista_cargo.append(candidato)
                    linhas.append(
                        f"{candidato.numero} - {candidato.nome} - "
                        f"{candidato.sigla} - {candidato.votos} votos"
                    )
            linhas.append(
                f"Brancos: {self.brancos[cargo]} | Nulos: {self.nulos[cargo]}"
            )

            if cargo == "prefeito":
                self._mostrar_vencedor_prefeito(lista_cargo, linhas)
            else:
                self._mostrar_vereadores_eleitos(lista_cargo, linhas)
            linhas.append("")
        return "\n".join(linhas)

    def _mostrar_vencedor_prefeito(self, candidatos, linhas):
        # Guarda os candidatos que estão empatados na maior contagem.
        maior_numero_de_votos = 0
        lideres = []
        for candidato in candidatos:
            if candidato.votos > maior_numero_de_votos:
                maior_numero_de_votos = candidato.votos
                lideres = [candidato]
            elif candidato.votos == maior_numero_de_votos and candidato.votos > 0:
                lideres.append(candidato)

        if maior_numero_de_votos == 0:
            linhas.append("Não houve votos válidos para prefeito.")
        elif len(lideres) > 1:
            linhas.append("Empate na primeira colocação: OCORRERÁ SEGUNDO TURNO.")
        else:
            linhas.append(f"Prefeito vencedor: {lideres[0].nome} ({lideres[0].sigla}).")

    def _mostrar_vereadores_eleitos(self, candidatos, linhas):
        # Remove da disputa os candidatos que não receberam votos.
        candidatos_com_votos = []
        for candidato in candidatos:
            if candidato.votos > 0:
                candidatos_com_votos.append(candidato)

        # Ordena do maior para o menor usando comparações simples.
        # A troca de posições deixa o funcionamento mais visível para iniciantes.
        for i in range(len(candidatos_com_votos)):
            for j in range(i + 1, len(candidatos_com_votos)):
                if candidatos_com_votos[j].votos > candidatos_com_votos[i].votos:
                    temporario = candidatos_com_votos[i]
                    candidatos_com_votos[i] = candidatos_com_votos[j]
                    candidatos_com_votos[j] = temporario
        linhas.append("Melhores colocados para vereador:")

        quantidade = min(3, len(candidatos_com_votos))
        for posicao in range(quantidade):
            candidato = candidatos_com_votos[posicao]
            linhas.append(
                f"{posicao + 1}º - {candidato.nome}: {candidato.votos} votos"
            )

        vagas_vazias = 3 - quantidade
        if vagas_vazias > 0:
            linhas.append(f"Vagas não preenchidas/desertas: {vagas_vazias}.")

