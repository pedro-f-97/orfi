# Orfi

**Orfi** organiza ficheiros soltos por pastas categorizadas através da linha de comandos.

[![CI](https://github.com/pedro-f-97/orfi/actions/workflows/ci.yml/badge.svg)](https://github.com/pedro-f-97/orfi/actions/workflows/ci.yml)

## Funcionalidades

- Organização automática de ficheiros por extensão
- Pasta por defeito para ficheiros não reconhecidos
- Suporte para mover ou copiar ficheiros
- Reversão da organização
- Categorias de ficheiros configuráveis
- Configuração específica por utilizador
- Datação dos ficheiros com a data de criação
- Reversão da datação
- Registo de logs

## Instalação

Requer Python 3.11 ou superior.
Na pasta do projeto:

```bash
python -m pip install .
```

Depois da instalação, o programa pode ser executado através do comando:

```bash
orfi
```

## Opções

| Opção            | Descrição                          |
|------------------|-------------------------------------|
| `-a`, `--alvo`   | Permite definir a pasta alvo                 |
| `-c`, `--copiar` | Copia os ficheiros em vez de os mover |
| `-r`, `--reverter` | Reverte a organização              |
| `-d`, `--datar`  | Adiciona a data de criação ao nome dos ficheiros  |

## Utilização

Organizar a pasta atual:

```bash
orfi
```

Selecionar uma pasta específica:

```bash
orfi -a
```

Copiar os ficheiros em vez de os mover:

```bash
orfi -c
```

Reverter a organização por categorias:

```bash
orfi -r
```

Adicionar a data de criação ao nome dos ficheiros:

```bash
orfi -d
```

Por exemplo:

```text
relatorio.pdf → 260903_relatorio.pdf
```

Copiar e datar os ficheiros:

```bash
orfi -d -c
```

Reverter a datação:

```bash
orfi -d -r
```

Copiar os ficheiros enquanto reverte a datação:

```bash
orfi -d -r -c
```

As opções podem ser combinadas. Por exemplo, para selecionar uma pasta, copiar os ficheiros e datá-los:

```bash
orfi -a -c -d
```

## Configuração

As categorias e respetivas extensões são definidas através do ficheiro `config.toml`.

O Orfi inclui uma configuração standard que é copiada automaticamente para a localização de configuração do utilizador na primeira execução.

### Localização

No Windows:

```text
%APPDATA%\orfi\config.toml
```

No Linux:

```text
~/.config/orfi/config.toml
```

O ficheiro de configuração do utilizador não é substituído quando o Orfi é atualizado ou reinstalado.

### Logs

O Orfi regista as operações executadas num ficheiro `orfi.log`, localizado junto do ficheiro de configuração.

### Categorias

Cada categoria pode definir um conjunto de extensões:

```toml
[[categorias]]
nome = "Imagens"
extensoes = [".jpg", ".png", ".gif"]
```

Uma categoria pode ser definida como categoria por defeito:

```toml
[[categorias]]
nome = "Outros"
extensoes = []
defeito = true
```

Os ficheiros cuja extensão não corresponda a nenhuma categoria são encaminhados para a categoria por defeito.

A configuração permite criar, alterar ou remover categorias e extensões de acordo com as necessidades do utilizador.

## Testes

Os testes podem ser executados com:

```bash
pytest
```

O projeto utiliza `pytest` para testar as diferentes funcionalidades do Orfi.