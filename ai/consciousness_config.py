"""
Consciousness Configuration - Centralized Configuration for the 12-Module Consciousness Architecture

This module provides centralized configuration management for all consciousness modules:
- Module enable/disable flags
- Performance optimization settings
- Real-time processing parameters
- State persistence configuration
- Integration settings
- Blank slate vs standard mode configuration
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class ConsciousnessMode(Enum):
    """Consciousness operational modes"""
    BLANK_SLATE = "blank_slate"    # Starting from zero consciousness
    STANDARD = "standard"          # Normal consciousness operation
    ENHANCED = "enhanced"          # Enhanced consciousness features
    MINIMAL = "minimal"            # Minimal consciousness for performance

class ProcessingPriority(Enum):
    """Processing priority levels for consciousness modules"""
    CRITICAL = "critical"          # Critical for consciousness
    HIGH = "high"                 # Important for consciousness
    MEDIUM = "medium"             # Normal priority
    LOW = "low"                   # Low priority, can be throttled
    OPTIONAL = "optional"         # Optional features

@dataclass
class ModuleConfig:
    """Configuration for a single consciousness module"""
    enabled: bool = True
    priority: ProcessingPriority = ProcessingPriority.MEDIUM
    max_cpu_usage: float = 0.1  # Maximum CPU usage percentage
    update_interval: float = 1.0  # Update interval in seconds
    save_state: bool = True
    save_interval: int = 300  # Save interval in seconds
    debug_logging: bool = False
    performance_monitoring: bool = True

class ConsciousnessConfig:
    """
    Centralized configuration for the 12-module consciousness architecture.
    
    This class manages all configuration settings for consciousness modules,
    ensuring optimal performance and proper integration.
    """
    
    def __init__(self):
        # Core configuration
        self.mode = self._get_consciousness_mode()
        self.enable_real_time_processing = True
        self.enable_state_persistence = True
        self.enable_performance_monitoring = True
        self.enable_consciousness_logging = True
        
        # Performance settings
        self.max_total_cpu_usage = 0.4  # Maximum total CPU for consciousness (increased for 12 modules)
        self.consciousness_thread_priority = "normal"  # "low", "normal", "high"
        self.enable_adaptive_processing = True
        self.min_response_time_ms = 100  # Minimum response time requirement
        
        # Debugging and monitoring (initialize before modules)
        self.debug_mode = os.getenv('CONSCIOUSNESS_DEBUG', 'false').lower() == 'true'
        self.performance_profiling = False
        self.event_logging_level = "info"  # "debug", "info", "warning", "error"
        self.enable_consciousness_dashboard = False
        
        # Module configurations
        self.modules = self._initialize_module_configs()
        
        # Integration settings
        self.voice_integration_enabled = True
        self.llm_integration_enabled = True
        self.memory_integration_enabled = True
        self.emotion_response_modulation = True
        self.consciousness_response_enhancement = True
        
        # State persistence
        self.state_save_directory = Path("consciousness_states")
        self.enable_automatic_backup = True
        self.backup_interval_hours = 24
        self.max_backup_files = 7
        
        # Real-time constraints
        self.max_processing_delay_ms = 50
        self.enable_graceful_degradation = True
        self.fallback_to_simple_responses = True
        
        # Initialize based on mode
        self._apply_mode_settings()
    
    def _get_consciousness_mode(self) -> ConsciousnessMode:
        """Determine consciousness mode from environment or default"""
        mode_str = os.getenv('BUDDY_CONSCIOUSNESS_MODE', 'standard').lower()
        blank_slate = os.getenv('BUDDY_BLANK_SLATE', 'false').lower() == 'true'
        
        if blank_slate:
            return ConsciousnessMode.BLANK_SLATE
        
        mode_mapping = {
            'blank_slate': ConsciousnessMode.BLANK_SLATE,
            'minimal': ConsciousnessMode.MINIMAL,
            'standard': ConsciousnessMode.STANDARD,
            'enhanced': ConsciousnessMode.ENHANCED
        }
        
        return mode_mapping.get(mode_str, ConsciousnessMode.STANDARD)
    
    def _initialize_module_configs(self) -> Dict[str, ModuleConfig]:
        """Initialize configuration for all 12 consciousness modules"""
        modules = {}
        
        # 1. Global Workspace Theory Hub - Critical for consciousness coordination
        modules['global_workspace'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.CRITICAL,
            max_cpu_usage=0.05,
            update_interval=0.1,
            save_state=True,
            save_interval=300,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 2. Self-Model System - Critical for identity
        modules['self_model'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.CRITICAL,
            max_cpu_usage=0.03,
            update_interval=1.0,
            save_state=True,
            save_interval=600,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 3. Emotional Engine - High priority for human-like responses
        modules['emotion_engine'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.HIGH,
            max_cpu_usage=0.04,
            update_interval=0.5,
            save_state=True,
            save_interval=300,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 4. Motivation & Goals System - High priority for goal-oriented behavior
        modules['motivation_system'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.HIGH,
            max_cpu_usage=0.03,
            update_interval=2.0,
            save_state=True,
            save_interval=600,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 5. Inner Monologue Generator - Medium priority
        modules['inner_monologue'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.MEDIUM,
            max_cpu_usage=0.03,
            update_interval=3.0,
            save_state=True,
            save_interval=600,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 6. Temporal Awareness Module - High priority for memory formation
        modules['temporal_awareness'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.HIGH,
            max_cpu_usage=0.03,
            update_interval=1.0,
            save_state=True,
            save_interval=300,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 7. Subjective Experience Tracker - Medium priority
        modules['subjective_experience'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.MEDIUM,
            max_cpu_usage=0.02,
            update_interval=2.0,
            save_state=True,
            save_interval=600,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 8. Entropy & Uncertainty Engine - Medium priority for natural variation
        modules['entropy_system'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.MEDIUM,
            max_cpu_usage=0.02,
            update_interval=1.0,
            save_state=True,
            save_interval=600,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 9. Free Thought Engine - Low priority, autonomous thinking
        modules['free_thought_engine'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.LOW,
            max_cpu_usage=0.02,
            update_interval=5.0,
            save_state=True,
            save_interval=900,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 10. Narrative & Story Tracker - Medium priority
        modules['narrative_tracker'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.MEDIUM,
            max_cpu_usage=0.02,
            update_interval=10.0,
            save_state=True,
            save_interval=600,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 11. Attention & Focus Manager - High priority for selective consciousness
        modules['attention_focus_manager'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.HIGH,
            max_cpu_usage=0.03,
            update_interval=0.5,
            save_state=True,
            save_interval=300,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        # 12. Meta-Cognitive Monitor - Medium priority for thinking about thinking
        modules['metacognitive_monitor'] = ModuleConfig(
            enabled=True,
            priority=ProcessingPriority.MEDIUM,
            max_cpu_usage=0.02,
            update_interval=1.0,
            save_state=True,
            save_interval=300,
            debug_logging=self.debug_mode,
            performance_monitoring=True
        )
        
        return modules
    
    def _apply_mode_settings(self):
        """Apply settings based on consciousness mode"""
        if self.mode == ConsciousnessMode.BLANK_SLATE:
            # Blank slate mode - reduce initial complexity
            self.modules['free_thought_engine'].enabled = False  # Start without autonomous thoughts
            self.modules['narrative_tracker'].update_interval = 60.0  # Slower narrative building
            self.modules['inner_monologue'].update_interval = 10.0  # Less frequent thoughts initially
            
        elif self.mode == ConsciousnessMode.MINIMAL:
            # Minimal mode - optimize for performance
            self.max_total_cpu_usage = 0.15
            self.modules['free_thought_engine'].enabled = False
            self.modules['subjective_experience'].update_interval = 5.0
            self.modules['inner_monologue'].update_interval = 10.0
            self.modules['metacognitive_monitor'].update_interval = 5.0
            
        elif self.mode == ConsciousnessMode.ENHANCED:
            # Enhanced mode - full features
            self.max_total_cpu_usage = 0.5
            self.enable_consciousness_dashboard = True
            self.performance_profiling = True
            for module_config in self.modules.values():
                module_config.debug_logging = True
                module_config.performance_monitoring = True
    
    def is_module_enabled(self, module_name: str) -> bool:
        """Check if a consciousness module is enabled"""
        return self.modules.get(module_name, ModuleConfig()).enabled
    
    def get_module_config(self, module_name: str) -> ModuleConfig:
        """Get configuration for a specific module"""
        return self.modules.get(module_name, ModuleConfig())
    
    def set_module_enabled(self, module_name: str, enabled: bool):
        """Enable or disable a consciousness module"""
        if module_name in self.modules:
            self.modules[module_name].enabled = enabled
    
    def get_processing_priority(self, module_name: str) -> ProcessingPriority:
        """Get processing priority for a module"""
        return self.modules.get(module_name, ModuleConfig()).priority
    
    def should_save_state(self, module_name: str) -> bool:
        """Check if a module should save its state"""
        return (self.enable_state_persistence and 
                self.modules.get(module_name, ModuleConfig()).save_state)
    
    def get_save_interval(self, module_name: str) -> int:
        """Get save interval for a module in seconds"""
        return self.modules.get(module_name, ModuleConfig()).save_interval
    
    def get_update_interval(self, module_name: str) -> float:
        """Get update interval for a module in seconds"""
        return self.modules.get(module_name, ModuleConfig()).update_interval
    
    def get_max_cpu_usage(self, module_name: str) -> float:
        """Get maximum CPU usage for a module"""
        return self.modules.get(module_name, ModuleConfig()).max_cpu_usage
    
    def should_log_debug(self, module_name: str) -> bool:
        """Check if debug logging is enabled for a module"""
        return (self.debug_mode or 
                self.modules.get(module_name, ModuleConfig()).debug_logging)
    
    def should_monitor_performance(self, module_name: str) -> bool:
        """Check if performance monitoring is enabled for a module"""
        return (self.enable_performance_monitoring and
                self.modules.get(module_name, ModuleConfig()).performance_monitoring)
    
    def get_state_file_path(self, module_name: str, filename: str = None) -> Path:
        """Get state file path for a module"""
        self.state_save_directory.mkdir(exist_ok=True)
        
        if filename is None:
            filename = f"ai_{module_name}.json"
        
        return self.state_save_directory / filename
    
    def optimize_for_real_time(self):
        """Optimize configuration for real-time voice interaction"""
        self.max_processing_delay_ms = 25
        self.enable_graceful_degradation = True
        
        # Reduce update intervals for critical modules
        critical_modules = [name for name, config in self.modules.items() 
                          if config.priority == ProcessingPriority.CRITICAL]
        
        for module_name in critical_modules:
            current_interval = self.modules[module_name].update_interval
            self.modules[module_name].update_interval = min(current_interval, 0.5)
    
    def enable_development_mode(self):
        """Enable development mode with enhanced debugging"""
        self.debug_mode = True
        self.performance_profiling = True
        self.enable_consciousness_dashboard = True
        self.event_logging_level = "debug"
        
        for module_config in self.modules.values():
            module_config.debug_logging = True
            module_config.performance_monitoring = True
    
    def enable_production_mode(self):
        """Enable production mode with optimized performance"""
        self.debug_mode = False
        self.performance_profiling = False
        self.enable_consciousness_dashboard = False
        self.event_logging_level = "warning"
        
        for module_config in self.modules.values():
            module_config.debug_logging = False
    
    def get_enabled_modules(self) -> Dict[str, ModuleConfig]:
        """Get all enabled modules"""
        return {name: config for name, config in self.modules.items() if config.enabled}
    
    def get_consciousness_status(self) -> Dict[str, Any]:
        """Get overall consciousness configuration status"""
        enabled_modules = len([c for c in self.modules.values() if c.enabled])
        total_cpu_budget = sum(c.max_cpu_usage for c in self.modules.values() if c.enabled)
        
        return {
            "mode": self.mode.value,
            "enabled_modules": enabled_modules,
            "total_modules": len(self.modules),
            "total_cpu_budget": total_cpu_budget,
            "max_cpu_limit": self.max_total_cpu_usage,
            "real_time_processing": self.enable_real_time_processing,
            "state_persistence": self.enable_state_persistence,
            "performance_monitoring": self.enable_performance_monitoring,
            "debug_mode": self.debug_mode,
            "voice_integration": self.voice_integration_enabled,
            "llm_integration": self.llm_integration_enabled
        }
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate consciousness configuration"""
        issues = []
        warnings = []
        
        # Check CPU budget
        total_cpu = sum(c.max_cpu_usage for c in self.modules.values() if c.enabled)
        if total_cpu > self.max_total_cpu_usage:
            issues.append(f"Total CPU budget ({total_cpu:.2f}) exceeds limit ({self.max_total_cpu_usage:.2f})")
        
        # Check critical modules
        critical_modules = ['global_workspace', 'self_model']
        for module in critical_modules:
            if not self.modules.get(module, ModuleConfig()).enabled:
                issues.append(f"Critical module '{module}' is disabled")
        
        # Check update intervals
        for name, config in self.modules.items():
            if config.enabled and config.update_interval < 0.1:
                warnings.append(f"Module '{name}' has very fast update interval ({config.update_interval}s)")
        
        # Check state directory
        if self.enable_state_persistence:
            try:
                self.state_save_directory.mkdir(exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create state directory: {e}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "total_cpu_usage": total_cpu,
            "enabled_modules": len([c for c in self.modules.values() if c.enabled])
        }
    
    def export_config(self) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            "mode": self.mode.value,
            "performance": {
                "max_total_cpu_usage": self.max_total_cpu_usage,
                "enable_real_time_processing": self.enable_real_time_processing,
                "max_processing_delay_ms": self.max_processing_delay_ms,
                "enable_graceful_degradation": self.enable_graceful_degradation
            },
            "modules": {
                name: {
                    "enabled": config.enabled,
                    "priority": config.priority.value,
                    "max_cpu_usage": config.max_cpu_usage,
                    "update_interval": config.update_interval,
                    "save_state": config.save_state,
                    "save_interval": config.save_interval,
                    "debug_logging": config.debug_logging,
                    "performance_monitoring": config.performance_monitoring
                }
                for name, config in self.modules.items()
            },
            "integration": {
                "voice_integration_enabled": self.voice_integration_enabled,
                "llm_integration_enabled": self.llm_integration_enabled,
                "memory_integration_enabled": self.memory_integration_enabled,
                "emotion_response_modulation": self.emotion_response_modulation,
                "consciousness_response_enhancement": self.consciousness_response_enhancement
            },
            "debugging": {
                "debug_mode": self.debug_mode,
                "performance_profiling": self.performance_profiling,
                "event_logging_level": self.event_logging_level,
                "enable_consciousness_dashboard": self.enable_consciousness_dashboard
            }
        }


# Create global consciousness configuration instance
consciousness_config = ConsciousnessConfig()