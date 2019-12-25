"""
/*******************************************************************************
 * @author  Joseph Kamel
 * @email   josephekamel@gmail.com
 * @date    28/11/2018
 * @version 2.0
 *
 * SCA (Secure Cooperative Autonomous systems)
 * Copyright (c) 2013, 2018 Institut de Recherche Technologique SystemX
 * All rights reserved.
 *******************************************************************************/
"""

import os
import json
import numpy as np
from numpy import array

class MlDataCollector:
	
	initCollection = False

	ValuesData = []
	TargetData = []

	valuesCollection = np.array([])
	targetCollection = np.array([])

	curDateStr = ''

	savePath = ''

	def setCurDateSrt(self, datastr):
		self.curDateStr = datastr

	def getValuesCollection(self):
		return self.valuesCollection

	def setSavePath(self, datastr):
		self.savePath = datastr

	def getTargetCollection(self):
		return self.targetCollection

	def saveData(self):
		print("initvalue")
		self.initValuesData(self.ValuesData)
		print("inittarget")
		self.initTargetData(self.TargetData)
		print("del")
		del self.ValuesData[:]
		del self.TargetData[:]
		print("4empat")
		self.ValuesData = []
		self.TargetData = []
		np.save('valuesSave12jam.npy', self.valuesCollection)
		np.save('targetSave12jam.npy', self.targetCollection)
		print("4empat")       
		os._exit(0)
	def loadData(self):
		self.valuesCollection = np.load('valuesSave24.npy' )
		self.targetCollection = np.load('targetSave24.npy')
		#print(self.valuesCollection[0:2])
		#print(self.targetCollection[0:2])
		self.initCollection = True	

	def collectData(self,bsmArray):
		self.ValuesData.append([array(bsmArray[0])])
		self.TargetData.append([array(bsmArray[1])])

	def initValuesData(self,New_Rows):
		if self.valuesCollection.shape[0] == 0:
			self.valuesCollection = np.concatenate([row for row in New_Rows])
		else:
			self.valuesCollection  = np.concatenate([self.valuesCollection, np.concatenate([row for row in New_Rows])])

	def initTargetData(self,New_Rows):
		if self.targetCollection.shape[0] == 0:
			self.targetCollection = np.concatenate([row for row in New_Rows])
		else:
			self.targetCollection  = np.concatenate([self.targetCollection, np.concatenate([row for row in New_Rows])])
		
