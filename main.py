import bpy
import os
import sys
import importlib

# Ensure path finds your scripts [cite: 44]
blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

import scene_manager
importlib.reload(scene_manager)
from scene_manager import SceneManager

if __name__ == "__main__":
    # Graceful error handling [cite: 17]
    try:
        app = SceneManager()
        app.run()
        print("Forest Generation Successful.")
    except Exception as e:
        print(f"Error caught: {e}")