from idautils import *
from idc import *
from idaapi import *

def cmp_operands_finder():
    #проходимся по каждому сегменту и находим там cmp, получаем её операнды
    operands=[] #в будущем список значений операндов
    for seg_ea in Segments(): # список начальных адресов сегментов
        for heads in Heads(seg_ea, SegEnd(seg_ea)): # список инсрукций и данных между началом и концом
            mnem = GetMnem(head) #возвращает название инструкции. "может вернуть не то, что мы видим на экране"
            if mnem in ['cmp','CMP']:
                for i in range(2):
                    if GetOpType(mnem, i) == 5: #GetOpType return == 5 => immediate value
                    value = GetOperandValue(mnem, i) #возвращает -1, если операнд не существует
                    if value != -1:
                        operands.append(value)
    return operands 

def