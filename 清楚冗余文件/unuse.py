#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# 使用方法：python py文件 Xcode工程文件目录

__author__ = 'sxyang'

import sys
import os
import re
import stat

if len(sys.argv) == 1:
    print '请在.py文件后面输入工程路径' 
    sys.exit()

projectPath = sys.argv[1]
print '工程路径为%s' % projectPath

resourcefile = []
totalClass = set([])
totalXmlClass = set([])
totalJsonClass = set([])
totalPlistClass = set([])
unusedFile = []
pbxprojFile = []
xmlfile = []
plistfile = []
jsonfile = []

writeAllResourceFile = []
writeAllReferenceFile = set([])
writeunusedFIle = []
writeAllprojFile = []
writeAllxmlfile = []
writeAllplistfile = []
writeAlljsonfile = []
writeAllplistClass = []
writeAllJsonClass = []
writeAllXmlClass = []

def Getallfile(rootDir): #遍历目录下所有文件
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists) 
        if os.path.isdir(path): #递归
            Getallfile(path) 
        else:
            ex = os.path.splitext(path)[1]  #根据扩展名把resource和projectFlie分出来
            if ex == '.m' or ex == '.mm' or ex == '.h':
                resourcefile.append(path)
                writeAllResourceFile.append(path + '\n')
            elif ex == '.pbxproj':
                pbxprojFile.append(path)
                writeAllprojFile.append(path + '\n')
            elif ex == '.xml':
                xmlfile.append(path)
                writeAllxmlfile.append(path + '\n')
            elif ex == '.plist':
                plistfile.append(path)
                writeAllplistfile.append(path + '\n')
            elif ex == '.json':
                jsonfile.append(path)
                writeAlljsonfile.append(path + '\n')

Getallfile(projectPath)


#print '工程中所使用的类列表为：'
#for ff in resourcefile:
    #print ff

writeAllProjPath = '%s文件夹内所有的pbxproj文件.txt' % projectPath
f = open(writeAllProjPath,'w+')
f.writelines(writeAllprojFile)
f.close()

writeAllProjPath = '%s文件夹内所有的xml文件.txt' % projectPath
f = open(writeAllProjPath,'w+')
f.writelines(writeAllxmlfile)
f.close()

for x in xmlfile:
    with open(x,'r') as f:
        content = f.read()
        array = re.findall(r'Name\s*=\s*"([\w,\+]+)"\W',content)#正则表达式以h，m结尾，前面是字母的字符串
        see = set(array)#把list变成了set 
        totalXmlClass = totalXmlClass|see

print(totalXmlClass)

writeAllXmlClass = '%sXml中的class.txt' % projectPath
with open(writeAllXmlClass,'w+') as f:
    f.writelines(totalXmlClass)

writeAllProjPath = '%s文件夹内所有的plist文件.txt' % projectPath
f = open(writeAllProjPath,'w+')
f.writelines(writeAllplistfile)
f.close()

for x in plistfile:
    with open(x,'r') as f:
        content = f.read()
        array = re.findall(r'\>([\w,\+]+)\<',content)
        see = set(array)
        totalPlistClass = totalPlistClass|see

print(totalPlistClass)

writeAllPlistClass = '%sPlist中的class.txt' % projectPath
with open(writeAllPlistClass,'w+') as f:
    f.writelines(totalPlistClass)


writeAllProjPath = '%s文件夹内所有的json文件.txt' % projectPath
f = open(writeAllProjPath,'w+')
f.writelines(writeAlljsonfile)
f.close()

for x in jsonfile:
    with open(x,'r') as f:
        content = f.read()
        array = re.findall(r'commandStr":"([\w,\+]+)",',content)#正则表达式以h，m结尾，前面是字母的字符串
        see = set(array)#把list变成了set 
        totalJsonClass = totalJsonClass|see

print(totalJsonClass)

writeAllJsonClass = '%sJson中的class.txt' % projectPath
with open(writeAllJsonClass,'w+') as f:
    f.writelines(totalJsonClass)

#raw_input()

writeAllResourcePath = '%s文件夹内的所有.m.h.mm文件.txt' % projectPath
f = open(writeAllResourcePath,'w+')
f.writelines(writeAllResourceFile)
f.close()

for e in pbxprojFile:
    f = open(e, 'r')
    content = f.read()
    array = re.findall(r'\s+([\w,\+]+\.[h,m]{1,2})\s+',content)#正则表达式以h，m结尾，前面是字母的字符串
    #print array
    see = set(array)#把list变成了set 
    totalClass = totalClass|see
    writeAllReferenceFile = writeAllReferenceFile|see
    f.close()

print '工程中所引用的.h与.m及.mm文件'
#for x in totalClass:
 #   print x
#print '--------------------------'

writeAllReferencePath = '%s根据proj文件所得被引用的所有.m.h.mm文件.txt' % projectPath
f = open(writeAllReferencePath,'w+')
for x in writeAllReferenceFile:
    f.writelines(x+'\n')
f.close()

for x in resourcefile:
    #ex = os.path.splitext(x)[1]
    #if ex == '.h': #.h头文件可以不用检查
        #continue
    fileName = os.path.split(x)[1]
    if fileName not in totalClass:
        unusedFile.append(x)

for x in unusedFile:
    resourcefile.remove(x)

allinfile = []#resourcesfile对应的全部文件名
for x in resourcefile:
    fileName = os.path.split(x)[1]
    allinfile.append(fileName)
