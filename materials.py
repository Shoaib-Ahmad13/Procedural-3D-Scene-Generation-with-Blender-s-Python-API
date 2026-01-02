import bpy
import random
import math

class MaterialAssigner:
    """
    ENHANCED: Now includes materials for rocks, bushes, flowers, mushrooms, AND BUTTERFLIES!
    Handles all procedural material creation and assignment.
    """
    
    def __init__(self):
        self.material_cache = {}
        
        # Existing color variants
        self.bark_color_variants = [
            (0.25, 0.15, 0.08), (0.15, 0.08, 0.03), (0.30, 0.20, 0.10),
            (0.12, 0.08, 0.05), (0.20, 0.12, 0.08),
        ]
        
        self.leaf_base_colors = [
            (0.03, 0.25, 0.03),  
            (0.04, 0.30, 0.04),
            (0.05, 0.35, 0.05),  
        ]
        
        self.ground_colors = [
            (0.15, 0.25, 0.10), (0.20, 0.30, 0.12), (0.12, 0.20, 0.08),
        ]
        
        # Rock color variants
        self.rock_colors = [
            (0.3, 0.3, 0.3),
            (0.2, 0.2, 0.2),
            (0.15, 0.15, 0.15),
            (0.25, 0.22, 0.18),
            (0.18, 0.18, 0.20),
        ]
        
        # Bush color variants
        self.bush_colors = [
            (0.08, 0.40, 0.08),
            (0.12, 0.50, 0.10),
            (0.15, 0.55, 0.12),
            (0.10, 0.45, 0.15),
        ]
        
        # Flower petal colors
        self.flower_colors = [
            (0.9, 0.2, 0.3),
            (0.95, 0.7, 0.2),
            (0.8, 0.3, 0.8),
            (1.0, 0.5, 0.0),
            (0.9, 0.1, 0.5),
            (1.0, 1.0, 0.9),
        ]
        
        # Mushroom colors
        self.mushroom_cap_colors = [
            (0.8, 0.2, 0.2),
            (0.9, 0.6, 0.3),
            (0.7, 0.5, 0.3),
            (0.95, 0.95, 0.9),
        ]
        
        # NEW: Butterfly wing colors
        self.butterfly_colors = [
            (0.95, 0.6, 0.1),   # Orange Monarch
            (0.2, 0.6, 0.95),   # Blue Morpho
            (0.95, 0.9, 0.3),   # Yellow Swallowtail
            (0.9, 0.3, 0.7),    # Pink
            (0.3, 0.8, 0.4),    # Green
            (0.95, 0.5, 0.2),   # Orange-Red
        ]
    
    def apply_smooth_shading(self, obj):
        """Removes harsh edges."""
        if obj and obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.shade_smooth()
            obj.select_set(False)
    
    # ============ EXISTING MATERIALS ============
    
    def create_bark_material(self, name_suffix=""):
        mat_name = f"Bark_Material_{name_suffix}_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.bark_color_variants)
        color_variation = random.uniform(-0.05, 0.08)
        final_color = (
            max(0, min(1, base_color[0] + color_variation)),
            max(0, min(1, base_color[1] + color_variation)),
            max(0, min(1, base_color[2] + color_variation)),
            1.0
        )
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = random.uniform(0.6, 0.95)
        bsdf_node.inputs['Specular IOR Level'].default_value = random.uniform(0.1, 0.4)
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_leaf_material(self, name_suffix=""):
        mat_name = f"Leaf_Material_{name_suffix}_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.leaf_base_colors)
        hue_shift = random.uniform(-0.08, 0.12)
        brightness_shift = random.uniform(-0.10, 0.15)
        final_color = (
            max(0, min(1, base_color[0] + hue_shift)),
            max(0, min(1, base_color[1] + brightness_shift)),
            max(0, min(1, base_color[2] + hue_shift)),
            1.0
        )
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = random.uniform(0.2, 0.7)
        bsdf_node.inputs['Subsurface Weight'].default_value = random.uniform(0.15, 0.4)
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_ground_material(self):
        mat_name = "Ground_Material_Base"
        if mat_name in bpy.data.materials:
            return bpy.data.materials[mat_name]
        
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.ground_colors)
        final_color = (base_color[0], base_color[1], base_color[2], 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = 0.85
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_cloud_material(self):
        mat_name = f"Cloud_Material_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        whiteness = random.uniform(0.85, 0.98)
        cloud_color = (whiteness, whiteness, whiteness, 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = cloud_color
        bsdf_node.inputs['Roughness'].default_value = 0.9
        bsdf_node.inputs['Subsurface Weight'].default_value = 0.3
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_bird_material(self):
        mat_name = f"Bird_Material_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        darkness = random.uniform(0.05, 0.15)
        bird_color = (darkness, darkness * 0.8, darkness * 0.6, 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = bird_color
        bsdf_node.inputs['Roughness'].default_value = 0.7
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    # ============ MATERIALS FOR NEW OBJECTS ============
    
    def create_rock_material(self):
        """Creates realistic rock material with gray/brown tones."""
        mat_name = f"Rock_Material_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.rock_colors)
        variation = random.uniform(-0.03, 0.03)
        final_color = (
            max(0, min(1, base_color[0] + variation)),
            max(0, min(1, base_color[1] + variation)),
            max(0, min(1, base_color[2] + variation)),
            1.0
        )
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = random.uniform(0.8, 1.0)
        bsdf_node.inputs['Specular IOR Level'].default_value = random.uniform(0.05, 0.15)
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_bush_material(self):
        """Creates leafy bush material with green variations."""
        mat_name = f"Bush_Material_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.bush_colors)
        variation = random.uniform(-0.05, 0.08)
        final_color = (
            max(0, min(1, base_color[0] + variation)),
            max(0, min(1, base_color[1] + variation)),
            max(0, min(1, base_color[2] + variation)),
            1.0
        )
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = random.uniform(0.4, 0.7)
        bsdf_node.inputs['Subsurface Weight'].default_value = random.uniform(0.2, 0.4)
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_flower_petal_material(self):
        """Creates vibrant flower petal material."""
        mat_name = f"Flower_Petal_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.flower_colors)
        final_color = (base_color[0], base_color[1], base_color[2], 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = random.uniform(0.3, 0.6)
        bsdf_node.inputs['Specular IOR Level'].default_value = random.uniform(0.4, 0.7)
        bsdf_node.inputs['Subsurface Weight'].default_value = random.uniform(0.3, 0.5)
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_flower_stem_material(self):
        """Creates green stem material for flowers."""
        mat_name = "Flower_Stem_Material"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        stem_color = (0.1, 0.4, 0.1, 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = stem_color
        bsdf_node.inputs['Roughness'].default_value = 0.6
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_mushroom_cap_material(self):
        """Creates colorful mushroom cap material."""
        mat_name = f"Mushroom_Cap_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.mushroom_cap_colors)
        final_color = (base_color[0], base_color[1], base_color[2], 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = random.uniform(0.4, 0.7)
        bsdf_node.inputs['Specular IOR Level'].default_value = random.uniform(0.3, 0.5)
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_mushroom_stalk_material(self):
        """Creates white/cream mushroom stalk material."""
        mat_name = "Mushroom_Stalk_Material"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        stalk_color = (0.9, 0.88, 0.85, 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = stalk_color
        bsdf_node.inputs['Roughness'].default_value = 0.7
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    # ============ NEW: BUTTERFLY MATERIALS ============
    
    def create_butterfly_body_material(self):
        """Creates dark body material for butterfly."""
        mat_name = f"Butterfly_Body_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        body_color = (0.05, 0.05, 0.05, 1.0)  # Dark brown/black
        
        bsdf_node.inputs['Base Color'].default_value = body_color
        bsdf_node.inputs['Roughness'].default_value = 0.8
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    def create_butterfly_wing_material(self):
        """Creates vibrant wing material for butterfly."""
        mat_name = f"Butterfly_Wing_{random.randint(1000, 9999)}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        base_color = random.choice(self.butterfly_colors)
        final_color = (base_color[0], base_color[1], base_color[2], 1.0)
        
        bsdf_node.inputs['Base Color'].default_value = final_color
        bsdf_node.inputs['Roughness'].default_value = random.uniform(0.2, 0.4)
        bsdf_node.inputs['Specular IOR Level'].default_value = random.uniform(0.5, 0.8)
        bsdf_node.inputs['Metallic'].default_value = random.uniform(0.1, 0.3)  # Slight shimmer
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        self.material_cache[mat_name] = mat
        return mat
    
    # ============ MATERIAL APPLICATION METHODS ============
    
    def assign_material_to_object(self, obj, material):
        """Safely assigns material to a Blender object."""
        if obj is None or not hasattr(obj, 'data'):
            print(f"Warning: Invalid object for material assignment")
            return
        
        try:
            obj.data.materials.clear()
            obj.data.materials.append(material)
        except Exception as e:
            print(f"Error assigning material to {obj.name}: {e}")
    
    def apply_tree_materials(self, trunk_obj, leaves_obj):
        """Applies materials to tree components."""
        bark_mat = self.create_bark_material(name_suffix=trunk_obj.name)
        leaf_mat = self.create_leaf_material(name_suffix=leaves_obj.name)
        
        self.assign_material_to_object(trunk_obj, bark_mat)
        self.assign_material_to_object(leaves_obj, leaf_mat)
        self.apply_smooth_shading(trunk_obj)
        self.apply_smooth_shading(leaves_obj)
    
    def apply_ground_material(self, ground_obj):
        """Applies ground material to ground plane."""
        ground_mat = self.create_ground_material()
        self.assign_material_to_object(ground_obj, ground_mat)
    
    def apply_rock_material(self, rock_obj):
        """Applies rock material."""
        rock_mat = self.create_rock_material()
        self.assign_material_to_object(rock_obj, rock_mat)
        self.apply_smooth_shading(rock_obj)
    
    def apply_bush_material(self, bush_obj):
        """Applies bush material."""
        bush_mat = self.create_bush_material()
        self.assign_material_to_object(bush_obj, bush_mat)
        self.apply_smooth_shading(bush_obj)
    
    def apply_flower_materials(self, stem_obj, petal_obj):
        """Applies materials to flower parts."""
        stem_mat = self.create_flower_stem_material()
        petal_mat = self.create_flower_petal_material()
        
        self.assign_material_to_object(stem_obj, stem_mat)
        self.assign_material_to_object(petal_obj, petal_mat)
        self.apply_smooth_shading(petal_obj)
    
    def apply_mushroom_materials(self, stalk_obj, cap_obj):
        """Applies materials to mushroom parts."""
        stalk_mat = self.create_mushroom_stalk_material()
        cap_mat = self.create_mushroom_cap_material()
        
        self.assign_material_to_object(stalk_obj, stalk_mat)
        self.assign_material_to_object(cap_obj, cap_mat)
        self.apply_smooth_shading(stalk_obj)
        self.apply_smooth_shading(cap_obj)
    
    def apply_butterfly_materials(self, body_obj, left_wing_obj, right_wing_obj):
        """Applies materials to butterfly parts."""
        body_mat = self.create_butterfly_body_material()
        wing_mat = self.create_butterfly_wing_material()  # Same color for both wings
        
        self.assign_material_to_object(body_obj, body_mat)
        self.assign_material_to_object(left_wing_obj, wing_mat)
        self.assign_material_to_object(right_wing_obj, wing_mat)
        self.apply_smooth_shading(body_obj)
    
    # ============ SKY ELEMENTS ============
    
    def create_cloud(self, collection, position):
        """Creates a cloud with slow drifting animation."""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=random.uniform(1.5, 2.5), location=position)
        cloud = bpy.context.active_object
        cloud.name = f"Cloud_{random.randint(100, 999)}"

        for c in cloud.users_collection:
            c.objects.unlink(cloud)
        collection.objects.link(cloud)

        # Scale cloud for fluffy shape
        cloud.scale = (
            random.uniform(2.5, 4.0),
            random.uniform(1.5, 3.0),
            random.uniform(0.8, 1.5)
        )

        cloud_mat = self.create_cloud_material()
        self.assign_material_to_object(cloud, cloud_mat)

        # ==========================
        # ☁️ CLOUD ANIMATION
        # ==========================
        start_frame = 1
        end_frame = 240

        start_x, start_y, start_z = position

        # Random wind direction
        wind_dir = random.uniform(0, math.pi * 2)
        drift_distance = random.uniform(8, 15)
        vertical_wobble = random.uniform(0.5, 1.2)

        end_x = start_x + math.cos(wind_dir) * drift_distance
        end_y = start_y + math.sin(wind_dir) * drift_distance

        # Start keyframe
        cloud.location = (start_x, start_y, start_z)
        cloud.keyframe_insert(data_path="location", frame=start_frame)

        # End keyframe
        cloud.location = (end_x, end_y, start_z)
        cloud.keyframe_insert(data_path="location", frame=end_frame)

        # Gentle vertical wobble
        for frame in range(start_frame, end_frame + 1, 40):
            z_offset = math.sin(frame * 0.05) * vertical_wobble
            cloud.location = (
                start_x + math.cos(wind_dir) * drift_distance * (frame / end_frame),
                start_y + math.sin(wind_dir) * drift_distance * (frame / end_frame),
                start_z + z_offset
            )
            cloud.keyframe_insert(data_path="location", frame=frame)

        return cloud

        
    def create_bird(self, collection, position):
        """Creates an animated bird that flies across the sky."""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=position)
        bird = bpy.context.active_object
        bird.name = f"Bird_{random.randint(100, 999)}"
        
        for c in bird.users_collection:
            c.objects.unlink(bird)
        collection.objects.link(bird)
        
        # Scale to bird-like proportions
        bird.scale = (1.5, 0.3, 0.2)
        bird.rotation_euler.z = random.uniform(0, math.pi * 2)
        
        bird_mat = self.create_bird_material()
        self.assign_material_to_object(bird, bird_mat)
        
        # ANIMATION: Bird flies in a path across the sky
        start_pos = position
        
        # Choose random flight pattern
        flight_pattern = random.choice(['straight', 'circular', 'wavy'])
        
        if flight_pattern == 'straight':
            # Straight line flight
            direction = random.uniform(0, math.pi * 2)
            distance = random.uniform(30, 50)
            
            end_x = start_pos[0] + math.cos(direction) * distance
            end_y = start_pos[1] + math.sin(direction) * distance
            end_z = start_pos[2] + random.uniform(-2, 3)
            
            # Start position
            bird.location = start_pos
            bird.rotation_euler.z = direction
            bird.keyframe_insert(data_path="location", frame=1)
            bird.keyframe_insert(data_path="rotation_euler", frame=1)
            
            # End position
            bird.location = (end_x, end_y, end_z)
            bird.keyframe_insert(data_path="location", frame=120)
            
        elif flight_pattern == 'circular':
            # Circular flight pattern
            radius = random.uniform(8, 15)
            center_x = start_pos[0]
            center_y = start_pos[1]
            base_z = start_pos[2]
            
            for frame in range(1, 121, 10):
                angle = (frame / 120) * math.pi * 4  # 2 full circles
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                z = base_z + math.sin(frame / 15) * 2  # Up and down motion
                
                bird.location = (x, y, z)
                bird.rotation_euler.z = angle + math.pi/2  # Face direction of movement
                bird.keyframe_insert(data_path="location", frame=frame)
                bird.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        else:  # wavy
            # Wavy flight pattern
            direction = random.uniform(0, math.pi * 2)
            distance = random.uniform(30, 50)
            wave_amplitude = random.uniform(3, 6)
            
            for frame in range(1, 121, 10):
                progress = frame / 120
                
                # Main direction movement
                base_x = start_pos[0] + math.cos(direction) * distance * progress
                base_y = start_pos[1] + math.sin(direction) * distance * progress
                
                # Add wavy motion perpendicular to direction
                wave = math.sin(progress * math.pi * 6) * wave_amplitude
                x = base_x + math.cos(direction + math.pi/2) * wave
                y = base_y + math.sin(direction + math.pi/2) * wave
                z = start_pos[2] + math.sin(progress * math.pi * 4) * 2
                
                bird.location = (x, y, z)
                bird.rotation_euler.z = direction + math.sin(progress * math.pi * 6) * 0.3
                bird.keyframe_insert(data_path="location", frame=frame)
                bird.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        return bird

    def generate_sky_elements(self, collection, count_clouds=3, count_birds=6):
        """Generates clouds and animated birds in the sky."""
        print(f"Generating {count_clouds} clouds and {count_birds} birds...")
        
        # Generate clouds at higher altitude
        for i in range(count_clouds):
            pos = (
                random.uniform(-20, 20),
                random.uniform(-20, 20),
                random.uniform(15, 25)  # Higher up for clouds
            )
            self.create_cloud(collection, pos)
        
        # Generate birds at lower altitude (below clouds) with ANIMATION
        for i in range(count_birds):
            pos = (
                random.uniform(-15, 15),
                random.uniform(-15, 15),
                random.uniform(8, 14)  # Lower than clouds
            )
            self.create_bird(collection, pos)
        
        print("✅ Sky elements with animated birds generated!")