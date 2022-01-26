import gmpy2
from gmpy2 import mpz

'''
List of fixed prime numbers < 1000, in order to check that p and q will not be coprimes
with small primes.
'''
small_primes = [
    mpz(2), mpz(3), mpz(5), mpz(7), mpz(11), mpz(13), mpz(17), mpz(19), mpz(23), mpz(29), 
    mpz(31), mpz(37), mpz(41), mpz(43), mpz(47), mpz(53), mpz(59), mpz(61), mpz(67), mpz(71), 
    mpz(73), mpz(79), mpz(83), mpz(89), mpz(97), mpz(101), mpz(103), mpz(107), mpz(109), mpz(113), 
    mpz(127), mpz(131), mpz(137), mpz(139), mpz(149), mpz(151), mpz(157), mpz(163), mpz(167), mpz(173), 
    mpz(179), mpz(181), mpz(191), mpz(193), mpz(197), mpz(199), mpz(211), mpz(223), mpz(227), mpz(229), 
    mpz(233), mpz(239), mpz(241), mpz(251), mpz(257), mpz(263), mpz(269), mpz(271), mpz(277), mpz(281), 
    mpz(283), mpz(293), mpz(307), mpz(311), mpz(313), mpz(317), mpz(331), mpz(337), mpz(347), mpz(349), 
    mpz(353), mpz(359), mpz(367), mpz(373), mpz(379), mpz(383), mpz(389), mpz(397), mpz(401), mpz(409), 
    mpz(419), mpz(421), mpz(431), mpz(433), mpz(439), mpz(443), mpz(449), mpz(457), mpz(461), mpz(463), 
    mpz(467), mpz(479), mpz(487), mpz(491), mpz(499), mpz(503), mpz(509), mpz(521), mpz(523), mpz(541), 
    mpz(547), mpz(557), mpz(563), mpz(569), mpz(571), mpz(577), mpz(587), mpz(593), mpz(599), mpz(601), 
    mpz(607), mpz(613), mpz(617), mpz(619), mpz(631), mpz(641), mpz(643), mpz(647), mpz(653), mpz(659), 
    mpz(661), mpz(673), mpz(677), mpz(683), mpz(691), mpz(701), mpz(709), mpz(719), mpz(727), mpz(733), 
    mpz(739), mpz(743), mpz(751), mpz(757), mpz(761), mpz(769), mpz(773), mpz(787), mpz(797), mpz(809), 
    mpz(811), mpz(821), mpz(823), mpz(827), mpz(829), mpz(839), mpz(853), mpz(857), mpz(859), mpz(863), 
    mpz(877), mpz(881), mpz(883), mpz(887), mpz(907), mpz(911), mpz(919), mpz(929), mpz(937), mpz(941), 
    mpz(947), mpz(953), mpz(967), mpz(971), mpz(977), mpz(983), mpz(991), mpz(997)
]


class DRSA:
    '''
    Deterministic RSA module that produces the parameters of a RSA key
    pair from a N bytes pseudo-random seed.
    '''
    
    def __init__(self, seed) -> None:
        '''
        Generates the p and q primes from the given seed, which is cut in half and converted to two
        gmpy.mpz instances (similar to int/long type but significanly faster for large values). From these
        instances, the next prime is calculated and attributed to p qnd q after the small prime division
        verification. From p, q and the fixed public exponent e (2^16+1), all the other parameters are generated.
        '''

        # Generate primes p and q from the given seed
        seed1 = seed[:len(seed) // 2]
        seed2 = seed[len(seed) // 2:]

        big_number1 = gmpy2.mpz(int.from_bytes(seed1, byteorder='big'))
        big_number2 = gmpy2.mpz(int.from_bytes(seed2, byteorder='big'))

        p = gmpy2.next_prime(big_number1)
        q = gmpy2.next_prime(big_number2)

        for small_prime in small_primes:
            if gmpy2.t_mod(p, small_prime) == 0:
                p = gmpy2.next_prime(p)
            if gmpy2.t_mod(q, small_prime) == 0:
                q = gmpy2.next_prime(q)

        self.p = p
        self.q = q

        # p and q must be different
        assert(self.p != self.q)

        # n and phi calculation
        self.n = gmpy2.mul(self.p, self.q)
        self.phi = gmpy2.mul(self.p-1, self.q-1)

        # Fixed value of e -> (2^16)+1
        self.e = pow(mpz(2), 16) + 1

        # d calculation and assert
        self.d = gmpy2.invert(self.e, self.phi)
        assert(self.d != 1)
        assert(gmpy2.t_mod(self.e*self.d, self.phi) == 1)



    def get_private_params(self):
        '''
        Retrieves the private parameters from the given DRSA instance (n, e, d, p, q).
        '''
        return self.n, self.e, self.d, self.p, self.q

    
    def get_public_params(self):
        '''
        Retrieves the public parameters from the given DRSA instance (n, e).
        '''
        return self.n, self.e