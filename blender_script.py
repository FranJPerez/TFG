#Todas las lineas de codigo necesarias para realizar el script completo para el modulo de blender

#El primer paso metemos el objeto que deseamos biseccionar

#Crearemos un cilindro en el centro
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

#Escalaremos el cilindro una tamaño suficientemente grande (p.e. 50m) 
bpy.ops.transform.resize(value=(1, 1, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

#Ahora haremos que el cilindro solo tenga 3 vertices 
bpy.ops.mesh.primitive_cylinder_add(vertices=3, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

#Ahora volvemos a seleccionar el objeto principal
ob = bpy.context.scene.objects["Cube"]       # Get the object
bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
ob.select_set(True)                          # Select the cube
