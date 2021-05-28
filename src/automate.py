# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase
import itertools


class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        resultat = []
        #ensemble: set[State]

        #s : State
        for i in range (0, len(listStates)):
            
            #temp : list[State]
            temp = self.succElem(listStates[i],lettre)
            #state: State
            for j in range(0,len(temp)):
                if temp[j] not in resultat:
                    resultat.append(temp[j])
        return resultat
            


    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        # listInit: list[State]
        listInit = auto.getListInitialStates()
        
        # listFinal: list[State]
        listFinal = auto.getListFinalStates()
        
        # listSucc: list[State]
        listSucc= auto.succ(listInit, mot[0])
        
        if len(mot)==1:
            #s : State
            for s in listInit:
                if s in ListFinal:
                    return True
            return False

        
        for i in range(1, len(mot)):
            listSucc = auto.succ(listSucc, mot[i])
            
            if i == len(mot)-1:
                #s : State
                for s in listSucc:
                    if s in listFinal:
                        return True
        return False 


    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        #lettre: str
        for lettre in alphabet:
            #s: State
            for s in auto.listStates:
                succElem = auto.succElem(s,lettre)
                if len(succElem) < 1 :
                    return False
        return True 

        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        # transitions
        trans = auto.listTransitions
        
        for i in range (0, len(trans)):
            t = trans[i]
            e1 = t.etiquette
            src1 = t.stateSrc
            for j in range(i+1, len(trans)):
                t2 = trans[j]
                e2 = t2.etiquette
                src2 = t2.stateSrc
                if e2 == e1 and src1==src2:
                    return False
        return True
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        if Automate.estComplet(auto,alphabet):
            return auto
        else:
            #autores : Automate 
            autores = copy.deepcopy(auto)
            #listTrans : list[Transitions]
            listTrans = autores.listTransitions

            #listStates : list[State]
            listStates = autores.listStates

            #lenState :int
            lenStates = len(listStates)
            
            #num : int
            num = listStates[lenStates-1].id
            
            #bin : State
            bin = State(num+1, False, False)

            autores.addState(bin)

            for lettre in alphabet:

                for s in listStates:
                    listSucc = autores.succElem(s,lettre)
                    
                    if len(listSucc) == 0:
                        trans = Transition(s,lettre,bin)
                        autores.addTransition(trans)   
            return autores

    @staticmethod
    def listToset(liste):
        """list[State]->set[State]"""
        #res = set[State]
        res = set()
        for e in liste:
            res.add(e)
        return res

    @staticmethod
    def setToList(ens):
        """set[State]->list[State]"""
        #res = list[State]
        res = []
        for e in ens:
            res.append(e)
        return res
    
    @staticmethod
    def final(ens):
        """set[State] -> bool
        renvoie vrai si l'ensemble contient au moins un état final"""

        for s in ens:
            if s.fin == True : 
                return True
        return False

    @staticmethod
    def initial(ens):
        """set[State] -> bool
        renvoie vrai si l'ensemble contient uniquement un état initial"""
        res = Automate.setToList(ens)
        return len(res)==1 and res[0].init == True


    @staticmethod
    def newStates(auto):
        """Automate -> list[set[State]]
        renvoie une liste d'ensemble d'états pour construire l'automate determinisé"""
        # alphabet : set[str]
        alphabet = [t.etiquette for t in auto.listTransitions]
        alphabet = Automate.listToset(alphabet)

        #listInit: list[State]
        listInit = auto.getListInitialStates()

        #listStates: list[set[State]]
        listStates = []
        #ajout des états initiaux de auto dans listStates 
        for s in listInit:
            listStates.append(set([s]))

        #on parcours chaque ensembles dans la listState et on créer un nouveau ensemble d'états successeurs de state
        # state: set[State]
        for state in listStates:
            for lettre in alphabet:
                succ = set()        # nouvel ensemble d'états dans l'automate déterminisé
                new = Automate.setToList(state)      # transforme l'ensemble en liste pour utiliser la fonction succ
                #succElem : list[State]     
                succElem = Automate.succ(auto, new,lettre)
                succElem = Automate.listToset(succElem)      # on transforme le résultat de succ en ensemble
                succ = succ.union(succElem)         # on fait l'union avec succ pour obtenir tous les états successeurs
                if succ not in listStates:          # si l'ensemble d'état n'est pas dans la liste des nouveux états on l'ajoute
                    listStates.append(succ) 
        return listStates

    @staticmethod
    def determinisation(auto):
        """ Automate  -> Automate
            rend l'automate déterminisé d'auto
            """
        if Automate.estDeterministe(auto) == True:
            return Automate(auto1.listTransitions)

        # alphabet : set[str]
        alphabet = [t.etiquette for t in auto.listTransitions]
        alphabet = Automate.listToset(alphabet)

        #listStates: list[set[State]]
        listStates = Automate.newStates(auto)

        #listAutomate : list[Transition]
        listAutomate = []

        # etape d'association des ensembles d'états pour construire les nouvelles transitions 
        for state in listStates:
            for lettre in alphabet:
                depart = Automate.setToList(state)      # etat de départ
                #succElem : list[State]     
                arrivee = Automate.succ(auto, depart,lettre)
                depart = Automate.listToset(depart)
                arrivee = Automate.listToset(arrivee)      # on transforme le resultat de succ en ensemble pour le retrouver dans listStates

                #Etape d'association
                #int
                id1 = listStates.index(depart) 
                id2 = listStates.index(arrivee)
                #bool
                init1 = Automate.initial(depart)
                init2 = Automate.initial(arrivee)
                #bool
                final1 = Automate.final(depart)
                final2 = Automate.final(arrivee)
                #State
                src = State(id1,init1,final1)
                dest = State(id2, init2,final2)

                #Transition et ajout dans listAutomate
                newTrans = Transition(src, lettre, dest)
                listAutomate.append(newTrans) 

        #On construit l'automate à partir des nouvelles transitions
        #autoRes : Automate 
        autoRes = Automate(listAutomate, label='Z')
        return autoRes

    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        # auto1 et auto2 : Automate
        auto1 = Automate.determinisation(auto)
        auto2 = Automate.completeAutomate(auto1, alphabet)

        for state in auto2.listStates :
            state.fin = not(state.fin)
        return auto2

    @staticmethod
    def etatsInter(auto1,auto2):
        """Automate*Automate -> list[tuple[State, State]]"""
        L1 = auto1.listStates
        L2 = auto2.listStates
        L = [item for item in itertools.product(L1, L2)]
        return L

    @staticmethod
    def transFrom(listTrans, lettre, state1, state2):    
        """list[Transition] *str*State*State -> bool
        retourne True s'il existe une transition state1-lettre->state2 dans une liste de transitions"""

        for e in listTrans:
            if e.stateSrc == state1 and e.stateDest==state2 and e.etiquette==lettre:
                return True
        return False

    @staticmethod
    def bothFinal(tup):
        """State * State -> bool"""
        state1, state2 = tup
        return state1.fin == True and state2.fin==True

    @staticmethod
    def bothInitial(tup):
        """tuple[State,State] -> bool"""
        state1, state2 = tup
        return state1.init == True and state2.init==True

    @staticmethod
    def intersection(auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates """

        # alphabet : set[str]
        alphabet = [t.etiquette for t in auto1.listTransitions]
        alphabet = Automate.listToset(alphabet)

        # listStates : list[tuple[State, State]]
        listStates = Automate.etatsInter(auto1,auto2)

        # list[Transition]
        list_trans1 = auto1.listTransitions
        list_trans2  = auto2.listTransitions

        # listTransition:list[Transition]
        listTransition = []
        print listStates
        for lettre in alphabet:
            for i in range(0, len(listStates)):
                # src: tuple[State,State]
                src = listStates[i]
                p1, q2 = src
                for j in range (i, len(listStates)):
                    dest = listStates[j]
                    p_1, q_2 = dest
                    # on vérifie s'il y a des transitions entre src et dest
                    bool1 = Automate.transFrom(list_trans1,lettre,p1, p_1)
                    bool2 = Automate.transFrom(list_trans2, lettre,q2, q_2)
                    if bool1 == True and bool2 == True:
                        #Etape d'association
                        #int
                        id1 = listStates.index(src) 
                        id2 = listStates.index(dest)
                        #bool
                        init1 = Automate.bothInitial(src)
                        init2 = Automate.bothInitial(dest)
                        #bool
                        final1 = Automate.bothFinal(src)
                        final2 = Automate.bothFinal(dest)
                        #State
                        source = State(id1,init1,final1)
                        destination = State(id2, init2,final2)

                        #Transition et ajout dans listTransition
                        newTrans = Transition(source, lettre, destination)
                        listTransition.append(newTrans)
                        
        #On construit l'automate à partir des nouvelles transitions
        #autoRes : Automate 
        autoRes = Automate(listTransition, label='Z')
        return autoRes

    @staticmethod
    def interInitFinal(listInit, listFinal):
        """renvoie True si l'intersection de la liste d'état initiaux et la liste d'état finaux est l'ensemble vide"""
        for e in listInit:
            if e in listFinal:
                return False
        return True

    @staticmethod
    def transToFinalState(listTrans):
        """renvoie la liste des Transitions qui ont un etat de destination final"""
        res = []
        for e in listTrans:
            state = e.stateDest
            if state.fin == True:
                res.append(e)
        return res

    @staticmethod
    def concatenation(auto1,auto2):
        """ Automate x Automate -> Automate
            rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        # listInit
        listInit1 = auto1.getListInitialStates()
        listInit2 = auto2.getListInitialStates()
        listFinal1 = auto1.getListFinalStates()


        # listStates 
        listStates1 = auto1.listStates
        listStates2 = auto2.listStates

        # listTrans
        listTrans1 = auto1.listTransitions
        listTrans2 = auto2.listTransitions
        
        listTransFinal = Automate.transToFinalState(listTrans1)

        newListTransitions = []

        bool = Automate.interInitFinal(listInit1, listFinal1)

        if bool == True:
            for state in listInit2:
                state.init = False

        for state in listStates1:
            state.fin == False
        
        for e in listTransFinal:
            for state in listInit2:
                lettre = e.etiquette
                src = e.stateSrc 
                newTrans = Transition(src, lettre, state)
                newListTransitions.append(newTrans)
        newListTransitions = listTrans1 + listTrans2 
        
        autores = Automate(newListTransitions, label ='Z')
        return autores





