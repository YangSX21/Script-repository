#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# 函数思路，如果在文件夹中只有一个png，则确定不能删除，如果有两个相同大小的png，能删掉其中的一个，有两个
# 不同大小的png，则无法进行进行确认是否删除，因为有2x，3x存在状况，有三个不同大小的png，删除最小的那个。

__author__ = 'sxyang'

import sys
import os
import re
import shutil

picDic = sys.argv[1]
resDoc = sys.argv[2]
#savedic = sys.argv[3]

willCleanPic = {} #可以进行筛选的，可能需要删除
dupPic = {} #确定需要删除的

def GetAllDic(rootDic):
	for lists in os.listdir(rootDic):
		path = os.path.join(rootDic, lists)
		if os.path.isdir(path):
			ex = os.path.splitext(path)[1]
			if ex == '.imageset': #最后一层dic
				count = 0
				sizeDic = {}
				for x in os.listdir(path):
					file = os.path.join(path, x)
					suf = os.path.splitext(file)[1]
					if suf == '.png':
						size = os.path.getsize(file) #获取png文件的size
						sizeDic[file] = size #形成dic，将文件地址作为key，size作为value
						count = count + 1
				if count < 2: #在文件夹中只有一个png或者只有pdf，不处理
					pass
				if count == 2: #文件中存在两个png
					for key in sizeDic.keys():
						if len(sizeDic) != len(set(sizeDic.values())):
							dupPic[key] = sizeDic[key] #在存在相同文件情况下，将其放入肯定需要删除dic
						elif sizeDic[key] == min(sizeDic.values()):
							willCleanPic[key] = sizeDic[key] #不然把较小的那个放入可能需要删除dic
							#print(key,sizeDic[key]) 
					#print(count)
					#print(sizeDic)
				if count == 3:
					for key in sizeDic.keys():
						if len(sizeDic) != len(set(sizeDic.values())):
							dupPic[key] = sizeDic[key] #在存在相同文件情况下，将其放入肯定需要删除dic
						elif sizeDic[key] == min(sizeDic.values()):
							dupPic[key] = sizeDic[key] #不然把较小的那个放入可能需要删除dic
				if count > 3: #一般不可能出现，出现就惊叹一下吧，
					print('wow')
					print(path)
			else :
				GetAllDic(path)

def SaveCleanedPic(saveDic,cleanedPic):
	for key in cleanedPic.keys():
		with open(cleanedPic[key],'r') as f:
			shutil.copy(cleanedPic[key],saveDic)
			os.remove(cleanedPic[key])


GetAllDic(picDic)

with open(resDoc,'w+') as f:
	for key in willCleanPic.keys():
		f.writelines(key + '\n')
#print('-------------checkPic----------')
#print(willCleanPic)
with open(resDoc,'a') as f:
	f.write('\n----------dupPic----------\n')
#print('-------------dupPic------------')
with open(resDoc,'a') as f:
	for key in dupPic.keys():
		f.writelines(key + '\n')
#print(dupPic)

#SaveCleanedPic(savedic,willCleanPic)