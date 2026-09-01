# Orfi

**Orfi** organiza ficheiros soltos por pastas categorizadas através da linha de comandos.

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
orfi            
orfi -a         
...   
```

## Testes

```bash
pytest
```
