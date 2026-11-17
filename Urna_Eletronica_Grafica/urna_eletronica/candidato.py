"""Classe simples usada para representar cada candidato."""


class Candidato:
    def __init__(self, numero, nome, sigla, partido, cargo):
        # Guarda os dados que identificam o candidato.
        self.numero = numero
        self.nome = nome
        self.sigla = sigla
        self.partido = partido
        self.cargo = cargo
        # Todo candidato começa com zero votos.
        self.votos = 0

