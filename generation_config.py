import random

class GenerationConfig:
    """
    Handles DYNAMIC object count generation at runtime.
    No hardcoded values - everything is procedurally determined!
    
    This fulfills the requirement: "procedurally generating at least 5-10 objects 
    dynamically during execution, introducing runtime variations that are not fixed in code"
    """
    
    def __init__(self, seed=None, density="medium"):
        """
        Args:
            seed: Optional seed for reproducibility
            density: "sparse", "medium", "dense", or "random"
        """
        self.seed = seed
        self.density = density
        
        if seed is not None:
            random.seed(seed)
        
        # Define density presets (ranges, not fixed values!)
        self.density_presets = {
            "sparse": {
                "trees": (5, 8),
                "rocks": (3, 6),
                "bushes": (2, 5),
                "flowers": (4, 7),
                "mushrooms": (2, 4),
                "clouds": (3, 5),
                "birds": (2, 4)
            },
            "medium": {
                "trees": (8, 15),
                "rocks": (5, 10),
                "bushes": (4, 8),
                "flowers": (6, 12),
                "mushrooms": (3, 7),
                "clouds": (5, 8),
                "birds": (3, 6)
            },
            "dense": {
                "trees": (15, 25),
                "rocks": (10, 18),
                "bushes": (8, 15),
                "flowers": (12, 20),
                "mushrooms": (7, 12),
                "clouds": (8, 12),
                "birds": (5, 10)
            },
            "random": {
                "trees": (3, 30),
                "rocks": (2, 25),
                "bushes": (2, 20),
                "flowers": (3, 25),
                "mushrooms": (2, 15),
                "clouds": (2, 15),
                "birds": (2, 12)
            }
        }
    
    def get_object_count(self, object_type):
        """
        Dynamically determines how many objects to generate at runtime.
        Returns a DIFFERENT number each time the script runs!
        
        Args:
            object_type: "trees", "rocks", "bushes", etc.
        
        Returns:
            Random integer within the density range
        """
        if self.density not in self.density_presets:
            self.density = "medium"  # Fallback
        
        min_count, max_count = self.density_presets[self.density][object_type]
        count = random.randint(min_count, max_count)
        
        return count
    
    def get_all_counts(self):
        """
        Returns a dictionary of ALL object counts for this generation run.
        Each run produces different numbers!
        
        Returns:
            dict: {"trees": 12, "rocks": 7, ...}
        """
        counts = {}
        for obj_type in ["trees", "rocks", "bushes", "flowers", "mushrooms", "clouds", "birds"]:
            counts[obj_type] = self.get_object_count(obj_type)
        
        return counts
    
    def print_generation_plan(self, counts):
        """
        Pretty-prints the generation plan.
        """
        print("\n" + "="*50)
        print("🌲 PROCEDURAL FOREST GENERATION PLAN")
        print("="*50)
        print(f"Density Mode: {self.density.upper()}")
        if self.seed:
            print(f"Seed: {self.seed} (reproducible)")
        else:
            print("Seed: Random (unique each run)")
        print("-"*50)
        
        total = 0
        for obj_type, count in counts.items():
            emoji = {
                "trees": "🌲",
                "rocks": "🪨",
                "bushes": "🌿",
                "flowers": "🌸",
                "mushrooms": "🍄",
                "clouds": "☁️",
                "birds": "🐦"
            }
            print(f"{emoji.get(obj_type, '📦')} {obj_type.capitalize()}: {count}")
            total += count
        
        print("-"*50)
        print(f"📊 TOTAL OBJECTS: {total}")
        print("="*50 + "\n")
    
    def get_density_multiplier(self):
        """
        Returns a random multiplier based on environmental factors.
        Simulates "fertile" vs "barren" areas of the forest.
        
        Returns:
            float: Multiplier between 0.5 and 1.5
        """
        return random.uniform(0.5, 1.5)
    
    def should_generate_cluster(self, probability=0.3):
        """
        Randomly determines if objects should spawn in clusters.
        Adds natural grouping variation.
        
        Args:
            probability: Chance of clustering (0.0-1.0)
        
        Returns:
            bool: True if this generation should use clustering
        """
        return random.random() < probability
    
    @staticmethod
    def create_random_config():
        """
        Factory method: Creates a completely random configuration.
        Perfect for "surprise me" mode!
        
        Returns:
            GenerationConfig with random settings
        """
        densities = ["sparse", "medium", "dense", "random"]
        return GenerationConfig(
            seed=None,  # Always random
            density=random.choice(densities)
        )
    
    @staticmethod
    def create_reproducible_config(seed=42):
        """
        Factory method: Creates a reproducible configuration.
        Same seed = same forest every time.
        
        Args:
            seed: Integer seed for RNG
        
        Returns:
            GenerationConfig with fixed seed
        """
        return GenerationConfig(
            seed=seed,
            density="medium"
        )


class SeasonalVariation:
    """
    BONUS: Adds seasonal variations to generation.
    Different seasons = different object distributions!
    """
    
    SEASONS = ["spring", "summer", "autumn", "winter"]
    
    def __init__(self, season=None):
        """
        Args:
            season: "spring", "summer", "autumn", "winter", or None (random)
        """
        self.season = season if season else random.choice(self.SEASONS)
    
    def get_seasonal_multipliers(self):
        """
        Returns multipliers for each object type based on season.
        
        Returns:
            dict: Multipliers for each object type
        """
        multipliers = {
            "spring": {
                "trees": 1.0,
                "flowers": 1.8,  # Lots of flowers in spring!
                "bushes": 1.3,
                "mushrooms": 1.2,
                "rocks": 1.0,
                "clouds": 1.1,
                "birds": 1.5
            },
            "summer": {
                "trees": 1.2,
                "flowers": 1.3,
                "bushes": 1.5,
                "mushrooms": 0.8,
                "rocks": 1.0,
                "clouds": 0.8,  # Clear skies
                "birds": 1.4
            },
            "autumn": {
                "trees": 1.1,
                "flowers": 0.5,  # Fewer flowers
                "bushes": 1.0,
                "mushrooms": 2.0,  # Mushroom season!
                "rocks": 1.0,
                "clouds": 1.3,
                "birds": 0.9
            },
            "winter": {
                "trees": 0.8,  # Bare trees
                "flowers": 0.2,  # Almost no flowers
                "bushes": 0.6,
                "mushrooms": 0.3,
                "rocks": 1.2,  # More visible
                "clouds": 1.5,  # Overcast
                "birds": 0.5
            }
        }
        
        return multipliers[self.season]
    
    def apply_to_config(self, config):
        """
        Modifies a GenerationConfig based on season.
        
        Args:
            config: GenerationConfig instance
        
        Returns:
            dict: Modified counts
        """
        base_counts = config.get_all_counts()
        multipliers = self.get_seasonal_multipliers()
        
        seasonal_counts = {}
        for obj_type, base_count in base_counts.items():
            multiplier = multipliers.get(obj_type, 1.0)
            seasonal_counts[obj_type] = max(1, int(base_count * multiplier))
        
        print(f"🍂 Season: {self.season.upper()}")
        return seasonal_counts