from hashlib import pbkdf2_hmac, sha256
import numpy as np


class PRBG:
    '''
    Pseudo-random Byte Generator (PRGB) that uses PBKDF2 and XorShift implementations
    to produce pseudo-random bytes from a given password, confusion string and iteration
    counter.
    '''

    def __init__(self, password, confusion_string, iteration_count) -> None:
        '''
        Initializes a PRBG object with a seed, which is generated using the PBKDF2 method with the
        password, the confusion string, and the iteration counter. The confusion pattern attribute is
        also generated.
        '''
        bytes_seed = self._compute_seed(password, confusion_string, iteration_count)
        self.seed = self._bytes_to_int(bytes_seed)
        self.seed = np.int64(self._bytes_to_int(bytes_seed) & 0xFFFFFFFF)
        self.iteration_count = int(iteration_count)
        self.consufion_pattern = self._get_confusion_pattern(confusion_string)
        self.buffer = Buffer(len(self.consufion_pattern))
        self.setted_up = False


    def _reseed(self, seed):
        '''
        Used to reseed the PRBG with a set of bytes.
        '''
        self.seed = np.int64(self._bytes_to_int(seed) & 0xFFFFFFFF)


    def setup(self):
        '''
        Sets up the generator to a state that can take an arbitrarily high computation time to reach.
        The current state is changed by generating the next byte until the confusion pattern is found
        amongst the last N bytes generated, for the given number of iterations. In the end of each iteration,
        the generator is reseeded.
        '''
        counter = 0
        for _ in range(self.iteration_count):
            while True:
                self.buffer.add(self.next_byte())
                counter += 1
                if self.consufion_pattern == self.buffer.buffer:
                    new_seed = []
                    for _ in range(64):
                        new_seed.append(self.next_byte())
                    new_seed = bytes(new_seed)
                    self._reseed(new_seed)
                    self.setted_up = True
                    break
            counter = 0

    def next_byte(self):
        '''
        Generates the next byte of the generator, according to the current seed, using
        a XorShift approach.
        '''
        s = self.seed
        s ^= s << np.int64(13)
        s ^= s >> np.int64(17)
        s ^= s << np.int64(5)
        self.seed = s
        return np.int64(s & np.int64(0xFF))


    def _compute_seed(self, password, confusion_string, iteration_count):
        '''
        Computes the PRBG seed with the PBKDF2 method, given a textual password and confusion
        string, and an integer as the iteration counter.
        '''
        key = pbkdf2_hmac(
            hash_name = 'sha1', 
            password = bytes(password, encoding='utf-8'), 
            salt =  bytes(confusion_string, encoding='utf-8'), 
            iterations = int(iteration_count), 
            dklen = 64
        )
        return key


    def _get_confusion_pattern(self, confusion_string):
        '''
        Generates the confusion pattern based on the given confusion string and it's SHA256 digest.
        '''
        hashvalue = sha256(confusion_string.encode()).digest()
        index = sum(hashvalue) % (len(hashvalue) - len(confusion_string))
        cp = hashvalue[index:index+len(confusion_string)]
        return [np.int64(c) for c in cp]

    def _bytes_to_int(self,bytes):
        '''
        Generates the confusion pattern, from the given confusion string.
        The confusion pattern is the result of a slice of the SHA-256 digest of the
        confusion string.
        '''
        result = 0
        for b in bytes:
            result = result * 256 + int(b)
        return result

    def __str__(self) -> str:
        return f"  PRGB geneartor:\n    current state: {self.seed}\n    cp: {self.consufion_pattern} (len={len(self.consufion_pattern)})\n    ic: {self.iteration_count}\n    setted up: {'yes' if self.setted_up else 'no'}"



class Buffer:
    '''
    Buffer structure that holds the rotating set of last bytes produced by the generator, and
    also the confusion pattern. It is essentially a list with a fixed size and rotating
    elements.
    '''

    def __init__(self, size) -> None:
        self.buffer = []
        self.size = size

    def add(self, byte):
        '''
        Adds the given byte representation to the end of the list,
        and removes the first element if the buffer is full.
        '''
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)
        self.buffer.append(byte)

    def clear(self):
        self.buffer = []

    def __str__(self) -> str:
        return str(self.buffer)