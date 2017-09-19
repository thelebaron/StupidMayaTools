"""
cmds.select(get_nodes_in_history_by_type('polyExtrudeFace'))
cmds.ls( selection=True, flatten=True )
cmds.select( clear=True )
cmds.ls( type='geometryShape', showType=True )


"""


import maya.cmds as cmds
import maya.mel as mel
import subprocess
import sys
import os

def start():
    #unused
    window = cmds.window( title="Long Name", iconName='Short Name', widthHeight=(200, 55) )
    cmds.columnLayout( adjustableColumn=True )
    cmds.button( label='Do Nothing' )
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    cmds.setParent( '..' )
    cmds.showWindow( window )


def get_nodes_in_history_by_type(typ):
    selection = cmds.ls(sl=True)
    nodes = []
    for obj in selection:
        for node in cmds.listHistory(obj):
            if cmds.nodeType(node) == typ:
                nodes.append(node)
    return nodes

def num(s):
    try:
        return float(s)
    except ValueError:
        return float(s)

def insetFunc(*args):
    origFaceSel = cmds.filterExpand( expand=True, sm=34 )
    origShape = cmds.listRelatives( origFaceSel , parent=True)
    origObj = cmds.listRelatives( origShape, parent=True)

    obj = cmds.ls( selection=True, flatten=True )

    translateAmount = 0.1
    textField_obj = cmds.textField( 'textField_action', query=True, text=True )

    if textField_obj and cmds.objExists( textField_obj ):
        translateAmount = num(textField_obj)

    cmds.polyExtrudeFacet( obj, offset=num(textField_obj), keepFacesTogether=True, localTranslateZ=0, localScale=(1, 1, 1),constructionHistory=True )

    history = get_nodes_in_history_by_type('polyExtrudeFace')
    cmds.select(get_nodes_in_history_by_type('polyExtrudeFace'))
    ############ setAttr "polyExtrudeFace1.offset" 0.25;
    #cmds.select('result')

    #cmds.displaySmoothness( polygonObject=3 )
    #cmds.select('result',deselect=True)


def uniteFunc(*args):
    origFaceSel = cmds.filterExpand( expand=True, sm=34 )
    origShape = cmds.listRelatives( origFaceSel , parent=True)
    origObj = cmds.listRelatives( origShape, parent=True)

    selection = cmds.ls( selection=True, flatten=True )
    for i in range(len(selection)):
           objectA = selection[0]
           objectB = selection[1]

    cmds.polyUnite( objectA, objectB, n='result' )
    cmds.xform('result', centerPivots=True)

    vertCount = cmds.polyEvaluate(v=True)
    cmds.select(cl=True)
    cmds.select('result'+'.vtx[0:'+str(vertCount)+']', add=True)
    cmds.polyMergeVertex(distance=0.15 )

    #invert selection
    #cmds.select('result'[0] + '.f[:]', toggle=True)
    cmds.select('result')

    cmds.displaySmoothness( polygonObject=3 )
    cmds.select('result',deselect=True)

def deleteUnusedTransforms(*args):
    transforms =  cmds.ls(type='transform')
    deleteList = []
    for tran in transforms:
        if cmds.nodeType(tran) == 'transform':
            children = cmds.listRelatives(tran, c=True)
            if children == None:
                print '%s, has no childred' %(tran)
                deleteList.append(tran)

    cmds.delete(deleteList)

def renameFunc(*args):
    targetObj = cmds.ls(sl = True)[len(cmds.ls(sl = True))-1]
    cmds.rename( targetObj, 'spinning_ball' )

def shellFunc(*args):
    origFaceSel = cmds.filterExpand( expand=True, sm=34 )
    origShape = cmds.listRelatives( origFaceSel , parent=True)
    origObj = cmds.listRelatives( origShape, parent=True)

    obj = cmds.ls( selection=True, flatten=True )

    translateAmount = 0.1

    textField_obj = cmds.textField( 'textField_action', query=True, text=True )
    if textField_obj and cmds.objExists( textField_obj ):
        translateAmount = textField_obj
    #else:
        #translateAmount = 0.1
		# Validate nodeType() is a joint
		#if cmds.nodeType( textField_obj ) == 'joint':
			#jointName = textField_obj

    cmds.polyExtrudeFacet( obj, keepFacesTogether=True, localTranslateZ=textField_obj, localScale=(1, 1, 1),constructionHistory=False )

