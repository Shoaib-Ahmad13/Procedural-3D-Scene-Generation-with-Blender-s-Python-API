import random
import math
import bpy

class VariationEngine:
    def __init__(self, spawn_range=15.0):
        # Manage state within class to avoid global variables [cite: 16]
        self.spawn_range = spawn_range
        self.min_height = 2.0
        self.max_height = 5.0

    def apply_random_transform(self, trunk, leaves):
        """Randomizes placement and scale for procedural diversity[cite: 9]."""
        pos_x = random.uniform(-self.spawn_range, self.spawn_range)
        pos_y = random.uniform(-self.spawn_range, self.spawn_range)
        
        trunk_h = random.uniform(self.min_height, self.max_height)
        tree_scale = random.uniform(0.7, 1.3)

        # Positioning Trunk (Cylinder)
        trunk.location = (pos_x, pos_y, trunk_h / 2)
        trunk.scale = (tree_scale, tree_scale, trunk_h)
        
        # Positioning Leaves (Cone) on top of Trunk
        leaves.location = (pos_x, pos_y, trunk_h*2)
        leaves.scale = (tree_scale * 2.5, tree_scale * 2.5, trunk_h * 1.1)
        leaves.rotation_euler.z = math.radians(random.uniform(0, 360))

    def apply_materials(self, trunk, leaves, ground):
        """Procedurally assigns material properties like color[cite: 9]."""
        # Trunk Material
        t_mat = bpy.data.materials.new(name="Trunk_Mat")
        t_mat.use_nodes = True
        t_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.1, 0.05, 0.02, 1)
        trunk.data.materials.append(t_mat)

        # Leaf Material (Random Green)
        l_mat = bpy.data.materials.new(name="Leaf_Mat")
        l_mat.use_nodes = True
        green_shade = random.uniform(0.2, 0.7)
        l_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.05, green_shade, 0.05, 1)
        leaves.data.materials.append(l_mat)
        
        # Ground Material (Grass)
        if ground and not ground.data.materials:
            g_mat = bpy.data.materials.new(name="Ground_Mat")
            g_mat.use_nodes = True
            g_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.02, 0.05, 0.01, 1)
            ground.data.materials.append(g_mat)