otherfile = []#引用的外部文件
for x in totalClass:
    if x not in allinfile:
        otherfile.append(x)

writeOtherFilePath = '%s引用的外部文件.txt' % projectPath
f = open(writeOtherFilePath,'w+')
for x in otherfile:
    s = '%s\n' % x 
    f.writelines(s)
f.close()


print '未引用到工程的文件列表为：'

writeNoReferencePath = '%s未引用到工程的.m.mm.h文件.txt' % projectPath
writeFile = []
f = open(writeNoReferencePath,'w+')
for unImport in unusedFile:
    ss = '%s\n' % unImport
    f.writelines(ss)
    #print unImport
f.close()

unusedFile = []

allClassDic = {}

writeallClass = []

writeRePath = '%s引用的所有文件.txt' % projectPath
ff = open(writeRePath,'w+')

for x in resourcefile:#去掉了未引用的.m.mm.h文件之后，文件夹内的文件
    f = open(x,'r')
    y = x + '\n'
    ff.writelines(y)
    content = f.read()
    array = re.findall(r'@interface\s+([\w,\+]+)\s+:',content)#类名
    for xx in array:
        allClassDic[xx] = x#文件中所有interface的类的路径，value为path，key为类名
    f.close()
ff.close()

print '所有类及其路径：'
writeallClassPath = '%s所有类及其路径.txt' % projectPath
f = open(writeallClassPath,'w+')
for x in allClassDic.keys():
    line = x + ':' + allClassDic[x] + '\n'
    f.writelines(line)
    #print x,':',allClassDic[x]
f.close()

def checkClass(path,className):#在path的文件里面有classname
    f = open(path,'r')
    content = f.read()
    #match = re.search(r'(#define|\:|\[)\s*)(%s)(\s+|\<|\*)' % className,content)#继承
    #if not match:
    #match = re.search(r'@"(%s)"' % className,content)#动态调用

    if os.path.splitext(path)[1] == '.h':
        match = re.search(r'((#define|\:|\[)\s*(%s)(\s+|\<|\*))' % className, content)#继承
        #match = re.search(r':(\s+(%s)\s+)' % className,content)#继承
        if not match:
           match = re.search(r'(%s)\s*\*' % className,content)#建指针
    else:
        match = re.search(r'(%s)\s+\w+' % className,content)#建对象
        if not match:
            match = re.search(r'@"(%s)"' % className,content)#动态调用
            if not match:
                match = re.search(r'(%s)\s*\*' % className,content)#建指针

    f.close()
    if match:
        return True

ivanyuan = 0
totalIvanyuan = len(allClassDic.keys())
usedFile = []

for key in allClassDic.keys():#类名
    path = allClassDic[key]#path
    
    index = resourcefile.index(path)#path的index
    count = len(resourcefile)
    
    used = False
    
    offset = 1
    ivanyuan += 1
    print '完成',ivanyuan,'共:',totalIvanyuan,'path:%s'%path
    
    
    while index+offset < count or index-offset > 0:
        if index+offset < count:
            subPath = resourcefile[index+offset]
            if checkClass(subPath,key):
                used = True
                break
        if index - offset > 0:
            subPath = resourcefile[index-offset]
            if checkClass(subPath,key):
                used = True
                break
        offset += 1

    if key in totalJsonClass|totalXmlClass|totalPlistClass:
        used = True

    if used:
        str = '以使用的类：%s 文件路径：%s\n' %(key,path)
        usedFile.append(str)

    if not used:#引用了但是没有在别的文件中check到的文件
        str = '未使用的类：%s 文件路径：%s\n' %(key,path)
        unusedFile.append(str)
        writeFile.append(str)

for p in unusedFile:
    print '未使用的类：%s' % p

filePath = os.path.split(projectPath)[0]
writePath = '%s未使用的类.txt' % projectPath
writeUsePath = '%s已使用的类.txt' % projectPath
ff = open(writeUsePath,'w+')
ff.writelines(usedFile)
ff.close()
f = open(writePath,'w+')
f.writelines(writeFile)
f.close()

def filiter(NouseDir,generFile):
    classname = []
    f = open(NouseDir,'r')
    g = open(generFile,'w+')
    while 1:
        string = f.readline()
        if '：' in string:
            line = string.split('：')[2]
            name = string.split('：')[1].split(' ')[0]
            classname.append(name)
            line2 = line[:-1]
            ff = open(line2,'r')
            comtent = ff.read()
            ff.close()
            array = re.findall(r'@interface\s+([\w,\+]+)\s+:',comtent)
            if set(classname) & set(array) == set(array):
                g.writelines(line2 + '\n')
        if not string:
            break
    f.close()
    g.close()

filiterPath = '%s未使用的文件.txt' % projectPath
filiter(writePath,filiterPath)

sortedPath = '%s已排序的文件.txt' % projectPath
Sorted = []

with open(filiterPath,'r') as f:
    lines = f.readlines()
    lines.sort()
    for line in lines:
        Sorted.append(line)

with open(sortedPath,'w+') as f:
    f.writelines(Sorted)

Filted = Sorted[:]
for x in Sorted:
    name = os.path.split(x)[1]
    ex = os.path.splitext(name)[1].strip()
    if ex == '.m' or ex == '.mm':
        Filted.remove(x)
    elif 'Command' in x:
        Filted.remove(x)
    elif 'Addin' in x:
        Filted.remove(x)

lastPath = '%s最后的文件.txt' % projectPath

with open(lastPath,'w+') as f:
    f.writelines(Filted)