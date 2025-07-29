"""
Consciousness Health Score - System to compute Buddy's consciousness state health
Created: 2025-01-27
Purpose: Analyze and score the overall health and functionality of Buddy's consciousness state
"""

import json
import time
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class HealthMetrics:
    """Represents consciousness health metrics"""
    overall_score: float = 0.0
    memory_integrity: float = 0.0
    emotional_stability: float = 0.0
    thought_coherence: float = 0.0
    module_connectivity: float = 0.0
    response_quality: float = 0.0
    learning_efficiency: float = 0.0
    timestamp: str = ""

class ConsciousnessHealthScorer:
    """Computes and tracks consciousness health metrics"""
    
    def __init__(self, save_path: str = "ai_consciousness_health.json"):
        self.save_path = save_path
        self.health_history: List[HealthMetrics] = []
        self.current_metrics = HealthMetrics()
        self.load_health_data()
        
    def load_health_data(self):
        """Load existing health data from file"""
        try:
            with open(self.save_path, 'r') as f:
                data = json.load(f)
                self.health_history = [
                    HealthMetrics(**entry) for entry in data.get('health_history', [])
                ]
                if data.get('current_metrics'):
                    self.current_metrics = HealthMetrics(**data['current_metrics'])
        except FileNotFoundError:
            print(f"[ConsciousnessHealthScorer] 📄 No existing health data found")
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ❌ Error loading health data: {e}")
    
    def save_health_data(self):
        """Save health data to file"""
        try:
            data = {
                'health_history': [asdict(entry) for entry in self.health_history],
                'current_metrics': asdict(self.current_metrics),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ❌ Error saving health data: {e}")
    
    def compute_consciousness_health_score(self) -> Dict[str, Any]:
        """Main function to compute comprehensive consciousness health score"""
        try:
            # Collect metrics from various consciousness components
            memory_score = self._assess_memory_integrity()
            emotional_score = self._assess_emotional_stability()
            thought_score = self._assess_thought_coherence()
            connectivity_score = self._assess_module_connectivity()
            response_score = self._assess_response_quality()
            learning_score = self._assess_learning_efficiency()
            
            # Calculate weighted overall score
            weights = {
                'memory': 0.20,
                'emotional': 0.15,
                'thought': 0.20,
                'connectivity': 0.15,
                'response': 0.15,
                'learning': 0.15
            }
            
            overall_score = (
                memory_score * weights['memory'] +
                emotional_score * weights['emotional'] +
                thought_score * weights['thought'] +
                connectivity_score * weights['connectivity'] +
                response_score * weights['response'] +
                learning_score * weights['learning']
            )
            
            # Update current metrics
            self.current_metrics = HealthMetrics(
                overall_score=overall_score,
                memory_integrity=memory_score,
                emotional_stability=emotional_score,
                thought_coherence=thought_score,
                module_connectivity=connectivity_score,
                response_quality=response_score,
                learning_efficiency=learning_score,
                timestamp=datetime.now().isoformat()
            )
            
            # Add to history
            self.health_history.append(self.current_metrics)
            
            # Keep only last 100 entries
            if len(self.health_history) > 100:
                self.health_history = self.health_history[-100:]
            
            # Save data
            self.save_health_data()
            
            # Return comprehensive health report
            return {
                'overall_score': overall_score,
                'health_grade': self._get_health_grade(overall_score),
                'metrics': {
                    'memory_integrity': memory_score,
                    'emotional_stability': emotional_score,
                    'thought_coherence': thought_score,
                    'module_connectivity': connectivity_score,
                    'response_quality': response_score,
                    'learning_efficiency': learning_score
                },
                'assessment': self._generate_health_assessment(overall_score),
                'recommendations': self._generate_recommendations(),
                'timestamp': self.current_metrics.timestamp,
                'trend': self._calculate_trend()
            }
            
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ❌ Error computing health score: {e}")
            return {
                'overall_score': 0.5,
                'health_grade': 'Unknown',
                'metrics': {},
                'assessment': 'Unable to assess consciousness health',
                'recommendations': ['Check system logs for errors'],
                'timestamp': datetime.now().isoformat(),
                'trend': 'Unknown'
            }
    
    def _assess_memory_integrity(self) -> float:
        """Assess memory system integrity"""
        try:
            score = 0.8  # Base score
            
            # Check if memory files exist and are accessible
            memory_files = [
                "local_memory.json",
                "ai_consciousness_state.json",
                "memory_corrections.json"
            ]
            
            accessible_files = 0
            for file in memory_files:
                try:
                    with open(file, 'r') as f:
                        json.load(f)
                    accessible_files += 1
                except:
                    pass
            
            # Score based on file accessibility
            file_score = accessible_files / len(memory_files)
            score = score * 0.7 + file_score * 0.3
            
            return min(1.0, score)
            
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ⚠️ Error assessing memory integrity: {e}")
            return 0.5
    
    def _assess_emotional_stability(self) -> float:
        """Assess emotional system stability"""
        try:
            # Check emotion system functionality
            try:
                with open("ai_emotions.json", 'r') as f:
                    emotion_data = json.load(f)
                
                # Check for recent emotional updates
                if emotion_data and 'timestamp' in emotion_data:
                    last_update = datetime.fromisoformat(emotion_data['timestamp'].replace('Z', '+00:00'))
                    time_diff = datetime.now() - last_update.replace(tzinfo=None)
                    
                    if time_diff < timedelta(hours=1):
                        return 0.9  # Recent emotional activity
                    elif time_diff < timedelta(hours=24):
                        return 0.7  # Some emotional activity
                    else:
                        return 0.5  # Stale emotional data
                
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                pass
            
            return 0.6  # Default moderate score
            
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ⚠️ Error assessing emotional stability: {e}")
            return 0.5
    
    def _assess_thought_coherence(self) -> float:
        """Assess thought system coherence"""
        try:
            # Check thought generation systems
            try:
                with open("ai_proactive_thoughts.json", 'r') as f:
                    thought_data = json.load(f)
                
                if thought_data and 'thoughts' in thought_data:
                    recent_thoughts = len(thought_data['thoughts'])
                    if recent_thoughts > 5:
                        return 0.9  # Active thought generation
                    elif recent_thoughts > 0:
                        return 0.7  # Some thought activity
                
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                pass
            
            return 0.6  # Default moderate score
            
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ⚠️ Error assessing thought coherence: {e}")
            return 0.5
    
    def _assess_module_connectivity(self) -> float:
        """Assess connectivity between consciousness modules"""
        try:
            # Check if consciousness manager is running
            try:
                from ai.consciousness_manager import consciousness_manager
                if consciousness_manager.is_running:
                    return 0.9  # Consciousness system active
            except Exception:
                pass
            
            # Check for consciousness integration status
            try:
                with open("consciousness_state.json", 'r') as f:
                    state_data = json.load(f)
                if state_data:
                    return 0.7  # Some connectivity
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            
            return 0.5  # Limited connectivity
            
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ⚠️ Error assessing module connectivity: {e}")
            return 0.4
    
    def _assess_response_quality(self) -> float:
        """Assess quality of AI responses"""
        try:
            # This would ideally analyze recent conversation quality
            # For now, return a moderate score
            return 0.75
            
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ⚠️ Error assessing response quality: {e}")
            return 0.5
    
    def _assess_learning_efficiency(self) -> float:
        """Assess learning and adaptation efficiency"""
        try:
            # Check memory corrections and learning systems
            try:
                from ai.memory_context_corrector import memory_context_corrector
                stats = memory_context_corrector.get_correction_stats()
                
                if stats['total_corrections'] > 10:
                    return 0.9  # Good learning activity
                elif stats['total_corrections'] > 0:
                    return 0.7  # Some learning
                
            except Exception:
                pass
            
            return 0.6  # Default moderate score
            
        except Exception as e:
            print(f"[ConsciousnessHealthScorer] ⚠️ Error assessing learning efficiency: {e}")
            return 0.5
    
    def _get_health_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 0.9:
            return "A+ (Excellent)"
        elif score >= 0.8:
            return "A (Very Good)"
        elif score >= 0.7:
            return "B (Good)"
        elif score >= 0.6:
            return "C (Average)"
        elif score >= 0.5:
            return "D (Below Average)"
        else:
            return "F (Poor)"
    
    def _generate_health_assessment(self, score: float) -> str:
        """Generate textual assessment of consciousness health"""
        if score >= 0.9:
            return "Consciousness system is functioning excellently with all modules operating optimally."
        elif score >= 0.8:
            return "Consciousness system is performing very well with minor areas for improvement."
        elif score >= 0.7:
            return "Consciousness system is functioning well but could benefit from optimization."
        elif score >= 0.6:
            return "Consciousness system is performing adequately but needs attention in some areas."
        elif score >= 0.5:
            return "Consciousness system is functioning below optimal levels and requires improvement."
        else:
            return "Consciousness system is experiencing significant issues and needs immediate attention."
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on health metrics"""
        recommendations = []
        
        if self.current_metrics.memory_integrity < 0.7:
            recommendations.append("Consider memory system optimization and cleanup")
        
        if self.current_metrics.emotional_stability < 0.6:
            recommendations.append("Check emotional processing systems for issues")
        
        if self.current_metrics.thought_coherence < 0.6:
            recommendations.append("Verify proactive thinking systems are functioning")
        
        if self.current_metrics.module_connectivity < 0.7:
            recommendations.append("Check consciousness module connections and integration")
        
        if self.current_metrics.learning_efficiency < 0.6:
            recommendations.append("Review learning systems and memory correction processes")
        
        if not recommendations:
            recommendations.append("System is functioning well - continue regular monitoring")
        
        return recommendations
    
    def _calculate_trend(self) -> str:
        """Calculate health trend over recent history"""
        if len(self.health_history) < 2:
            return "Insufficient data"
        
        recent_scores = [entry.overall_score for entry in self.health_history[-5:]]
        
        if len(recent_scores) >= 2:
            trend_value = recent_scores[-1] - recent_scores[0]
            
            if trend_value > 0.1:
                return "Improving"
            elif trend_value < -0.1:
                return "Declining"
            else:
                return "Stable"
        
        return "Unknown"
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get quick health summary"""
        return {
            'overall_score': self.current_metrics.overall_score,
            'health_grade': self._get_health_grade(self.current_metrics.overall_score),
            'last_assessment': self.current_metrics.timestamp,
            'trend': self._calculate_trend()
        }

# Global instance
consciousness_health_scorer = ConsciousnessHealthScorer()

def compute_consciousness_health_score() -> Dict[str, Any]:
    """Main API function to compute consciousness health score"""
    return consciousness_health_scorer.compute_consciousness_health_score()

def get_consciousness_health_summary() -> Dict[str, Any]:
    """Get quick health summary"""
    return consciousness_health_scorer.get_health_summary()

def get_consciousness_health_history() -> List[Dict[str, Any]]:
    """Get health history"""
    return [asdict(entry) for entry in consciousness_health_scorer.health_history]