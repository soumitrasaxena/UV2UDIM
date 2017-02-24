#UV 2 UDIMs
import maya.cmds as cmds
import sys
import functools

def uv2udim(meshes, u_min, v_min):
    
    uv = []
    u = u_min
    v = v_min
        
    for i, mesh in enumerate(meshes):
        
        #Starting u from 1 for v = 0
        u = (u_min + i) % 10        
        
        if u == 0:
            v = v+1
        
        udim_number = 1000 + (u+1) + (v*10) #Calculating the UDIM number
        
        cmds.select(mesh, r=True)
        cmds.select(cmds.polyListComponentConversion(tuv=True))
        selectedUVs = cmds.polyEditUV(query=True)
        cmds.polyEditUV( uValue=u, vValue=v )
        
        #Create and update UDIM attributes on every mesh
        addCustomUDIMMeshAttributes(mesh)
        setCustomAttributes(mesh, 'udim', udim_number)
        
    uv.append(u)
    uv.append(v)
    return uv
    
def addCustomUDIMGroupAttributes(groupName):
    #Adding custom UDIM attributes to group
    #cmds.select(groupName)
    try:
        if not cmds.objExists('%s.UDIM' % groupName):
            cmds.addAttr(groupName, shortName='udim', longName='UDIM', at='bool', keyable=True)
		
        if not cmds.objExists('%s.mesh_count' % groupName):    
            cmds.addAttr(groupName, shortName='count', longName='mesh_count', defaultValue=1.0, at='short', keyable=True)
        
        if not cmds.objExists('%s.u_max' % groupName):
            cmds.addAttr(groupName, shortName='umax', longName='u_max', defaultValue=1.0, at='short', keyable=True)
        
        if not cmds.objExists('%s.v_max' % groupName):
            cmds.addAttr(groupName, shortName='vmax', longName='v_max', defaultValue=0.0, at='short', keyable=True)
        
        if not cmds.objExists('%s.mesh_list' % groupName):
            cmds.addAttr(groupName, shortName='meshes', longName='mesh_list', dt='stringArray')          
                
    except:
        print "It seems that you've already run the script on this group. Do you want to update UDIMs instead ?"
        sys.exit()
        
def addCustomUDIMMeshAttributes(mesh_name):
    #Adding custom UDIM attribute to meshes in a group
    if not cmds.objExists('%s.udim' % mesh_name):
        cmds.addAttr(mesh_name, shortName='udim', longName='udim', at='short', defaultValue= 1002, keyable=True)
        
def setMeshList(groupName, mesh_list):
    #Appending the mesh list attribute of the group
    try:
        if cmds.objExists('%s.mesh_list' % groupName):
            cmds.setAttr('%s.mesh_list' % groupName, type='stringArray',*([len(mesh_list)] + mesh_list))        
    except:
        print "It seems that you've already run the script on this group. Do you want to update UDIMs instead ?"
        sys.exit()        
    
    print "Group : %s contains the following meshes : %s" % (groupName, mesh_list)
  
def setCustomAttributes(groupName, attribute, value):
    cmds.setAttr('%s.%s' % (groupName, attribute), value)  

def updateUDIMS(groupName):
    
    #Checking if it's already UDIMfied
    if cmds.objExists('%s.UDIM' % groupName):
        if cmds.getAttr('%s.UDIM' % groupName):
            #Get the list of meshes in the group's mesh_list variable
            old_mesh_list = cmds.getAttr('%s.mesh_list' % groupName)
            old_mesh_count = cmds.getAttr('%s.mesh_count' % groupName)
    
            #Get the list of meshes in the group currently   
            new_mesh_list = cmds.listRelatives(groupName, children=True, f=True) #WIP Check if there are valid meshes inside               
    
            new_mesh_count = len(new_mesh_list)
    
            if new_mesh_count == old_mesh_count:
                print "It seems that there are no new UDIMs to update"
                sys.exit()
        
            setCustomAttributes(groupName, 'mesh_count', new_mesh_count )
    
            #Setting mesh_list = list of meshes
            setMeshList(groupName, new_mesh_list)
        
            #Get the names of new meshes
            temp_set = set(old_mesh_list)
            new_meshes = [x for x in new_mesh_list if x not in temp_set]
            print 'New meshes added to the group are : %s ' % new_meshes
    
            #Using U_max and V_max, figure out the value of the next U and V
            u_max = cmds.getAttr('%s.u_max' % groupName)
            v_max = cmds.getAttr('%s.v_max' % groupName) 
    
            uv = []    
            u = u_max + 1;
            v = v_max;
    
            uv = uv2udim(new_meshes, u, v)      
        
            #Update relevant variables on the group
            setCustomAttributes(groupName, 'u_max',int(uv[0]))
            setCustomAttributes(groupName, 'v_max',int(uv[1]))
        else:
            print "The group's UDIM variable is OFF. Please contact TD"
            sys.exit()
    else:
        print "It seems that you've not UDIMfied the group. Please create UDIMs"
        sys.exit()
		

def convertToUDIM(groupName):            
    
    meshes = cmds.listRelatives(groupName, children=True, f=True) #WIP Check if there are valid meshes inside

    #Checking if we've already UDIMfied this group
    if cmds.objExists('%s.UDIM' % groupName):
        if cmds.getAttr('%s.UDIM' % groupName):
            print "Already UDIMfied . Do you want to update UDIMs instead ?"
	    sys.exit()  
			
    #Adding custom attributes
    addCustomUDIMGroupAttributes(groupName)
    
    mesh_count = len(meshes)
    
    setCustomAttributes(groupName, 'mesh_count', mesh_count )
    
    #Setting mesh_list = list of meshes
    setMeshList(groupName, meshes)
    
    uv = []
    u_min = 1 #Starting from u=1
    v = 0 #Default V for UDIMS (bottom row)
    
    uv = uv2udim(meshes, u_min, v)
            
    setCustomAttributes(groupName, 'u_max',int(uv[0]))
    setCustomAttributes(groupName, 'v_max',int(uv[1])) 
    setCustomAttributes(groupName, 'UDIM', True)        
              
