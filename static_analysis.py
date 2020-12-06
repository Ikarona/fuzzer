from idautils import *
from idc import *
from idaapi import *
from collections import deque


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

def get_children(BB): # получаем list базисных блоков, которые являются детьми данного
    childList = []
    startsDeque = deque([])
    copyDeque = deque([])
    if len(BB.succs()):
        return childList
    for succ_block in BB.succs(): # succs() - list of all successors
        startsDeque.append(succ_block.startEA)
        copyDeque.append(succ_block)
    while copyDeque:
        currBlock = copyDeque.popleft()
        startsDeque.popleft()
        if currBlock not in childList:
            childList.append(currBlock.startEA)
        for curBlSucc in currBlock.succs(): # проверка на всякий случай
            if (curBlSucc.startEA not in childList) and (curBlSucc.startEA not in startsDeque):
                copyDeque.append(curBlSucc)
                startsDeque.append(curBlSucc)
    del startsDeque
    del copyDeque
    return childList

def if_path(fromBB, toBB, backedge): 
    #backedge  - list of tuple(startEA, endEA)
    visitedId = set()
    noPath = False
    succsDeque = deque([])
    if fromBB.startEA == toBB.startEA:
        return True
    for fsucc in fromBB.succs():
        if((fromBB.startEA, fsucc.startEA)) not in backedge:
            noPath = True
        visitedId.add(fsucc.id)
        succsDeque.append(fsucc)
    if noPath == False:
        return noPath
    while succsDeque:
        currSucc = succsDeque.pop()
        if currSucc.id == toBB.id:
            return noPath
        for ccurrSucc in currSucc.succs():
            if ccurrSucc.id not in visitedId and (currSucc.startEA, ccurrSucc.startEA) not in backedge:
                succsDeque.append(ccurrSucc)
                visitedId.add(ccurrSucc.Id)
            else:
                continue
    return False

def get_backedges(root):
    tmp=deque([])
    visited=set()
    backedge=[]# a list of tuple of the form (startEA,endEA), denoting an edge.
    tmp.append(root)
    while len(tmp)>0:
        cur=tmp.popleft()
        visited.add(cur.startEA)
        for ccur in cur.succs():
            if ccur.startEA in visited and get_path(ccur,cur,backedge) == True:
                backedge .append((cur.startEA,ccur.startEA))
            elif ccur.startEA not in visited:
                visited.add(ccur.startEA)
                tmp.append(ccur)
            else:
                pass
    # now we repeat the above step to prune backedges that we got so far.
    tmp.clear()
    visited=set()
    backedgeF=[]
    tmp.append(root)
    while len(tmp)>0:
        cur=tmp.popleft()
        visited.add(cur.startEA)
        for ccur in cur.succs():
            if ccur.startEA in visited and get_path(ccur,cur,backedge) == True:
                backedgeF.append((cur.startEA,ccur.startEA))
            elif ccur.startEA not in visited:
                visited.add(ccur.startEA)
                tmp.append(ccur)
                #print "visited: %x"% ccur.startEA
            else:
                pass
    return backedge
