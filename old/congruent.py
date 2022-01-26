import gmpy2

class LCG:

    def __init__(self, seed) -> None:
        self.seed = gmpy2.mpz(self._bytes_to_int(seed))
    def reseed(self,seed):
        self.seed = gmpy2.mpz(self._bytes_to_int(seed))

    def next_32_bit(self):
        self.seed = (self.seed * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFF # 32 bits -> 4 byte
        return self.seed

    def next_16_bit(self):
        self.seed = (self.seed * 6364136223846793005 + 1442695040888963407) & 0xFFFF # 16 bits -> 2 byte
        return self.seed

    def next_byte(self):
        self.seed = (self.seed * 6364136223846793005 + 1442695040888963407) & 0xFF # 8 bits -> 1 byte
        return self.seed

    def _bytes_to_int(self,bytes):
        result = 0
        for b in bytes:
            result = result * 256 + int(b)
        return result