# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from parser import *
from automate import *
import itertools

automate = Automate.creationAutomate("exempleAutomate.txt")
automate.show("exempleAutomate")


#SEANCE DU 18/11/2020 16h-17h45


#création de l'automate 2.1

# création d'états
# s0 : State
s0 = State(0, True, False)
# s1 : State
s1 = State(1, False, False)
# s2 : State
s2 = State(2, False, True)

# création de transitions
# t1 : Transition
t1 = Transition(s0,"a",s0)
# t2 : Transition
t2 = Transition(s0,"b",s1)
# t3 : Transition
t3 = Transition(s1,"b",s2)
# t4 : Transition
t4 = Transition(s1,"a",s2)
# t5 : Transition
t5 = Transition(s2,"b",s1)
# t6 : Transition
t6 = Transition(s2,"a",s0)
#t7 : Transition
t7 = Transition(s0,"a",s1)

# liste : list[Transition]
liste = [t1,t2,t3,t4,t5,t6]

# création de l’automate
# auto : Automate=
auto = Automate(liste)

print(auto)
#auto.show("A_ListeTrans")

# auto1 : Automate
auto1 = Automate([t1,t2,t3,t4,t5,t6,t7], [s0,s1,s2])

print(auto1)
auto1.show("auto1")

# auto2 : Automate
auto2 = Automate.creationAutomate("auto.txt")
print(auto2)
auto2.show("Auto2")


# 2.2.1

# t: Transition
t= Transition(s0, "a", s1)

#auto.removeTransition(t)
print(auto)

auto.removeTransition(t1)
print(auto) #on remarque que l'appel à removeTransition avec t1 en argument à supprimer la transition (0,a,1)

#auto.addTransition(t1)
print(auto) # l'automate otenu est bien le même qu'initialement

# 2.2.2

#auto.removeState(s1)
print(auto) #toutes les transitions impliquant s1 ont été supprimées.

#auto.addState(s1)
print(auto) #l'état s1 a été ajouté mais pas les transitions l'impliquant

# # s2: State
# s2 = State(0, True, False)
#auto.addState(s2)
# print(auto) #l'état s2 n'as pas été ajouté à auto


# 2.2.3
#listeTrans: List[Transition]
listeTrans=auto1.getListTransitionsFrom(s1)
print(listeTrans)

#test de succElem
#list=list[State]
print "Liste succElem"
list = auto1.succElem(s1,"a")
print(list)


#test de succ
#list=list[State]
list2 = auto1.succ(list,"b")
list3 = auto1.succ(list,"a")
print "Liste succ"
print(list2+list3)

#test de la méthode accepte
if Automate.accepte(auto1,"ba"):
    print "L'automate accepte le mot ba"
else:
    print "L'automate n'accepte pas le mot ba"


#alphabet
alphabet = ['a','b']

#test estComplet
print("estComplet sur auto:")
print(Automate.estComplet(auto,alphabet)) # pas complet à ce stade donc False
print("estComplet sur auto1:")
print(Automate.estComplet(auto1,alphabet)) # complet donc True

#test estDeterministe
print("estDeterministe sur auto1:")
print(Automate.estDeterministe(auto1))  # False 


#test completeAutomate
autobis = Automate.completeAutomate(auto,alphabet) #automate auto complété
autobis.show("A_ListeTrans") #on voit que auto a bien été complété par l'ajout de l'état 'poubelle' numéro 3
print("estComplet sur autobis:")
print(Automate.estComplet(autobis,alphabet)) # True


#test fonction determinisation
auto1bis = Automate.determinisation(auto1)
auto1bis.show("auto1bis")
#test estDeterministe sur auto1bis
print("estDeterministe sur auto1bis:")
print(Automate.estDeterministe(auto1bis))  # True 


import itertools
# L1 = [1, 2, 3]
# L2 = ["a", "b", "c"]
# L = [item for item in itertools.product(L1, L2)]
# print L

# test intersection 
autoInter = Automate.intersection(auto1, auto2)
autoInter.show("autoInter")


# concaténation de deux automates

autoConcat = Automate.concatenation(auto1, auto2)
autoConcat.show("autoConcat")




