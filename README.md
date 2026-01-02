**Procedural 3D Scene Generation with Blender's Python API**
**Group Members**
1. Muhammad Ahmad Shoaib 538790
2. Muhammad Kashan Nazim 537545
3. Hafsah Sahsiddiqah 498790
4. Hamna Malik 537579
5. Zarshina Baltistani 498673

🌲 Procedural 3D Forest Scene Generation with Blender's Python API
A fully procedural, animated 3D forest ecosystem built entirely with Blender's Python API (bpy). Every run generates a unique forest with dynamic object counts, varied geometries, realistic materials, and complex animations.

🎯 Project Overview
This project creates immersive animated forest scenes featuring:

Procedurally generated trees with multiple crown shapes (cone, sphere, rounded variants)
Animated wildlife including birds flying across the sky and butterflies fluttering around flowers
Dynamic weather elements with drifting clouds and an animated sun moving from sunrise to sunset
Diverse flora including bushes, flowers, mushrooms with unique materials
Environmental details like rocks with realistic textures
Wind simulation affecting all vegetation with swaying, bending, and wobbling animations


✨ Key Features
🎲 Fully Procedural Generation

Zero hardcoded values - all object counts determined at runtime
Dynamic object generation - generates 5-50+ objects per type based on density settings
Unique every run - no two forests are identical
Seasonal variations - optional system for spring/summer/autumn/winter themes

🎬 Rich Animation System

Trees: Grow from roots with continuous wind sway
Bushes: Dramatic swaying in multiple axes
Flowers: Stems bend, petals spin/wiggle in wind
Mushrooms: Flexible wobbling motion
Butterflies: Circular flight paths with wing flapping
Birds: Multiple flight patterns (straight, circular, wavy)
Clouds: Slow drifting with vertical wobble
Sun: Animated arc from sunrise to sunset with changing intensity

🎨 Procedural Materials

Tree bark: 5+ brown/gray variants with roughness variation
Leaves: 3+ green tones with subsurface scattering
Flowers: 6+ vibrant petal colors
Mushrooms: 4+ cap colors (red, orange, brown, white)
Butterflies: 6+ wing color variants (orange monarch, blue morpho, etc.)
Rocks: Realistic gray/brown textures
Ground: Natural grass-like green variations


📁 Project Structure
Procedural-3D-Scene-Generation-with-Blender-s-Python-API/
│
├── main.py                    # Entry point - orchestrates execution
├── scene_manager.py           # Main scene orchestration & object generation
├── variations.py              # Randomization engine for transforms
├── materials.py               # Procedural material creation & assignment
├── generation_config.py       # Dynamic object count configuration
├── diversity.py               # Runtime diversity parameters (merged into variations.py)
└── README.md                  # This file

🔧 Module Breakdown
main.py

Entry point that imports and runs the SceneManager
Includes error handling and success confirmation
Manages Blender path configuration

scene_manager.py ⭐ Core Controller
Orchestrates the entire forest generation pipeline:

Scene initialization and cleanup
Object generation methods for all forest elements
Animation systems for growth, wind, and wildlife
Sun and lighting setup
Timeline configuration (frames 1-160)

Key Methods:

generate_tree() - Creates trees with random crown shapes
generate_flower() - Flowers with butterflies (30% spawn chance)
generate_butterfly_near_flower() - Animated butterfly creation
generate_mushroom() - Mushrooms with wobble animation
generate_bush() - Bushes with wind sway
generate_rock() - Rocks with settling animation
animate_tree_with_wind() - Advanced wind simulation
setup_sun_light() - Animated sun with day cycle

variations.py
Handles all transformation randomization:

Position, scale, height, and rotation generation
Tree-type-specific crown positioning
Integration with RuntimeDiversity engine

Classes:

RuntimeDiversity - Core randomization parameters
VariationEngine - Applies transforms to objects

materials.py 🎨 Material Factory
Creates and assigns all procedural materials:

20+ unique material creation methods
Color variant systems for natural diversity
Smooth shading application
Node-based shader setup with Principled BSDF

Material Types:

Tree materials (bark, leaves)
Flora materials (bushes, flowers, mushrooms)
Wildlife materials (butterflies, birds)
Environmental materials (rocks, ground, clouds)

generation_config.py 🎲 Dynamic Generation System
The heart of procedural generation - determines object counts at runtime:
Classes:

GenerationConfig - Main configuration class
SeasonalVariation - Optional seasonal multipliers

Density Modes:

Sparse: 5-8 trees, 3-6 rocks, 2-5 bushes
Medium: 8-15 trees, 5-10 rocks, 4-8 bushes
Dense: 15-25 trees, 10-18 rocks, 8-15 bushes
Random: 3-30 trees, 2-25 rocks (complete chaos!)

Key Methods:

get_object_count() - Returns random count for object type
get_all_counts() - Returns full generation plan
print_generation_plan() - Pretty-prints generation info
create_random_config() - Factory for random forests
create_reproducible_config() - Factory for seeded generation


