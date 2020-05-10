#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from combinatorics import Combinatorics
from help import Help
import math
import sys

class CodeBuilder:
    
    def __init__(self, n, p):
        self.p = p
        self.n = n
        self.entropy = (-1) * p * math.log2(p) + (-1) * (1 - p) * math.log2(1 - p)
        self.r = int(n * self.entropy) + 1
        self.k = self.n - self.r
        self.d = self.calculate_dist()
        self.t = (self.d - 1) // 2
        self.H_transpose = list()
        self.H_matrix = list()
        self.G_matrix = list()
        self.words = list()
        self.standart_placement = list()
        self.syndrom_table = list()
        '''
        print("entropy = ", self.entropy)
        print("n = ", self.n)
        print("r = ", self.r)
        print("d = ", self.d)
        print("t = ", self.t)
        '''

    def calculate_dist(self):
        helper = Help()
        sum_combs = 1
        i = 1
        flag = True
        #print("2**r = ", 2 ** self.r)
        while flag:
            #print("i = ", i, ": ", helper.calculate_comb(self.n - 1, i))
            sum_combs = sum_combs + helper.calculate_comb(self.n - 1, i)
            #print("sum_combs = ", sum_combs)
            if (sum_combs >= 2 ** self.r):
                flag = False
            else:
                i = i + 1
        dist = i + 1
        if (dist <= self.r - 1):
            return dist
        else:
            return self.r - 1

    def check_for_depend(self):
        helper = Help()
        Comb = Combinatorics()
        for i in range(2, self.d):
            allCombinations = []
            Comb.GenerationAllCombinations(allCombinations, self.n, i)
            for combination in allCombinations:
                new_vector = helper.sum_of_vectors(self.H_transpose, combination)
                #print("new_vector = ", new_vector)
                if (new_vector.count(1) == 0):
                    print("False")
                    print("count = ", new_vector.count(1))
                    print("combination = ", combination)
                    for index in combination:
                        print(self.H_transpose[index])
                    return
        print("True")
        Comb.GenerationAllCombinations(allCombinations, self.n, self.d)
        for combination in allCombinations:
            new_vector = helper.sum_of_vectors(self.H_transpose, combination)
            if (new_vector.count(1) == 0):
                print("depend for d")
                print("combination = ", combination)
                return
        return

    def print_H_matrix(self):
        print("H_matrix:")
        for curr_str in self.H_matrix:
            print(curr_str)

    def print_G_matrix(self):
        print("G_matrix:")
        for curr_str in self.G_matrix:
            print(curr_str)

    def create_depended_cols(self, size, depend_list):
        helper = Help()
        Comb = Combinatorics()
        for i in range(2, self.d):
            allCombinations = []
            Comb.GenerationAllCombinations(allCombinations, size, i)
            for combination in allCombinations:
                new_vector = helper.sum_of_vectors(self.H_transpose, combination)
                dec = helper.convert_binary_to_decimal(new_vector, self.r)
                #print("dec = ", dec)
                depend_list[dec] = 1
        return

    def create_H_matrix(self):
        helper = Help()
        Comb = Combinatorics()
        depend_list = [0 for x in range(0, 2 ** self.r)]
        depend_list[0] = 1
        for i in range(0, self.r):
            curr_list = [0 for x in range(0, self.r)]
            curr_list[i] = 1
            dec = helper.convert_binary_to_decimal(curr_list, self.r)
            depend_list[dec] = 1
            self.H_transpose.append(curr_list)
        size = self.r
        while size < self.n - 1:
            self.create_depended_cols(size, depend_list)
            zero_index = depend_list.index(0)
            new_vector = helper.convert_decimal_to_binary(zero_index, self.r)
            self.H_transpose.append(new_vector)
            depend_list[zero_index] = 1
            size = size + 1
        dep_combination = [j for j in range(0, self.d - 1)]
        new_vector = helper.sum_of_vectors(self.H_transpose, dep_combination)
        self.H_transpose.append(new_vector)
        helper.change_rows_order(self.H_transpose)
        self.H_matrix = helper.transpose_matrix(self.H_transpose)

    def create_G_matrix(self):
        helper = Help()
        #G_0_transpose = list()
        G_0_transpose = [ list(self.H_matrix[i][0 : self.k]) for i in range(0, self.r) ]
        G_0 = helper.transpose_matrix(G_0_transpose)
        for i in range(0, self.k):
            curr_list = [0 for x in range(0, self.k)]
            curr_list[i] = 1
            self.G_matrix.append(curr_list)
        for i in range(0, self.k):
            for j in range(0, len(G_0[i])):
                self.G_matrix[i].append(G_0[i][j])
        #print("check_G_H_product = ", self.check_G_H_product())
        return

    def check_G_H_product(self):
        helper = Help()
        matrix = helper.mult_matrix_for_matrix(self.G_matrix, self.H_transpose)
        '''
        print("G_H_product:")
        for row in matrix:
            print(row)
        '''
        sum_ones = 0
        for row in matrix:
            sum_ones = sum_ones + row.count(1)
        if (sum_ones == 0):
            return True
        else:
            return False

    def create_words(self):
        helper = Help()
        for i in range(0, 2 ** self.k):
            word = helper.convert_decimal_to_binary(i, self.k)
            self.words.append(word)
        return

    def create_standart_placement(self):
        helper = Help()
        code_words = list()
        for word in self.words:
            code_word = helper.mult_vector_for_matrix(word, self.G_matrix)
            code_words.append(code_word)
        '''
        print("code_words:")
        for code_word in code_words:
            print(code_word)
        '''
        self.standart_placement.append(code_words)
        depend_list = [0 for x in range(0, 2 ** self.n)]
        for code_word in code_words:
            dec = helper.convert_binary_to_decimal(code_word, self.n)
            depend_list[dec] = 1
        for i in range(0, 2 ** self.r - 1):
            leader = helper.find_min_weight_in_depend_list(depend_list, self.n)
            #print("leader = ", leader)
            coset = list()
            for code_word in code_words:
                coset_word = helper.xor(leader, code_word)
                dec = helper.convert_binary_to_decimal(coset_word, self.n)
                depend_list[dec] = 1
                #print("coset_word = ", coset_word)
                coset.append(coset_word)
            self.standart_placement.append(coset)
        #print("depend_list = ", depend_list)
        return

    def create_syndrom_table(self):
        helper = Help()
        for coset in self.standart_placement:
            leader = coset[0]
            syndrom = helper.mult_matrix_for_vector(self.H_matrix, leader)
            self.syndrom_table.append(syndrom)
        '''
        print("syndrom_table:")
        for syndrom in self.syndrom_table:
            print(syndrom)
        '''
        return

    def write_dict_for_decode(self):
        helper = Help()
        print("dictionary_for_decoder:")
        for i in range(0, len(self.standart_placement)):
            syndrom_leader = self.syndrom_table[i]
            print("{", syndrom_leader, ": " , end = '')
            weight_list = list()
            for coset in self.standart_placement[i]:
                weight = helper.calculate_weight_for_vector(coset)
                if (weight <= self.t):
                    weight_list.append(list(coset))
            print(weight_list, "} ")

    def write_code_to_file(self, out_file):
        out_file_desc = open(out_file, "w")
        prob = self.calculate_probability()
        out_file_desc.write(str(prob))
        out_file_desc.write("\n")
        param_list = [self.n, self.k, self.r, self.d, self.t]
        out_file_desc.write(str(self.n))
        out_file_desc.write(" ")
        out_file_desc.write(str(self.k))
        out_file_desc.write(" ")
        out_file_desc.write(str(self.r))
        out_file_desc.write(" ")
        out_file_desc.write(str(self.d))
        out_file_desc.write(" ")
        out_file_desc.write(str(self.t))
        out_file_desc.write("\n")
        syn_leader_list = list()
        i = 0
        while i < len(self.standart_placement):
            #syn_leader = [self.syndrom_table[i], self.standart_placement[i][0]]
            #syn_leader_list.append(syn_leader)
            #out_file_desc.write(str(syn_leader))
            j = 0
            for syndrom in self.syndrom_table[i]:
                out_file_desc.write(str(syndrom))
                if (j < len(self.syndrom_table[i]) - 1):
                    out_file_desc.write(" ")
                    j = j + 1
                else:
                    out_file_desc.write(",")
            j = 0
            for leader in self.standart_placement[i][0]:
                out_file_desc.write(str(leader))
                if (j < len(self.standart_placement[i][0]) - 1):
                    out_file_desc.write(" ")
                    j = j + 1
                else:
                    out_file_desc.write("\n")
            i = i + 1
        out_file_desc.write("G_matrix:")
        out_file_desc.write("\n")
        for curr_list in self.G_matrix:
            j = 0
            for elem in curr_list:
                out_file_desc.write(str(elem))
                if (j < len(curr_list) - 1):
                    out_file_desc.write(" ")
                    j = j + 1
                else:
                    out_file_desc.write("\n")
        out_file_desc.write("H_matrix:")
        out_file_desc.write("\n")
        for curr_list in self.H_matrix:
            #out_file_desc.write(str(curr_list))
            #out_file_desc.write("\n")
            j = 0
            for elem in curr_list:
                out_file_desc.write(str(elem))
                if (j < len(curr_list) - 1):
                    out_file_desc.write(" ")
                    j = j + 1
                else:
                    out_file_desc.write("\n")
        return

    def print_standart_placement(self):
        print("standart_placement:")
        for coset in self.standart_placement:
            print(coset)

    def check_for_liniar_code(self):
        helper = Help()
        i = 0
        code_words = self.standart_placement[0]
        while i < len(code_words):
            j = i + 1
            while j < len(code_words):
                sum_vector = helper.xor(code_words[i], code_words[j])
                if (not(sum_vector in code_words)):
                    print("code is not liniar")
                    print("i = ", i)
                    print("j = ", j)
                    print(code_words[i])
                    print(code_words[j])
                j = j + 1
            i = i + 1
        print("code is liniar")
        return

    def calculate_probability(self):
        helper = Help()
        syn_leader_list = list()
        weight_and_count = dict()
        for i in range(0, self.t + 1):
            weight_and_count[i] = 0
        i = 0
        while i < len(self.standart_placement):
            leader = self.standart_placement[i][0]
            weight = helper.calculate_weight_for_vector(leader)
            if (weight <= self.t):
                weight_and_count[weight] = weight_and_count[weight] + 1
            i = i + 1
        prob_e_leader = 0
        for weight in weight_and_count.keys():
            prob = (self.p ** weight) * ((1 - self.p) ** (self.n - weight))
            prob_e_leader = prob_e_leader + (weight_and_count[weight] * prob)
        prob_e_not_leader = 1 - prob_e_leader
        return prob_e_not_leader

    def print_code_words(self):
        print("code_words:")
        for code_word in self.standart_placement[0]:
            print(code_word)