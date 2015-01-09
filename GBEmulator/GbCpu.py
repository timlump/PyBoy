__author__ = 'Timothy'

import GbRegisterSet
import time

class GbCpu:
    _i = []
    _cb = []
    _iParam = []
    _cbParam = []
    for x in range(0x100):
        _i.append(None)
        _cb.append(None)
        _iParam.append(None)
        _cbParam.append(None)

    def __init__(self,memory):
        self._r = GbRegisterSet()
        self._m = memory

    def run(self):
        while True:
            sTime = int(time.time())
            opcode = self._fetch()
            instruction,params = self._decode(opcode)
            self._execute(instruction,params)

    def reset(self):
        self._r.reset()

    def _fetch(self):
        return self._m[self._r['PC']]

    def _decode(self,opcode):
        if opcode == 0xCB:
            self._r['PC'] += 1
            newOpcode = self._m[self._r['PC']]
            return self._cb[newOpcode],self._cbParam[newOpcode]
        else:
            return self._i[opcode],self._iParam[opcode]

    def _execute(self,instruction,params):
        if instruction != None:
            instruction(self,params)

    def _wait(self,sTime,cycles):
        pass

    #load instructions
    def _load_r_r(self,params):
        self._r[params[0]] = self._r[params[1]]
        self._r['PC'] += 1

    def _load_r_a(self,params):
        addr = self._r[params[1]]
        self._r[params[0]] = self._m[addr]
        self._r['PC'] += 1

    def _load_a_r(self,params):
        addr = self._r[params[0]]
        self._m[addr] = self._r[params[1]]
        self._r['PC'] += 1

    def _load_n_r(self,params):
        addr = GbRegisterSet.GbRegister()
        pc = self._r['PC']
        if params[0] == 1:
            addr.full = self._m[pc+1]
            self._r['PC'] += 1
        else:
            addr.fields.hi = self._m[pc+1]
            addr.fields.lo = self._m[pc+2]
            self._r['PC'] += 2
        self._m[addr.full] = self._r[params[1]]

    def _load_r_n(self,params):
        reg = params[0]
        if params[1] == 1:
            self._r[reg] = self._m[self._r['PC']+1]
            self._r['PC'] += 1
        else:
            val = GbRegisterSet.GbRegister()
            pc = self._r['PC']
            val.fields.hi = self._m[pc+1]
            val.fields.lo = self._m[pc+2]
            self._r[reg] = val.full
            self._r['PC'] += 2

    def _load_a_n(self,params):
        addr = self._r[params[0]]
        if params[1] == 1:
            self._m[addr] = self._m[self._r['PC']+1]
            self._r['PC'] += 1
        else:
            val = GbRegisterSet.GbRegister()
            pc = self._r['PC']
            val.fields.hi = self._m[pc+1]
            val.fields.lo = self._m[pc+2]
            self._m[addr] = val.full
            self._r['PC'] += 2

    def _push_r16(self,params):
        reg = GbRegisterSet()
        reg.full = self._r[params[0]]
        self._r['SP'] += 1
        self._m[self._r['SP']] = reg.fields.hi
        self._r['SP'] += 1
        self._m[self._r['SP']] = reg.fields.lo
        self._r['PC'] += 2

    def _pull_r16(self,params):
        reg = GbRegisterSet()
        reg.fields.lo = self._m[self._r['SP']]
        self._r['SP'] -= 1
        reg.fields.hi = self._m[self._r['SP']]
        self._r['SP'] -= 1
        self._r[params[0]] = reg.full
        self._r['PC'] += 2

    def _inc_r8(self,params):
        before = self._r[params[0]]
        after = before + 1
        self._r[params[0]] = after
        #set flags
        if after == 0:
            self._r['Zf'] = 1
        self._r['Nf'] = 0
        if (after & 0xF) < (before & 0xF):
            self._r['Hf'] = 1
        self._r['PC'] += 1

    def _inc_a8(self,params):
        addr = self._r[params[0]]
        before = self._m[addr]
        after = before + 1
        self._m[addr] = after
        #set flags
        if after == 0:
            self._r['Zf'] = 1
        self._r['Nf'] = 0
        if (after & 0xF) < (before & 0xF):
            self._r['Hf'] = 1
        self._r['PC'] += 1


    def _dec_r8(self,params):
        before = self._r[params[0]]
        after = before - 1
        self._r[params[0]] = after
        #set flags
        if after == 0:
            self._r['Zf'] = 1
        self._r['Nf'] = 1
        if (after & 0xF) == (before & 0xF):
            self._r['Hf'] = 1
        self._r['PC'] += 1

    def _dec_a8(self,params):
        addr = self._r[params[0]]
        before = self._m[addr]
        after = before - 1
        self._m[addr] = after
        #set flags
        if after == 0:
            self._r['Zf'] = 1
        self._r['Nf'] = 1
        if (after & 0xF) == (before & 0xF):
            self._r['Hf'] = 1
        self._r['PC'] += 1

    #0x00

    #0x01
    _i[0x01] = _load_r_n
    _iParam[0x01] = ('BC',2)

    #0x02
    _i[0x02] = _load_a_r
    _iParam[0x02] = ('BC','A')

    #0x03

    #0x04
    _i[0x04] = _inc_r8
    _iParam[0x04] = ('B')

    #0x05
    _i[0x05] = _dec_r8
    _iParam[0x05] = ('B')

    #0x06
    _i[0x06] = _load_r_n
    _iParam[0x06] = ('B',1)

    #0x07

    #0x08
    _i[0x08] = _load_n_r
    _iParam[0x08] = (2,'SP')

    #0x09

    #0x0A
    _i[0x0A] = _load_r_a
    _iParam[0x0A] = ('A','BC')

    #0x0B

    #0x0C
    _i[0x0C] = _inc_r8
    _iParam[0x0C] = ('C')

    #0x0D
    _i[0x0D] = _dec_r8
    _iParam[0x0D] = ('C')


if __name__ == "__main__":
    pass
