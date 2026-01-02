import bpy
import math
import importlib
import random
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
        bpy.context.scene.frame_end = 160

    def generate_tree(self, ground):
        """Procedurally creates tree geometry with RANDOM SHAPES!"""
        # Create Cylinder for Trunk
        bpy.ops.mesh.primitive_cylinder_add(vertices=15)
        trunk = bpy.context.active_object
        trunk.name = f"Tree_Trunk_{random.randint(100, 9999)}"
        
        # RANDOM TREE CROWN SHAPES!
        tree_type = random.choice(['cone', 'sphere', 'ico_sphere', 'round_cone'])
        
        if tree_type == 'cone':
            # Classic cone tree
            bpy.ops.mesh.primitive_cone_add(vertices=15)
            leaves = bpy.context.active_object
        elif tree_type == 'sphere':
            # Round bushy tree
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=15)
            leaves = bpy.context.active_object
        elif tree_type == 'ico_sphere':
            # Dense rounded tree
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2)
            leaves = bpy.context.active_object
        else:  # round_cone
            # Rounded cone hybrid
            bpy.ops.mesh.primitive_cone_add(vertices=20)
            leaves = bpy.context.active_object
            # Make it rounder at the top
            leaves.scale = (1.2, 1.2, 0.8)
        
        leaves.name = f"Tree_Leaves_{random.randint(100, 9999)}"
        
        for part in [trunk, leaves]:
            for c in part.users_collection:
                c.objects.unlink(part)
            self.collection.objects.link(part)
            
        self.var_engine.apply_random_transform(trunk, leaves, tree_type)
        self.var_engine.apply_materials(trunk, leaves, ground)
        
        # NEW: Enhanced growth and wind animations
        self.animate_tree_with_wind(trunk, leaves)
        
        return trunk, leaves

    def generate_rock(self):
        """Creates procedural rocks with subtle settling animation."""
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
        final_scale = (
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
        
        # # Animate: rock appears from underground (grows up)
        # start_z = rock.location.z
        # rock.location.z = -0.5  # Start underground
        # rock.scale = (0.1, 0.1, 0.1)
        # rock.keyframe_insert(data_path="location", frame=1)
        # rock.keyframe_insert(data_path="scale", frame=1)
        
        # # Pop up to surface
        # rock.location.z = start_z + 0.2  # Slight overshoot
        # rock.scale = final_scale
        # rock.keyframe_insert(data_path="location", frame=35)
        # rock.keyframe_insert(data_path="scale", frame=35)
        
        # # Settle down
        # rock.location.z = start_z
        # rock.keyframe_insert(data_path="location", frame=45)
        
        return rock

    def generate_bush(self):
        """Creates procedural bushes using ico spheres with wind animation."""
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
        final_scale = (
            random.uniform(1.2, 2.0),
            random.uniform(1.2, 2.0),
            random.uniform(0.6, 1.0)
        )
        
        # Apply bush material
        self.material_engine.apply_bush_material(bush)
        
        # Animate: bush grows
        bush.scale = (0, 0, 0)
        bush.keyframe_insert(data_path="scale", frame=1)
        bush.scale = final_scale
        bush.keyframe_insert(data_path="scale", frame=50)
        
        # Wind animation - bushes sway side to side
        base_rotation = bush.rotation_euler.copy()
        sway_angle = math.radians(random.uniform(8.0, 15.0))  # Bushes sway a lot
        wind_speed = random.uniform(1.0, 1.8)
        
        for frame in range(50, 121, 5):
            progress = (frame - 50) / 70
            wind_phase = progress * math.pi * 4 * wind_speed
            
            # Sway on both axes for natural movement
            bush.rotation_euler.y = base_rotation.y + math.sin(wind_phase) * sway_angle
            bush.rotation_euler.x = base_rotation.x + math.sin(wind_phase * 1.2) * sway_angle * 0.6
            bush.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        return bush

    def generate_flower(self):
        """Creates flowers with spinning petals and stem bending in wind."""
        # Flower stem (thicker and taller cylinder)
        stem_location = (
            random.uniform(-10, 10),
            random.uniform(-10, 10),
            random.uniform(0.4, 0.6) 
        )
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=15,
            radius=0.12,  
            depth=random.uniform(0.8, 1.2), 
            location=stem_location
        )
        stem = bpy.context.active_object
        stem.name = f"Flower_Stem_{random.randint(100, 999)}"
        
        # Link to collection
        for c in stem.users_collection:
            c.objects.unlink(stem)
        self.collection.objects.link(stem)
        
        # Flower petals (MUCH BIGGER cone on top)
        stem_height = stem.dimensions.z
        petal_location = (
            stem.location.x,
            stem.location.y,
            stem.location.z + stem_height/2 + 0.25
        )
        
        bpy.ops.mesh.primitive_cone_add(
            vertices=5,
            radius1=random.uniform(0.4, 0.6),
            depth=0.5,
            location=petal_location
        )
        petals = bpy.context.active_object
        petals.name = f"Flower_Petals_{random.randint(100, 999)}"
        
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
        
        # NEW: Stem bends in wind
        stem_base_rotation = stem.rotation_euler.copy()
        stem_sway = math.radians(random.uniform(5.0, 12.0))
        
        for frame in range(70, 121, 5):
            progress = (frame - 70) / 50
            wind_phase = progress * math.pi * 3
            
            stem.rotation_euler.y = stem_base_rotation.y + math.sin(wind_phase) * stem_sway
            stem.rotation_euler.x = stem_base_rotation.x + math.sin(wind_phase * 1.5) * stem_sway * 0.7
            stem.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        # NEW: Petals spin slowly in wind
        petal_base_rotation = random.uniform(0, math.pi * 2)
        petals.rotation_euler.z = petal_base_rotation
        petals.keyframe_insert(data_path="rotation_euler", frame=70)
        
        # Spin animation
        spin_choice = random.choice(['full_spin', 'wiggle'])
        
        if spin_choice == 'full_spin':
            # Full rotation
            petals.rotation_euler.z = petal_base_rotation + math.pi * 4  # 2 full rotations
            petals.keyframe_insert(data_path="rotation_euler", frame=120)
        else:
            # Wiggle back and forth
            for frame in range(70, 121, 5):
                progress = (frame - 70) / 50
                wiggle = math.sin(progress * math.pi * 6) * math.radians(30)
                petals.rotation_euler.z = petal_base_rotation + wiggle
                petals.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        # Generate butterfly near this flower (30% chance)
        if random.random() < 0.3:
            self.generate_butterfly_near_flower(stem.location)
        
        return stem, petals

    def generate_butterfly_near_flower(self, flower_position):
        """Creates animated butterfly near flower."""
        # Create butterfly body (small cylinder)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6,
            radius=0.08,
            depth=0.3,
            location=(
                flower_position.x + random.uniform(-0.5, 0.5),
                flower_position.y + random.uniform(-0.5, 0.5),
                flower_position.z + random.uniform(0.8, 1.5)
            )
        )
        body = bpy.context.active_object
        body.name = f"Butterfly_Body_{random.randint(100, 999)}"
        body.rotation_euler.x = math.pi / 2
        
        # Link to collection
        for c in body.users_collection:
            c.objects.unlink(body)
        self.collection.objects.link(body)
        
        # Create wings (two flat cubes)
        start_pos = body.location.copy()
        
        # Left wing
        bpy.ops.mesh.primitive_cube_add(
            size=0.4,
            location=(start_pos.x - 0.25, start_pos.y, start_pos.z)
        )
        left_wing = bpy.context.active_object
        left_wing.name = f"Butterfly_Wing_L_{random.randint(100, 999)}"
        left_wing.scale = (0.15, 1.2, 0.02)
        
        for c in left_wing.users_collection:
            c.objects.unlink(left_wing)
        self.collection.objects.link(left_wing)
        
        # Right wing
        bpy.ops.mesh.primitive_cube_add(
            size=0.4,
            location=(start_pos.x + 0.25, start_pos.y, start_pos.z)
        )
        right_wing = bpy.context.active_object
        right_wing.name = f"Butterfly_Wing_R_{random.randint(100, 999)}"
        right_wing.scale = (0.15, 1.2, 0.02)
        
        for c in right_wing.users_collection:
            c.objects.unlink(right_wing)
        self.collection.objects.link(right_wing)
        
        # Apply butterfly materials
        self.material_engine.apply_butterfly_materials(body, left_wing, right_wing)
        
        # Animate butterfly: flying in circles around flower
        butterfly_parts = [body, left_wing, right_wing]
        
        # Initial position
        for part in butterfly_parts:
            part.keyframe_insert(data_path="location", frame=1)
        
        # Create circular flight path
        radius = random.uniform(0.8, 1.5)
        center_x = flower_position.x
        center_y = flower_position.y
        height = start_pos.z
        
        for frame in range(20, 121, 20):
            angle = (frame / 120) * math.pi * 4  # Two full circles
            
            new_x = center_x + radius * math.cos(angle)
            new_y = center_y + radius * math.sin(angle)
            new_z = height + math.sin(frame / 10) * 0.3  # Bobbing motion
            
            for part in butterfly_parts:
                offset_x = part.location.x - body.location.x
                offset_z = part.location.z - body.location.z
                
                part.location = (new_x + offset_x, new_y, new_z + offset_z)
                part.keyframe_insert(data_path="location", frame=frame)
                
                # Rotate body to face direction of movement
                if part == body:
                    part.rotation_euler.z = angle + math.pi/2
                    part.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        # Wing flapping animation
        for wing in [left_wing, right_wing]:
            for frame in range(1, 121, 5):
                flap = math.sin(frame / 2) * 0.4
                if wing == left_wing:
                    wing.rotation_euler.y = flap
                else:
                    wing.rotation_euler.y = -flap
                wing.keyframe_insert(data_path="rotation_euler", frame=frame)

    def generate_mushroom(self):
        """Creates procedural mushrooms with wobble animation."""
        # Mushroom stalk (THICKER)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=5,
            radius=random.uniform(0.2, 0.35),
            depth=random.uniform(0.7, 1.0),
            location=(
                random.uniform(-8, 8),
                random.uniform(-8, 8),
                random.uniform(0.35, 0.5)
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
            ring_count=5,
            radius=random.uniform(0.5, 0.8),
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
        
        # NEW: Mushroom wobble animation (they're flexible!)
        stalk_base_rotation = stalk.rotation_euler.copy()
        wobble_angle = math.radians(random.uniform(3.0, 8.0))
        
        for frame in range(80, 121, 5):
            progress = (frame - 80) / 40
            wobble_phase = progress * math.pi * 5
            
            stalk.rotation_euler.y = stalk_base_rotation.y + math.sin(wobble_phase) * wobble_angle
            stalk.rotation_euler.x = stalk_base_rotation.x + math.sin(wobble_phase * 1.3) * wobble_angle * 0.8
            stalk.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            # Cap follows stalk movement
            cap.rotation_euler.y = stalk.rotation_euler.y * 0.8
            cap.rotation_euler.x = stalk.rotation_euler.x * 0.8
            cap.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        return stalk, cap

    def animate_tree_with_wind(self, trunk, leaves):
        """Enhanced tree animation: grows from roots + continuous wind sway."""
        # Store final scales
        trunk_final = trunk.scale.copy()
        leaves_final = leaves.scale.copy()
        
        # Growth from roots (bottom up)
        trunk.scale = (trunk_final.x, trunk_final.y, 0.001)  # Start flat
        trunk.keyframe_insert(data_path="scale", frame=1)
        trunk.scale = trunk_final
        trunk.keyframe_insert(data_path="scale", frame=50)
        
        leaves.scale = (0.001, 0.001, 0.001)  # Start invisible
        leaves.keyframe_insert(data_path="scale", frame=1)
        leaves.scale = leaves_final
        leaves.keyframe_insert(data_path="scale", frame=60)
        
        # Wind sway animation (continuous throughout)
        base_rotation_trunk = trunk.rotation_euler.copy()
        base_rotation_leaves = leaves.rotation_euler.copy()
        
        # Wind parameters - trees sway in Y and X axes
        trunk_sway_y = math.radians(random.uniform(1.5, 3.0))  # Trunk sways less
        trunk_sway_x = math.radians(random.uniform(0.5, 1.5))
        leaves_sway_y = math.radians(random.uniform(4.0, 8.0))  # Leaves sway more
        leaves_sway_x = math.radians(random.uniform(2.0, 5.0))
        
        wind_speed = random.uniform(0.8, 1.5)  # Random wind speed per tree
        
        for frame in range(60, 121, 5):
            progress = (frame - 60) / 60
            wind_phase = progress * math.pi * 4 * wind_speed
            
            # Trunk sway (gentle)
            trunk.rotation_euler.y = base_rotation_trunk.y + math.sin(wind_phase) * trunk_sway_y
            trunk.rotation_euler.x = base_rotation_trunk.x + math.sin(wind_phase * 1.3) * trunk_sway_x
            trunk.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            # Leaves sway (more dramatic)
            leaves.rotation_euler.y = base_rotation_leaves.y + math.sin(wind_phase) * leaves_sway_y
            leaves.rotation_euler.x = base_rotation_leaves.x + math.sin(wind_phase * 1.3) * leaves_sway_x
            leaves.keyframe_insert(data_path="rotation_euler", frame=frame)

    def setup_sun_light(self):
        """Creates animated sun with warm lighting."""
        # Create sun light
        bpy.ops.object.light_add(type='SUN', location=(15, -15, 25))
        sun = bpy.context.active_object
        sun.name = "Sun_Light"
        
        # Link to collection
        for c in sun.users_collection:
            c.objects.unlink(sun)
        self.collection.objects.link(sun)
        
        # Configure sun properties
        sun.data.energy = 3.5
        sun.data.color = (1.0, 0.95, 0.8)  # Warm sunlight
        sun.data.angle = 0.009  # Soft shadows
        
        # Animate sun movement (sunrise to sunset arc)
        # Starting position (sunrise)
        sun.location = (20, -20, 10)
        sun.rotation_euler = (math.radians(60), 0, math.radians(45))
        sun.keyframe_insert(data_path="location", frame=1)
        sun.keyframe_insert(data_path="rotation_euler", frame=1)
        
        # Noon position (overhead)
        sun.location = (5, 0, 30)
        sun.rotation_euler = (math.radians(30), 0, 0)
        sun.keyframe_insert(data_path="location", frame=60)
        sun.keyframe_insert(data_path="rotation_euler", frame=60)
        
        # Sunset position
        sun.location = (-20, 20, 10)
        sun.rotation_euler = (math.radians(60), 0, math.radians(-45))
        sun.keyframe_insert(data_path="location", frame=120)
        sun.keyframe_insert(data_path="rotation_euler", frame=120)
        
        # Animate sun intensity (brighter at noon)
        sun.data.energy = 2.0
        sun.data.keyframe_insert(data_path="energy", frame=1)
        sun.data.energy = 4.5
        sun.data.keyframe_insert(data_path="energy", frame=60)
        sun.data.energy = 2.0
        sun.data.keyframe_insert(data_path="energy", frame=120)
        
        print("☀️ Animated sun created!")
        return sun

    def run(self):
        """
        Main execution pipeline - NOW WITH FULLY DYNAMIC GENERATION!
        """
        self.reset_scene()
        
        # Complete environment setup
        bpy.ops.mesh.primitive_plane_add(size=40)
        ground = bpy.context.active_object
        for c in ground.users_collection:
            c.objects.unlink(ground)
        self.collection.objects.link(ground)
        
        # Setup animated sun instead of static light
        self.setup_sun_light()
        
        # Pure random generation config
        config = GenerationConfig.create_random_config()
        counts = config.get_all_counts()
        
        # Printing generation plan
        config.print_generation_plan(counts)
        
        # Generating objects with DYNAMIC counts!
        print("🌲 Generating Trees with RANDOM SHAPES...")
        for _ in range(counts["trees"]):
            self.generate_tree(ground)
        
        print("🪨 Generating Rocks...")
        for _ in range(counts["rocks"]):
            self.generate_rock()
        
        print("🌿 Generating Bushes...")
        for _ in range(counts["bushes"]):
            self.generate_bush()
        
        print("🌸 Generating Flowers with Butterflies...")
        for _ in range(counts["flowers"]):
            self.generate_flower()

        print("🍄 Generating Mushrooms...")
        for _ in range(counts["mushrooms"]):
            self.generate_mushroom()
        
        print("☁️ Generating Sky Elements...")
        self.material_engine.generate_sky_elements(
            self.collection, 
            count_clouds=counts["clouds"], 
            count_birds=counts["birds"]
        )
        
        # Automatically move playhead to Frame 90 to see everything
        bpy.context.scene.frame_set(90)
        
        print("\n✅ PROCEDURAL FOREST GENERATION COMPLETE!")
        print(f"📊 Total Objects Generated: {sum(counts.values())}")
        print("🌳 Trees grow from roots with continuous wind sway!")
        print("🌿 Bushes sway dramatically in the wind!")
        print("🌸 Flowers spin and bend - petals rotate with wind!")
        print("🍄 Mushrooms wobble like they're flexible!")
        print("🪨 Rocks emerge from underground!")
        print("☀️ Sun moves across the sky during animation!")
        print("🦋 Butterflies flutter around flowers!")
        print("🎬 Run again for a completely different forest!\n")