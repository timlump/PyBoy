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
            if instruction != None:
                self._wait(sTime,instruction.cycles)

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

    #0x00

    #0x01
    _i[0x01] = _load_r_n
    _iParam[0x01] = ('BC',2)

    #0x02
    _i[0x02] = _load_a_r
    _iParam[0x02] = ('BC','A')


if __name__ == "__main__":
    pass
