#!/usr/bin/env python3
"""
Comprehensive Consciousness Architecture Analysis
Analyzes all consciousness-related files to ensure proper wiring and port separation
"""

import os
import re
import importlib.util
from typing import Dict, List, Any
import json

class ConsciousnessArchitectureAnalyzer:
    def __init__(self):
        self.issues = []
        self.files_analyzed = []
        self.port_usage = {"5001": [], "5002": [], "other": []}
        self.consciousness_modules = []
        self.memory_systems = []
        self.errors = []
        
    def analyze_all_files(self):
        """Analyze all consciousness-related files"""
        print("🧠 COMPREHENSIVE CONSCIOUSNESS ARCHITECTURE ANALYSIS")
        print("="*80)
        
        # Key directories and files to analyze
        paths_to_analyze = [
            "ai/",
            "main.py",
            "cognitive_modules/",
            "memory/",
            "voice/",
            "audio/"
        ]
        
        for path in paths_to_analyze:
            if os.path.exists(path):
                if os.path.isdir(path):
                    self._analyze_directory(path)
                else:
                    self._analyze_file(path)
        
        self._generate_report()
    
    def _analyze_directory(self, directory: str):
        """Analyze all Python files in a directory"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    self._analyze_file(filepath)
    
    def _analyze_file(self, filepath: str):
        """Analyze a single Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.files_analyzed.append(filepath)
            
            # Check for port usage
            self._check_port_usage(filepath, content)
            
            # Check for consciousness modules
            self._check_consciousness_modules(filepath, content)
            
            # Check for memory systems
            self._check_memory_systems(filepath, content)
            
            # Check for architectural issues
            self._check_architectural_issues(filepath, content)
            
        except Exception as e:
            self.errors.append(f"Error analyzing {filepath}: {e}")
    
    def _check_port_usage(self, filepath: str, content: str):
        """Check which ports are being used"""
        # Check for localhost:5001 (main LLM)
        if re.search(r'localhost:5001|127\.0\.0\.1:5001', content):
            self.port_usage["5001"].append(filepath)
            
            # Check if this file is doing consciousness processing on port 5001 (BAD)
            consciousness_keywords = [
                'consciousness', 'memory', 'emotion', 'belief', 'inner_thought',
                'self_model', 'motivation', 'temporal_awareness', 'subjective_experience'
            ]
            if any(keyword in content.lower() for keyword in consciousness_keywords):
                self.issues.append(f"⚠️ {filepath}: Using port 5001 for consciousness processing (should only be response generation)")
        
        # Check for localhost:5002 (Gemma consciousness)
        if re.search(r'localhost:5002|127\.0\.0\.1:5002', content):
            self.port_usage["5002"].append(filepath)
        
        # Check for other ports
        other_ports = re.findall(r'localhost:(\d+)|127\.0\.0\.1:(\d+)', content)
        for match in other_ports:
            port = match[0] or match[1]
            if port not in ["5001", "5002"]:
                self.port_usage["other"].append(f"{filepath} uses port {port}")
    
    def _check_consciousness_modules(self, filepath: str, content: str):
        """Check for consciousness module implementations"""
        consciousness_patterns = [
            r'class.*Consciousness.*:',
            r'class.*Emotion.*:',
            r'class.*Memory.*:',
            r'class.*Belief.*:',
            r'class.*Motivation.*:',
            r'class.*InnerMonologue.*:',
            r'class.*SelfModel.*:',
            r'class.*TemporalAwareness.*:',
            r'class.*SubjectiveExperience.*:',
            r'class.*GlobalWorkspace.*:',
            r'class.*Entropy.*:'
        ]
        
        for pattern in consciousness_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.consciousness_modules.append(filepath)
                break
    
    def _check_memory_systems(self, filepath: str, content: str):
        """Check for memory system implementations"""
        memory_patterns = [
            r'class.*Memory.*Manager.*:',
            r'class.*Memory.*Timeline.*:',
            r'class.*Local.*Memory.*:',
            r'def.*store.*memory',
            r'def.*get.*memory',
            r'def.*remember',
            r'def.*recall'
        ]
        
        for pattern in memory_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.memory_systems.append(filepath)
                break
    
    def _check_architectural_issues(self, filepath: str, content: str):
        """Check for specific architectural issues"""
        
        # Check for LLM calls in wrong places
        if 'localhost:5001' in content and any(word in content.lower() for word in ['memory', 'consciousness', 'emotion']):
            if 'simple_llm_handler' not in filepath:  # Exception for the designated handler
                self.issues.append(f"🚨 {filepath}: Making LLM calls to port 5001 with consciousness processing")
        
        # Check for missing error handling
        if 'requests.post' in content and 'except' not in content:
            self.issues.append(f"⚠️ {filepath}: HTTP requests without error handling")
        
        # Check for blocking operations in main thread
        if 'time.sleep' in content and 'thread' not in content.lower():
            self.issues.append(f"⚠️ {filepath}: Potentially blocking sleep operations")
        
        # Check for proper memory persistence
        if 'memory' in filepath.lower() and 'json.dump' not in content and 'save' not in content.lower():
            self.issues.append(f"⚠️ {filepath}: Memory system without persistence")
    
    def _generate_report(self):
        """Generate comprehensive analysis report"""
        print(f"\n📊 ANALYSIS COMPLETE")
        print(f"Files analyzed: {len(self.files_analyzed)}")
        print(f"Issues found: {len(self.issues)}")
        print(f"Errors: {len(self.errors)}")
        
        print(f"\n🔌 PORT USAGE ANALYSIS:")
        print(f"Port 5001 (Main LLM): {len(self.port_usage['5001'])} files")
        for file in self.port_usage['5001']:
            print(f"  - {file}")
        
        print(f"\nPort 5002 (Gemma Consciousness): {len(self.port_usage['5002'])} files")
        for file in self.port_usage['5002']:
            print(f"  - {file}")
        
        print(f"\nOther ports: {len(self.port_usage['other'])} instances")
        for item in self.port_usage['other']:
            print(f"  - {item}")
        
        print(f"\n🧠 CONSCIOUSNESS MODULES FOUND: {len(self.consciousness_modules)}")
        for module in self.consciousness_modules:
            print(f"  - {module}")
        
        print(f"\n💾 MEMORY SYSTEMS FOUND: {len(self.memory_systems)}")
        for system in self.memory_systems:
            print(f"  - {system}")
        
        if self.issues:
            print(f"\n🚨 CRITICAL ISSUES FOUND:")
            for issue in self.issues:
                print(f"  {issue}")
        
        if self.errors:
            print(f"\n❌ ANALYSIS ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        # Save detailed report
        report = {
            "timestamp": "2025-01-17T12:00:00Z",
            "files_analyzed": len(self.files_analyzed),
            "issues_count": len(self.issues),
            "port_usage": {
                "5001": self.port_usage['5001'],
                "5002": self.port_usage['5002'],
                "other": self.port_usage['other']
            },
            "consciousness_modules": self.consciousness_modules,
            "memory_systems": self.memory_systems,
            "issues": self.issues,
            "errors": self.errors
        }
        
        with open('consciousness_architecture_analysis.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Detailed report saved to: consciousness_architecture_analysis.json")
        
        # Provide specific recommendations
        self._provide_recommendations()
    
    def _provide_recommendations(self):
        """Provide specific recommendations for fixes"""
        print(f"\n🔧 SPECIFIC RECOMMENDATIONS:")
        
        print(f"\n1. PORT SEPARATION:")
        if len(self.port_usage['5001']) > 1:
            print(f"   - ⚠️ Multiple files using port 5001 - should only be simple_llm_handler.py")
            print(f"   - Move consciousness processing to port 5002")
        
        if len(self.port_usage['5002']) == 0:
            print(f"   - 🚨 No files using port 5002 - consciousness processing not properly routed")
        
        print(f"\n2. MEMORY SYSTEM:")
        print(f"   - Ensure local_memory_manager.py handles immediate name storage")
        print(f"   - Verify memory persistence across sessions")
        print(f"   - Test name recognition: 'I'm David' -> 'What's my name?' workflow")
        
        print(f"\n3. RESPONSE FLOW:")
        print(f"   - Port 5001 should only receive minimal prompt with injected consciousness")
        print(f"   - All consciousness processing should happen on port 5002 in background")
        print(f"   - Immediate response generation without consciousness loops")
        
        print(f"\n4. CONSCIOUSNESS MODULES:")
        print(f"   - Fix GoalStatus.COMPLETED attribute error")
        print(f"   - Fix AutonomousAction missing arguments")
        print(f"   - Ensure all modules start properly without errors")
        
        print(f"\n5. AUDIO INTEGRATION:")
        print(f"   - Verify Kokoro server connection")
        print(f"   - Test voice output with simple phrases")
        print(f"   - Ensure audio doesn't block main response flow")

def main():
    analyzer = ConsciousnessArchitectureAnalyzer()
    analyzer.analyze_all_files()

if __name__ == "__main__":
    main()