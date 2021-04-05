import random
import paramset

class Data:
    random_obj = None
    denominator = 50
    cutFirst  = 0.1
    cutSecond = 0.3
    cutThird  = 0.5
    cutFourth = 0.7
    minLength = 25
    def __init__(self, random_object, den=50):
        self.random_obj = random_object
        self.denominator = den

    #mutators = [Crossover, MixRand, AddRand, DelRandPart,DelRandEnd]

    def Die(self, str):
        print(str)
        return 1

    def RandomStr(self, length, sourse=None): # создание произвольно строки
        if sourse is None:
            sourse = [chr(n) for n in range(256)]
        return ''.join(random.choice(sourse) for i in range(length))

    def RandomFile(self, origin, file=None):
        size = len(origin)
        return ''.join(self.RandomStr(size, ))

    def CutPart(self, size, file): # выбор места для отреза
        empty = True
        file_in_list = False
        if len(paramset.TAINTANALYSISINFO) > 0:
            empty = False
            if file in paramset.TAINTANALYSISINFO.keys():
                cmp_sets = paramset.TAINTANALYSISINFO[file][0]
                file_in_list = True
        if empty == False and file_in_list == True:
            cutPosition = random.randint(0,size)
        return cutPosition

    def DelRandEnd(self, origin, file=None): # удалить произвольную часть в конце
        cut_size = random.randint(1,max(1,len(origin)/self.denominator))
        cutPosition = random.randint(len(origin)/2, len(origin)-cut_size)
        res_obj = origin[:cutPosition] + origin[cutPosition+cut_size]
        return res_obj

    def DelRandPart(self, origin, file):  # удаление произвольной части
        size = len(origin)
        cut_size = random.randint(1,max(1,size/self.denominator))
        cutPosition = self.CutPart(size, file)
        result = origin[:cutPosition] + origin[cutPosition+cut_size]
        return result

    def AddRand(self, sourse, cutPos): # добавление произвольной части
        size = len(sourse)
        if not cutPos:
            size_of_adding = max(1, random.randint(1, max(1, size/self.denominator)))
        else:
            size_of_adding = cutPos
        return ''.join(sourse[:size_of_adding] + self.RandomStr(size_of_adding ,None))

    def MixRand(self, sourse, cutPos): # добавление произвольной части,где символы из исходной части
        size = len(sourse)
        if not cutPos:
            size_of_adding = max(1, random.randint(1, max(1, size/self.denominator)))
        else:
            size_of_adding = cutPos
        cutting_size = size - size_of_adding
        return ''.join( sourse[ :cutting_size ] + self.RandomStr( size_of_adding, sourse[ cutting_size: ] ) )

    def Crossover(self, parent1, parent2): # смешивание двух родителей в 2 ребенка с одной точкой среза
        len1 = len(parent1)
        len2 = len(parent2)
        minLen = min( len1, len2 )
        if minLen < self.minLength:
            return parent1, parent2
        cutPlace = random.uniform(self.cutFirst, self.cutSecond)
        cutPoint1 = len1*cutPlace
        cutPoint2 = len2*cutPlace
        child1 = parent1[ :cutPoint1 ] + parent2[ cutPoint2: ]
        child2 = parent2[ :cutPoint2 ] + parent1[ cutPoint1: ]
        return child1, child2

    def DoubleCrossover(self, parent1, parent2): # смешивание двух родителей в 2 ребенка с 2 точками среза
        len1 = len(parent1)
        len2 = len(parent2)
        minLen = min( len1, len2 )
        if minLen < self.minLength:
            return parent1, parent2
        cutPlace1 = random.uniform(self.cutFirst, self.cutSecond)
        cutPlace2 = random.uniform(self.cutSecond, self.cutThird)
        cutPoint11 = int( len1 * cutPlace1 )
        cutPoint12 = int( len1 * cutPlace2 )
        cutPoint21 = int( len2 * cutPlace1 )
        cutPoint22 = int( len2 * cutPlace2 )
        child1 = parent1[ :cutPoint11 ]+parent2[ cutPoint21:cutPoint22 ]+parent1[ cutPoint12: ]
        child2 = parent2[ :cutPoint21 ]+parent1[ cutPoint11:cutPoint12 ]+parent2[ cutPoint22: ]
        return child1, child2

    def TripleCrossover(self, parent1, parent2): # смешивание двух родителей в 2 ребенка с 3 точками среза
        len1 = len(parent1)
        len2 = len(parent2)
        minLen = min( len1, len2 )
        if minLen < self.minLength:
            return parent1, parent2
        cutPlace1 = random.uniform( self.cutFirst, self.cutSecond )
        cutPlace2 = random.uniform( self.cutSecond, self.cutThird )
        cutPlace3 = random.uniform( self.cutFirst, self.cutSecond )
        cutPoint11 = int( len1 * cutPlace1 )
        cutPoint12 = int( len1 * cutPlace2 )
        cutPoint13 = int( len1 * cutPlace3 )
        cutPoint21 = int( len2 * cutPlace1 )
        cutPoint22 = int( len2 * cutPlace2 )
        cutPoint23 = int( len2 * cutPlace3 )
        child1 = parent1[ :cutPoint11 ]+parent2[ cutPoint22:cutPoint23 ]+parent2[ cutPoint21:cutPoint22 ]+parent1[ cutPoint13: ]
        child2 = parent2[ :cutPoint21 ]+parent1[ cutPoint12:cutPoint13 ]+parent1[ cutPoint11:cutPoint12 ]+parent2[ cutPoint23: ]
        return child1, child2

    def ChangeRandom(self, parent, file=None): # замена произвольного байта на произвольное значение
        len1 = len(parent)
        cutPos = random.randint(1, len1)
        randByte = chr(random.randint(0,255))
        child = parent[ :cutPos - 1] + randByte + parent[ cutPos + 1: ]
        return child

    def ChangeMultiRandom(self, parent, file=None): # замена произвольного числа байта на произвольное значение
        len1 = len( parent )
        changeNum = random.randint( 1, len1 // 2 )
        changeBytes = {}
        tmpByte = chr( random.randint( 0, 255 ) )
        tmpPos  = random.randint( 1, len1 )
        changeBytes[ tmpPos ] = tmpByte
        for i in range( 0, changeNum ):
            while tmpPos in changeBytes:
                tmpPos  = random.randint( 1, len1 )
            tmpByte = chr( random.randint( 0, 255 ) )
            changeBytes[ tmpPos ] = tmpByte
        child = parent
        for i in changeBytes:
            child = child[ :i - 1 ] + changeBytes[ i ] + child[ i + 1: ]
        return child

    def ReplaceFromParamset(self, parent, file=None):
        if len( paramset.TAINTANALYSISINFO ) == 0:
            print( "No Taint Analysis info" )
            return parent
        if file in paramset.TAINTANALYSISINFO:
            cmpSets = paramset.TAINTANALYSISINFO[ file ][ 0 ]
        else:
            cmpSets = paramset.TAINTANALYSISINFO[ random.choice( paramset.TAINTANALYSISINFO.keys() ) ][ 0 ]


    mutators = [Crossover, MixRand, AddRand, DelRandPart, DelRandEnd, ReplaceFromParamset, ChangeMultiRandom, ChangeRandom, TripleCrossover, DoubleCrossover]