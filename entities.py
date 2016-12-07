from __future__ import print_function

from os import path as _path
import sys as _sys
import re as _re  # Needed for svg
import math as _math
import numpy as np
import pandas as pd 
import networkx as nx
import vispy as vp
import pdb


#from OCC.ChFi3d import *
#from OCC.BlockFix import *
class entity(object):
    """  An entity is a solid and attachment entities

        a link entitie is a tuple (contact point, direction)
        a link entities define either an affine line or an affine plane
        affine lines and affine planes are used for establishing links
        between solids. 

        Links are either. 
            + Contact intersection of two affine lines
            + Symmetry wrt to an affine plane
    """
    def __init__(self,s1):

        self.solid = s1
        self.G = nx.DiGraph()
        self.G.pos={}
        
        lshell = self.solid.subshapes('shell')
            
        for k,sh in enumerate(lshell):
            
            self.G.pos[k] = sh.center()
            lentities = np.array([[]])
            lentities.shape=(3,0)
            lface = sh.subshapes('face')

            for fa in lface:
                face_type = fa.type()
                lwire = fa.subshapes('wire')
                for wi in lwire:
                    pt_contact = np.array(wi.center())[:,None]
                    lentities = np.append(lentities,pt_contact,axis=1)
                if face_type == 'plane':
                    pass
                if face_type == 'cylinder': 
                    pass       
            self.G.add_node(k,entities=lentities,shape=sh)

    def analyze(self):
        """ solid analysis

        http://videolectures.net/etvc08_guibas_dosarp/

        Estimate of Frequencies of Geometric Regularities
        for Use in Reverse Engineering of
        Simple Mechanical Components


        http://ralph.cs.cf.ac.uk/papers/Geometry/survey.pdf
        http://ralph.cs.cf.ac.uk/papers/Geometry/appsym.pdf
        
        1 : decompose the solid into sub-shells
        2 : each shell becomes a node of the graph 
        3 : The center of mass of the shell becomes the node position 

        """
        lshell = self.subshapes('shell')
        self.G = nx.DiGraph()
        self.G.pos={}
        for k,s in enumerate(lshell):
            self.G.add_node(k)
            self.G.pos[k] = s.center()


