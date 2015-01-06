__author__ = 'Timothy'

import GbRegisterSet
import time

class GbCpu:
    def __init__(self,memory):
        self._r = GbRegisterSet()
        self._m = memory
        self._i = []
        self._cb = []
        for x in range(0x100):
            self._i.append(None)
            self._cb.append(None)

    def run(self):
        while True:
            sTime = int(time.time())
            pc = self._r["PC"]
            opcode = self._fetch(pc)
            instruction = self._decode(opcode,pc)
            self._execute(instruction,pc)
            if instruction != None:
                self._wait(sTime,instruction.cycles)

    def reset(self):
        pass

    def _fetch(self,pc):
        return self._m[pc]

    def _decode(self,opcode,pc):
        if opcode == 0xCB:
            newOpcode = self._m[pc+1]
            return self._cb[newOpcode]
        else:
            return self._i[opcode]

    def _execute(self,instruction,pc):
        if instruction != None:
            instruction(self,pc)

    def _wait(self,sTime,cycles):
        pass


if __name__ == "__main__":
    pass