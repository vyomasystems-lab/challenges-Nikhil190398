import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def up_down_counter_test(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut._log.info("------------Verifying Reset------------\n")
    dut.rst.value = 0
    await FallingEdge(dut.clk)  
    dut.rst.value = 1
    await FallingEdge(dut.clk)
    dut.rst.value = 0
    assert(dut.data_out.value == 0000),"rst error, Reset not working properly"
    dut._log.info("\n\tReset working properly !\n")



    """ UP COUNT VERIFICATION """
    dut._log.info("------------Verifying UP count------------\n")
    for i in range(0,20):        
        dut.updown.value = 1
        previous_count = int(dut.data_out.value)        
        await FallingEdge(dut.clk)

        present_count = previous_count + 1
        if present_count>15:
            present_count=0
            
        output = int(dut.data_out.value)

        dut._log.info(f'updown = {dut.updown.value},load = {dut.load.value},Prev_cnt = {previous_count},Prsnt_count = {present_count}, DUT_count = {int(dut.data_out.value)}')
        assert (output == present_count),"Error while counting up"
    dut._log.info("\n\t UP counter verified ! \n")

    """ DOWN COUNT VERIFICATION """
    dut._log.info("------------Verifying DOWN count------------\n")
    for i in range(0,20):        
        dut.updown.value = 0
        previous_count = int(dut.data_out.value)        
        await FallingEdge(dut.clk)

        present_count = previous_count - 1
        if present_count < 0:
            present_count=15
            
        output = int(dut.data_out.value)

        dut._log.info(f'updown = {dut.updown.value},load = {dut.load.value},Prev_cnt = {previous_count},Prsnt_count = {present_count}, DUT_count = {int(dut.data_out.value)}')
        assert (output == present_count),"Error while counting down"
    dut._log.info("\n\t DOWN counter verified ! \n")
    
    """ UP COUNT VERIFICATION WITH LOADING"""
    dut._log.info("------------Verifying Data loading while UP count------------\n")
    for i in range(0,20):        
        dut.updown.value = 1
        if(i == 8):
            dut.load.value = 1
            data_inserted = dut.data.value = 12
            await FallingEdge(dut.clk)
            dut._log.info("----------------------------------------------------")
            dut._log.info(f'load = {dut.load.value},Data loaded = {data_inserted},DUT_count = {int(dut.data_out.value)}')
            dut._log.info("----------------------------------------------------")
            dut.load.value = 0
            assert(int(dut.data_out.value)==dut.data.value),"Error loading data, data_loaded={data_in} != data_out={previous_cnt}".format(data_in=int(dut.data.value),previous_cnt=int(dut.data_out.value))
        
        previous_count = int(dut.data_out.value)        
        await FallingEdge(dut.clk)

        present_count = previous_count + 1
        if present_count>15:
            present_count=0
            
        output = int(dut.data_out.value)
        dut._log.info(f'updown = {dut.updown.value},load = {dut.load.value},Prev_cnt = {previous_count},Prsnt_count = {present_count}, DUT_count = {int(dut.data_out.value)}')
        assert (output == present_count),"Error while counting up"
    dut._log.info("\n\tData loaded successfully while Up count ! \n")

    """ DOWN COUNT VERIFICATION WITH LOADING"""

    dut._log.info("------------Verifying Data loading while DOWN count------------\n")
    for i in range(0,20):        
        dut.updown.value = 0
        if(i == 8):
            dut.load.value = 1
            data_inserted = dut.data.value = 12
            await FallingEdge(dut.clk)
            dut._log.info("----------------------------------------------------")
            dut._log.info(f'load = {dut.load.value},Data loaded = {data_inserted},DUT_count = {int(dut.data_out.value)}')
            dut._log.info("----------------------------------------------------")
            dut.load.value = 0
            assert(int(dut.data_out.value)==dut.data.value),"Error loading data, data_loaded={data_in} != data_out={previous_cnt}".format(data_in=int(dut.data.value),previous_cnt=int(dut.data_out.value))
        
        previous_count = int(dut.data_out.value)        
        await FallingEdge(dut.clk)

        present_count = previous_count - 1
        if present_count < 0:
            present_count=15
            
        output = int(dut.data_out.value)

        dut._log.info(f'updown = {dut.updown.value},load = {dut.load.value},Prev_cnt = {previous_count},Prsnt_count = {present_count}, DUT_count = {int(dut.data_out.value)}')
        assert (dut.data_out.value == present_count),"Error while counting down"
    dut._log.info("\n\t Data loaded successfully while DOWN count ! \n")