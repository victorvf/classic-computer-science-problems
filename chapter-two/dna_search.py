from enum import IntEnum
from typing import Tuple, List

Nucleotide: IntEnum = IntEnum("Nucleotide", ("A", "C", "G", "T"))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = List[Codon]

gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCC"


def string_to_gene(s: str) -> Gene:
    gene: Gene = []

    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene  # Não avança para além do final!
        # Inicializa codon a partir de três nucleotídeos
        codon: Codon = (
            Nucleotide[s[i]],
            Nucleotide[s[i + 1]],
            Nucleotide[s[i + 2]],
        )
        gene.append(codon)  # Adiciona codon em gene

    return gene


my_gene: Gene = string_to_gene(gene_str)

# flake8: noqa
# Representação mais simples: print(acg in my_gene)
def linear_contains(gene: Gene, key_codon: Codon) -> bool:
    # Pior dos casos O(n)
    for codon in gene:
        if codon == key_codon:
            return True
    return False


acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)
print(linear_contains(my_gene, acg))
print(linear_contains(my_gene, gat))


def binary_contains(gene: Gene, key_codon: Codon) -> bool:
    # Pior dos casos O(lg n), porém exige ordenação e o melhor algoritmo de
    # ordenação pode levar O(n lg n).
    low: int = 0
    high: int = len(gene) - 1
    while low <= high:  # Enquanto ainda houver um espaço para pesquisa
        mid: int = (low + high) // 2
        # Ele verifica se cada enum de gene[mid] é menor do que o enum da
        # key_codon
        if gene[mid] < key_codon:
            low = mid + 1
        # Ele verifica se cada enum de gene[mid] é maior do que o enum da
        # key_codon
        elif gene[mid] > key_codon:
            high = mid - 1
        # Ele adimite que todos são iguais
        else:
            return True
    return False


my_sorted_gene: Gene = sorted(my_gene)
print(binary_contains(my_sorted_gene, acg))
print(binary_contains(my_sorted_gene, gat))