🚀 Installation & Usage
Prerequisites

Blender 3.0+ (tested on 3.6+)
Python 3.10+ (included with Blender)

Setup

Clone the repository
Open Blender
Load your .blend file or create a new one
Save the file (required for path resolution)
Place all Python scripts in the same directory as your .blend file

Running the Generator
Method 1: Blender Text Editor
pythonimport main
import importlib
importlib.reload(main)
# Run main.py - watch your forest come to life!
Method 2: Scripting Tab

Open Blender's Scripting workspace
Click Open and select main.py
Click Run Script (▶️ button)

Method 3: Command Line
bashblender --python main.py
Viewing the Animation
After generation completes:

Scene automatically moves to Frame 90 (mid-animation)
Press Spacebar to play animation
Navigate timeline: Frames 1-160
Use Timeline scrubbing to see different animation phases


🎬 Animation Timeline
FramesEvent1-50Trees grow from roots1-35Rocks emerge from underground1-50Bushes grow1-70Flowers bloom1-80Mushrooms pop up1-120Birds fly across sky (multiple patterns)1-120Clouds drift gently1-120Sun moves from sunrise → noon → sunset50-120Trees sway continuously in wind50-120Bushes sway dramatically70-120Flower petals spin/wiggle70-120Flower stems bend in wind80-120Mushrooms wobble20-120Butterflies flutter around flowers

🎨 Customization Options
Changing Generation Density
Modify in scene_manager.py:
python# Current: Random density
config = GenerationConfig.create_random_config()

# Change to specific density:
config = GenerationConfig(seed=None, density="dense")
Reproducible Generation
For the same forest every time:
pythonconfig = GenerationConfig.create_reproducible_config(seed=42)
Adding Seasonal Variations
pythonfrom generation_config import SeasonalVariation

season = SeasonalVariation(season="autumn")
counts = season.apply_to_config(config)
Adjusting Animation Speed
Modify frame ranges in scene_manager.py:
python# Faster animations:
bpy.context.scene.frame_end = 100  # Instead of 160

# Slower animations: Adjust keyframe intervals

📊 Output Examples
Each run generates different counts, for example:
==================================================
🌲 PROCEDURAL FOREST GENERATION PLAN
==================================================
Density Mode: RANDOM
Seed: Random (unique each run)
--------------------------------------------------
🌲 Trees: 18
🪨 Rocks: 14
🌿 Bushes: 11
🌸 Flowers: 16 (with ~5 butterflies)
🍄 Mushrooms: 9
☁️ Clouds: 7
🦅 Birds: 8
--------------------------------------------------
📊 TOTAL OBJECTS: 83
==================================================

🧪 Technical Highlights
Procedural Generation Techniques

Runtime object counting - No hardcoded quantities
Shape variation - Trees use 4 different crown geometries
Material diversity - Each object gets unique material instance
Spatial distribution - Random positioning with configurable ranges

Animation Techniques

Keyframe animation - All movements use Blender keyframes
Sinusoidal motion - Wind uses sine waves for natural movement
Multi-axis rotation - Objects sway in X, Y, Z axes
Hierarchical animation - Stems and petals move together
Path interpolation - Birds/butterflies follow curved paths

Material System

Node-based shaders - Uses Principled BSDF
Procedural color variation - Runtime color adjustments
Subsurface scattering - For leaves and petals
Roughness variation - Realistic surface properties
Material caching - Efficient material reuse


🐛 Troubleshooting
Scene doesn't generate

Ensure Blender file is saved (path resolution requires saved file)
Check Blender version (3.0+)
Verify all scripts are in the same directory

Animation doesn't play

Press Spacebar in viewport
Check timeline range (should be 1-160)
Ensure you're in camera view (Numpad 0)

Missing objects

Random generation might produce low counts
Try density="dense" for more objects
Check Blender outliner for generated collection

Performance issues

Reduce density mode to "sparse"
Lower object counts in generation_config.py
Disable viewport shadows during playback


🔮 Future Enhancements
Potential additions:

Weather systems - Rain, snow, fog effects
Animal variety - Deer, squirrels, rabbits
Water features - Rivers, ponds with reflections
Terrain generation - Hills, valleys using displacement
Sound integration - Wind, birds, rustling leaves
Day/night cycle - Complete 24-hour simulation
Seasons animation - Transition between seasons


📝 Technical Requirements

Blender: 3.0 or higher
Python: 3.10+ (bundled with Blender)
RAM: 4GB minimum, 8GB recommended
Storage: ~500MB for project files


🎓 Learning Resources
This project demonstrates:

Blender Python API (bpy) fundamentals
Procedural mesh generation
Keyframe animation systems
Node-based material creation
Scene management and collections
Randomization and diversity systems


👨‍💻 Development Notes
Code Philosophy:

Zero hardcoded values - Everything procedurally determined
Modular architecture - Clear separation of concerns
Extensible design - Easy to add new object types
Commented code - Inline documentation throughout
Error handling - Graceful failure management

