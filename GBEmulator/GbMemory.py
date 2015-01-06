__author__ = 'Timothy'

class GbMemory:
    _mBios = [0x31, 0xFE, 0xFF, 0xAF, 0x21, 0xFF, 0x9F, 0x32, 0xCB, 0x7C, 0x20, 0xFB, 0x21, 0x26, 0xFF, 0x0E,
              0x11, 0x3E, 0x80, 0x32, 0xE2, 0x0C, 0x3E, 0xF3, 0xE2, 0x32, 0x3E, 0x77, 0x77, 0x3E, 0xFC, 0xE0,
              0x47, 0x11, 0x04, 0x01, 0x21, 0x10, 0x80, 0x1A, 0xCD, 0x95, 0x00, 0xCD, 0x96, 0x00, 0x13, 0x7B,
              0xFE, 0x34, 0x20, 0xF3, 0x11, 0xD8, 0x00, 0x06, 0x08, 0x1A, 0x13, 0x22, 0x23, 0x05, 0x20, 0xF9,
              0x3E, 0x19, 0xEA, 0x10, 0x99, 0x21, 0x2F, 0x99, 0x0E, 0x0C, 0x3D, 0x28, 0x08, 0x32, 0x0D, 0x20,
              0xF9, 0x2E, 0x0F, 0x18, 0xF3, 0x67, 0x3E, 0x64, 0x57, 0xE0, 0x42, 0x3E, 0x91, 0xE0, 0x40, 0x04,
              0x1E, 0x02, 0x0E, 0x0C, 0xF0, 0x44, 0xFE, 0x90, 0x20, 0xFA, 0x0D, 0x20, 0xF7, 0x1D, 0x20, 0xF2,
              0x0E, 0x13, 0x24, 0x7C, 0x1E, 0x83, 0xFE, 0x62, 0x28, 0x06, 0x1E, 0xC1, 0xFE, 0x64, 0x20, 0x06,
              0x7B, 0xE2, 0x0C, 0x3E, 0x87, 0xF2, 0xF0, 0x42, 0x90, 0xE0, 0x42, 0x15, 0x20, 0xD2, 0x05, 0x20,
              0x4F, 0x16, 0x20, 0x18, 0xCB, 0x4F, 0x06, 0x04, 0xC5, 0xCB, 0x11, 0x17, 0xC1, 0xCB, 0x11, 0x17,
              0x05, 0x20, 0xF5, 0x22, 0x23, 0x22, 0x23, 0xC9, 0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B,
              0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E,
              0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99, 0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC,
              0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E, 0x3c, 0x42, 0xB9, 0xA5, 0xB9, 0xA5, 0x42, 0x4C,
              0x21, 0x04, 0x01, 0x11, 0xA8, 0x00, 0x1A, 0x13, 0xBE, 0x20, 0xFE, 0x23, 0x7D, 0xFE, 0x34, 0x20,
              0xF5, 0x06, 0x19, 0x78, 0x86, 0x23, 0x05, 0x20, 0xFB, 0x86, 0x20, 0xFE, 0x3E, 0x01, 0xE0, 0x50]
    def __init__(self):
        self._mInterruptEnable = False
        self._mRomBank = 0x1
        self._mRamBank = 0x1
        self._mRamEnabled = False
        self._mInBios = True
        self._mMemoryModel = 0 #default 16/8 mode
        self._mVram = []
        self._mWram = []
        self._mZram = []
        self._mEram = []
        self._mOam = []
        for i in range(8192):
            self._mVram.append(0x0)
            self._mWram.append(0x0)
        for i in range(127):
            self._mZram.append(0x0)
        for i in range(32768):
            self._mEram.append(0x0)
        for i in range(160):
            self._mOam.append(0x0)

    def printStatus(self):
        print "Interrupt Enabled",self._mInterruptEnable
        print "Rom Bank",self._mRomBank
        print "Ram Bank",self._mRamBank
        print "Ram Enabled",self._mRamEnabled
        print "Memory Model",self._mMemoryModel

    def loadProgram(self,filename):
        code = []
        with open(filename,'rb') as f:
            byte = f.read(1)
            while byte!="":
                val = int(byte.encode('hex'),16)
                code.append(val)
                byte = f.read(1)
        self._mCode = code

    def __getitem__(self, addr):
        #ROM bank 0
        if 0x0000 <= addr <= 0x3FFF:
            if addr >= 0x100:
                self._mInBios = False
            if self._mInBios:
                return self._mBios[addr]
            else:
                return self._mCode[addr]
        #ROM bank n
        elif 0x4000 <= addr <= 0x7FFF:
            if self._mRomBank == 0x0:
                self._mRomBank = 0x1
            return self._mCode[(0x4000*self._mRomBank-1)+addr]
        #VRAM
        elif 0x8000 <= addr <= 0x9FFF:
            return self._mVram[0x1FFF & addr]
        #switchable RAM banks
        elif 0xA000 <= addr <= 0xBFFF:
            if self._mRamEnabled:
                return self._mEram[(0x2000*self._mRamBank-1) + (addr & 0x1FFF)]
            else:
                return 0
        #RAM bank + shadow
        elif 0xC000 <= addr <= 0xFDFF:
            return self._mWram[0x1FFF & addr]
        #sprite attrib table
        elif 0xFE00 <= addr <= 0xFEFF:
            return self._mOam[0xFF & addr]
        #device mappings
        elif 0xFF00 <= addr <= 0xFF7F:
            return 0
        #high RAM area
        elif 0xFF80 <= addr <= 0xFFFE:
            return self._mZram[0x7F & addr]
        #interrupt enable registers
        elif addr == 0xFFFF:
            return 0
        #out of bounds
        else:
            raise IndexError("Address out of bounds")

    def __setitem__(self, addr, val):
        #ROM
        if 0x0000 <= addr <= 0x7FFF:
            #RAM enable
            if 0x0000 <= addr <= 0x1FFF:
                if (val & 0x0F) == 0x0A:
                    self._mRamEnabled = True
                else:
                    self._mRamEnabled = False
            #select ROM bank
            elif 0x2000 <= addr <= 0x3FFF:
                self._mRomBank &= 0xE0
                self._mRomBank |= val
            #select RAM bank/most significant ROM address
            elif 0x4000 <= addr <= 0x5FFF:
                #msb ROM
                if self._mMemoryModel == 0:
                    bits = (val & 0x3) << 5
                    bits &= 0x60
                    self._mRomBank &= 0x9F
                    self._mRomBank |= bits
                #RAM bank
                else:
                    self._mRamBank = val & 0xFC
            #select memory model
            elif 0x6000 <= addr <= 0x7FFF:
                if (val & 0x0F) == 0x00:
                    self._mMemoryModel = 0
                elif (val & 0x0F) == 0x01:
                    self._mMemoryModel = 1

        #VRAM
        elif 0x8000 <= addr <= 0x9FFF:
            self._mVram[0x1FFF & addr] = val
        #switchable RAM banks
        elif 0xA000 <= addr <= 0xBFFF:
            if self._mRamEnabled:
                self._mEram[(0x2000*self._mRamBank-1) + (addr & 0x1FFF)] = val
        #RAM bank + shadow
        elif 0xC000 <= addr <= 0xDFFF:
            self._mWram[0x1FFF & addr] = val
        #sprite attrib table
        elif 0xFE00 <= addr <= 0xFEFF:
            self._mOam[0xFF & addr] = val
        #device mappings
        elif 0xFF00 <= addr <= 0xFF7F:
            pass
        #high RAM area
        elif 0xFF80 <= addr <= 0xFFFE:
            self._mZram[0x7F & addr] = val
        #interrupt enable registers
        elif addr == 0xFFFF:
            pass
        #out of bounds
        else:
            raise IndexError("Address out of bounds")

