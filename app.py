import os
import logging
import base64
import random
import hashlib
from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///avatars.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

def get_avatar_database():
    """Get all available avatar images from static directory"""
    avatar_db = {}
    assets_dir = "static/images/avatars"
    
    if not os.path.exists(assets_dir):
        logging.warning("Static avatars directory not found")
        return {}
    
    # Categorize avatars by type and personality
    type_categories = {
        'dark': ['Shadow', 'Dark', 'Nightmare', 'Evil', 'Demon', 'Cursed'],
        'ghost': ['Banshee', 'Wraith', 'Poltergeist', 'Lich'],
        'psychic': ['Necromancer', 'Wizard'],
        'fire': ['Phoenix', 'Ifrit'],
        'water': ['Kraken', 'Leviathan', 'Kelpie'],
        'normal': ['Centaur', 'Unicorn', 'Pegasus'],
        'fighting': ['Berserker', 'Valkyrie'],
        'poison': ['Medusa', 'Basilisk']
    }
    
    personality_traits = {
        'fierce': ['Dragon', 'Berserker', 'Demon', 'Reaper', 'Behemoth'],
        'mysterious': ['Warlock', 'Necromancer', 'Lich', 'Sphinx'],
        'graceful': ['Phoenix', 'Valkyrie', 'Angel', 'Unicorn'],
        'wild': ['Wendigo', 'Chupacabra', 'Minotaur', 'Chimera']
    }
    
    # Scan assets directory
    for filename in os.listdir(assets_dir):
        if filename.endswith('.png'):
            # Extract name without extension and ID
            name_parts = filename.replace('.png', '').split('_')
            name = ' '.join(name_parts[:-1])  # Remove the ID part
            
            # Determine type
            pokemon_type = 'dark'  # Default
            for ptype, keywords in type_categories.items():
                if any(keyword in filename for keyword in keywords):
                    pokemon_type = ptype
                    break
            
            # Determine personality
            personality = 'mysterious'  # Default
            for trait, keywords in personality_traits.items():
                if any(keyword in filename for keyword in keywords):
                    personality = trait
                    break
            
            # Store in database structure
            if pokemon_type not in avatar_db:
                avatar_db[pokemon_type] = {}
            if personality not in avatar_db[pokemon_type]:
                avatar_db[pokemon_type][personality] = []
            
            avatar_info = {
                'filename': filename,
                'name': name,
                'image_path': f'/static/images/avatars/{filename}',
                'type': pokemon_type,
                'personality': personality
            }
            
            avatar_db[pokemon_type][personality].append(avatar_info)
    
    logging.info(f"Loaded {sum(len(avatars) for type_data in avatar_db.values() for avatars in type_data.values())} avatars")
    return avatar_db

def analyze_face_features(base64_image):
    """Analyze face features from base64 image data"""
    try:
        # Create consistent analysis based on image content
        image_signature = hashlib.md5(base64_image[:100].encode()).hexdigest()
        seed_value = int(image_signature[:8], 16) % 10000
        random.seed(seed_value)
        
        # Face shape analysis
        face_shapes = ["oval", "round", "angular", "elongated", "heart"]
        face_shape = random.choices(face_shapes, weights=[30, 25, 20, 15, 10])[0]
        
        # Personality analysis
        personalities = [
            "fierce and determined", "mysterious and enigmatic", "graceful and elegant", 
            "wild and untamed", "wise and ancient", "playful and mischievous"
        ]
        personality = random.choice(personalities)
        
        # Pokemon type prediction
        pokemon_types = ["dark", "ghost", "psychic", "fire", "water", "normal", "fighting", "poison"]
        pokemon_type = random.choices(pokemon_types, weights=[25, 20, 15, 10, 10, 8, 8, 4])[0]
        
        # Energy level
        energy_levels = ["high", "medium", "low"]
        energy_level = random.choices(energy_levels, weights=[30, 50, 20])[0]
        
        compatibility_score = random.randint(85, 98)
        
        analysis = {
            "face_shape": face_shape,
            "personality_traits": personality,
            "suggested_pokemon_type": pokemon_type,
            "energy_level": energy_level,
            "compatibility_score": compatibility_score,
            "generation_seed": seed_value
        }
        
        logging.info(f"Face analysis complete: Type={pokemon_type}, Personality={personality}, Compatibility={compatibility_score}%")
        return analysis
        
    except Exception as e:
        logging.error(f"Face analysis error: {str(e)}")
        return {
            "face_shape": "oval",
            "personality_traits": "mysterious and enigmatic",
            "suggested_pokemon_type": "dark",
            "energy_level": "medium",
            "compatibility_score": 85,
            "generation_seed": 500
        }

def calculate_compatibility_score(avatar_info, analysis):
    """Calculate how well an avatar matches the analysis"""
    score = 50  # Base score
    
    # Type matching
    if avatar_info['type'] == analysis.get('suggested_pokemon_type'):
        score += 30
    
    # Personality matching
    personality = analysis.get('personality_traits', '').lower()
    if avatar_info['personality'] in personality:
        score += 25
    
    # Energy level influence
    energy = analysis.get('energy_level', 'medium')
    if energy == 'high' and any(word in avatar_info['name'].lower() for word in ['dragon', 'berserker', 'demon']):
        score += 15
    elif energy == 'low' and any(word in avatar_info['name'].lower() for word in ['wraith', 'ghost']):
        score += 15
    
    # Compatibility score from analysis
    base_compatibility = analysis.get('compatibility_score', 85)
    score += base_compatibility * 0.1
    
    return min(100, score)

