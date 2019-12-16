from unittest import TestCase
from prog3 import Memory

class TestMemory(TestCase):
    def test_set_instruction(self):
        my_mem = Memory()
        my_program = [0,1,2,3,4,5,6,7,8,9,10,11]
        my_mem.set_instruction(my_program)
        self.assertEqual(my_program, my_mem.get_page(0)[0:len(my_program)])

    def test_get_page_offset(self):
        my_mem = Memory()
        pageid =my_mem.get_pageid_and__offset(1025)
        res = (1,1)
        self.assertEqual(res, pageid)

    def test_set_get_mem(self):
        my_mem = Memory()
        my_mem.set_mem(1025,1)
        res = my_mem.get_mem(1025)
        self.assertEqual(res, 1)

    def test_get_mult_mem(self):
        my_mem = Memory()
        my_mem.set_mem(1023,1)
        my_mem.set_mem(1024,2)
        my_mem.set_mem(1025,3)
        res = my_mem.get_mult_mem(1023,3)
        self.assertEqual(res, [1,2,3])

