import random
from gmpy2 import invert


def gcd(a, b):
    '''
    Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
    '''
    while b != 0:
        a, b = b, a % b
    return a


def modinv(a, m):

    return int(invert(a, m))

    # g, x, y = egcd(a, m)
    # if g != 1:
    #     raise Exception('modular inverse does not exist')
    # else:
    #     return x % m


def rabinMiller(num):
    '''
    Tests to see if a number is prime.
    Returns True or False
    '''

    if num % 2 == 0:
        return False

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(5):  # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)

        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def generate_keypair():

    # Size of N must be size(P) + size(Q) + 1

    upper_bound = 2**31 - 1  # upper bound for an int_32 holdint 32 bits
    lower_bound = 2**30 - 1  # lower bound for an int_32 holding 31 bits

    # Generate Prime Values for p and q
    while(True):
        p = random.randint(lower_bound, upper_bound)

        if rabinMiller(p):
            break

    while(True):
        q = random.randint(lower_bound, upper_bound)

        if rabinMiller(q) and q != p:
            break

    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = modinv(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character
    # using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    (e, n), (d, n) = generate_keypair()
    print("e:", e)
    print("d:", d)
    print("n:", n)

    # print("RSA Encrypter/ Decrypter")
    # print("Generating your public/private keypairs now . . .")
    # public, private = generate_keypair()
    # print("Your public key is " + str(public) + " and your private key is "
    #       + str(private))
    # message = input("Enter a message to encrypt with your private key: ")
    # encrypted_msg = encrypt(private, message)
    # print("Your encrypted message is: ")
    # print(''.join(map(lambda x: str(x), encrypted_msg)))
    # print("Decrypting message with public key " + public + " . . .")
    # print("Your message is:")
    # print(decrypt(public, encrypted_msg))
