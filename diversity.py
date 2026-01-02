# diversity.py
import random
import math

class RuntimeDiversity:
    def __init__(
        self,
        pos_range=15.0,
        scale_range=(0.7, 1.3),
        height_range=(2.0, 5.0),
        rotation_range=(0, 360),
        seed=None
    ):
        """
        Handles all randomness and procedural realism.
        No hardcoded values outside this class.
        """

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
