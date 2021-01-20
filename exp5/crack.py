from Crypto.Cipher import AES
from Crypto.Hash import MD5
from hashlib import md5
from itertools import product

KnownBytes = b"flag"
CipherText = bytes.fromhex("7c57216bbf519627ae0288f29f36ad50e68a3e4ff0d55bce9c8e09104980c943a576f9aa6156cb5ad9495c2d9a436766")
KeyLen = 2

def KeyPoolGen(KeyLen):
    KeyPool = []
    for i in range(KeyLen):
        KeyPool.append([j for j in range(256)])
    return KeyPool

def MD5PoolGen(candidateKey):
    HashPool = []
    key = bytes.fromhex(candidateKey)
    for i in range(5):
        key = md5(key).digest()
        HashPool.append(key)
    HashPool.reverse()
    return HashPool

def decrypt(plain, key):
    return AES.new(key, AES.MODE_ECB).decrypt(plain)

def crack():
    KeyPool = KeyPoolGen(KeyLen)
    for candidate in product(*KeyPool):
        Plain = CipherText
        key = ''.join(list(map(lambda x: hex(x)[2:].zfill(2), candidate)))
        hashes = MD5PoolGen(key)
        for i in range(5):
            Plain = decrypt(Plain, hashes[i])
        if KnownBytes in Plain:
            print(candidate, Plain)
            break

crack()

