__author__ = 'Timothy'
import ctypes

class GbRegisterFields(ctypes.Structure):
    _fields_ = [("lo",ctypes.c_ubyte),("hi",ctypes.c_ubyte)]
class GbRegister(ctypes.Union):
    _fields_ = [("full",ctypes.c_ushort),("fields",GbRegisterFields)]

class GbRegisterSet:
    def __init__(self):
        self.AF = GbRegister()
        self.BC = GbRegister()
        self.DE = GbRegister()
        self.HL = GbRegister()
        self.PC = GbRegister()
        self.SP = GbRegister()
        self.reset()

    def reset(self):
        self.AF.full = 0
        self.BC.full = 0
        self.DE.full = 0
        self.HL.full = 0
        self.PC.full = 0
        self.SP.full = 0

    def __setitem__(self, key, value):
        if key == "AF":
            self.AF.full = value
        if key == "BC":
            self.BC.full = value
        if key == "DE":
            self.DE.full = value
        if key == "HL":
            self.HL.full = value
        if key == "PC":
            self.PC.full = value
        if key == "SP":
            self.SP.full = value
        if key == "A":
            self.AF.fields.hi = value
        if key == "F":
            self.AF.fields.lo = value
        if key == "B":
            self.BC.fields.hi = value
        if key == "C":
            self.BC.fields.lo = value
        if key == "D":
            self.DE.fields.hi = value
        if key == "E":
            self.DE.fields.lo = value
        if key == "H":
            self.HL.fields.hi = value
        if key == "L":
            self.HL.fields.lo = value
        if key == "Zf":
            self._setFlagBit(7,value)
        if key == "Nf":
            self._setFlagBit(6,value)
        if key == "Hf":
            self._setFlagBit(5,value)
        if key == "Cf":
            self._setFlagBit(4,value)

    def __getitem__(self, item):
        if item == "AF":
            return self.AF.full
        if item == "BC":
            return self.BC.full
        if item == "DE":
            return self.DE.full
        if item == "HL":
            return self.HL.full
        if item == "PC":
            return self.PC.full
        if item == "SP":
            return self.SP.full
        if item == "A":
            return self.AF.fields.hi
        if item == "F":
            return self.AF.fields.lo
        if item == "B":
            return self.BC.fields.hi
        if item == "C":
            return self.BC.fields.lo
        if item == "D":
            return self.DE.fields.hi
        if item == "E":
            return self.DE.fields.lo
        if item == "H":
            return self.HL.fields.hi
        if item == "L":
            return self.HL.fields.lo
        if item == "Zf":
            return self._readFlagBit(7)
        if item == "Nf":
            return self._readFlagBit(6)
        if item == "Hf":
            return self._readFlagBit(5)
        if item == "Cf":
            return self._readFlagBit(4)

    def _setFlagBit(self,index,value):
        if value == True:
            self.AF.fields.lo |= 1 << index
        else:
            self.AF.fields.lo &= ~(1 << index)

    def _readFlagBit(self,index):
        bit = self.AF.fields.lo & (1 << index)
        if bit == 0x0:
            return False
        else:
            return True

def testRegisters(rs):
    #make sure reset works
    rs['AF'] = 10
    if rs['AF'] != 10:
        print "AF assignment fail"
    rs.reset()
    if rs['AF'] != 0:
        print "Register Set Reset Fail"
    #test field assignment
    rs['C'] = 0xFF
    if rs['C'] != 0xFF:
        print "Register Field Assignment Fail"
    if rs['BC'] != 0xFF:
        print "Register/Field Mismatch"
    rs['B'] = 0xAF
    if rs['B'] != 0xAF:
        print "Register Field Assignment Fail"
    if rs['BC'] != 0xAFFF:
        print "Fields don't match full value"
    rs.reset()
    #test flag
    rs['Zf'] = True
    if rs['Zf'] != True:
        print "Z Flag failure"

    rs['Nf'] = True
    if rs['Nf'] != True:
        print "N Flag failure"

if __name__ == "__main__":
    rs = GbRegisterSet()
    testRegisters(rs)