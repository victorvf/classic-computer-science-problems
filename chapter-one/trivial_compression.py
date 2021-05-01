class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1

        for nucleotide in gene.upper():
            self.bit_string <<= 2  # desloca dois bits para a esquerda

            if nucleotide == "A":  # muda os dois últimos bits para 00
                self.bit_string |= 0b00
            elif nucleotide == "C":  # muda os dois últimos bits para 01
                self.bit_string |= 0b01
            elif nucleotide == "G":  # muda os dois últimos bits para 10
                self.bit_string |= 0b10
            elif nucleotide == "T":  # muda os dois últimos bits para 11
                self.bit_string |= 0b11
            else:
                raise ValueError(f"Invalid Nucleotide: {nucleotide}")

    def decompress(self) -> str:
        gene: str = ""

        for i in range(0, self.bit_string.bit_length() - 1, 2):  # - 1 para excluir a sentinela
            bits: int = self.bit_string >> i & 0b11  # obtém apenas 2 bits relevantes

            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else:
                raise ValueError("Invalid bits: {bits}")
        
        return gene[::-1]
    
    def __str__(self) -> str:
        return self.decompress()


if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print(f"Original is {getsizeof(original)} bytes")
    compressed: CompressedGene = CompressedGene(original)
    print(f"Compressed is {getsizeof(compressed.bit_string)} bytes")
    print(compressed)
    print(f"Original and Decompressed are the same: {original == compressed.decompress()}")
