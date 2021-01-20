from pwn import *
from hashlib import md5
from Crypto.Cipher import ARC4, AES
from Crypto.Util.number import bytes_to_long, long_to_bytes
from base64 import b64encode, b64decode
from string import printable
import time


def checksum_generator(message, xored_result):
    buffer = message + xored_result
    checksum = md5(buffer).digest()
    return checksum

def construct_message(plaintext):
    header = b'66119'
    payload = ARC4.new(xored_result).encrypt(plaintext)
    timestamp = int(time.time()).to_bytes(4, byteorder="little")
    len_padding = (len(header + timestamp + payload) + 16 + 4).to_bytes(4, byteorder='little')
    message = header + len_padding + timestamp + payload
    checksum = checksum_generator(message, xored_result)
    message += checksum
    return message

def message_parse(message):
    message = b64decode(message)
    message = message[27:] # "Receive from Device..."
    header = message[0:5] # 55511
    payload = message[13:-16] # actual data
    checksum = message[-16:]
    plain = ARC4.new(xored_result).decrypt(payload)
    return (header, plain, checksum)

def analyze_flag_len():
    p.sendline(construct_message(b""))
    base_flag_len = len(message_parse(p.recvline())[1]) # obtain the length of flag with padding
    p.recvline() # Please input your message
    for i in range(1, 16):
        payload = b"A" * i
        probe = construct_message(payload)
        p.sendline(probe)
        temp = message_parse(p.recvline())[1]
        probe_len = len(temp)
        print("[Sending] Adding", i, "bytes; Total Len is", probe_len)
        p.recvline() # Please input your message
        if probe_len > base_flag_len: # when the frontier dummy block is long enough to pop back the flag for just 1 byte
            # print(temp[-16:])
            # p.sendline(construct_message(16 * b'\x10'))
            # r = message_parse(p.recvline())[1]
            # print(r[:16])
            # p.recvline()
            return base_flag_len - i
    return base_flag_len



def analyze_flag(flag_len):
    

    controlled_block = b""
    known_flag = b""
    known_len = 1
    while known_len <= flag_len:
        for i in printable:
            controlled_block = i.encode() + known_flag[:15] # the pattern of our controlled block is fixed
            padding_len = AES.block_size - len(controlled_block)
            controlled_block += padding_len * long_to_bytes(padding_len) # target byte + known_flag + padding(optional)
            place_holder = (13 + known_len) * b'A' # dummy block for poping back the flag text
            temp = construct_message(controlled_block + place_holder)
            p.sendline(temp)
            plain = message_parse(p.recvline())[1]
            p.recvline() # Please input your message
            if plain[:16] in [plain[-16:], plain[-32:-16], plain[-48:-32]]: # the concernerd block is not always the last block
                known_flag = i.encode() + known_flag
                print("[*] Cracking", known_flag)
                known_len += 1
                break
    return known_flag


# begin cracking

p = remote("148.70.157.176", 55511)

R1 = "YmVfa2luZF9hbHdheXNfXw=="
R2 = "AzozDgAxDD4OMwMIJhA3Kg=="
xored_result = xor(b64decode(R1), b64decode(R2))
print("[*] RC4 key is", xored_result)

print("\n" + "*"*100)
print("\t\t\t\t\t\t\t\t Communication Begins \t\t\t\t\t\t\t\t")
print("*"*100+"\n")

print("[Server]",p.recvline())
p.sendline(R1)
print("[Sending]", R1)
print("[Server]",p.recvline())
p.sendline(R2)
print("[Sending]", R2)
print("[Server]", p.recvline())
print("[Server]", p.recvline())
print("[Server]", p.recvline())
print("[Server]", p.recvline())

m1 = construct_message(b64encode(b'Jujutsu Kaisen'))
p.sendline(m1)
print("[Sending]", m1)
print("[Server]", p.recvline())
r = p.recvline()
print("[Server]", r)
print("[*] Cracked flag1 is ", b64decode(r))
print("[Server]", p.recvline())
print("[Server]", message_parse(p.recvline())[1])
print("[Server]", p.recvline())

flag_len = analyze_flag_len()
print("[*] flag len is", flag_len)

# flag2 = analyze_flag(flag_len)
# print("[*] Cracked flag2 is ", flag2)

print("*"*100)
print("\t\t\t Communication Ends \t\t\t")
print("*"*100+"\n")



