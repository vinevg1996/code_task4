#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from combinatorics import Combinatorics
from help import Help
from code_builder import CodeBuilder
from encoder import Encoder
from decoder import Decoder
import math
import sys

if (sys.argv[1] == "mode=1"):
    n = int(sys.argv[2])
    p = float(sys.argv[3])
    code = CodeBuilder(n, p)
    code.create_H_matrix()
    code.create_G_matrix()
    code.create_words()
    code.create_standart_placement()
    code.create_syndrom_table()
    print("n = ", code.n)
    print("k = ", code.k)
    print("d = ", code.d)
    print("t = ", code.t)
    code.write_dict_for_decode()
    code.write_code_to_file(sys.argv[4])
    prob = code.calculate_probability()
    print("prob for decode error = ", prob)
elif (sys.argv[1] == "mode=2"):
    m = [ int(sym) for sym in sys.argv[3] ]
    if (len(sys.argv) == 4):
        enc = Encoder(sys.argv[2], m)
    else:
        e = [ int(sym) for sym in sys.argv[4] ]
        enc = Encoder(sys.argv[2], m, e)
    enc.create_code()
else:
    y = [ int(sym) for sym in sys.argv[3] ]
    dec = Decoder(sys.argv[2], y)
    dec.decode_recieve_mess()