def extractFunc(*args):
    origFaceSel = cmds.filterExpand( expand=True, sm=34 )
    origShape = cmds.listRelatives( origFaceSel , parent=True)
    origObj = cmds.listRelatives( origShape, parent=True)

    #invert selection
    cmds.select(origObj[0] + '.f[:]', toggle=True)
    #save selection
    unselectedFace = cmds.ls(sl=True)
    #invert selection again just for sake of preserving user selection
    cmds.select(origObj[0] + '.f[:]', toggle=True)
    #duplicate original
    dupeObject = cmds.duplicate(origObj, upstreamNodes=True)[0]
    #foreach face in all unselected, replace from original to duplicated
    for i in range(len(unselectedFace)):
           unselectedFace[i] = unselectedFace[i].replace(origObj[0],dupeObject)

    cmds.delete(unselectedFace)
    cmds.delete(origFaceSel)
    cmds.select(dupeObject)

def cloneFunc(*args):
    origFaceSel = cmds.filterExpand( expand=True, sm=34 )
    origShape = cmds.listRelatives( origFaceSel , parent=True)
    origObj = cmds.listRelatives( origShape, parent=True)

    #invert selection
    cmds.select(origObj[0] + '.f[:]', toggle=True)
    #save selection
    unselectedFace = cmds.ls(sl=True)
    #invert selection again just for sake of preserving user selection
    cmds.select(origObj[0] + '.f[:]', toggle=True)
    #duplicate original
    dupeObject = cmds.duplicate(origObj, upstreamNodes=True)[0]
    #foreach face in all unselected, replace from original to duplicated
    for i in range(len(unselectedFace)):
           unselectedFace[i] = unselectedFace[i].replace(origObj[0],dupeObject)

    cmds.delete(unselectedFace)
    #cmds.delete(origFaceSel)
    cmds.select(dupeObject)

def openAtom(*args):
    """Weird quirk but sys doesnt allow for user docs to be opened, as atom is installed to user dir.
     batch file opens atom and this script, plopped into firefox dir works"""

    print ("opening atom")
    #atomPath = "C:\Users\thele\AppData\Local\atom\app-1.19.3"
    #subprocess.call(['C:\Program Files (x86)\Mozilla Firefox\\firefox.exe', '-new-tab'])
    #subprocess.Popen(['C:\Program Files (x86)\Mozilla Firefox\\firefox.exe', '-new-tab'])
    #subprocess.Popen(['C:\Users\thele\Documents\maya\2017\scripts\tools\\mayapyscript.bat'])
    subprocess.Popen(['C:\Program Files (x86)\Mozilla Firefox\\mayapyscript.bat'])

def countSelection(*args):
    print (len(cmds.ls(sl=1)));

def centerToWorldButtonPush(*args):
    selection = cmds.ls(sl=1)
    print (selection);

    if not selection:
        print ("no objects to perform");
    else:
        #declare a var and get selected objects
        targetObj = cmds.ls(sl = True)[len(cmds.ls(sl = True))-1]
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        #make a temp sphere
        temp = cmds.sphere( n='TEMPORARY_DELETE_99' )
        #copy gizmo
        pivotTranslate = cmds.xform (temp, q = True, ws = True, rotatePivot = True)
        cmds.xform (targetObj, ws = True, pivots = pivotTranslate)
        #delete temp sphere
        cmds.delete( temp )
        #center the pivot to object xform bounding box
        cmds.xform(targetObj, centerPivots=True)
        #move translate to center
        cmds.xform(targetObj, ws = True, translation=(0,0,0))
        worldCoords = cmds.xform(targetObj,q=1,ws=1,rp=1)
        X = worldCoords[0]
        Y = worldCoords[1]
        Z = worldCoords[2]
        cmds.move( -X, -Y, -Z, targetObj, absolute=True )
        cmds.select(targetObj)

        print ("done");

def printValFunc(*args):
    print ("done");

def slider_drag_callback(*args):
    print 'Slider Dragged'

def value_change_callback(*args):
    print 'Value Changed'
    print ("done");





def windowArghFunc(*args):
    print("hello")
    cmds.shelfLayout( 'Argh', cellWidth=255,cellHeight=145 )
    #shelfLayout content below
    cmds.text( label='Argh Group goes here' )
    cmds.floatSliderGrp(label='Drag Callback', field=True, value=0, dc=slider_drag_callback)
    cmds.floatSliderGrp(label='Change Callback', field=True, value=0, cc=value_change_callback)

    cmds.setParent( '..' )
