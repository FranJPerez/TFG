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
    "name": "LOT 9000 (Laminador de Objetos Tridimensionales 9000",
    "author": "Francisco Javier Pérez Heredia",
    "version": (0.1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > LOT 9000",
    "description": "Laminate a 3D object according to certain parameters",
    "warning": "",
    "wiki_url": "https://github.com/FranJPerez/TFG",
    "category": "All",
}

import bpy
import bmesh
import mathutils.geometry
import math


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

class borrarElementos(Operator):
    bl_idname = 'mesh.borrar'
    bl_label = 'borro'
    bl_optons = {"REGISTER", "UNDO"}
    #Primero elimino todos los objetos de la escena y solo dejo el objeto que voy a laminar
    bpy.ops.object.select_all(action='SELECT') #Deselecciono todo
    bpy.ops.object.delete(use_global=False)
    
    def borro():
        bpy.ops.object.select_all(action='SELECT') #Deselecciono todo
        bpy.ops.object.delete(use_global=False)
        return {'FINISHED'}
    
    
    #len(bpy.data.objects) == 0 

class escaladoMetrico(Operator):
    bl_idname = 'mesh.escaladoMetrico'
    bl_label = 'escaladoMetrico'
    bl_optons = {"REGISTER", "UNDO"}
    
    def pasarMilimetros(valor):
        resultado = valor / 1000
        return resultado
    
    def pasarCentimetros(valor):
        resultado = valor / 100
        return resultado
   
    
