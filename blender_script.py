#Todas las lineas de codigo necesarias para realizar el script completo para el modulo de blender

#El primer paso metemos el objeto que deseamos biseccionar
Falta el codigo



#Crearemos un cilindro en el centro con 3 vertices
bpy.ops.mesh.primitive_cylinder_add(vertices=3, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

#Escalaremos el cilindro una tamaño suficientemente grande (p.e. 50m) 
bpy.ops.transform.resize(value=(1, 1, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


#Ahora volvemos a seleccionar el objeto principal
ob = bpy.context.scene.objects["Cube"]       # Get the object
bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
ob.select_set(True)                          # Select the cube

#Guardar el tamaño del objeto en X, Y y Z, nos puede ser de utilidad mas tarde
xSize =ob.dimensions.x
ySize =ob.dimensions.y
zSize =ob.dimensions.z


#PAra aplicar el modificador booleano que crea el agujero dentro de la pieza, con el objeto que quiero agujerear ya seleccionado y el cilindro en pantalla
bpy.context.space_data.context = 'MODIFIER' #Me voy a modificadores Esta instruccion parece que no me hace falta
bpy.ops.object.modifier_add(type='BOOLEAN') #Elijo el modificador boolean
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cylinder"] #Selecciono el objeto que lo modifica que es el cilindro
bpy.ops.object.modifier_apply(modifier="Boolean") #Aplico el modificador
#Selecciono el cilindro y lo elimino
bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
bpy.context.scene.objects["Cylinder"].select_set(True)  #Selecciono el cilindro
bpy.ops.object.delete(use_global=False) #lo elimino


#hacer un bisect del objeto
bpy.ops.object.editmode_toggle()#Paso al modo edicion
bpy.ops.mesh.select_all(action='SELECT') #Selecciono todo
numero_pieza = 0
for j in range(20):
  bpy.ops.mesh.bisect(plane_co=(0, 0,(10-j)/10), plane_no=(0,0,1))
  bpy.ops.mesh.select_all(action='SELECT')
#Una vez cortado los trozos vamos al modo objeto
bpy.ops.object.objectmode_toggle()




#PAra organizar los cortes en un tablon cada vez que haga uno de ellos
#Una vez guardado el tamaño de x e y los comparo y me quedo con el mas grande

#Ahora creo un tablero multiplicando el numero de cortes por x o y 