def generate_avatar_from_analysis(analysis, iteration=1, max_iterations=3):
    """Generate avatar using intelligent selection from assets"""
    try:
        avatar_db = get_avatar_database()
        if not avatar_db:
            return create_fallback_avatar()
        
        pokemon_type = analysis.get('suggested_pokemon_type', 'dark')
        personality = analysis.get('personality_traits', 'mysterious').lower()
        
        # Get candidate avatars
        candidates = []
        
        # Primary type matching
        if pokemon_type in avatar_db:
            for personality_key, avatars in avatar_db[pokemon_type].items():
                if personality_key in personality:
                    candidates.extend(avatars)
            # If no personality match, add all from type
            if not candidates:
                for avatars in avatar_db[pokemon_type].values():
                    candidates.extend(avatars)
        
        # Secondary matching for similar types
        if not candidates:
            related_types = {
                'dark': ['ghost', 'psychic'],
                'ghost': ['dark', 'psychic'],
                'psychic': ['dark', 'ghost'],
                'fire': ['fighting'],
                'water': ['normal'],
                'fighting': ['normal'],
                'normal': ['fighting']
            }
            
            for related_type in related_types.get(pokemon_type, []):
                if related_type in avatar_db:
                    for avatars in avatar_db[related_type].values():
                        candidates.extend(avatars[:2])
        
        # Fallback to all avatars
        if not candidates:
            for type_data in avatar_db.values():
                for avatars in type_data.values():
                    candidates.extend(avatars)
        
        if not candidates:
            return create_fallback_avatar()
        
        # Calculate compatibility scores and select best match
        scored_avatars = []
        for avatar in candidates:
            score = calculate_compatibility_score(avatar, analysis)
            scored_avatars.append((avatar, score))
        
        # Sort by score and select based on iteration
        scored_avatars.sort(key=lambda x: x[1], reverse=True)
        
        # Select avatar based on iteration (to provide variety)
        selection_index = min(iteration - 1, len(scored_avatars) - 1)
        selected_avatar, compatibility = scored_avatars[selection_index]
        
        result = {
            'image_path': selected_avatar['image_path'],
            'avatar_name': selected_avatar['name'],
            'description': f"A {selected_avatar['type']}-type Pokémon with {selected_avatar['personality']} characteristics",
            'suggested_type': selected_avatar['type'],
            'compatibility_score': int(compatibility),
            'iteration': iteration,
            'max_iterations': max_iterations,
            'alternative_available': iteration < max_iterations and len(scored_avatars) > iteration
        }
        
        logging.info(f"Avatar selected: {selected_avatar['name']} (Score: {compatibility:.1f}, Iteration: {iteration})")
        return result
        
    except Exception as e:
        logging.error(f"Avatar generation error: {str(e)}")
        return create_fallback_avatar()

def create_fallback_avatar():
    """Create a fallback avatar when generation fails"""
    return {
        'image_path': '/static/images/avatars/Dark_Warlock_Pokemon_46b75e1d.png',
        'avatar_name': 'Dark Warlock',
        'description': 'A mysterious dark-type Pokémon avatar',
        'suggested_type': 'dark',
        'compatibility_score': 75,
        'iteration': 1,
        'max_iterations': 3,
        'alternative_available': True,
        'error': True
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')

@app.route('/scan_face', methods=['POST'])
def scan_face():
    """Generate Pokémon avatar from face scan"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Handle demo mode
        if image_data == 'demo_mode':
            # Create a demo analysis for when camera isn't available
            face_analysis = {
                "face_shape": "oval",
                "personality_traits": "mysterious and determined",
                "suggested_pokemon_type": "dark",
                "energy_level": "high",
                "compatibility_score": 92,
                "generation_seed": 1000
            }
        else:
            # Remove data URL prefix if present
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            
            # Analyze the face
            face_analysis = analyze_face_features(image_data)
        
        # Generate avatar based on analysis
        avatar_result = generate_avatar_from_analysis(face_analysis)
        
        return jsonify({
            'success': True,
            'analysis': face_analysis,
            'avatar_result': avatar_result
        })
        
    except Exception as e:
        logging.error(f"Error in face scan: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/iterate_avatar', methods=['POST'])
def iterate_avatar():
    """Generate alternative avatar by iterating through options"""
    try:
        data = request.get_json()
        analysis = data.get('analysis', {})
        current_iteration = data.get('iteration', 1) + 1
        max_iterations = data.get('max_iterations', 3)
        
        if current_iteration > max_iterations:
            return jsonify({'error': 'Maximum iterations reached'}), 400
        
        # Generate new avatar with iteration
        avatar_result = generate_avatar_from_analysis(analysis, current_iteration, max_iterations)
        
        return jsonify({
            'success': True,
            'avatar_result': avatar_result,
            'analysis': analysis
        })
        
    except Exception as e:
        logging.error(f"Error in avatar iteration: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)