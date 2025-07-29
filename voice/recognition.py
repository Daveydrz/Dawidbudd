# voice/recognition.py - Clean Centroid-based Voice Recognition with Clustering
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from config import DEBUG, SAMPLE_RATE, VOICE_CONFIDENCE_THRESHOLD
import time
from datetime import datetime
from voice.database import known_users, save_known_users, handle_same_name_collision

# Try enhanced modules first
try:
    from voice.speaker_profiles import enhanced_speaker_profiles
    from voice.voice_models import dual_voice_model_manager
    ENHANCED_AVAILABLE = True
    print("[Recognition] ✅ Enhanced modules available")
except ImportError:
    ENHANCED_AVAILABLE = False
    print("[Recognition] ⚠️ Using basic recognition")

# Fallback to basic resemblyzer
try:
    from resemblyzer import VoiceEncoder
    encoder = VoiceEncoder()
    RESEMBLYZER_AVAILABLE = True
except ImportError:
    RESEMBLYZER_AVAILABLE = False
    print("[Recognition] ⚠️ Resemblyzer not available")

def generate_voice_embedding(audio):
    """🎯 Enhanced voice embedding generation with clustering support"""
    if ENHANCED_AVAILABLE:
        # Use dual model system
        result = dual_voice_model_manager.generate_dual_embedding(audio)
        if result and 'resemblyzer' in result:
            return np.array(result['resemblyzer'])
        return None
    elif RESEMBLYZER_AVAILABLE:
        # Fallback to basic resemblyzer
        try:
            if len(audio) < SAMPLE_RATE:
                return None
            
            audio_float = audio.astype(np.float32)
            if np.max(np.abs(audio_float)) > 1.0:
                audio_float = audio_float / 32768.0
            
            embedding = encoder.embed_utterance(audio_float)
            return embedding if embedding is not None else None
        except Exception as e:
            if DEBUG:
                print(f"[Recognition] ❌ Basic embedding error: {e}")
            return None
    else:
        return None

def identify_speaker_with_confidence(audio):
    """✅ ENHANCED: Centroid-based speaker identification with clustering"""
    try:
        # Ensure database is loaded
        from voice.database import ensure_database_loaded, known_users, anonymous_clusters, save_known_users
        ensure_database_loaded()
        
        # Generate embedding for the audio
        embedding = generate_voice_embedding(audio)
        if embedding is None:
            return "UNKNOWN", 0.0
        
        # ✅ STEP 1: Check against known users using centroid clustering
        best_user = None
        best_confidence = 0.0
        
        for username, profile in known_users.items():
            if isinstance(profile, dict) and 'embeddings' in profile:
                # Calculate centroid of all embeddings for this user
                embeddings = profile['embeddings']
                if embeddings and len(embeddings) > 0:
                    embeddings_np = [np.array(emb) if isinstance(emb, list) else emb for emb in embeddings]
                    centroid = np.mean(embeddings_np, axis=0)
                    similarity = cosine_similarity([embedding], [centroid])[0][0]
                    
                    if similarity > best_confidence:
                        best_confidence = similarity
                        best_user = username
            elif isinstance(profile, list) and len(profile) == 256:
                # Legacy single embedding format
                similarity = cosine_similarity([embedding], [profile])[0][0]
                if similarity > best_confidence:
                    best_confidence = similarity
                    best_user = username
        
        # If confidence is high enough, return known user
        if best_confidence > VOICE_CONFIDENCE_THRESHOLD:
            print(f"[Recognition] ✅ Recognized user: {best_user} (confidence: {best_confidence:.3f})")
            return best_user, best_confidence
        
        # ✅ STEP 2: Check against anonymous clusters
        cluster_match, cluster_confidence = check_anonymous_clusters(audio, embedding)
        if cluster_match != "UNKNOWN" and cluster_confidence > 0.6:
            print(f"[Recognition] 🔍 Matched anonymous cluster: {cluster_match} (confidence: {cluster_confidence:.3f})")
            return cluster_match, cluster_confidence
        
        # ✅ STEP 3: Create new anonymous cluster if no match
        new_cluster_id = create_new_anonymous_cluster(audio, embedding)
        if new_cluster_id:
            print(f"[Recognition] 🆕 Created new anonymous cluster: {new_cluster_id}")
            return new_cluster_id, 0.9  # High confidence for new cluster creation
        
        return "Anonymous_Speaker", 0.5
        
    except Exception as e:
        print(f"[Recognition] ❌ Error in identification: {e}")
        return "UNKNOWN", 0.0

def check_anonymous_clusters(audio, embedding=None):
    """✅ Enhanced anonymous cluster checking with centroid-based matching"""
    try:
        from voice.database import anonymous_clusters, load_known_users
        
        # Ensure anonymous_clusters is loaded
        if not anonymous_clusters:
            load_known_users()
        
        # Generate embedding if not provided
        if embedding is None:
            embedding = generate_voice_embedding(audio)
            if embedding is None:
                return "UNKNOWN", 0.0
        
        best_cluster = None
        best_confidence = 0.0
        
        for cluster_id, cluster_data in anonymous_clusters.items():
            if isinstance(cluster_data, dict) and 'embeddings' in cluster_data:
                embeddings = cluster_data['embeddings']
                if embeddings and len(embeddings) > 0:
                    # Calculate centroid of cluster embeddings
                    embeddings_np = [np.array(emb) if isinstance(emb, list) else emb for emb in embeddings]
                    centroid = np.mean(embeddings_np, axis=0)
                    similarity = cosine_similarity([embedding], [centroid])[0][0]
                    
                    if similarity > best_confidence:
                        best_confidence = similarity
                        best_cluster = cluster_id
        
        # Return best match if confidence is high enough
        if best_confidence > 0.6:  # Lower threshold for anonymous clusters
            return best_cluster, best_confidence
        
        return "UNKNOWN", 0.0
        
    except Exception as e:
        print(f"[Recognition] ❌ Error checking anonymous clusters: {e}")
        return "UNKNOWN", 0.0

