# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Bisect plus",
    "author": "Francisco Javier Pérez Heredia",
    "version": (0.1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Bisect plus",
    "description": "Bisect plus object selection for the cutting plane",
    "warning": "",
    "wiki_url": "https://github.com/FranJPerez/TFG",
    "category": "All",
}

import bpy
import bmesh
import mathutils.geometry

from bpy.props import (
        PointerProperty,
        StringProperty,
        FloatProperty,
        BoolProperty,
        IntProperty,
        )

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        )

class bisectioner(Operator):
    bl_idname = 'mesh.bisectioner'
    bl_label = 'Bisectioner'
    bl_optons = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        #objs = context.selected_objects
        #return objs != [] and objs[0].type == "MESH"
        #obj = bpy.ops.mesh.primitive_cylinder_add(vertices=3, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        
        return obj
    
    def execute(self, context):
        #print("Hello World")
        
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.scene.objects["Camera"].select_set(True)  #Selecciono la camara
        bpy.ops.object.delete(use_global=False) #lo elimino
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.scene.objects["Light"].select_set(True)  #Selecciono la luz
        bpy.ops.object.delete(use_global=False) #lo elimino
        
        ob = bpy.context.scene.objects["Cube"]       # Get the object || Comentario de francisco para intentar en lugar de "Cube" quito las comillas y pongo 0 sin comillas[0]
        bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
        bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
        ob.select_set(True)                          # Select the cube

        #Guardar el tamaño del objeto en X, Y y Z, nos puede ser de utilidad mas tarde
        xSize =ob.dimensions.x
        ySize =ob.dimensions.y
        zSize =ob.dimensions.z
        
        
        
        
        
        
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 2))
        
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.view_layer.objects.active = bpy.context.scene.objects["Cube"]

        #bpy.context.space_data.context = 'MODIFIER' #Me voy a modificadores Esta instruccion parece que no me hace falta
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
          #ESTAS DOS INSTRUCCIONES ALOMEJOR TENGO QUE HACERLAS UNA VEZ YA SEAN OBJETOS
          bpy.ops.object.convert(target='GPENCIL')  #Convierto el objeto a grease pencil para exportarlo a svg para inkscape
          bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
          ######################################
          bpy.ops.mesh.select_all(action='SELECT')
        
        return {'FINISHED'}
        #return obj
        #return objs != [] and objs[0].type == "MESH"
  

#ui class
class OBJECTSELECTION_Panel(Panel):
    bl_idname = 'OBJECTSELECTION_Panel'
    bl_label = 'Bisect Plus'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bisectplus'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        
        box = column.box()
        
        cell_props = context.window_manager.objectselection_props
        
        obj = context.active_object
        cell_props.bisecttarget = obj.name
        box.label(text="Select the number of cuts:")
        box.prop(cell_props, "slices")
        
        box.label(text="Select material thickness:")
        box.prop(cell_props, "thickness")
        
        
        column.separator()
        column.operator("mesh.bisectioner", icon='NONE', text="Start bisectioner")
        

class ObjectSelectionProperties(PropertyGroup):

    thickness: FloatProperty(
            name="Material thickness",
            description="Select material thickness",
            default=1,
            min=1,
            max=50,
            precision=1,
            )
    #Aqui creo las propiedades para la caja que he creado en la interfaz slices.
    slices: IntProperty(
            name="Number of slices:",
            description="Selection of the number of slices on the vertical axis",
            default=1,
            min=1,
            max=50,
            )

            
classes = (
    ObjectSelectionProperties,
    #bisectplus,
    OBJECTSELECTION_Panel,
    bisectioner,
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.WindowManager.objectselection_props = PointerProperty(
        type=ObjectSelectionProperties
    )

def unregister():
    del bpy.types.WindowManager.objectselection_props

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__" :
    register()
