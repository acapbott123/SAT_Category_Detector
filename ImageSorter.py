import os

def getJPG(listdr):
    for fileName in os.listdir(listdr):
        if fileName.endswith('.JPG'):
            jpeglist.append('data/obj/'+listdr+'/'+fileName)
            

#print(os.getcwd())
#print(os.listdir('Images'))
#print(os.listdir('Images/TB-10'))
jpeglist = []
for folderName in os.listdir('Images'):
    getJPG('Images/'+folderName, )




#print(jpeglist)
#print(len(jpeglist))
trainlist = int(.8*len(jpeglist))
trainList = jpeglist[0:trainlist]
testList = jpeglist[trainlist:]
s = "\n"
#print(len(trainList))
#print(len(testList))

testList = s.join(testList)
trainList = s.join(trainList)

ft = open("test.txt", "w")
ft.write(testList)
ft.close()


f = open("train.txt", "w")
f.write(trainList)
f.close()

