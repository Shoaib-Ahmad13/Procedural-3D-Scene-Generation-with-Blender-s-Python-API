import bpy
import math

class SceneManager:
    def __init__(self):
        """
        Initialize the manager.
        We store the collection name in 'self' to avoid global variables. 
        """
        self.collection_name = "Procedural_City_Group_Project"
        self.collection = None
        
        # Ensure Blender is in Object Mode to prevent context errors
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

    def reset_scene(self):
        """
        Cleans up the previous run's data.
        Removes the specific project collection and objects inside it. 
        """
        # Check if our collection already exists
        if self.collection_name in bpy.data.collections:
            self.collection = bpy.data.collections[self.collection_name]
            
            # Loop through all objects in this collection and remove them
            for obj in self.collection.objects:
                bpy.data.objects.remove(obj, do_unlink=True)
            
            # Remove the collection itself
            bpy.data.collections.remove(self.collection)

        # Create a fresh, empty collection for this run
        self.collection = bpy.data.collections.new(self.collection_name)
        bpy.context.scene.collection.children.link(self.collection)
        
        # Reset the timeline to Frame 1
        bpy.context.scene.frame_set(1)
        
        # Set animation range (e.g., 250 frames) [cite: 10]
        bpy.context.scene.frame_end = 250
        
        print("Scene Reset Complete.")

    def setup_camera_and_light(self):
        """
        Sets up the environment so the scene is visible. 
        """
        # 1. Create a Sun Light
        light_data = bpy.data.lights.new(name="Sun", type='SUN')
        light_obj = bpy.data.objects.new(name="Sun", object_data=light_data)
        self.collection.objects.link(light_obj)
        light_obj.location = (0, 0, 20)
        light_obj.data.energy = 5.0

        # 2. Create a Camera
        cam_data = bpy.data.cameras.new(name="Main_Camera")
        cam_obj = bpy.data.objects.new(name="Main_Camera", object_data=cam_data)
        self.collection.objects.link(cam_obj)
        
        # Position Camera (x, y, z)
        cam_obj.location = (30, -30, 25)
        # Rotate Camera (Euler angles in radians)
        cam_obj.rotation_euler = (math.radians(55), 0, math.radians(45))
        
        # Set as active camera
        bpy.context.scene.camera = cam_obj

    def run(self):
        """
        The Main Pipeline. 
        Controls the order of execution. 
        """
        print("--- Starting Procedural Generation ---")
        
        # 1. Reset everything
        self.reset_scene()
        
        # 2. Setup the stage
        self.setup_camera_and_light()
        
        # 3. FUTURE STEPS (Placeholders for other roles)
        # self.generate_buildings()
        # self.animate_scene()
        
        print("--- Generation Finished ---")