def create_new_anonymous_cluster(audio, embedding):
    """✅ Create a new anonymous cluster for unrecognized voice"""
    try:
        from voice.database import anonymous_clusters, save_known_users
        
        # Generate unique cluster ID
        cluster_count = len(anonymous_clusters) + 1
        cluster_id = f"Anonymous_{cluster_count:03d}"
        
        # Ensure unique ID
        while cluster_id in anonymous_clusters:
            cluster_count += 1
            cluster_id = f"Anonymous_{cluster_count:03d}"
        
        # Create cluster data
        cluster_data = {
            'embeddings': [embedding.tolist()],
            'created_at': time.time(),
            'sample_count': 1,
            'quality_scores': [0.8],  # Assume good quality for new cluster
            'last_updated': time.time(),
            'linked_user': None  # Will be set when user reveals their identity
        }
        
        # Add to anonymous clusters
        anonymous_clusters[cluster_id] = cluster_data
        save_known_users()
        
        print(f"[Recognition] 🆕 Created anonymous cluster: {cluster_id}")
        return cluster_id
        
    except Exception as e:
        print(f"[Recognition] ❌ Error creating anonymous cluster: {e}")
        return None

def link_anonymous_cluster_to_user(cluster_id: str, username: str):
    """Link an anonymous cluster to a named user"""
    try:
        from voice.database import anonymous_clusters, known_users, save_known_users
        
        if cluster_id not in anonymous_clusters:
            print(f"[Recognition] ❌ Cluster {cluster_id} not found")
            return False
        
        cluster_data = anonymous_clusters[cluster_id]
        
        # Create or update user profile
        if username not in known_users:
            known_users[username] = {
                'embeddings': [],
                'created_at': time.time(),
                'display_name': username,
                'voice_samples': 0,
                'quality_scores': [],
                'last_interaction': time.time()
            }
        
        # Transfer embeddings from cluster to user
        user_profile = known_users[username]
        cluster_embeddings = cluster_data.get('embeddings', [])
        
        if 'embeddings' not in user_profile:
            user_profile['embeddings'] = []
        
        # Add cluster embeddings to user profile
        user_profile['embeddings'].extend(cluster_embeddings)
        user_profile['voice_samples'] = len(user_profile['embeddings'])
        
        # Transfer quality scores
        if 'quality_scores' not in user_profile:
            user_profile['quality_scores'] = []
        user_profile['quality_scores'].extend(cluster_data.get('quality_scores', []))
        
        # Mark cluster as linked
        cluster_data['linked_user'] = username
        cluster_data['linked_at'] = time.time()
        
        save_known_users()
        
        print(f"[Recognition] 🔗 Linked cluster {cluster_id} to user {username}")
        print(f"[Recognition] 📊 User now has {len(user_profile['embeddings'])} voice samples")
        
        return True
        
    except Exception as e:
        print(f"[Recognition] ❌ Error linking cluster to user: {e}")
        return False

def identify_speaker(audio):
    """Wrapper function for backward compatibility"""
    identified_user, confidence = identify_speaker_with_confidence(audio)
    return identified_user

# Additional utility functions
def add_voice_sample_to_user(username, audio):
    """Add a voice sample to an existing user profile"""
    try:
        from voice.database import known_users, save_known_users
        
        embedding = generate_voice_embedding(audio)
        if embedding is None:
            return False
        
        if username not in known_users:
            known_users[username] = {'embeddings': []}
        
        user_profile = known_users[username]
        if isinstance(user_profile, dict):
            if 'embeddings' not in user_profile:
                user_profile['embeddings'] = []
            user_profile['embeddings'].append(embedding.tolist())
        else:
            # Convert legacy format
            known_users[username] = {
                'embeddings': [user_profile, embedding.tolist()],
                'created_at': time.time()
            }
        
        save_known_users()
        print(f"[Recognition] ✅ Added voice sample to user: {username}")
        return True
        
    except Exception as e:
        print(f"[Recognition] ❌ Error adding voice sample: {e}")
        return False

def link_anonymous_cluster_to_user(cluster_id, username):
    """Link an anonymous cluster to a named user"""
    try:
        from voice.database import anonymous_clusters, known_users, save_known_users
        
        if cluster_id not in anonymous_clusters:
            print(f"[Recognition] ❌ Cluster {cluster_id} not found")
            return False
        
        cluster_data = anonymous_clusters[cluster_id]
        cluster_embeddings = cluster_data.get('embeddings', [])
        
        # Create or update user profile
        if username not in known_users:
            known_users[username] = {'embeddings': []}
        
        user_profile = known_users[username]
        if isinstance(user_profile, dict):
            if 'embeddings' not in user_profile:
                user_profile['embeddings'] = []
            user_profile['embeddings'].extend(cluster_embeddings)
        else:
            # Convert legacy format
            known_users[username] = {
                'embeddings': [user_profile] + cluster_embeddings,
                'created_at': time.time()
            }
        
        # Remove from anonymous clusters
        del anonymous_clusters[cluster_id]
        save_known_users()
        
        print(f"[Recognition] 🔗 Linked cluster {cluster_id} to user {username}")
        return True
        
    except Exception as e:
        print(f"[Recognition] ❌ Error linking cluster to user: {e}")
        return False