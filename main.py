import sys
from pathlib import Path

import configs
import ficheiros
import pastas

while True:
    pasta = Path(input(f"{configs.CoresTexto.AZUL}Definir pasta para organizar: {configs.CoresTexto.RESET}"))
    if pasta.is_dir():
        break
    print(f"{configs.CoresTexto.AMARELO}Pasta inválida.{configs.CoresTexto.RESET}")

categorias = configs.iniciarCategorias()

pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pasta), categorias)

if pastasParaCriar == set():
    print(f"{configs.CoresTexto.AMARELO}Nada para fazer.{configs.CoresTexto.RESET}")
    sys.exit()

confirmacao = input(f"{configs.CoresTexto.AZUL}Criar as pastas {pastasParaCriar}? (s/n): {configs.CoresTexto.RESET}")
if confirmacao.lower() == "s":
    pastas.criaPastas(pasta, pastasParaCriar, categorias)
else:
    print(f"{configs.CoresTexto.AMARELO}Operação Cancelada{configs.CoresTexto.RESET}")
    sys.exit()

ficheirosLista = ficheiros.devolveFicheiros(pasta)

total = 0
for ficheiro in ficheirosLista:
    destino = ficheiros.defineDestino(ficheiro, categorias)
    if destino is not None:
        total += ficheiros.copiaFicheiro(ficheiro, destino)
    else:
        print(f"{configs.CoresTexto.AMARELO}Categoria ou caminho não encontrados para {ficheiro.name}{configs.CoresTexto.RESET}")

print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros copiados.{configs.CoresTexto.RESET}")