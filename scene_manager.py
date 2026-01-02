import bpy
import math
import importlib
import variations 
import materials
import generation_config

importlib.reload(variations)
importlib.reload(materials)
importlib.reload(generation_config)
from variations import VariationEngine
from materials import MaterialAssigner
from generation_config import GenerationConfig, SeasonalVariation


class SceneManager:
    def __init__(self):
        self.collection_name = "Procedural_Forest_Project"
        self.collection = None
        self.var_engine = VariationEngine()
        self.material_engine = MaterialAssigner() 
        
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

    def reset_scene(self):
        """Cleans previous project data and resets timeline."""
        if self.collection_name in bpy.data.collections:
            coll = bpy.data.collections[self.collection_name]
            for obj in coll.objects:
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(coll)

        self.collection = bpy.data.collections.new(self.collection_name)
        bpy.context.scene.collection.children.link(self.collection)
        
        # Mandatory timeline setup 
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 120

    def generate_tree(self, ground):
        """Procedurally creates tree geometry."""
        # Create Cylinder for Trunk and Cone for Leaves
        bpy.ops.mesh.primitive_cylinder_add(vertices=12)
        trunk = bpy.context.active_object
        bpy.ops.mesh.primitive_cone_add(vertices=12)
        leaves = bpy.context.active_object
        
        for part in [trunk, leaves]:
            for c in part.users_collection:
                c.objects.unlink(part)
            self.collection.objects.link(part)
            
        self.var_engine.apply_random_transform(trunk, leaves)
        self.var_engine.apply_materials(trunk, leaves, ground)
        self.animate_growth(trunk, leaves)

    def generate_rock(self):
        """Creates procedural rocks using UV spheres with deformation."""
        import random
        
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=8,
            ring_count=6,
            radius=random.uniform(0.5, 1.5),
            location=(
                random.uniform(-15, 15),
                random.uniform(-15, 15),
                random.uniform(0.3, 0.8)
            )
        )
        rock = bpy.context.active_object
        rock.name = f"Rock_{random.randint(100, 999)}"
        
        # Link to collection
        for c in rock.users_collection:
            c.objects.unlink(rock)
        self.collection.objects.link(rock)
        
        # Deform to look like rock (squashed, irregular)
        rock.scale = (
            random.uniform(0.8, 1.5),
            random.uniform(0.8, 1.5),
            random.uniform(0.4, 0.8)
        )
        rock.rotation_euler = (
            random.uniform(0, math.pi/4),
            random.uniform(0, math.pi/4),
            random.uniform(0, math.pi*2)
        )
        
        # Apply rock material
        self.material_engine.apply_rock_material(rock)
        
        # Animate: rock appears by scaling up
        rock.scale = (0, 0, 0)
        rock.keyframe_insert(data_path="scale", frame=1)
        final_scale = (
            random.uniform(0.8, 1.5),
            random.uniform(0.8, 1.5),
            random.uniform(0.4, 0.8)
        )
        rock.scale = final_scale
        rock.keyframe_insert(data_path="scale", frame=40)
        
        return rock

    def generate_bush(self):
        """Creates procedural bushes using ico spheres."""
        import random
        
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=2,
            radius=random.uniform(0.8, 1.5),
            location=(
                random.uniform(-12, 12),
                random.uniform(-12, 12),
                random.uniform(0.5, 1.0)
            )
        )
        bush = bpy.context.active_object
        bush.name = f"Bush_{random.randint(100, 999)}"
        
        # Link to collection
        for c in bush.users_collection:
            c.objects.unlink(bush)
        self.collection.objects.link(bush)
        
        # Make it bushy (wider than tall)
        bush.scale = (
            random.uniform(1.2, 2.0),
            random.uniform(1.2, 2.0),
            random.uniform(0.6, 1.0)
        )
        
        # Apply bush material
        self.material_engine.apply_bush_material(bush)
        
        # Animate: bush grows
        bush.scale = (0, 0, 0)
        bush.keyframe_insert(data_path="scale", frame=1)
        final_scale = (
            random.uniform(1.2, 2.0),
            random.uniform(1.2, 2.0),
            random.uniform(0.6, 1.0)
        )
        bush.scale = final_scale
        bush.keyframe_insert(data_path="scale", frame=50)
        
        return bush

    def generate_flower(self):
        """Creates simple flowers using small cones - NOW BIGGER!"""
        import random
        
        # Flower stem (thicker and taller cylinder)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6,
            radius=0.12,  
            depth=random.uniform(0.8, 1.2), 
            location=(
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(0.4, 0.6) 
            )
        )
        stem = bpy.context.active_object
        stem.name = f"Flower_Stem_{random.randint(100, 999)}"
        
        # Link to collection
        for c in stem.users_collection:
            c.objects.unlink(stem)
        self.collection.objects.link(stem)
        
        # Flower petals (MUCH BIGGER cone on top)
        stem_height = stem.dimensions.z
        bpy.ops.mesh.primitive_cone_add(
            vertices=5,
            radius1=random.uniform(0.4, 0.6),  # Increased from 0.15-0.25
            depth=0.5,  # Increased from 0.2
            location=(
                stem.location.x,
                stem.location.y,
                stem.location.z + stem_height/2 + 0.25
            )
        )
        petals = bpy.context.active_object
        petals.name = f"Flower_Petals_{random.randint(100, 999)}"
        petals.rotation_euler.z = random.uniform(0, math.pi*2)
        
        # Link to collection
        for c in petals.users_collection:
            c.objects.unlink(petals)
        self.collection.objects.link(petals)
        
        # Apply flower materials
        self.material_engine.apply_flower_materials(stem, petals)
        
        # Animate: flowers bloom
        for obj in [stem, petals]:
            obj.scale = (0, 0, 0)
            obj.keyframe_insert(data_path="scale", frame=1)
            obj.scale = (1, 1, 1)
            obj.keyframe_insert(data_path="scale", frame=70)
        
        return stem, petals

    def generate_mushroom(self):
        """Creates procedural mushrooms - NOW BIGGER!"""
        import random
        
        # Mushroom stalk (THICKER)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=random.uniform(0.2, 0.35),  # Increased from 0.08-0.15
            depth=random.uniform(0.7, 1.0),  # Increased from 0.3-0.5
            location=(
                random.uniform(-8, 8),
                random.uniform(-8, 8),
                random.uniform(0.35, 0.5)  # Raised up
            )
        )
        stalk = bpy.context.active_object
        stalk.name = f"Mushroom_Stalk_{random.randint(100, 999)}"
        
        # Link to collection
        for c in stalk.users_collection:
            c.objects.unlink(stalk)
        self.collection.objects.link(stalk)
        
        # Mushroom cap (BIGGER squashed sphere)
        stalk_height = stalk.dimensions.z
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12,
            ring_count=8,
            radius=random.uniform(0.5, 0.8),  # Increased from 0.2-0.4
            location=(
                stalk.location.x,
                stalk.location.y,
                stalk.location.z + stalk_height/2
            )
        )
        cap = bpy.context.active_object
        cap.name = f"Mushroom_Cap_{random.randint(100, 999)}"
        cap.scale.z = 0.5  # Flatten the cap
        
        # Link to collection
        for c in cap.users_collection:
            c.objects.unlink(cap)
        self.collection.objects.link(cap)
        
        # Apply mushroom materials
        self.material_engine.apply_mushroom_materials(stalk, cap)
        
        # Animate: mushrooms pop up
        for obj in [stalk, cap]:
            obj.scale = (0, 0, 0)
            obj.keyframe_insert(data_path="scale", frame=1)
            final_scale = obj.scale.copy()
            if obj == cap:
                final_scale.z = 0.5
            obj.scale = final_scale if obj == cap else (1, 1, 1)
            obj.keyframe_insert(data_path="scale", frame=80)
        
        return stalk, cap

    def animate_growth(self, trunk, leaves):
        """Fulfills mandatory keyframe animation requirement."""
        for obj in [trunk, leaves]:
            final_scale = obj.scale.copy()
            # Frame 1: Hidden (Size 0)
            obj.scale = (0, 0, 0)
            obj.keyframe_insert(data_path="scale", frame=1)
            # Frame 60: Full Size
            obj.scale = final_scale
            obj.keyframe_insert(data_path="scale", frame=60)

    def run(self):
        """
        Main execution pipeline - NOW WITH FULLY DYNAMIC GENERATION!
        Every run produces DIFFERENT numbers of objects!
        """
        self.reset_scene()
        
        # Complete environment setup
        bpy.ops.mesh.primitive_plane_add(size=40)
        ground = bpy.context.active_object
        for c in ground.users_collection:
            c.objects.unlink(ground)
        self.collection.objects.link(ground)
        
        bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
        

        
        #  Pure random 
        config = GenerationConfig.create_random_config()
        counts = config.get_all_counts()
        

        
        # Printing generation plan
        config.print_generation_plan(counts)
        
        # Generating objects with DYNAMIC counts!
        print(" Generating Trees...")
        for _ in range(counts["trees"]):
            self.generate_tree(ground)
        
        print(" Generating Rocks...")
        for _ in range(counts["rocks"]):
            self.generate_rock()
        
        print(" Generating Bushes...")
        for _ in range(counts["bushes"]):
            self.generate_bush()
        
        print(" Generating Flowers...")
        for _ in range(counts["flowers"]):
            self.generate_flower()

        print(" Generating Mushrooms...")
        for _ in range(counts["mushrooms"]):
            self.generate_mushroom()
        
        print(" Generating Sky Elements...")
        self.material_engine.generate_sky_elements(
            self.collection, 
            count_clouds=counts["clouds"], 
            count_birds=counts["birds"]
        )
        
        # Automatically move playhead to Frame 90 to see everything
        bpy.context.scene.frame_set(90)
        
        print("\n✅ PROCEDURAL FOREST GENERATION COMPLETE!")
        print(f" Total Objects Generated: {sum(counts.values())}")
        print(" Run again for a completely different forest!\n")