from Crypto.Util.number import long_to_bytes
seed_bytes = b""

def rand():
	global seed_bytes
	a4 = seed_bytes
	a4 = a4 * 0x41C64E6D + 0x3039
	seed_bytes = a4
	a5 = seed_bytes
	a5 = a5 >> 0x10
	seed_bytes = seed_bytes & ((1 << 65) - 1)
	return long_to_bytes(a5)[-1]

def file_decrypt():
	global seed_bytes
	filename = "pdf.encrypted"
	seed_bytes = int.from_bytes(b"%PDF-1.1", "little")
	cipher_text = open(filename, "rb").read()
	fn = open("decrypted.pdf", "wb")
	for i in range(len(cipher_text)):
		fn.write(bytes([cipher_text[i] ^ rand()]))
	fn.close()

file_decrypt()
