﻿#-*- coding: utf-8 -*-

"""
Authors: 
- Florian Thonier, florian.thonier@gmail.com (2014)
- Nathan Foulquier, nathan.foulquier.pro@gmail.com (2014)
- Jean Coquet, coquet.jean@gmail.com (2014)
"""


################################################################
#######################    LIBRARIES    ########################
################################################################
# Django libs:
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str, smart_unicode 
from django.utils.translation import ugettext_lazy as _

# External libs:
from datetime import datetime
import random
import time
import codecs
import os, tempfile, zipfile
from base64 import decodestring
from math import sqrt

from django.db import models
from SmellGuess.models  import *
from SmellGalaxy.models import *
from SmellGift.models   import *

cat1 = [[_(u'Intensités (0~100)'),_(u'Appreciations (0~100)')]]
cat2 = [f.name for f in Food.objects.all()]
################################################################
#########################    VIEWS    ##########################
################################################################
def mean_std_dev(l_durations):
    """ Calculate mean and standard deviation of data durations[]: """
    
    length, mean, std = len(l_durations), 0, 0
    
    for duration in l_durations:
        mean = mean + duration
    
    mean = mean / float(length)
    
    for duration in l_durations:
        std = std + (duration - mean) ** 2
    
    std = sqrt(std / float(length))
    mean = int(round(mean))
    std = int(round(std))
    
    return mean, std


#Intervalle de confiance à 95%:
def errorInterval(l_data):

    n = len(l_data)
    meanData, ecartType = mean_std_dev(l_data)
    
    demiLargeur = 1.96*(ecartType / sqrt(n))
    
    low = meanData - demiLargeur
    high = meanData + demiLargeur
    
    return low, high




# Nathan view
def graphesView(request):
    paramToGenerateTemplate = dict()
    paramToGenerateTemplate['HistoGraphs']    = createListHisto()
    paramToGenerateTemplate['HistoGraphsRE']  = createListHistoRE()
    paramToGenerateTemplate['PiesGraphs']     = createListPie()
    paramToGenerateTemplate['LinesGraphs']    = createListLines()

    return render(request, 'SmellGalaxyTemplate/Graphes.html', paramToGenerateTemplate) 





def paraGraphesView(request):
    
    paramToGenerateTemplate = dict()
    paramToGenerateTemplate['HistoGraphs']    = createListHisto()
    paramToGenerateTemplate['HistoGraphsRE']  = createListHistoRE()
    paramToGenerateTemplate['PiesGraphs']     = createListPie()
    paramToGenerateTemplate['LinesGraphs']    = createListLines()

    return render(request, 'SmellGalaxyTemplate/paraGraphes.html', paramToGenerateTemplate) 