class ejes(Operator):
    bl_idname = 'mesh.ejes'
    bl_label = 'ejes'
    bl_optons = {"REGISTER", "UNDO"}
    
    #Eje silple formado por un cubo aplanado hasta el grosor de la lamina y altura indicada por el propio objeto + grosor de la lamina para entrar dentro de una base 
    def crearEjePlano(alturaObjReal, anchura, grosorLamina):
        alturaEje = alturaObjReal 
        eje = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        
        bpy.ops.transform.resize(value=(grosorLamina, anchura, alturaEje), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return eje
    
    def crearEje3Vertices(altura):
        eje = bpy.ops.mesh.primitive_cylinder_add(vertices=3, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(15, 0.15, altura))
        return eje
    
    #def crearEjePiramide(altura)
    
class base(Operator):
    bl_idname = 'mesh.base'
    bl_label = 'base'
    bl_optons = {"REGISTER", "UNDO"}
    
    def crearBaseSimple(largoX, anchoY, grosorZ):
        base = bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.resize(value=(largoX, anchoY, grosorZ), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return base
    
class plantilla(Operator):
    bl_idname = 'mesh.plantilla'
    bl_label = 'plantilla'
    bl_optons = {"REGISTER", "UNDO"}
    
    def crearPlantilla(largo, ancho):
        plantilla=bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        #dimensionX=plantilla.dimensions.x
        bpy.ops.transform.resize(value=(largo,  ancho, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return base
    
class bisectioner(Operator):
    bl_idname = 'mesh.bisectioner'
    bl_label = 'Bisectioner'
    bl_optons = {"REGISTER", "UNDO"}
    
    @classmethod
    
    #poll me hace que tenga que tener un objeto activo
    def poll(cls, context):
        objs = context.selected_objects
        return objs != [] and objs[0].type == "MESH"
    
    def execute(self, context):
        objectselection_props = context.window_manager.objectselection_props
        
        #Primero elimino todos los objetos de la escena y solo dejo el objeto que voy a laminar
        
        bpy.data.objects[0].name='objeto' #Renombro el objeto que voy a laminar
        
        #bpy.data.objects[0].location=(0, 0, 0) #llevo el objeto al centro del mundo mundial
        
        ob = bpy.context.scene.objects[0]       # Get the object || Comentario de francisco para intentar en lugar de "Cube" quito las comillas y pongo 0 sin comillas[0]
        bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
        bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
        ob.select_set(True)                          # Select the cube
        
        
        #Hago el calculo segun los valores de entrada en la interfaz para el numero de cortes y el posterior reparto en la lamina de corte
        #Guardar el tamaño del objeto en X, Y y Z, nos puede ser de utilidad mas tarde ya que son los tamaños iniciales, no reales
        xInicial =ob.dimensions.x 
        yInicial =ob.dimensions.y
        zInicial =ob.dimensions.z
        
        grosorInicial = (objectselection_props.thickness) / 10
        grosor = grosorInicial
        
        numeroCortes = int(objectselection_props.objectHigh/grosorInicial)
        altura = objectselection_props.objectHigh
        #Calculo las dimensiones reales.
        xReal = ((objectselection_props.objectHigh/zInicial) * xInicial)/100
        yReal = ((objectselection_props.objectHigh/zInicial) * yInicial)/100
        zReal = objectselection_props.objectHigh / 100
        
        longitudMateriaReal = objectselection_props.lengthSheet /100
        anchuraMaterialReal = objectselection_props.widthSheet / 100
        
        
        
        #Calculamos si dicho objeto con los cortes calculados cabera en la lamina.
        #Primero calculamos el espacio en el eje x, que seria el largo de la lamina.
        if longitudMateriaReal/xReal < 1:
            print("La lamina es demasiado corta o el objeto demasiado grande")
            return {'FINISHED'}
        else:
            #numeroCortes/cortesX)*yReal >= widthSheet
            objHorizontalesIniciales= int(longitudMateriaReal/xReal)
            
            print("OBJVerticales sin math.ceil")
            print(numeroCortes/objHorizontalesIniciales)
            
            objVerticalesIniciales = math.ceil(numeroCortes/objHorizontalesIniciales)
            if (objVerticalesIniciales * yReal) > anchuraMaterialReal:
                print("La lamina es demasiado estrecha o el objeto demasiado grande")
                return {'FINISHED'}
            
            else:
                #El numero de columnas sera objHorizontales
                objHorizontales = int(longitudMateriaReal/xReal)
                #El numero de filas sera objVerticales
                objVerticales = math.ceil(numeroCortes/objHorizontales)
                
        
        #Creo un cubo con una altura zReal + grosor, largo(x) por defecto de 3 mm y una anchura del grosor y un pelín mas que sera el eje mas tarde pero ahora sera el hueco en el objeto
   #     ejes.crearEjePlano(zInicial, 0.05, grosor)
    #    
    #    bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
    #    bpy.context.view_layer.objects.active = bpy.context.scene.objects[0]
    #    bpy.ops.object.modifier_add(type='BOOLEAN') #Elijo el modificador boolean
    #    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cube"] #Selecciono el objeto que lo modifica que es el cilindro
    #    bpy.ops.object.modifier_apply(modifier="Boolean") #Aplico el modificador
        #Selecciono el cilindro y lo elimino
    #    bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
    #    bpy.context.scene.objects["Cube"].select_set(True)  #Selecciono el cilindro
    #    bpy.ops.object.delete(use_global=False) #lo elimino
    #    bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
    #    bpy.context.scene.objects["objeto"].select_set(True) 
        
        
        escaladoX = (xReal)*100/ xInicial
        escaladoY = (yReal)*100/ yInicial
        escaladoZ = zReal*100 /zInicial
        bpy.ops.transform.resize(value=(escaladoX, escaladoY, escaladoZ), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        #Subo la figura por encima de 0 en el eje z, tengo que arreglar el 2.5
        bpy.ops.transform.translate(value=(0, 0, 2.5), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        
        xFinal =ob.dimensions.x 
        yFinal =ob.dimensions.y
        zFinal =ob.dimensions.z
        print("xFinal y xReal?")
        print(xFinal)
        print(xReal)
        
        #Creo la baje y el eje y los renombro
        ejes.crearEjePlano(zFinal/2, 0.5, grosor/2)
        bpy.ops.transform.translate(value=(0, 0, 2.5), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.data.objects['Cube'].name='Eje'
        base.crearBaseSimple(xFinal/2,yFinal/2, grosor)
        bpy.data.objects['Cube'].name='Base'
        
        #Aplico el modificador boleano al objeto y la base con el eje
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.view_layer.objects.active = bpy.context.scene.objects['objeto'] 
        bpy.ops.object.modifier_add(type='BOOLEAN') #Elijo el modificador boolean
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Eje"] #Selecciono el objeto que lo modifica que es el cilindro
        bpy.ops.object.modifier_apply(modifier="Boolean") #Aplico el modificador
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.scene.objects["objeto"].select_set(True) 
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.view_layer.objects.active = bpy.context.scene.objects['Base']
        bpy.ops.object.modifier_add(type='BOOLEAN') #Elijo el modificador boolean
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Eje"] #Selecciono el objeto que lo modifica que es el cilindro
        bpy.ops.object.modifier_apply(modifier="Boolean") #Aplico el modificador
        #bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        #bpy.context.scene.objects["objeto"].select_set(True) 
        
        #Muevo el eje y la base donde no me estorben
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.scene.objects["Eje"].select_set(True)
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        movimientoEjeY = bpy.context.scene.objects['Eje'].dimensions.y/2
        movimientoEjeX = bpy.context.scene.objects['Eje'].dimensions.z/2
        bpy.ops.transform.translate(value=(-movimientoEjeX, movimientoEjeY, -altura), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.scene.objects["Base"].select_set(True)
        movimientoBaseY = bpy.context.scene.objects['Base'].dimensions.y/2 + movimientoEjeY*2
        movimientoBaseX = bpy.context.scene.objects['Base'].dimensions.x/2
        bpy.ops.transform.translate(value=(-movimientoBaseX, movimientoBaseY, -altura), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        
        #Selecciono el objeto
        bpy.ops.object.select_all(action='DESELECT') #Deselecciono todo
        bpy.context.scene.objects["objeto"].select_set(True) 
        
        
        #Hacer un bisect del objeto
        bpy.ops.object.editmode_toggle()#Paso al modo edicion
        bpy.ops.mesh.select_all(action='SELECT') #Selecciono todo
        i=0.000
        primerCorte = altura - grosorInicial / 10
        print("escalado, grosor y primer corte")
        print(escaladoZ, grosorInicial, primerCorte)
        
        #j=2
        for j in range(numeroCortes):
          numero_pieza = bpy.ops.mesh.bisect(plane_co=(0, 0, primerCorte-i), plane_no=(0,0,1))
          bpy.ops.mesh.separate(type = 'SELECTED') #Separo el objeto que acabo de biseccionar y creo un nuevo objeto xxx.XXX
          bpy.ops.mesh.select_all(action='SELECT')
          i += (grosor) #ahora estaria en mm reales
          
        
        bpy.ops.object.editmode_toggle()#Paso al modo edicion
        
        #elimino el objeto principal
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects["objeto"].select_set(True)  #Selecciono la luz
        bpy.ops.object.delete(use_global=False) #lo elimino
        
        
        #j=2
        ultimaPosX=0
        ultimaPosY=0
        for j in range(2, numeroCortes+2):
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects[j].select_set(True)  #Selecciono la primera lamina
            bpy.context.view_layer.objects.active = bpy.context.scene.objects[j]
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')  #Hago el centro de la lamina para moverlo
            bpy.ops.transform.translate(value=(xFinal/2, yFinal/2, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            
            j += 1
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        
        n=0
        j=0
        i=1
        x = numeroCortes * -1
        
        for i in range(objVerticalesIniciales):
            for x in range(objHorizontalesIniciales):
                if n != numeroCortes:
                    j -= 1
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.scene.objects[j].select_set(True)  #Selecciono la primera lamina
                    bpy.context.view_layer.objects.active = bpy.context.scene.objects[j]
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')  #Hago el centro de la lamina para moverlo
                    if j != -1:
                        bpy.ops.transform.translate(value=((xFinal)*(i), (xFinal)*(x), 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        
                    #bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                    n += 1
                    x += 1
                    
                
            i += 1
        #Por ultimo convierto todo a GPencil
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.convert(target='GPENCIL')

        return {'FINISHED'}
  

#ui class
class OBJECTSELECTION_Panel(Panel):
    bl_idname = 'OBJECTSELECTION_Panel'
    bl_label = 'LOT 9000'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LOT 9000'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        
        box = column.box()
        
        cell_props = context.window_manager.objectselection_props
        
        obj = context.active_object
        cell_props.bisecttarget = obj.name
        #box.label(text="Selecciona el numero de cortes:")
        #box.prop(cell_props, "slices")
        
        box.label(text="Altura del objeto:")
        box.prop(cell_props, "objectHigh")
        
        box.label(text="Grosor de la lamina:")
        box.prop(cell_props, "thickness")
        
        box.label(text="Largo de la lamina:")
        box.prop(cell_props, "lengthSheet")
        
        box.label(text="Ancho de la lamina:")
        box.prop(cell_props, "widthSheet")
        
        
        column.separator()
        column.operator("mesh.bisectioner", icon='NONE', text="Start LOT 9000")
        
        #column.separator()
        #column.operator("mesh.borrar", icon='NONE', text="Borrar elementos")
        
    @classmethod
    def poll(cls, context):
        #using selected_objects to only show the ui if the object is a mesh
        #and the operation can be done on it
        objs = context.selected_objects
        return objs != [] and objs[0].type == "MESH"
        

class ObjectSelectionProperties(PropertyGroup):

    thickness: IntProperty(
            name="Grosor lamina",
            description="Grosor de la lamina en mm",
            default=2,
            min=1,
            max=50,
            )
    #Aqui creo las propiedades para la caja que he creado en la interfaz slices.
    slices: IntProperty(
            name="Number of slices:",
            description="Selection of the number of slices on the vertical axis",
            default=1,
            min=1,
            max=50,
            )
            
    objectHigh: FloatProperty(
            name = "Altura del objeto",
            description="Altura real que tendra el objeto en cm",
            default=5,
            min=5,
            max=20,
            precision=2,
            )
            
    lengthSheet: IntProperty(
            name = "Largo de lamina",
            description="Largo de la lamina donde imprimir el objeto en cm",
            default=100,
            min=10,
            max=200,
            )
            
    widthSheet: IntProperty(
            name = "Ancho de lamina",
            description="Anchura de la lamina donde imprimir el objeto en cm",
            default=100,
            min=10,
            max=200,
            )
    
    
#Encapsulado de metodos

#class methodGroup(methods):
    
            
classes = (
    ejes,
    base,
    plantilla,
    borrarElementos,
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
