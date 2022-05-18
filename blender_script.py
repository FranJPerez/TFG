#Todas las lineas de codigo necesarias para realizar el script completo para el modulo de blender

#Selecciono y elimino tanto la camara como la iluminacion
bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
bpy.context.scene.objects["Camera"].select_set(True)  #Selecciono la camara
bpy.ops.object.delete(use_global=False) #lo elimino
bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
bpy.context.scene.objects["Light"].select_set(True)  #Selecciono la luz
bpy.ops.object.delete(use_global=False) #lo elimino
#En lugar de hacerlo 1 a 1 lo selecciono todo y lo elimino todo
bpy.ops.object.select_all(action='SELECT') 
bpy.ops.object.delete(use_global=False) 


#El primer paso metemos el objeto que deseamos biseccionar(ESTO IRA COMO BOTON EN LA UI) Para probar puedo meter un cubo para hacer los cortes
Falta el codigo



#Crearemos un cilindro en el centro con 3 vertices
bpy.ops.mesh.primitive_cylinder_add(vertices=3, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

#Escalaremos el cilindro una tamaño suficientemente grande (p.e. 50m) 
bpy.ops.transform.resize(value=(1, 1, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
#Cambiar la scala en y para hacer isosceles el cilindro

#Ahora volvemos a seleccionar el objeto principal
ob = bpy.context.scene.objects["Cube"]       # Get the object || Comentario de francisco para intentar en lugar de "Cube" quito las comillas y pongo 0 sin comillas[0]
bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
ob.select_set(True)                          # Select the cube

#Guardar el tamaño del objeto en X, Y y Z, nos puede ser de utilidad mas tarde
xSize =ob.dimensions.x
ySize =ob.dimensions.y
zSize =ob.dimensions.z

###########################################
# Intentar meter desde la linea 20 a la 25 debajo de las dimensiones para hacer el cilindro con la altura justa.
##########################################

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
for j in range(20):
  numero_pieza = bpy.ops.mesh.bisect(plane_co=(0, 0,(10-j)/10), plane_no=(0,0,1))
  bpy.ops.mesh.separate(type = 'SELECTED') #Separo el objeto que acabo de biseccionar y creo un nuevo objeto xxx.XXX
  bpy.ops.mesh.select_all(action='SELECT')
  
#Una vez cortado los trozos vamos al modo objeto
bpy.ops.object.editmode_toggle() #Si, es el mismo comando para ir al modo objeto y al modo edicion
numero_pieza = 1 #Creo un contadorpara las piezas 

for j in range(20)
  bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
  bpy.context.scene.objects["Cube.*"].select_set(True)  #Selecciono el corte
  bpy.context.scene.objects["Cube"].location = (20, 20, 10) #Para mover los objetos, este funciona, esta probado
  numero_pieza =+1





#PAra organizar los cortes en un tablon cada vez que haga uno de ellos
#Una vez guardado el tamaño de x e y los comparo y me quedo con el mas grande

#Ahora creo un tablero multiplicando el numero de cortes por x o y 
