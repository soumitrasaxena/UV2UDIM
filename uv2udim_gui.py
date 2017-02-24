#uv 2 udim gui
#UV 2 UDIMs
import maya.cmds as cmds
import sys
import functools
import uv2udim

def createUI():
    
    windowID = 'myWindowID'

    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window(windowID, title='UV2UDIM GUI', width=400, height=200, sizeable=False )
    
    cmds.columnLayout("mainColumn", adjustableColumn=True) 
          
    cmds.button(label = 'Convert Selection to UDIM',command=functools.partial(convertToUDIMS))
    cmds.separator()
    cmds.button(label = 'Update UDIMs for Selection',command=functools.partial(updateUDIMScallback))
    cmds.separator() 

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
                
    cmds.button(label = 'Cancel',command=cancelCallback)
        
    cmds.showWindow()
        
def convertToUDIMS(*pArgs) :
    
    print "Convert Selection to UDIM"
    
    selectedGroups = []
    for groupName in cmds.ls(sl=1, transforms=1):
    	    selectedGroups.append(groupName) #WIP Check if the selection is actually a group
    		
    for groupName in selectedGroups:  
		uv2udim.convertToUDIM(groupName)          
        
def updateUDIMScallback(*pArgs) :
    
    print "Update UDIMS"
    
    selectedGroups = []
    for groupName in cmds.ls(sl=1, transforms=1):
    	    selectedGroups.append(groupName) #WIP Check if the selection is actually a group
    		
    for groupName in selectedGroups:
        uv2udim.updateUDIMS(groupName)
          
        
              