def testRamEnable(mem):
    mem[0x0000] = 0x0A
    if mem._mRamEnabled != True:
        print "Ram Enable Fail"
    mem[0x1FFF] = 0x00
    if mem._mRamEnabled != False:
        print "Ram Disable Fail"

def testMemoryModel(mem):
    mem[0x6000] = 0x01
    if mem._mMemoryModel != 1:
        print "Memory Model Fail"
    mem[0x7FFF] = 0x00
    if mem._mMemoryModel !=0:
        print "Memory Model Fail"

def testBiosSwitch(mem):
    mem[0x0000]
    if mem._mInBios != True:
        print "Bios Fail"
    mem[0x100]
    if mem._mInBios != False:
        print "Bios Switch Fail"

def testRomBankSwitch(mem):
    mem[0x2000] = 0x2
    if mem._mRomBank != 2:
        print "Rom Switch Fail"
    mem[0x3FFF] = 0x5
    if mem._mRomBank != 5:
        print "Rom Switch Fail"
    mem[0x6000] = 0x0
    mem[0x4000] = 0x2
    if mem._mRomBank != 0x45:
        print "MSB Rom Switch Fail"
        print mem._mRomBank

def testRamBankSwitch(mem):
    pass

if __name__ == "__main__":
    mem = GbMemory()
    mem.loadProgram("c:\\pkmblue.gb")
    mem.printStatus()

    #unit tests
    testRamEnable(mem)
    testMemoryModel(mem)
    testBiosSwitch(mem)
    testRomBankSwitch(mem)
