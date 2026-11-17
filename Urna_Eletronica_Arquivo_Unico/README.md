# Urna Eletrônica em Arquivo Único

## Sobre

Simulação acadêmica de votação em Python, executada no terminal e reunida em um único arquivo. Não é um sistema eleitoral oficial.

## Requisitos

- Python 3 instalado.
- Não são necessárias bibliotecas externas.

## Como iniciar

Abra um terminal nesta pasta e execute:

```text
python Urna_PagUnica.py
```

No Windows, também pode funcionar com:

```text
py Urna_PagUnica.py
```

## Como usar

- No menu, digite `1` para Zerésima, `2` para iniciar a votação ou `3` para sair.
- Digite o número do candidato ou `B` para voto em branco. Número não cadastrado para o cargo é tratado como voto nulo.
- Digite `S` para confirmar a escolha ou `N` para corrigir.
- Após votar para vereador e prefeito, digite `C` para continuar com outro eleitor ou `F` para finalizar e ver a totalização.

Os votos ficam somente na memória enquanto o programa está aberto. Ao fechar o programa, a contagem é perdida. A Zerésima também reinicia as contagens.

## Arquivo principal

- `Urna_PagUnica.py`: cadastro dos candidatos, votação, contagem e apresentação dos resultados.

Esta aplicação é uma simulação didática e não tem validade eleitoral.
