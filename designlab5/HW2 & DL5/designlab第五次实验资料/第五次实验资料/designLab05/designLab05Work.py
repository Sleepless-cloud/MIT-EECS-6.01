import lib601.sig as sig
import lib601.ts as ts
import lib601.poly as poly
import lib601.sf as sf

def controller(k):
   return sf.Gain(k)

def plant1(T):
   return sf.Cascade(sf.Gain(T), sf.R())

def plant2(T, V):
   return sf.Cascade(sf.Cascade(sf.R(), sf.Gain(T*V)), sf.FeedbackAdd(sf.Gain(1), sf.R()))

def wallFollowerModel(k, T, V):
   up = sf.Cascade(sf.Cascade(controller(k), plant1(T)), plant2(T, V))
   return sf.FeedbackSubtract(up, sf.Gain(1))
