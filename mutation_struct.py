import random
import paramset

class Data:
    random_obj = None
    denominator = 50
    cut_first = 0.1
    cut_second = 0.7
    def __init__(self, random_object, den=50):
        self.random_obj = random_object
        self.denominator = den

    mutators = [crossover, mix_random, add_random, del_rand_part,del_rand_endpart]

    def random_str(self, length, sourse=None): # создание произвольно строки
        if sourse is None:
            sourse = [chr(n) for n in range(256)]
        return ''.join(random.choice(sourse) for i in range(length))

    def random_file(self, origin, file=None):
        size = len(origin)
        return ''.join(self.random_str(size, ))

    def cut_part(self, size, file): # выбор места для отреза
        empty = True
        file_in_list = False
        if len(paramset.TAINTANALYSISINFO) > 0:
            empty = False
            if file in paramset.TAINTANALYSISINFO.keys():
                cmp_sets = paramset.TAINTANALYSISINFO[file][0]
                file_in_list = True
        if empty == False and file_in_list == True:
            cut_position = random.randint(0,size)
        return cut_position

    def del_rand_endpart(self, origin, file=None): # удалить произвольную часть в конце
        cut_size = random.randint(1,max(1,len(origin)/self.denominator))
        cut_position = random.randint(len(origin)/2, len(origin)-cut_size)
        res_obj = origin[:cut_position] + origin[cut_position+cut_size]
        return res_obj

    def del_rand_part(self, origin, file):  # удаление произвольной части
        size = len(origin)
        cut_size = random.randint(1,max(1,size/self.denominator))
        cut_position = self.cut_part(size, file)
        result = origin[:cut_position] + origin[cut_position+cut_size]
        return result

    def add_random(self, sourse, cut_pos): # добавление произвольной части
        size = len(sourse)
        if not cut_pos:
            size_of_adding = max(1, random.randint(1, max(1, size/self.denominator)))
        else:
            size_of_adding = cut_pos
        return ''.join(sourse[:size_of_adding] + self.random_str(size_of_adding ,None))

    def mix_random(self, sourse, cut_pos): # добавление произвольной части,где символы из исходной части
        size = len(sourse)
        if not cut_pos:
            size_of_adding = max(1, random.randint(1, max(1, size/self.denominator)))
        else:
            size_of_adding = cut_pos
        cutting_size = size - size_of_adding
        return ''.join(sourse[:cutting_size] + self.random_str(size_of_adding, sourse[cutting_size:]))

    def crossover(self, parent1, parent2): # смешивание двух родителей в 2 ребенка
        cut_place = random.uniform(self.cut_first, self.cut_second)
        len1 = len(parent1)
        len2 = len(parent2)
        cut_point1 = len1*cut_place
        cut_point2 = len2*cut_place
        child1 = parent1[:cut_point1] + parent2[cut_point2:]
        child2 = parent2[:cut_point2] + parent1[cut_point1:]
        return child1, child2
