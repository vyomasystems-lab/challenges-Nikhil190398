# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock
# from bitstring import BitArray

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_src1  =    0xFFFFFFFF
    mav_putvalue_src2  =    0x3
    mav_putvalue_src3  =    0x3
    mav_putvalue_instr =    0b00100001010101011001000000110011

    # expected output from the model
    expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

    # f3 = [0b000,0b001,0b010,0b011,0b100,0b101,0b110,0b111]
    # f7 = [0b01000000,0b0010000,0b0110000,0b0100100,0b0010100,0b0110100,0b0000100,0b0000101]
    f3 = ['000','001','010','011','100','101','110','111']
    f7 = ['0100000','0010000','0110000','0100100','0010100','0110100','000010','0000101']

    def drive_values():
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr

    for i in range(0,20):
        opcode = '0110011'
        fun7 = f7[0]
        fun3 = [f3[7],f3[6],f3[4]]
        for i in fun3:
            for j in range (0,5):
                mav_putvalue_src1  =    random.randint(0,0xFFFFFFFF)
                mav_putvalue_src2  =    random.randint(0,0xFFFFFFFF)
                mav_putvalue_src3  =    random.randint(0,0xFFFFFFFF)

                string = fun7+'0000000000'+f3[7]+'10101'+opcode
                converted = int(str(string).rjust(32, '0'))
                mav_putvalue_instr = hex(converted)
                drive_values()
                yield Timer(1)




    # # driving the input transaction
    #             def drive_values():
    #                 dut.mav_putvalue_src1.value = mav_putvalue_src1
    #                 dut.mav_putvalue_src2.value = mav_putvalue_src2
    #                 dut.mav_putvalue_src3.value = mav_putvalue_src3
    #                 dut.EN_mav_putvalue.value = 1
    #                 dut.mav_putvalue_instr.value = mav_putvalue_instr
  
    yield Timer(1) 

    # obtaining the output
    dut_output = dut.mav_putvalue.value

    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
    cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    
    # comparison
    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    assert dut_output == expected_mav_putvalue, error_message
