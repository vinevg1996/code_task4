#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from help import Help
from random import random

class Decoder:

    def __init__(self, code_info_file, y):
        code_info_desc = open(code_info_file, "r")
        lines = code_info_desc.readlines()
        self.prob = float(lines[0])
        param_list = lines[1].split(' ')
        self.n = int(param_list[0])
        self.k = int(param_list[1])
        self.r = int(param_list[2])
        self.d = int(param_list[3])
        self.t = int(param_list[4])
        #[self.n, self.k, self.r, self.d, self.t] = param_list
        self.mess = y
        self.syndrom_and_leader = dict()
        self.G_matrix = list()
        self.H_matrix = list()
        i = 2
        while (not("G_matrix" in lines[i])):
            line_without_endline = lines[i][ : len(lines[i]) - 1]
            [syndrom_str, leader_str] = line_without_endline.split(',')
            curr_syndrom_str = syndrom_str.split(' ')
            curr_leader_str = leader_str.split(' ')
            curr_leader = [ int(elem) for elem in curr_leader_str ]
            curr_syndrom = [ int(elem) for elem in curr_syndrom_str ]
            self.syndrom_and_leader[str(curr_syndrom)] = curr_leader
            i = i + 1
        i = i + 1
        while (not("H_matrix" in lines[i])):
            line_without_endline = lines[i][ : len(lines[i]) - 1]
            curr_list_str = line_without_endline.split(' ')
            curr_list = [ int(elem) for elem in curr_list_str ]
            self.G_matrix.append(curr_list)
            i = i + 1
        i = i + 1
        while i < len(lines):
            line_without_endline = lines[i][ : len(lines[i]) - 1]
            curr_list_str = line_without_endline.split(' ')
            curr_list = [ int(elem) for elem in curr_list_str ]
            self.H_matrix.append(curr_list)
            i = i + 1

    def decode_recieve_mess(self):
        helper = Help()
        syndrom = helper.mult_matrix_for_vector(self.H_matrix, self.mess)
        leader = self.syndrom_and_leader.get(str(syndrom))
        decode_mess = helper.xor(self.mess, leader)
        print("decode_mess = ", decode_mess[0 : self.k])
        print("prob = ", self.prob)

    def print_syndrom_and_leader(self):
        for syndrom in self.syndrom_and_leader.keys():
            leader = self.syndrom_and_leader[syndrom]
            print("syndrom = ", syndrom, end = ' : ')
            print("leader = ", leader)

    def print_G_matrix(self):
        print("G_matrix:")
        for curr_str in self.G_matrix:
            print(curr_str)

    def print_H_matrix(self):
        print("H_matrix:")
        for curr_str in self.H_matrix:
            print(curr_str)