import random
import math
import bpy
import importlib

# Import the MaterialAssigner
import materials
importlib.reload(materials)
from materials import MaterialAssigner

class RuntimeDiversity:
    """
    Handles all randomness and procedural realism.
    Merged from diversity.py into variations.py
    """
    def __init__(
        self,
        pos_range=15.0,
        scale_range=(0.7, 1.3),
        height_range=(2.0, 5.0),
        rotation_range=(0, 360),
        seed=None
    ):
        self.pos_range = pos_range
        self.scale_range = scale_range
        self.height_range = height_range
        self.rotation_range = rotation_range

        # Optional reproducibility
        if seed is not None:
            random.seed(seed)

    def random_position(self):
        return (
            random.uniform(-self.pos_range, self.pos_range),
            random.uniform(-self.pos_range, self.pos_range)
        )

    def random_scale(self):
        return random.uniform(*self.scale_range)

    def random_height(self):
        return random.uniform(*self.height_range)

    def random_rotation(self):
        return math.radians(
            random.uniform(*self.rotation_range)
        )

class VariationEngine:
    def __init__(self, spawn_range=15.0):
        # Initialize the RuntimeDiversity engine
        self.diversity = RuntimeDiversity(
            pos_range=spawn_range,
            scale_range=(0.7, 1.3),
            height_range=(2.0, 5.0),
            rotation_range=(0, 360)
        )
        # Initialize material engine
        self.material_assigner = MaterialAssigner()

    def apply_random_transform(self, trunk, leaves, tree_type='cone'):
        """
        Now uses RuntimeDiversity for all randomization.
        Enhanced to handle different tree crown shapes!
        """
        # Get random position using diversity engine
        pos_x, pos_y = self.diversity.random_position()
        
        # Get random dimensions
        trunk_h = self.diversity.random_height()
        tree_scale = self.diversity.random_scale()
        leaf_rotation = self.diversity.random_rotation()

        # Positioning Trunk (Cylinder)
        trunk.location = (pos_x, pos_y, trunk_h / 2)
        trunk.scale = (tree_scale, tree_scale, trunk_h)
        
        # Positioning Leaves - VARIES BY TREE TYPE!
        if tree_type == 'cone':
            # Classic cone tree (pine/fir)
            leaves.location = (pos_x, pos_y, trunk_h * 2)
            leaves.scale = (tree_scale * 2.5, tree_scale * 2.5, trunk_h * 1.1)
            
        elif tree_type in ['sphere', 'ico_sphere']:
            # Round bushy tree (oak/maple style)
            leaves.location = (pos_x, pos_y, trunk_h + trunk_h * 0.8)
            leaves.scale = (
                tree_scale * 3.0,
                tree_scale * 3.0,
                tree_scale * 2.5
            )
            
        else:  # round_cone
            # Hybrid rounded cone
            leaves.location = (pos_x, pos_y, trunk_h * 1.8)
            leaves.scale = (
                tree_scale * 2.8,
                tree_scale * 2.8,
                trunk_h * 0.9
            )
        
        leaves.rotation_euler.z = leaf_rotation

    def apply_materials(self, trunk, leaves, ground):
        """Uses MaterialAssigner class for procedural material assignment."""
        # Apply tree materials
        self.material_assigner.apply_tree_materials(trunk, leaves)
        
        # Apply ground material only once
        if ground and len(ground.data.materials) == 0:
            self.material_assigner.apply_ground_material(ground)