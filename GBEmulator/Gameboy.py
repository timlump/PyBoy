__author__ = 'Timothy'

import GbMemory
import GbCpu

mem = GbMemory.GbMemory()
cpu = GbCpu.GbCpu(mem)

if __name__ == "__main__":
    cpu.run()


