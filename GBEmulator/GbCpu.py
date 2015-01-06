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
            pc = self._r["PC"]
            opcode = self._fetch(pc)
            instruction,params = self._decode(opcode,pc)
            self._execute(instruction,params,pc)
            if instruction != None:
                self._wait(sTime,instruction.cycles)

    def reset(self):
        self._r.reset()

    def _fetch(self,pc):
        return self._m[pc]

    def _decode(self,opcode,pc):
        if opcode == 0xCB:
            self._r[pc] = pc+1
            newOpcode = self._m[self._r[pc]]
            return self._cb[newOpcode],self._cbParam[newOpcode]
        else:
            return self._i[opcode],self._iParam[opcode]

    def _execute(self,instruction,params,pc):
        if instruction != None:
            instruction(self,params,pc)

    def _wait(self,sTime,cycles):
        pass

    #instructions


if __name__ == "__main__":
    pass
