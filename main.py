import sys
from pathlib import Path

import configs
import ficheiros
import pastas

while True:
    pasta = Path(input("Definir pasta para organizar: "))
    if pasta.is_dir():
        break
    print("Pasta inválida.")

categorias = configs.iniciarCategorias()

pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pasta), categorias)

if pastasParaCriar == set():
    print("Nada para fazer.")
    sys.exit()

confirmacao = input(f"Criar as pastas {pastasParaCriar}? (s/n): ")
if confirmacao.lower() == "s":
    pastas.criaPastas(pasta, pastasParaCriar, categorias)
else:
    print("Operação Cancelada")
    sys.exit()

ficheirosLista = ficheiros.devolveFicheiros(pasta)

total = 0
for ficheiro in ficheirosLista:
    destino = ficheiros.defineDestino(ficheiro, categorias)
    if destino is not None:
        total += ficheiros.copiaFicheiro(ficheiro, destino)
    else:
        print(f"Categoria ou caminho não encontrados para {ficheiro.name}")

print(f"Feito, {total} ficheiros copiados.")