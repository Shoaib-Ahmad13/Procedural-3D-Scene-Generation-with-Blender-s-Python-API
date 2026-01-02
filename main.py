import bpy
import sys
import os
import importlib

# 1. SETUP PATHS
# Get the folder where your .blend file is saved
# This allows Python to find your other scripts (scene_manager.py)
blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

# 2. IMPORT & RELOAD
# We use 'importlib.reload' to ensure Blender uses the latest version of your code
import scene_manager
importlib.reload(scene_manager)

# Import the class AFTER reloading the module
from scene_manager import SceneManager

# 3. EXECUTION
# This is the "Clean Entry Point" required by the project 
if __name__ == "__main__":
    # Instantiate the controller class
    try:
        app = SceneManager()
        print("Forest Generation Successful.")
        # Run the main execution pipeline
        app.run()
    except Exception as e:
        print(f"Error caught: {e}")