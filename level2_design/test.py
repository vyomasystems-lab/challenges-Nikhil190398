import binarystring
from binarystring import BitArray
string = '0100000000000000111101010110011'
instr_value = BitArray(bin=string).int
print(instr_value)