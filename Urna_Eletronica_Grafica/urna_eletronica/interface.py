"""Janela principal da urna didática feita com Tkinter."""

import json
import os
import tkinter as tk
from tkinter import messagebox

from .apuracao import Apuracao
from .catalogo import criar_candidatos


class UrnaApp:
    def __init__(self, janela):
        # Prepara os dados e carrega uma sessão que já tenha sido salva.
        self.janela = janela
        self.janela.title("Urna Eletrônica Didática")
        self.janela.geometry("760x620")
        self.candidatos = criar_candidatos()
        self.apuracao = Apuracao(self.candidatos)
        pasta_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.arquivo_estado = os.path.join(pasta_projeto, "urna_estado.json")
        self.zeresima_feita = False
        self.votacao_ativa = False
        self.votacao_finalizada = False
        self.etapa = "vereador"
        self.erro_ao_carregar = False
        self.carregar_estado()
        self.montar_tela_inicial()
        if self.erro_ao_carregar:
            messagebox.showwarning(
                "Estado salvo inválido",
                "O arquivo salvo não pôde ser lido. A votação começou com contagens zeradas.",
            )

    def salvar_estado(self):
        # Salva os votos e a etapa atual para permitir continuar depois.
        estado = {
            "votos": {},
            "brancos": self.apuracao.brancos,
            "nulos": self.apuracao.nulos,
            "zeresima_feita": self.zeresima_feita,
            "votacao_ativa": self.votacao_ativa,
            "votacao_finalizada": self.votacao_finalizada,
            "etapa": self.etapa,
        }
        for candidato in self.candidatos:
            estado["votos"][candidato.numero] = candidato.votos
        try:
            with open(self.arquivo_estado, "w", encoding="utf-8") as arquivo:
                json.dump(estado, arquivo, ensure_ascii=False, indent=2)
        except OSError as erro:
            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar a votação: {erro}")

    def carregar_estado(self):
        # Na primeira execução ainda não existe arquivo, então tudo começa em zero.
        if not os.path.exists(self.arquivo_estado):
            return
        try:
            with open(self.arquivo_estado, "r", encoding="utf-8") as arquivo:
                estado = json.load(arquivo)
            votos_salvos = estado.get("votos", {})
            for candidato in self.candidatos:
                candidato.votos = votos_salvos.get(candidato.numero, 0)
            self.apuracao.brancos = estado.get("brancos", self.apuracao.brancos)
            self.apuracao.nulos = estado.get("nulos", self.apuracao.nulos)
            self.zeresima_feita = estado.get("zeresima_feita", False)
            self.votacao_ativa = estado.get("votacao_ativa", False)
            self.votacao_finalizada = estado.get("votacao_finalizada", False)
            self.etapa = estado.get("etapa", "vereador")
        except (OSError, ValueError, TypeError):
            self.erro_ao_carregar = True

    def limpar_tela(self):
        for item in self.janela.winfo_children():
            item.destroy()

    def montar_tela_inicial(self):
        self.limpar_tela()
        tk.Label(
            self.janela, text="Urna Eletrônica Didática",
            font=("Arial", 20, "bold"), pady=18,
        ).pack()
        tk.Label(
            self.janela, text="Simulação acadêmica - Projeto Integrador UNISA",
            font=("Arial", 11),
        ).pack(pady=4)
        tk.Button(
            self.janela, text="Zerésima", width=22, height=2,
            command=self.fazer_zeresima,
        ).pack(pady=8)

        if self.votacao_ativa:
            texto_botao = "Continuar Votação"
        else:
            texto_botao = "Iniciar Votação"
        estado_botao = "disabled" if self.votacao_finalizada else "normal"
        self.botao_iniciar = tk.Button(
            self.janela, text=texto_botao, width=22, height=2,
            state=estado_botao, command=self.iniciar_votacao,
        )
        self.botao_iniciar.pack(pady=8)

        tk.Label(self.janela, text="Relatório da sessão", font=("Arial", 12, "bold")).pack(pady=4)
        self.caixa_texto = tk.Text(self.janela, width=82, height=22, font=("Consolas", 10))
        self.caixa_texto.pack(padx=16, pady=8, fill="both", expand=True)
        if self.zeresima_feita:
            texto = self.apuracao.criar_zeresima()
        elif self.votacao_finalizada:
            texto = self.apuracao.criar_totalizacao()
        elif self.votacao_ativa:
            texto = f"Sessão salva. Próxima etapa: {self.etapa}. Clique em Continuar Votação."
        else:
            texto = "Pronto para votar. A Zerésima é opcional e pode ser usada para limpar a sessão."
        self.mostrar_texto(texto)

    def mostrar_texto(self, texto):
        self.caixa_texto.configure(state="normal")
        self.caixa_texto.delete("1.0", "end")
        self.caixa_texto.insert("1.0", texto)
        self.caixa_texto.configure(state="disabled")

    def tem_votos(self):
        # Confere votos de candidatos, brancos e nulos antes de apagar a sessão.
        for candidato in self.candidatos:
            if candidato.votos > 0:
                return True
        for cargo in ["prefeito", "vereador"]:
            if self.apuracao.brancos[cargo] > 0 or self.apuracao.nulos[cargo] > 0:
                return True
        return False

    def fazer_zeresima(self):
        # A Zerésima é opcional; ao escolhê-la, ela reinicia a votação salva.
        if self.tem_votos() and not messagebox.askyesno(
            "Confirmar", "A Zerésima apagará os votos salvos. Deseja continuar?"
        ):
            return
        self.apuracao.zerar_votos()
        self.zeresima_feita = True
        self.votacao_ativa = False
        self.votacao_finalizada = False
        self.etapa = "vereador"
        self.salvar_estado()
        self.montar_tela_inicial()

    def iniciar_votacao(self):
        # Uma eleição encerrada exige Zerésima; uma sessão ativa pode ser retomada.
        if self.votacao_finalizada:
            messagebox.showwarning("Votação encerrada", "Faça a Zerésima para iniciar outra sessão.")
            return
        self.votacao_ativa = True
        self.salvar_estado()
        if self.etapa == "finalizar":
            self.perguntar_se_continua()
        else:
            self.mostrar_tela_de_voto()

    def mostrar_tela_de_voto(self):
        self.limpar_tela()
        cargo = self.etapa
        quantidade_digitos = 5 if cargo == "vereador" else 2
        tk.Label(
            self.janela, text=f"Votação para {cargo.capitalize()}",
            font=("Arial", 20, "bold"), pady=14,
        ).pack()
        tk.Label(
            self.janela,
            text=f"Digite {quantidade_digitos} dígitos ou escolha voto em branco.",
            font=("Arial", 11),
        ).pack(pady=5)

        linha = tk.Frame(self.janela)
        linha.pack(pady=10)
        self.entrada_numero = tk.Entry(linha, font=("Arial", 20), width=10, justify="center")
        self.entrada_numero.grid(row=0, column=0, padx=5)
        tk.Button(
            linha, text="Consultar número", command=self.consultar_numero_atual,
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            self.janela, text="Votar em branco", command=self.preparar_voto_branco_atual,
        ).pack(pady=8)

        self.mensagem = tk.Label(
            self.janela, text="", font=("Arial", 13), wraplength=680, pady=14,
        )
        self.mensagem.pack()
        self.botoes_confirmacao = tk.Frame(self.janela)
        self.botoes_confirmacao.pack(pady=8)

        tk.Label(self.janela, text="Candidatos cadastrados", font=("Arial", 11, "bold")).pack(pady=8)
        for candidato in self.candidatos:
            if candidato.cargo == cargo:
                tk.Label(
                    self.janela,
                    text=f"{candidato.numero} - {candidato.nome} ({candidato.sigla})",
                    font=("Arial", 10),
                ).pack()

    def consultar_numero_atual(self):
        # O cargo atual é salvo em self.etapa.
        self.consultar_numero(self.etapa)

    def preparar_voto_branco_atual(self):
        self.preparar_voto_branco(self.etapa)

    def consultar_numero(self, cargo):
        numero = self.entrada_numero.get().strip()
        escolhido = None
        for candidato in self.candidatos:
            if candidato.numero == numero and candidato.cargo == cargo:
                escolhido = candidato
        if escolhido:
            texto = f"Candidato: {escolhido.nome}\nPartido: {escolhido.sigla} - {escolhido.partido}"
            self.preparar_confirmacao(cargo, "candidato", escolhido, texto)
        else:
            texto = "Número não encontrado. O voto será computado como NULO."
            self.preparar_confirmacao(cargo, "nulo", None, texto)

    def preparar_voto_branco(self, cargo):
        self.preparar_confirmacao(cargo, "branco", None, "A escolha será registrada como voto em BRANCO.")

    def preparar_confirmacao(self, cargo, tipo, candidato, texto):
        # A escolha só fica na memória temporária até ser confirmada.
        self.voto_pendente = {"cargo": cargo, "tipo": tipo, "candidato": candidato}
        self.mensagem.configure(text=texto)
        for botao in self.botoes_confirmacao.winfo_children():
            botao.destroy()
        tk.Label(self.botoes_confirmacao, text="Confirma a escolha?").pack(side="left", padx=5)
        tk.Button(
            self.botoes_confirmacao, text="CONFIRMAR (S)", command=self.confirmar_voto,
        ).pack(side="left", padx=5)
        tk.Button(
            self.botoes_confirmacao, text="CORRIGIR (N)", command=self.cancelar_voto,
        ).pack(side="left", padx=5)

    def cancelar_voto(self):
        self.voto_pendente = None
        self.entrada_numero.delete(0, "end")
        self.mensagem.configure(text="Escolha cancelada. Digite novamente ou escolha branco.")
        for botao in self.botoes_confirmacao.winfo_children():
            botao.destroy()

    def confirmar_voto(self):
        # Registra o voto e salva imediatamente para evitar perda ao fechar.
        voto = self.voto_pendente
        self.apuracao.registrar_voto(voto["cargo"], voto["tipo"], voto["candidato"])
        self.voto_pendente = None
        if self.etapa == "vereador":
            self.etapa = "prefeito"
            self.salvar_estado()
            messagebox.showinfo("Voto confirmado", "Agora será registrado o voto para Prefeito.")
            self.mostrar_tela_de_voto()
        else:
            self.etapa = "finalizar"
            self.salvar_estado()
            self.perguntar_se_continua()

    def perguntar_se_continua(self):
        # Salva a etapa antes de exibir a pergunta, para retomá-la se fechar.
        continuar = messagebox.askyesno(
            "Finalizar a votação ou continuar",
            "Finalizar a votação ou continuar?\n\n"
            "Sim: continuar com o próximo eleitor.\n"
            "Não: finalizar e mostrar a totalização.",
        )
        if continuar:
            self.etapa = "vereador"
            self.salvar_estado()
            self.mostrar_tela_de_voto()
        else:
            self.votacao_ativa = False
            self.votacao_finalizada = True
            self.salvar_estado()
            self.mostrar_resultado()

    def mostrar_resultado(self):
        self.limpar_tela()
        tk.Label(self.janela, text="Resultado da apuração", font=("Arial", 20, "bold"), pady=16).pack()
        caixa = tk.Text(self.janela, width=82, height=28, font=("Consolas", 10))
        caixa.pack(padx=16, pady=8, fill="both", expand=True)
        caixa.insert("1.0", self.apuracao.criar_totalizacao())
        caixa.configure(state="disabled")
        tk.Button(
            self.janela, text="Voltar ao menu inicial", command=self.montar_tela_inicial,
        ).pack(pady=8)


def executar():
    janela = tk.Tk()
    UrnaApp(janela)
    janela.mainloop()

