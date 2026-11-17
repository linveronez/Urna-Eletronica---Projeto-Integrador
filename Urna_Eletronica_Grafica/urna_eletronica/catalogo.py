"""Cadastro inicial dos candidatos da simulação."""

from .candidato import Candidato


def criar_candidatos():
    # A lista tem os três candidatos a prefeito e os doze a vereador.
    candidatos = [
        Candidato("11", "Ana Silva", "PE", "Partido da Esperança", "prefeito"),
        Candidato("22", "Carlos Souza", "PP", "Partido do Progresso", "prefeito"),
        Candidato("33", "Mariana Costa", "PM", "Partido da Mudança", "prefeito"),
        Candidato("11111", "João Lima", "PE", "Partido da Esperança", "vereador"),
        Candidato("11222", "Beatriz Rocha", "PE", "Partido da Esperança", "vereador"),
        Candidato("11333", "Fernando Dias", "PE", "Partido da Esperança", "vereador"),
        Candidato("11444", "Renata Castro", "PE", "Partido da Esperança", "vereador"),
        Candidato("22111", "Maria Oliveira", "PP", "Partido do Progresso", "vereador"),
        Candidato("22222", "Lucas Martins", "PP", "Partido do Progresso", "vereador"),
        Candidato("22333", "Juliana Alves", "PP", "Partido do Progresso", "vereador"),
        Candidato("22444", "Roberto Mendes", "PP", "Partido do Progresso", "vereador"),
        Candidato("33111", "Camila Pereira", "PM", "Partido da Mudança", "vereador"),
        Candidato("33222", "Gabriel Santos", "PM", "Partido da Mudança", "vereador"),
        Candidato("33333", "Patricia Barbosa", "PM", "Partido da Mudança", "vereador"),
        Candidato("33444", "Ricardo Gomes", "PM", "Partido da Mudança", "vereador"),
    ]
    return candidatos

