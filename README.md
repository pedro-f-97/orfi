# Orfi

**Orfi** é uma ferramenta de linha de comandos que organiza ficheiros soltos em pastas categorizadas automaticamente.

## Funcionalidades

- Organização automática por extensão
- Pasta por defeito para ficheiros não reconhecidos
- Suporte para mover ou copiar ficheiros
- Reversão da organização

## Instalação

```bash
python -m pip install .
```

## Opções

| Opção            | Descrição                          |
|------------------|-------------------------------------|
| `-a`, `--alvo`   | Permite definir a pasta alvo                 |
| `-c`, `--copiar` | Copia os ficheiros em vez de os mover |
| `-r`, `--reverter` | Reverte a organização              |

## Utilização

```bash
orfi            # organiza a pasta atual
orfi -a         # permite definir a pasta alvo
orfi -a  -c     # copia os ficheiros para a pasta alvo
orfi -a  -r     # reverte a organização
```

## Testes

```bash
pytest
```
