import pyvisa

rm = pyvisa.ResourceManager()

instr = rm.open_resource("TCPIP::192.168.2.115::hislip0")

print(instr.query("*IDN?"))

instr.close()