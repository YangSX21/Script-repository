#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# 第一个参数是文件夹内所有的pbxproj文件地址，第二个参数是dev需要删除的文件，第三个参数是pbxproj文件备份地方，第四个参数是需要注释的文件
# 用python ，python3提示解码错误

__author__ = 'sxyang'

import sys
import os
import re
import stat
import shutil

phxfiles = sys.argv[1]
patternfile = sys.argv[2]
saveDir = sys.argv[3]
WillComFile = sys.argv[4]

AllFilePath = [] 
patterns = []
phxPath = []

with open(WillComFile,'r') as f:
	content = f.readlines()
	for line in content:
		path = line.strip()
		AllFilePath.append(path) #读取全部需要注释的文件地址


with open(patternfile,'r') as f:
	content = f.readlines()
	for x in content:
		filename = os.path.split(x)[1].strip()
		classname = os.path.splitext(filename)[0]
		patterns.append(classname) #读取全部需要注释和删除的类名

#print(patterns)
flag = True

with open(phxfiles,'r') as f:
	content = f.readlines()
	for x in content:
		path = x.strip()
		phxPath.append(path) #读取全部需要处理的phx文件

#print(phxPath)

index = 0
total = len(phxPath)
lines = []
for x in phxPath:#按照pbx文件进行查找删除，同时备份在指定目录
	index += 1
	print'共有',total,'个，正在处理第',index,'个pbx。'
	with open(x,'r') as f:
		lines = f.readlines()
		shutil.copy(x,saveDir)#把pbx文件进行复制
		Dirname = os.path.split(x)[0]#取文件的上一级名称进行重命名
		Dirname2 = os.path.split(Dirname)[1]
		os.rename(saveDir+'/project.pbxproj',saveDir+'/'+os.path.splitext(Dirname2)[0]+'.pbxproject') 
	with open(x ,'w+') as g:
		for line in lines:
			for pattern in patterns:#按照引用文件进行查找
				match = re.search(r'\s+(%s)\.' % pattern, line)#匹配以空格开头以.结尾的行
				if match:
					flag = False
			if flag:
				g.writelines(line)
			flag = True

index = 0
total = len(patterns)
for pattern in patterns:#按照所有引用的文件进行进行查找注释
	index += 1
	print'共有',total,'个，正在处理第',index,'个引用文件。'
	for WillComFile in AllFilePath:
		if pattern in WillComFile:
			pass
		else:
			with open(WillComFile,'r') as f:
				lines = f.readlines()
			with open(WillComFile,'w') as g:
				for line in lines:
					match = re.search(r'(\"|\/)(%s)\.h' % pattern,line)#匹配以“或者\开头，以.h结尾的行
					if match:
						g.writelines('//'+line)#把相应行注释
					else:
						g.writelines(line)


