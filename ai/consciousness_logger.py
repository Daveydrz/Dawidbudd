"""
Consciousness Event Logger - Advanced Logging System for Consciousness Architecture

This module provides comprehensive logging for consciousness events:
- Structured event logging for all consciousness modules
- Performance monitoring and analysis
- Real-time consciousness state tracking
- Integration with voice and LLM systems
- Event correlation and pattern detection
"""

import logging
import json
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
import threading
from collections import deque, defaultdict

class EventLevel(Enum):
    """Consciousness event severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class EventCategory(Enum):
    """Categories of consciousness events"""
    CONSCIOUSNESS = "consciousness"
    ATTENTION = "attention"
    EMOTION = "emotion"
    MEMORY = "memory"
    REASONING = "reasoning"
    PERCEPTION = "perception"
    RESPONSE = "response"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    ERROR = "error"

@dataclass
class ConsciousnessEvent:
    """A single consciousness event"""
    timestamp: datetime
    module: str
    event_type: str
    category: EventCategory
    level: EventLevel
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    duration_ms: Optional[float] = None
    user_context: Optional[str] = None
    conversation_id: Optional[str] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

@dataclass
class PerformanceMetrics:
    """Performance metrics for consciousness modules"""
    module: str
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    processing_time_ms: float = 0.0
    events_per_second: float = 0.0
    error_rate: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class ConsciousnessState:
    """Current state of consciousness system"""
    timestamp: datetime
    active_modules: List[str]
    primary_focus: Optional[str]
    cognitive_load: float
    emotional_state: str
    attention_level: float
    processing_mode: str
    performance_overall: float

class ConsciousnessEventLogger:
    """
    Advanced event logging system for consciousness architecture.
    
    Provides structured logging, performance monitoring, and real-time
    analysis of consciousness events across all modules.
    """
    
    def __init__(self, log_file: str = "consciousness_events.log",
                 json_log_file: str = "consciousness_events.json",
                 max_events_memory: int = 10000):
        
        # File paths
        self.log_file = Path(log_file)
        self.json_log_file = Path(json_log_file)
        
        # In-memory event storage
        self.events: deque = deque(maxlen=max_events_memory)
        self.performance_metrics: Dict[str, PerformanceMetrics] = {}
        self.consciousness_states: deque = deque(maxlen=1000)
        
        # Event statistics
        self.event_counts: defaultdict = defaultdict(int)
        self.module_stats: defaultdict = defaultdict(lambda: defaultdict(int))
        self.error_counts: defaultdict = defaultdict(int)
        
        # Configuration
        self.log_level = EventLevel.INFO
        self.enable_file_logging = True
        self.enable_json_logging = True
        self.enable_console_logging = True
        self.enable_performance_monitoring = True
        
        # Real-time monitoring
        self.is_monitoring = False
        self.monitor_thread = None
        self.event_callbacks: List[Callable] = []
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Setup logging
        self._setup_logging()
        
        # Start monitoring
        self.start_monitoring()
        
        logging.info("[ConsciousnessLogger] 📝 Consciousness event logger initialized")
    
    def _setup_logging(self):
        """Setup file and console logging"""
        try:
            # Create log directory if needed
            self.log_file.parent.mkdir(exist_ok=True)
            self.json_log_file.parent.mkdir(exist_ok=True)
            
            # Setup standard logging
            log_format = '[%(asctime)s] [%(levelname)s] [Consciousness] %(message)s'
            logging.basicConfig(
                level=logging.INFO,
                format=log_format,
                handlers=[
                    logging.FileHandler(self.log_file),
                    logging.StreamHandler() if self.enable_console_logging else logging.NullHandler()
                ]
            )
            
        except Exception as e:
            print(f"[ConsciousnessLogger] ❌ Failed to setup logging: {e}")
    
    def start_monitoring(self):
        """Start real-time consciousness monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop real-time consciousness monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
    
    def log_event(self, module: str, event_type: str, message: str,
                  category: EventCategory = EventCategory.CONSCIOUSNESS,
                  level: EventLevel = EventLevel.INFO,
                  details: Dict[str, Any] = None,
                  duration_ms: float = None,
                  user_context: str = None,
                  conversation_id: str = None,
                  performance_metrics: Dict[str, float] = None,
                  tags: List[str] = None):
        """Log a consciousness event"""
        
        event = ConsciousnessEvent(
            timestamp=datetime.now(),
            module=module,
            event_type=event_type,
            category=category,
            level=level,
            message=message,
            details=details or {},
            duration_ms=duration_ms,
            user_context=user_context,
            conversation_id=conversation_id,
            performance_metrics=performance_metrics or {},
            tags=tags or []
        )
        
        with self.lock:
            # Add to memory
            self.events.append(event)
            
            # Update statistics
            self.event_counts[f"{module}:{event_type}"] += 1
            self.module_stats[module][event_type] += 1
            
            if level in [EventLevel.ERROR, EventLevel.CRITICAL]:
                self.error_counts[module] += 1
            
            # Update performance metrics
            if performance_metrics:
                self._update_performance_metrics(module, performance_metrics)
        
        # Log to files
        self._write_to_logs(event)
        
        # Trigger callbacks
        for callback in self.event_callbacks:
            try:
                callback(event)
            except Exception as e:
                logging.error(f"[ConsciousnessLogger] Callback error: {e}")
        
        # Console output for important events
        if level.value in ['warning', 'error', 'critical'] and self.enable_console_logging:
            log_message = f"[{module}] {event_type}: {message}"
            if level == EventLevel.WARNING:
                logging.warning(log_message)
            elif level == EventLevel.ERROR:
                logging.error(log_message)
            elif level == EventLevel.CRITICAL:
                logging.critical(log_message)
    
    def log_consciousness_state(self, active_modules: List[str],
                              primary_focus: str = None,
                              cognitive_load: float = 0.0,
                              emotional_state: str = "neutral",
                              attention_level: float = 0.5,
                              processing_mode: str = "conscious",
                              performance_overall: float = 1.0):
        """Log current consciousness state"""
        
        state = ConsciousnessState(
            timestamp=datetime.now(),
            active_modules=active_modules,
            primary_focus=primary_focus,
            cognitive_load=cognitive_load,
            emotional_state=emotional_state,
            attention_level=attention_level,
            processing_mode=processing_mode,
            performance_overall=performance_overall
        )
        
        with self.lock:
            self.consciousness_states.append(state)
        
        # Log as event
        self.log_event(
            module="consciousness_system",
            event_type="state_update",
            message=f"Consciousness state updated: {len(active_modules)} modules, focus: {primary_focus}",
            category=EventCategory.CONSCIOUSNESS,
            level=EventLevel.DEBUG,
            details={
                "active_modules": active_modules,
                "primary_focus": primary_focus,
                "cognitive_load": cognitive_load,
                "emotional_state": emotional_state,
                "attention_level": attention_level,
                "processing_mode": processing_mode,
                "performance_overall": performance_overall
            }
        )
    
    def log_voice_integration_event(self, event_type: str, message: str,
                                   user_id: str = None, text: str = None,
                                   audio_quality: float = None,
                                   processing_time_ms: float = None):
        """Log voice integration events"""
        details = {}
        if user_id:
            details["user_id"] = user_id
        if text:
            details["text"] = text[:100]  # Truncate long text
        if audio_quality:
            details["audio_quality"] = audio_quality
        
        self.log_event(
            module="voice_integration",
            event_type=event_type,
            message=message,
            category=EventCategory.INTEGRATION,
            level=EventLevel.INFO,
            details=details,
            duration_ms=processing_time_ms,
            user_context=user_id
        )
    
    def log_llm_integration_event(self, event_type: str, message: str,
                                 prompt: str = None, response: str = None,
                                 tokens_used: int = None,
                                 processing_time_ms: float = None,
                                 user_context: str = None):
        """Log LLM integration events"""
        details = {}
        if prompt:
            details["prompt_length"] = len(prompt)
            details["prompt_preview"] = prompt[:50]
        if response:
            details["response_length"] = len(response)
            details["response_preview"] = response[:50]
        if tokens_used:
            details["tokens_used"] = tokens_used
        
        self.log_event(
            module="llm_integration",
            event_type=event_type,
            message=message,
            category=EventCategory.INTEGRATION,
            level=EventLevel.INFO,
            details=details,
            duration_ms=processing_time_ms,
            user_context=user_context
        )
    
    def log_performance_event(self, module: str, cpu_usage: float = None,
                            memory_usage: float = None, processing_time_ms: float = None,
                            throughput: float = None):
        """Log performance metrics"""
        metrics = {}
        if cpu_usage is not None:
            metrics["cpu_usage"] = cpu_usage
        if memory_usage is not None:
            metrics["memory_usage"] = memory_usage
        if processing_time_ms is not None:
            metrics["processing_time_ms"] = processing_time_ms
        if throughput is not None:
            metrics["throughput"] = throughput
        
        self.log_event(
            module=module,
            event_type="performance_metrics",
            message=f"Performance metrics updated for {module}",
            category=EventCategory.PERFORMANCE,
            level=EventLevel.DEBUG,
            performance_metrics=metrics
        )
    
    def log_error(self, module: str, error_type: str, error_message: str,
                  exception: Exception = None, context: Dict[str, Any] = None):
        """Log consciousness errors"""
        details = {
            "error_type": error_type,
            "context": context or {}
        }
        
        if exception:
            details["exception"] = str(exception)
            details["exception_type"] = type(exception).__name__
        
        self.log_event(
            module=module,
            event_type="error",
            message=error_message,
            category=EventCategory.ERROR,
            level=EventLevel.ERROR,
            details=details
        )
    
    def get_recent_events(self, modules: List[str] = None,
                         categories: List[EventCategory] = None,
                         levels: List[EventLevel] = None,
                         time_window_minutes: int = 60,
                         limit: int = 100) -> List[ConsciousnessEvent]:
        """Get recent consciousness events with filtering"""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
            
            filtered_events = []
            for event in reversed(self.events):
                if event.timestamp < cutoff_time:
                    break
                
                # Apply filters
                if modules and event.module not in modules:
                    continue
                if categories and event.category not in categories:
                    continue
                if levels and event.level not in levels:
                    continue
                
                filtered_events.append(event)
                
                if len(filtered_events) >= limit:
                    break
            
            return list(reversed(filtered_events))
    
    def get_module_statistics(self, module: str = None,
                            time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get statistics for consciousness modules"""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
            
            if module:
                # Statistics for specific module
                module_events = [e for e in self.events 
                               if e.module == module and e.timestamp >= cutoff_time]
                
                if not module_events:
                    return {"error": "No events found for module"}
                
                error_events = [e for e in module_events if e.level in [EventLevel.ERROR, EventLevel.CRITICAL]]
                
                return {
                    "module": module,
                    "total_events": len(module_events),
                    "error_count": len(error_events),
                    "error_rate": len(error_events) / len(module_events) if module_events else 0,
                    "event_types": list(set(e.event_type for e in module_events)),
                    "performance_metrics": self.performance_metrics.get(module, PerformanceMetrics(module))
                }
            else:
                # Overall statistics
                recent_events = [e for e in self.events if e.timestamp >= cutoff_time]
                modules_active = list(set(e.module for e in recent_events))
                
                return {
                    "total_events": len(recent_events),
                    "active_modules": modules_active,
                    "modules_count": len(modules_active),
                    "error_rate": len([e for e in recent_events 
                                     if e.level in [EventLevel.ERROR, EventLevel.CRITICAL]]) / len(recent_events) if recent_events else 0,
                    "events_per_minute": len(recent_events) / time_window_minutes if time_window_minutes > 0 else 0
                }
    
    def get_consciousness_timeline(self, time_window_minutes: int = 60) -> List[Dict[str, Any]]:
        """Get consciousness activity timeline"""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
            
            timeline = []
            for state in self.consciousness_states:
                if state.timestamp >= cutoff_time:
                    timeline.append({
                        "timestamp": state.timestamp.isoformat(),
                        "active_modules": state.active_modules,
                        "primary_focus": state.primary_focus,
                        "cognitive_load": state.cognitive_load,
                        "emotional_state": state.emotional_state,
                        "attention_level": state.attention_level,
                        "processing_mode": state.processing_mode,
                        "performance_overall": state.performance_overall
                    })
            
            return sorted(timeline, key=lambda x: x["timestamp"])
    
    def register_event_callback(self, callback: Callable[[ConsciousnessEvent], None]):
        """Register a callback for real-time event processing"""
        self.event_callbacks.append(callback)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        with self.lock:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "modules": {},
                "overall": {
                    "total_events": len(self.events),
                    "error_rate": 0.0,
                    "average_cpu_usage": 0.0,
                    "average_memory_usage": 0.0
                }
            }
            
            # Module-specific performance
            total_cpu = 0.0
            total_memory = 0.0
            module_count = 0
            
            for module, metrics in self.performance_metrics.items():
                summary["modules"][module] = asdict(metrics)
                total_cpu += metrics.cpu_usage
                total_memory += metrics.memory_usage
                module_count += 1
            
            # Overall averages
            if module_count > 0:
                summary["overall"]["average_cpu_usage"] = total_cpu / module_count
                summary["overall"]["average_memory_usage"] = total_memory / module_count
            
            # Calculate error rate
            error_events = len([e for e in self.events 
                              if e.level in [EventLevel.ERROR, EventLevel.CRITICAL]])
            if len(self.events) > 0:
                summary["overall"]["error_rate"] = error_events / len(self.events)
            
            return summary
    
    def _update_performance_metrics(self, module: str, metrics: Dict[str, float]):
        """Update performance metrics for a module"""
        if module not in self.performance_metrics:
            self.performance_metrics[module] = PerformanceMetrics(module=module)
        
        perf = self.performance_metrics[module]
        
        # Update metrics
        if "cpu_usage" in metrics:
            perf.cpu_usage = metrics["cpu_usage"]
        if "memory_usage" in metrics:
            perf.memory_usage = metrics["memory_usage"]
        if "processing_time_ms" in metrics:
            perf.processing_time_ms = metrics["processing_time_ms"]
        if "events_per_second" in metrics:
            perf.events_per_second = metrics["events_per_second"]
        if "error_rate" in metrics:
            perf.error_rate = metrics["error_rate"]
        
        perf.last_updated = datetime.now()
    
    def _write_to_logs(self, event: ConsciousnessEvent):
        """Write event to log files"""
        try:
            # Standard log format
            if self.enable_file_logging:
                log_message = f"[{event.module}] {event.event_type}: {event.message}"
                logging.info(log_message)
            
            # JSON log format
            if self.enable_json_logging:
                event_dict = asdict(event)
                event_dict["timestamp"] = event.timestamp.isoformat()
                event_dict["category"] = event.category.value
                event_dict["level"] = event.level.value
                
                with open(self.json_log_file, 'a') as f:
                    f.write(json.dumps(event_dict) + '\n')
        
        except Exception as e:
            print(f"[ConsciousnessLogger] ❌ Failed to write to logs: {e}")
    
    def _monitoring_loop(self):
        """Real-time monitoring loop"""
        logging.info("[ConsciousnessLogger] 🔄 Monitoring loop started")
        
        while self.is_monitoring:
            try:
                # Periodic maintenance and analysis
                self._analyze_recent_activity()
                time.sleep(10.0)  # Check every 10 seconds
                
            except Exception as e:
                logging.error(f"[ConsciousnessLogger] ❌ Monitoring error: {e}")
                time.sleep(1.0)
        
        logging.info("[ConsciousnessLogger] 🔄 Monitoring loop ended")
    
    def _analyze_recent_activity(self):
        """Analyze recent consciousness activity for patterns"""
        # Get recent events (last 5 minutes)
        recent_events = self.get_recent_events(time_window_minutes=5)
        
        if len(recent_events) == 0:
            return
        
        # Check for high error rates
        error_events = [e for e in recent_events 
                       if e.level in [EventLevel.ERROR, EventLevel.CRITICAL]]
        
        error_rate = len(error_events) / len(recent_events)
        
        if error_rate > 0.1:  # More than 10% errors
            self.log_event(
                module="consciousness_logger",
                event_type="high_error_rate_detected",
                message=f"High error rate detected: {error_rate:.2%} in last 5 minutes",
                category=EventCategory.WARNING,
                level=EventLevel.WARNING,
                details={"error_rate": error_rate, "total_events": len(recent_events)}
            )


# Create global consciousness event logger
consciousness_logger = ConsciousnessEventLogger()