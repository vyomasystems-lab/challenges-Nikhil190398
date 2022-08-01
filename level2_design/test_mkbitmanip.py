# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
# import bitstring
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock
from bitstring import BitArray

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
    # mav_putvalue_src1  =    0xFFFFFFFF
    # mav_putvalue_src2  =    0x3
    # mav_putvalue_src3  =    0x3
    # # mav_putvalue_instr =    0b00100001010101011001000000110011

    # expected output from the model
    #expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
    instr_set = [0b01000000000000000111000000110011,0b01000000000000000110000000110011,0b01000000000000000100000000110011,0b00100000000000000001000000110011,
0b00100000000000000010000000110011,0b00100000000000000110000000110011,0b00100000000000000101000000110011,0b00100000000000000110000000110011,
0b01100000000000000001000000110011,0b01100000000000000101000000110011,0b01001000000000000001000000110011,0b01001000000000000101000000110011,
0b01001000000000000110000000110011,0b01001000000000000100000000110011,0b01001000000000000111000000110011,0b00101000000000000001000000110011,
0b00101000000000000101000000110011,0b01101000000000000001000000110011,0b01101000000000000101000000110011,0b00001000000000000110000000110011,							
0b00001000000000000100000000110011,0b00001000000000000111000000110011,0b00001000000000000001000000110011,0b00001000000000000101000000110011,
0b00001010000000000010000000110011,0b00001010000000000001000000110011,0b00001010000000000011000000110011,0b00001010000000000100000000110011,
0b00001010000000000101000000110011,0b00001010000000000110000000110011,0b00001010000000000111000000110011,0b00000110000000000001000000110011,
0b00000110000000000101000000110011,0b00000100000000000001000000110011,0b00000100000000000101000000110011,0b01100000000000000001000000010011,	
0b01100000000100000001000000010011,0b01100000001000000001000000010011,0b01100000010000000001000000010011,0b01100000010100000001000000010011,	
0b01100001000000000001000000010011,0b01100001000100000001000000010011,0b01100001001000000001000000010011,0b01100001100000000001000000010011,	
0b01100001100100000001000000010011,0b01100001101000000001000000010011,0b01001000000000000001000000010011,0b00101000000000000001000000010011,	0b01101000000000000001000000010011,	
0b01001000000000000001000000010011,0b01001000000000000101000000010011,0b00100000000000000101000000010011,0b01100000000000000101000000010011,	
0b00101000000000000101000000010011,0b01101000000000000101000000010011]

    def drive_values():
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr

    for i in range(1,len(instr_set)):
        mav_putvalue_src1  =    random.randint(0,0xFFFFFFFF)
        mav_putvalue_src2  =    random.randint(0,0xFFFFFFFF)
        mav_putvalue_src3  =    random.randint(0,0xFFFFFFFF)

        mav_putvalue_instr = instr_set[i]
        # mav_putvalue_instr = 0b00100000000000000101000000010011				

        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
        drive_values()
        yield Timer(1)
        dut_output = dut.mav_putvalue.value
        cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        assert dut_output == expected_mav_putvalue, error_message

        # for i in fun3:
        #     for j in range (0,5):
        #         mav_putvalue_src1  =    random.randint(0,0xFFFFFFFF)
        #         mav_putvalue_src2  =    random.randint(0,0xFFFFFFFF)
        #         mav_putvalue_src3  =    random.randint(0,0xFFFFFFFF)

        #         string = fun7+'000000000'+fun3+'10101'+opcode
        #         # s= atoi(string)
        #         print(string)
        #         instr_value = BitArray(bin=string).int
        #         print(instr_value)
        #         mav_putvalue_instr = instr_value
        #         expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
        #         drive_values()
        #         yield Timer(1)
        #         dut_output = dut.mav_putvalue.value
        #         cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #         cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        #         # comparison
        #         error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        #         assert dut_output == expected_mav_putvalue, error_message




    # # driving the input transaction
    #             def drive_values():
    #                 dut.mav_putvalue_src1.value = mav_putvalue_src1
    #                 dut.mav_putvalue_src2.value = mav_putvalue_src2
    #                 dut.mav_putvalue_src3.value = mav_putvalue_src3
    #                 dut.EN_mav_putvalue.value = 1
    #                 dut.mav_putvalue_instr.value = mav_putvalue_instr
  
    # yield Timer(1) 

    # obtaining the output
    # dut_output = dut.mav_putvalue.value

    # cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
    # cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    
    # # comparison
    # error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    # assert dut_output == expected_mav_putvalue, error_message