#main window
cmds.window(title="chris stupid tools",widthHeight=(650,75))
#shelf layout init
cmds.shelfTabLayout( 'mainShelfTab', image='smallTrash.png', imageVisible=True )
#first shelf tab
cmds.shelfLayout( 'StupidStuff',cellWidth=45,cellHeight=45 )
#shelfLayout content below
cmds.iconTextButton( label='clone',command=cloneFunc, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/clone32.png')
cmds.iconTextButton(label='extract',command=extractFunc, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/extract32.png')
cmds.iconTextButton( label='center', command=centerToWorldButtonPush, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/center32.png')
cmds.iconTextButton(label='count', command=countSelection, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/count32.png')
cmds.iconTextButton(label='atom', command=openAtom, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/atom32.png')
cmds.iconTextButton(label='rename', command=renameFunc, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/question32.png')
cmds.iconTextButton(label='shell', command=shellFunc, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/KoopaShell.png')
cmds.text( label='Amount' )
textField = cmds.textField( 'textField_action', insertText="0.1")
cmds.iconTextButton(label='unite', command=uniteFunc, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/question32.png')
cmds.iconTextButton(label='inset', command=insetFunc, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/parrot2.gif')

cmds.text( label='floatSlider' )
cmds.floatSlider(min=-1, max=5, value=0, step=0.1, cc=value_change_callback, dc=slider_drag_callback)


cmds.iconTextButton(label='printVal', command=printValFunc, style='iconAndTextVertical', image1='C:/Users/thele/Documents/maya/2017/scripts/tools/question32.png')

#cmds.text( label='floatfield' )
#textField = cmds.floatField( 'floatField_action', value=0.1)



cmds.setParent( '..' )


#why is this here?
windowArghFunc()


cmds.shelfLayout( 'More' , cellWidth=145,cellHeight=45 )

# ____[SHELF]____
cmds.text( label='More Group goes here' )


cmds.setParent( '..' )


def SelectCameraHead(*args):
    
    editor = 'renderView'
    print 'Selected Camera_Head.'
    cmds.select('Camera_Head')
    cmds.renderWindowEditor( editor, e=True, currentCamera='Camera_Head')

def SelectCamUpper(*args):
    
    editor = 'renderView'
    print 'Selected Camera_UpperBody.'
    cmds.select('Camera_UpperBody')
    cmds.renderWindowEditor( editor, e=True, currentCamera='Camera_UpperBody')

def SelectCamFull(*args):
    
    editor = 'renderView'
    print 'Selected Camera_FullBody.'
    cmds.select('Camera_FullBody')
    cmds.renderSettings(cam='Camera_FullBody')
    cmds.renderWindowEditor( editor, e=True, currentCamera='Camera_FullBody')

def SelectCamPersp(*args):
    print 'Selected persp Cam.'
    
    editor = 'renderView'
    cmds.select('persp')
    cmds.renderSettings(cam='persp')
    cmds.renderWindowEditor( editor, e=True, currentCamera='persp')
    
"""
    btPath = cmds.file (query=True, location=True)
    fileName = os.path.basename (btPath)
    cleanName = fileName.rsplit ('.mb')
    btInput = raw_input ('please insert path')
    print btInput
    cmds.setAttr ('defaultRenderGlobals.imageFormat', 8)
    editor = 'renderView'
    cmds.renderWindowEditor(editor, e=True, writeImage=btInput + cleanName[0] + '.jpg')
    cmds.setAttr ('defaultRenderGlobals.imageFormat', 51)


    import maya.cmds as cmds
    import maya.mel as mel
    import maya.app.general.createImageFormats as createImageFormats

    mel.eval('renderWindowRender redoPreviousRender renderView')
    editor = 'renderView'
    formatManager = createImageFormats.ImageFormats()
    formatManager.pushRenderGlobalsForDesc("JPEG")
    cmds.renderWindowEditor(editor, e=True, writeImage='C:/daten/testImage.jpg')
    formatManager.popRenderGlobals()"""

"""
setAttr "defaultResolution.width" 1280;
setAttr "defaultResolution.height" 720;
"""

# ____[SHELF]____
cmds.shelfLayout( 'renderStuff',cellWidth=145,cellHeight=45 )
cmds.button( label='Set CamHead', command=SelectCameraHead )
cmds.button( label='Set CamUpperBod', command=SelectCamUpper )
cmds.button( label='Set CamFullBod', command=SelectCamFull )
cmds.button( label='Set Persp', command=SelectCamPersp )
cmds.setParent( '..' )

def SelEdgeLoopDef(*args):
    print 'query hair func'

    selection = cmds.ls(sl=1)
    # First/Starting edge index 
    edgeStart = 0;

    # Get the number of edges from the node
    edgeCount = cmds.polyEvaluate( edge=True )
    print edgeCount

    if edgeCount > 0:
        #cmds.select( clear=True )
        selection = cmds.ls(sl=1)

            #maya wont select an edgeloop beyond a certain angle so this is useless
            #cmds.polySelect( selection, edgeLoop=1 )
            #cmds.polySelect( selection, edgeLoopPath=(1, edgeLoopLast) )

        edgeNumber = 1

        cmds.polySelect( selection, edgeLoop=edgeNumber, add=True)
        for edgeCount in range(0,edgeCount, 1):
            cmds.polySelect( selection, edgeLoop=edgeNumber, add=True)
            edgeNumber += 3
            #stupid maya doesnt register the above as a proper loop? not sure, but after the selection is made this works:
            #  ctrl click>shrink selection >shrink along loop. THEN converting to curve. BUT
            #   the script editor outputs it as polytraverse 6, when using 6 in the script it shrinks the selection(as expected)
            # when using 5, it works as intended(but not expected?) i dont understand pything/mel enough apparently
        
        
        # adds in unwanted faces?
        mel.eval('PolySelectTraverse(5)') 

        edgeDoNotWantNumber = 2

        #must be a more elegant way of doing this
        """for edgeCount in range(0,edgeCount, 1):
            cmds.polySelect( selection, edgeLoop=edgeDoNotWantNumber, deselect=True)
            edgeNumber += 3"""
        cmds.polySelect( selection, edgeLoop=edgeDoNotWantNumber, deselect=True)

        #output = mel.eval('polyToCurve')

        
        #cmds.group( em=True, name='xgenhairWorksCurveOutput' )
        #cmds.group( output, parent='xgenhairWorksCurveOutput' )
            # Clear the selection
        #cmds.select( clear=True )




def PolyToCurveDef(*args):
    print 'convert group of polymesh hair to curves'

    selection = cmds.ls(sl=1)

    origEdgeSel = cmds.filterExpand( expand=True, sm=32 ) #edges is 32, face 34, verts 31
    origShape = cmds.listRelatives( origEdgeSel , parent=True)
    origObj = cmds.listRelatives( origShape, parent=True)
    obj = cmds.ls( selection=True, flatten=True )

    groupSel = cmds.listRelatives( selection, children=True )
    print len(groupSel)

    for i in range(len(groupSel)):
        #cmds.select( clear=True )
        #target = cmds.ls(sl=1)[i]
        child = groupSel[i]
        cmds.select(child)

        
        # First/Starting edge index 
        edgeStart = 0; 

        # Get the number of edges from the node
        edgeCount = cmds.polyEvaluate( edge=True )
        print edgeCount

        if edgeCount > 0:
            #cmds.select( clear=True )
            selection = cmds.ls(sl=1)

            #maya wont select an edgeloop beyond a certain angle so this is useless
            #cmds.polySelect( selection, edgeLoop=1 )
            #cmds.polySelect( selection, edgeLoopPath=(1, edgeLoopLast) )

            edgeNumber = 1
            cmds.polySelect( selection, edgeLoop=edgeNumber, add=True)
            for edgeCount in range(0,edgeCount, 1):
                cmds.polySelect( selection, edgeLoop=edgeNumber, add=True)
                edgeNumber += 3
            #maya doesnt register the above as a proper loop? not sure, but after the selection is made this works:
            #  ctrl click>shrink selection >shrink along loop. THEN converting to curve. BUT
            #   the script editor outputs it as polytraverse 6, when using 6 in the script it shrinks the selection(as expected)
            # when using 5, it works as intended(but not expected?) i dont understand pything/mel enough apparently
            mel.eval('PolySelectTraverse(5)')
            edgeDoNotWantNumber = 2
            cmds.polySelect( selection, edgeLoop=edgeDoNotWantNumber, deselect=True)

            output = mel.eval('polyToCurve')

            
            #cmds.group( em=True, name='xgenhairWorksCurveOutput' )
            #cmds.group( output, parent='xgenhairWorksCurveOutput' )
            # Clear the selection
            cmds.select( clear=True )








#- get first edge from the array

#- convert it to an edge loop

#- get the loop edges

#- mesaure it

#- test the legth if it is greater than the last measured loop

#- if it's greater, store the edgeloop array and the length of this loop

#- remove the edge loop array from the alledgearray (you can do this by converting both array into a bitarray, than alledgearray - edgeloop)


# ____[SHELF]____
cmds.shelfLayout( 'hairCrap',cellWidth=145,cellHeight=45 )
cmds.button( label='polyToCurve', command=PolyToCurveDef )
cmds.button( label='selEdgeLoop', command=SelEdgeLoopDef )
cmds.setParent( '..' )


"""
doesnt work, in nodetype always goes to else but gives no error
allCams = cmds.listCameras()

for camera in allCams:
    if cmds.nodeType( 'camera', derived=True, isTypeName=True ) == 'persp':
        cmds.select('persp')
        print 'Button 1 was pushed.'
    else:
        print 'Button 2 was pushed.'
"""

# end
cmds.showWindow()



