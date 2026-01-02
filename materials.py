import bpy
import random
import math

class MaterialAssigner:
    """
    ENHANCED: Now includes materials for rocks, bushes, flowers, and mushrooms!
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
        (0.04, 0.30, 0.04),  # 
        (0.05, 0.35, 0.05),  
        ]
        
        self.ground_colors = [
            (0.15, 0.25, 0.10), (0.20, 0.30, 0.12), (0.12, 0.20, 0.08),
        ]
        
        # NEW: Rock color variants (gray, brown)
        self.rock_colors = [
            (0.3, 0.3, 0.3),    # Light gray
            (0.2, 0.2, 0.2),    # Medium gray
            (0.15, 0.15, 0.15), # Dark gray
            (0.25, 0.22, 0.18), # Brown-gray
            (0.18, 0.18, 0.20), # Blue-gray
        ]
        
       
        self.bush_colors = [
            (0.08, 0.40, 0.08), # Dark green
            (0.12, 0.50, 0.10), # Medium green
            (0.15, 0.55, 0.12), # Light green
            (0.10, 0.45, 0.15), # Yellow-green
        ]
        
        # NEW: Flower petal colors 
        self.flower_colors = [
            (0.9, 0.2, 0.3),    # Red
            (0.95, 0.7, 0.2),   # Yellow
            (0.8, 0.3, 0.8),    # Purple
            (1.0, 0.5, 0.0),    # Orange
            (0.9, 0.1, 0.5),    # Pink
            (1.0, 1.0, 0.9),    # White
        ]
        
        # NEW: Mushroom colors
        self.mushroom_cap_colors = [
            (0.8, 0.2, 0.2),    # Red cap
            (0.9, 0.6, 0.3),    # Orange cap
            (0.7, 0.5, 0.3),    # Brown cap
            (0.95, 0.95, 0.9),  # White cap with spots
        ]
    
    def apply_smooth_shading(self, obj):
        """Removes harsh edges."""
        if obj and obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.shade_smooth()
            obj.select_set(False)
    
    # ============ EXISTING MATERIALS (UNCHANGED) ============
    
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
    
    # ============ NEW MATERIALS FOR NEW OBJECTS ============
    
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
    
    # ============ SKY ELEMENTS ============
    
    def create_cloud(self, collection, position):
        """Creates a fluffy cloud."""
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, ring_count=8,
            radius=random.uniform(3, 6),
            location=position
        )
        cloud = bpy.context.active_object
        cloud.name = f"Cloud_{random.randint(100, 999)}"
        
        for c in cloud.users_collection:
            c.objects.unlink(cloud)
        collection.objects.link(cloud)
        
        cloud.scale = (
            random.uniform(1.5, 2.5),
            random.uniform(1.2, 2.0),
            random.uniform(0.4, 0.7)
        )
        
        cloud_mat = self.create_cloud_material()
        self.assign_material_to_object(cloud, cloud_mat)
        self.apply_smooth_shading(cloud)
        
        return cloud
    
    def create_bird(self, collection, position):
        """Creates a simple bird."""
        bpy.ops.mesh.primitive_cube_add(size=0.8, location=position)
        bird = bpy.context.active_object
        bird.name = f"Bird_{random.randint(100, 999)}"
        
        for c in bird.users_collection:
            c.objects.unlink(bird)
        collection.objects.link(bird)
        
        bird.scale = (1.5, 0.3, 0.2)
        bird.rotation_euler.z = random.uniform(0, math.pi * 2)
        
        bird_mat = self.create_bird_material()
        self.assign_material_to_object(bird, bird_mat)
        
        return bird
    
    def generate_sky_elements(self, collection, count_clouds=5, count_birds=3):
        """Generates clouds and birds in the sky."""
        print(f"Generating {count_clouds} clouds and {count_birds} birds...")
        
        for i in range(count_clouds):
            pos = (
                random.uniform(-20, 20),
                random.uniform(-20, 20),
                random.uniform(10, 18)
            )
            self.create_cloud(collection, pos)
        
        for i in range(count_birds):
            pos = (
                random.uniform(-20, 20),
                random.uniform(-20, 20),
                random.uniform(10, 18)
            )
            self.create_bird(collection, pos)
        
        print("✅ Sky elements generated!")