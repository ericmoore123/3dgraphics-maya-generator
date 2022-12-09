import maya.cmds as cmds
import maya.mel as mel
import random as rand
import os
cmds.file(new=True,force=True)

#This is a class that creates a simple user interface (UI)
class villageUI():
    global GUI_Path
    GUI_Path = ""
    def __init__(self, windowName="forrestWindow"):
        #Attributes of the class
        self.winTitle = "Make a forrest window"
        self.MoutainGroup = None
        #This is the name of the window
        self.windowName = windowName
        self.create() #create the window

    #This function will create the window
    def create(self):
        #Test to see if the window exists
        if cmds.window(self.windowName, exists=True):
            #delete the window
            	cmds.deleteUI(self.windowName)
        #create a new window
        cmds.window(self.windowName, title=self.winTitle)
        #make a layout
        self.mainCol = cmds.columnLayout( adjustableColumn=True)
        #make a button
        cmds.button(label="Make a Forest",bgc=(0.134,0.607,0.619))
        cmds.text(label="-----Choose Models Folder------")
        cmds.rowColumnLayout(numberOfColumns=2,adj=True)
        self.modelTextField=cmds.textField("textDir")
        self.modelOpenButton=cmds.button("Open",w=40,c=self.getPathByDialog)
        cmds.setParent( '..' )
        cmds.text(align="center",label="Land")
        self.rowLayout = cmds.rowColumnLayout(numberOfColumns=2)
        #row 1
        cmds.text(align="left",label="Land",w=100)
        self.landSlide = cmds.intSliderGrp(field=True,v=1,min=1,max=2,dc=self.createLandSample1)
        cmds.setParent( '..' )
        #TextScrollList
        cmds.text(align="center",label="Choose Plant Model Type")
        self.typeTextScrollList= cmds.textScrollList(numberOfRows=4,
        append=['SmallTree','NormalTree','BigTree','Grass'],selectItem='SmallTree')
        #Distance Horizontal
        self.rowLayout = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(align="left",label="Distance Horizontal",w=100)
        self.distanceHorizontalSlide = cmds.intSliderGrp(field=True,v=1,min=1,max=10)
        #Distance Vertical
        cmds.text(align="left",label="Distance Vertical",w=100)
        self.distanceVerticalSlide = cmds.intSliderGrp(field=True,v=1,min=1,max=10)
        cmds.setParent( '..' )
        #row 2
        cmds.text(align="center",label="Generate Tree Order")
        self.rowLayout = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(align="left",label="Grow Vertical",w=100)
        self.riceXSlide = cmds.intSliderGrp(field=True,v=1,min=1,max=13, dc=self.createRice)
        cmds.text(align="left",label="Grow Horizontal",w=100)
        self.riceYSlide = cmds.intSliderGrp(field=True,v=1,min=1,max=13, dc=self.createRice)
        cmds.setParent( '..' )
        #row 3
        cmds.text(align="center",label="Generate Tree Random")
        self.rowLayout = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(align="left",label="Grow Random Vertical",w=100)
        self.treeXSlide = cmds.intSliderGrp(field=True,v=1,min=1,max=10,dc=self.createTree)
        cmds.text(align="left",label="Grow Random Horizontal",w=100)
        self.treeYSlide = cmds.intSliderGrp(field=True,v=1,min=1,max=10,dc=self.createTree)
        cmds.setParent( '..' )
        self.changeRiceColor = cmds.button(label="Remove Shaders",bgc=(0.834,0.704,0.032),c=self.changeColorRice)
        #show the window
        cmds.showWindow( self.windowName )

    #Create Tree
    def createTree(self,args=None):
        GUI_Path =cmds.textField(self.modelTextField,q=True,text=True)
        if GUI_Path == '':
            GUI_Path = "D:/forestTool"
        model_type =cmds.textScrollList(self.typeTextScrollList,q=True,si=True)[0]
        print model_type
        hDis =  cmds.intSliderGrp(self.distanceHorizontalSlide,query=True,value=True)
        vDis =  cmds.intSliderGrp(self.distanceVerticalSlide,query=True,value=True)
        if cmds.objExists("Random"+model_type.split("Tree")[0])==True:
            cmds.delete("Random"+model_type.split("Tree")[0])
        Sample = cmds.file(GUI_Path + "/"+model_type+".ma", i=True, options="mo=1;lo=1", pr=True,f=True)
        cmds.select(Sample)
        cmds.group( em=True, n="Random"+model_type.split("Tree")[0])
        cmds.parent("|"+model_type+"Sample","Random"+model_type.split("Tree")[0])
        xDup =  cmds.intSliderGrp(self.treeXSlide,query=True,value=True)
        yDup =  cmds.intSliderGrp(self.treeYSlide,query=True,value=True)
        for i in range(xDup):
            for j in range(yDup):
                if (i%2) == 0 and (j%2) == 0:
                    dupRice = cmds.Duplicate("Random"+model_type.split("Tree")[0])
                    cmds.xform(piv = (0,-0.5,0))
                    cmds.move((10*rand.random())+i*hDis,0,(10*rand.random())+j*vDis)

    #Create Land
    def createLandSample1(self,args=None):
        sliderInt = cmds.intSliderGrp(self.landSlide,query=True,value=True)
        if cmds.objExists('Land')==True:
            cmds.delete("Land")
            cmds.delete("myLandShader")
        name1 = "LandSample1"
        self.createSurface(name1,sliderInt)
        cmds.move(0,0.5,0)
        cmds.group( em=True, n='Land' )
        cmds.parent("LandSample1","Land")
        myLandShader = cmds.shadingNode('blinn', asShader=True,name="myLandShader")
        cmds.setAttr("myLandShader.color", 0.0616, 0.3581, 0.021, type="double3")
        cmds.select("Land")
        cmds.hyperShade( assign=myLandShader )
            

    #Get the path to model
    def getPathByTextField(self,args=None):
        textFieldDir = cmds.textField(self.modelTextField,q=True,text=True)
        
    def getPathByDialog(self,args=None):
        global GUI_Path
        dialogDir = cmds.fileDialog2(fileMode=2, dialogStyle=2,returnFilter=True)
        print dialogDir[0]
        cmds.textField(self.modelTextField,edit=True,text=dialogDir[0])
        GUI_Path = dialogDir[0]
    
    #Create Plant Model
    def createRice(self,args=None):
        GUI_Path =cmds.textField(self.modelTextField,q=True,text=True)
        if GUI_Path == '':
            GUI_Path = "D:/forestTool"
        model_type =cmds.textScrollList(self.typeTextScrollList,q=True,si=True)[0]
        print model_type
        hDis =  cmds.intSliderGrp(self.distanceHorizontalSlide,query=True,value=True)
        vDis =  cmds.intSliderGrp(self.distanceVerticalSlide,query=True,value=True)
        if cmds.objExists(model_type.split("Tree")[0])==True:
            cmds.delete(model_type.split("Tree")[0])
        TreeSample = cmds.file(GUI_Path + "/"+model_type+".ma", i=True, options="mo=1;lo=1", pr=True,f=True)
        cmds.select(TreeSample)
        cmds.group( em=True, n=model_type.split("Tree")[0] )
        cmds.parent("|"+model_type+"Sample",model_type.split("Tree")[0])
        xDup =  cmds.intSliderGrp(self.riceXSlide,query=True,value=True)
        yDup =  cmds.intSliderGrp(self.riceYSlide,query=True,value=True)
        for i in range(xDup):
            for j in range(yDup):
                if (i%2) == 0 and (j%2) == 0:
                    dupRice = cmds.Duplicate(model_type+"Sample")
                    cmds.xform(piv = (0,-0.5,0))
                    cmds.move(i*hDis,0,j*vDis)

    #Make Element Field Change Color
    def changeColorRice(self,args=None):
        blinnShader = cmds.shadingNode('blinn', asShader=True,name="myLandShader")
        meshes=cmds.ls(type="mesh")
        cmds.select(meshes)
        cmds.hyperShade( assign=blinnShader )

    #Create surface for the land
    def createSurface(self,name,input):
        landsub = 100 #number of subdivisions on the plane
        maxheight = 15
        land = cmds.polyPlane(name = name, sx=100, sy=100, w=100, h=100)
        vtxnb = cmds.polyEvaluate(v=True)
        vtxCount = range(vtxnb)

        values = []
        if input == 2:
            high_values = [rand.triangular(0,0.01,0) for i in xrange(vtxnb/10)]
            low_values = [rand.uniform(0,0.01) for i in xrange(vtxnb/2)]
        else:
            high_values = [rand.triangular(0,0.06,0) for i in xrange(vtxnb/2)]
            low_values = [rand.uniform(0,0.01) for i in xrange(vtxnb/2)]
        values = low_values + high_values
        values_count = len(values)
        SEED = 448
        rand.seed(SEED)
        rand.shuffle(vtxCount)
        rand.shuffle(values)
        optimize_setter = []

        for x in vtxCount:
            mod = x % values_count
            # cmds.move(values[mod-1] * maxheight, land[0] + '.vtx[' + str(x) + ']',y=True, absolute=True)
            optimize_setter += [float(0),values[mod-1]*maxheight,float(0)]
        cmds.setAttr(name+'.vtx[:]', *optimize_setter)

inst = villageUI()