def createListHisto():
	#SetOptionHisto(titre, y, indicationCurseur, cat, donnees, erreur, soustitre) 
	listHisto = []
	
	cat1 = [[_(u'Intensités (0~100)')],[_(u'Appreciations (0~100)')]]
	cat2 = [_(u'Broccoli'), _(u'Gabbage'), _(u'Cauliflower'), _(u'Asparagus'), _(u'Fish'), _(u'Red meat'), _(u'Fast food'), _(u'Spicy food'), _(u'Alcohol'), _(u'Antibiotics')]
	# Intensity & Feeling by sex
	listHisto.append({
		'button': _(u'Données selon le sexe'), 'abscisseName': _(u'Sexe du donneur'), 'description': '',
		'titleLeft' : _(u'Intensités selon le sexe'),     'orderedNameLeft' : _(u'Intensités (0~100)'), 'categoriesLeft' : cat1[0],     'dataLeft' : getDataHistoBySex('intensity'),  'dataErrorLeft': '',
		'titleRight': _(u'Appréciations selon le sexe'),  'orderedNameRight': _(u'Appréciations (-50~50)'), 'categoriesRight' : cat1[1], 'dataRight': getDataHistoBySex('feeling'),  'dataErrorRight': ''})
	# Intensity & Feeling by age
	listHisto.append({
		'button': _(u'Données selon l\'âge'), 'abscisseName': _(u'Tranche d âge'), 'description': '',
		'titleLeft': _(u'Intensités selon l âge'),    'orderedNameLeft': _(u'Intensités (0~100)'), 'categoriesLeft' : cat1[0], 'dataLeft': getDataHistoBySliceOfAge('intensity'),  'dataErrorLeft': '',
		'titleRight': _(u'Appréciations selon l âge'),  'orderedNameRight': _(u'Apréciations'), 'categoriesRight' : cat1[1], 'dataRight': getDataHistoBySliceOfAge('feeling'),  'dataErrorRight': ''})
	# Intensity & Feeling by use of deodorant
	listHisto.append({
		'button': _(u'Données déodorant'),  'abscisseName': _(u'Utilisation de déodorant'),  'description': '',
		'titleLeft': _(u'Intensités selon l utilisation de déodorant'),    'orderedNameLeft': _(u'Intensités (0~100)'),  'categoriesLeft' : cat1[0], 'dataLeft': getDataHistoByDeo('intensity'),  'dataErrorLeft': '', 
		'titleRight': _(u'Appréciations selon l utilisation de déodorant'),  'orderedNameRight': _(u'Appréciations (-50~50)'), 'categoriesRight' : cat1[1], 'dataRight': getDataHistoByDeo('feeling'),  'dataErrorRight': ''})
	# Intensity & Feeling by Smoking
	listHisto.append({
		'button': _(u'Données fumeur'), 'abscisseName': _(u'Comsommation de cigarettes'), 'description': '',
		'titleLeft': _(u'Intensités selon la comsommation de cigarettes'),   'orderedNameLeft': _(u'Intensités (0~100)'), 'categoriesLeft' : cat1[0],   'dataLeft': getDataHistoBySmoker('intensity'),  'dataErrorLeft': '', 
		'titleRight': _(u'Appréciations selon la comsommation de cigarettes'), 'orderedNameRight': _(u'Appréciations (-50~50)'), 'categoriesRight' : cat1[1], 'dataRight': getDataHistoBySmoker('feeling'),  'dataErrorRight': ''})

	return listHisto

def createListHistoRE():
	#SetOptionHisto(titre, y, indicationCurseur, cat, donnees, erreur, soustitre) 
	listHisto = []
	# Intensity by Recently eaten
	listHisto.append({
		'button': _(u'Données selon l\'alimentation'), 'abscisseNameLeft': _(u'Consommation de cigarettes'), 
		'titleLeft': _(u'Intensités selon la consommation d aliments'),   'orderedNameLeft': _(u'Intensités (0~100)'),  'categoriesLeft' : cat2,  'dataLeft': getDataHistoByRegime('intensity'),  'dataErrorLeft': '', 
		'titleRight': _(u'Appréciations selon la consommation d aliments'),    'orderedNameRight': _(u'Appréciations (-50~50)'),   'categoriesRight' : cat2,  'dataRight': getDataHistoByRegime('feeling'),  'dataErrorRight': ''})

	return listHisto


def createListPie():
	listPie = []
	# Repartition by sex
	listPie.append({'title': _(u'Repartition selon le sexe'), 'button': _(u'Sexe des donneurs'), 'description': _(u'Pourcentage'), 'data': pieByCritereSex()})
	# Repartition between slice of Age
	listPie.append({'title': _(u'Repartition selon la tranche d âge'), 'button': _(u'Tranche d âge'), 'description': _(u'Pourcentage'), 'data': pieByCritereSliceOfAge()})
	# Repartition by smoker
	listPie.append({'title': _(u'Répartition par consommation de cigarettes'), 'button': _(u'Consommation de cigarettes'), 'description': _(u'Pourcentage'), 'data': pieByCritereSmoker()})
	return listPie


def createListLines():
	listLines = []
	# Pleasanteness in function of intensity
	listLines.append({'title': _(u"Apréciation en fonction de l intensité"), 'button': _(u'Apréciation par l intensité'), 'abscisseName': _(u'Intensités (0~100)'), 'orderedName': _(u'Apréciation'), 'nameLine1': _(u'Données brutes'), 'dataLine1': "[]", 'nameLine2': _(u'Données centrées'), 'dataLine2': intensityByFeelingCenter(), 'subtitle': ''})
	return listLines
