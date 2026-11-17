# Urna Eletrônica Gráfica

## Sobre

Protótipo acadêmico de votação com janela gráfica, feito em Python e Tkinter. Serve para demonstrar o fluxo de votação e apuração; não é um sistema eleitoral oficial.

## Requisitos

- Python 3 instalado.
- Tkinter, normalmente incluído na instalação do Python.
- Não são necessárias bibliotecas externas.

## Como iniciar

Abra um terminal nesta pasta e execute:

```text
python main.py
```

No Windows, também pode funcionar com:

```text
py main.py
```

## Como usar

1. Use **Iniciar Votação** para começar ou retomar uma sessão.
2. Se necessário, use **Zerésima** para reiniciar as contagens.
3. Vote primeiro para vereador, com cinco dígitos, e depois para prefeito, com dois dígitos. Em cada cargo, também é possível votar em branco.
4. Confira o candidato ou o tipo de voto e escolha confirmar ou corrigir.
5. Depois do voto para prefeito, escolha continuar com outro eleitor ou finalizar e ver a apuração.

O programa cria `urna_estado.json` nesta pasta para salvar as contagens e permitir retomar uma sessão. A Zerésima apaga os totais salvos e começa uma nova contagem.

## Arquivos principais

- `main.py`: inicia a janela.
- `urna_eletronica/`: contém os módulos da interface, candidatos e apuração.

Esta aplicação é uma simulação didática e não tem validade eleitoral.
