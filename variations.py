# variations.py
import bpy
from diversity import RuntimeDiversity

class VariationEngine:
    def __init__(self):
        self.diversity = RuntimeDiversity(
            pos_range=15.0,
            scale_range=(0.7, 1.3),
            height_range=(2.0, 5.0),
            seed=None  # Set value for reproducible forests
        )

    def apply_random_transform(self, trunk, leaves):
        pos_x, pos_y = self.diversity.random_position()
        trunk_h = self.diversity.random_height()
        tree_scale = self.diversity.random_scale()
        rotation_z = self.diversity.random_rotation()

        # Trunk
        trunk.location = (pos_x, pos_y, trunk_h / 2)
        trunk.scale = (tree_scale, tree_scale, trunk_h)

        # Leaves
        leaves.location = (pos_x, pos_y, trunk_h*2)
        leaves.scale = (tree_scale * 2.5, tree_scale * 2.5, trunk_h * 1.1)
        leaves.rotation_euler.z = rotation_z

    def apply_materials(self, trunk, leaves, ground):
        # Trunk Material
        t_mat = bpy.data.materials.new(name="Trunk_Mat")
        t_mat.use_nodes = True
        t_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.05, 0.02, 1)
        trunk.data.materials.append(t_mat)

        # Leaf Material
        l_mat = bpy.data.materials.new(name="Leaf_Mat")
        l_mat.use_nodes = True
        l_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.6, 0.05, 1)
        leaves.data.materials.append(l_mat)

        # Ground Material
        if ground and not ground.data.materials:
            g_mat = bpy.data.materials.new(name="Ground_Mat")
            g_mat.use_nodes = True
            g_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.05, 0.01, 1)
            ground.data.materials.append(g_mat)
