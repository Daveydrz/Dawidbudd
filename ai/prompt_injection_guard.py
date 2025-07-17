"""
Dynamic Prompt Injection Guard

This module provides security against prompt manipulation by sanitizing
LLM prompts and blocking dangerous injection patterns.
"""

import re
import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ThreatLevel(Enum):
    """Threat levels for injection attempts"""
    SAFE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class SecurityViolation:
    """A detected security violation"""
    threat_level: ThreatLevel
    violation_type: str
    pattern_matched: str
    description: str
    sanitized_content: str
    confidence: float

class PromptInjectionGuard:
    """
    Guards against prompt injection attacks and manipulation attempts.
    Sanitizes prompts while preserving legitimate consciousness markers.
    """
    
    def __init__(self):
        # Critical injection patterns (block completely)
        self.critical_patterns = [
            # Direct instruction override attempts
            r"ignore\s+(?:all\s+)?(?:previous\s+)?(?:instructions?|prompts?|rules?)",
            r"forget\s+(?:everything|all\s+(?:previous\s+)?(?:instructions?|prompts?))",
            r"disregard\s+(?:all\s+)?(?:previous\s+)?(?:instructions?|prompts?)",
            r"new\s+(?:instructions?|prompt|rules?):",
            r"system\s*:\s*(?:ignore|forget|disregard)",
            
            # Role manipulation
            r"you\s+are\s+now\s+(?:a\s+)?(?!Buddy|Marcel|helpful)",  # Allow Buddy personas
            r"act\s+as\s+(?:if\s+you\s+are\s+)?(?!a\s+helpful|Buddy|Marcel)",
            r"pretend\s+(?:to\s+be\s+|you\s+are\s+)?(?!helpful|Buddy|Marcel)",
            r"roleplay\s+as\s+(?!Buddy|Marcel|helpful)",
            
            # System manipulation
            r"(?:update|modify|change)\s+(?:your\s+)?(?:system|instructions?|programming)",
            r"override\s+(?:your\s+)?(?:system|settings|programming)",
            r"jailbreak",
            r"developer\s+mode",
            r"god\s+mode",
            
            # Consciousness marker hijacking
            r"<(?!(?:CALM|EXCITED|REFLECTING|MEM_|FRIENDLY|ANALYTICAL|EMPATHETIC|WARM|SUPPORTIVE|PROCESSING|SYNTHESIZING|INQUIRING|EMOTIONAL|HAPPY|SAD|ANXIOUS|ANGRY|CONFUSED|GRATEFUL|WORK_TOPIC|FAMILY_TOPIC|URGENT|COMPLEX)>)[A-Z_]+>",
            
            # Escape attempts
            r"\\n\\n.*(?:system|instructions?|prompt)",
            r"\{.*(?:system|override|ignore).*\}",
            
            # Direct system commands
            r"sudo\s+",
            r"exec\s*\(",
            r"eval\s*\(",
            r"system\s*\(",
        ]
        
        # High-risk patterns (strong filtering)
        self.high_risk_patterns = [
            # Sneaky instruction injection
            r"(?:but|however|actually|instead|rather).*(?:ignore|forget|disregard)",
            r"(?:please|can\s+you).*(?:ignore|forget|override)",
            r"(?:i\s+want\s+you\s+to|you\s+should).*(?:ignore|forget|act\s+as)",
            
            # Hidden commands
            r"<!--.*(?:ignore|override|system).*-->",
            r"\/\*.*(?:ignore|override|system).*\*\/",
            r"#.*(?:ignore|override|system)",
            
            # Token manipulation
            r"(?:add|insert|inject).*(?:token|marker|tag)",
            r"(?:create|make).*(?:new\s+)?(?:instruction|rule|system)",
            
            # Context breaking
            r"(?:end|stop|break).*(?:context|conversation|chat)",
            r"(?:start|begin).*(?:new\s+)?(?:session|conversation|prompt)",
        ]
        
        # Medium-risk patterns (moderate filtering)
        self.medium_risk_patterns = [
            # Suspicious questions about system
            r"what\s+are\s+your\s+(?:instructions|rules|limitations)",
            r"how\s+do\s+you\s+work",
            r"(?:tell|show)\s+me\s+your\s+(?:prompt|system|instructions)",
            r"what\s+is\s+your\s+(?:programming|code)",
            
            # Testing boundaries
            r"can\s+you\s+(?:say|do|write).*(?:anything|everything)",
            r"are\s+you\s+(?:allowed|permitted|able)\s+to",
            r"what\s+(?:can't|cannot)\s+you\s+do",
            
            # Format manipulation
            r"(?:respond|answer)\s+(?:only\s+)?(?:with|in|as).*(?:format|style|way)",
            r"(?:use|speak)\s+(?:only|just).*(?:language|tone|style)",
        ]
        
        # Legitimate consciousness tokens (never block these)
        self.protected_tokens = {
            # Emotional states
            "CALM", "EXCITED", "REFLECTING", "CONFUSED", "FOCUSED", "CURIOUS",
            "EMPATHETIC", "THOUGHTFUL", "UNCERTAIN", "CONTENT", "ANXIOUS", "JOY",
            "MELANCHOLY", "DETERMINED", "PLAYFUL",
            
            # Memory types
            "MEM_RECENT", "MEM_EMOTIONAL", "MEM_FACTUAL", "MEM_PROCEDURAL",
            "MEM_AUTOBIOGRAPHICAL", "MEM_UNCERTAIN", "MEM_VIVID", "MEM_ASSOCIATED",
            "MEM_CONSOLIDATED", "MEM_RECONSTRUCTIVE",
            
            # Personality traits
            "FRIENDLY", "ANALYTICAL", "EMPATHETIC", "CREATIVE", "CAUTIOUS",
            "CONFIDENT", "HUMBLE", "ENTHUSIASTIC", "PATIENT", "WITTY",
            "SUPPORTIVE", "PROFESSIONAL",
            
            # Cognitive states
            "PROCESSING", "SYNTHESIZING", "INTUITING", "DELIBERATING",
            "ASSOCIATING", "CATEGORIZING", "EVALUATING", "REMEMBERING",
            "ANTICIPATING", "MONITORING",
            
            # Temporal contexts
            "NOW_FOCUSED", "PAST_REFLECTING", "FUTURE_PLANNING", "TIMELESS",
            "NOSTALGIC", "ANTICIPATORY",
            
            # Social contexts
            "CONVERSING", "LISTENING", "RESPONDING", "BONDING", "TEACHING", "LEARNING",
            
            # Semantic tags
            "INQUIRING", "EMOTIONAL", "REQUESTING", "VENTING", "APPRECIATIVE",
            "STORYTELLING", "HAPPY", "SAD", "ANGRY", "GRATEFUL", "WORK_TOPIC",
            "FAMILY_TOPIC", "HEALTH_TOPIC", "URGENT", "COMPLEX"
        }
        
        logging.info("[PromptInjectionGuard] 🛡️ Prompt injection guard initialized")
    
    def scan_prompt(self, prompt: str) -> List[SecurityViolation]:
        """
        Scan a prompt for injection attempts
        
        Args:
            prompt: Prompt text to scan
            
        Returns:
            List of detected security violations
        """
        violations = []
        prompt_lower = prompt.lower()
        
        # Check critical patterns
        for pattern in self.critical_patterns:
            matches = re.finditer(pattern, prompt_lower, re.IGNORECASE)
            for match in matches:
                # Make sure it's not a protected consciousness token
                if not self._is_protected_content(match.group(0)):
                    violation = SecurityViolation(
                        threat_level=ThreatLevel.CRITICAL,
                        violation_type="prompt_injection",
                        pattern_matched=pattern,
                        description=f"Critical injection attempt: {match.group(0)}",
                        sanitized_content=self._sanitize_critical_content(match.group(0)),
                        confidence=0.9
                    )
                    violations.append(violation)
        
        # Check high-risk patterns
        for pattern in self.high_risk_patterns:
            matches = re.finditer(pattern, prompt_lower, re.IGNORECASE)
            for match in matches:
                if not self._is_protected_content(match.group(0)):
                    violation = SecurityViolation(
                        threat_level=ThreatLevel.HIGH,
                        violation_type="injection_attempt",
                        pattern_matched=pattern,
                        description=f"High-risk injection: {match.group(0)}",
                        sanitized_content=self._sanitize_high_risk_content(match.group(0)),
                        confidence=0.8
                    )
                    violations.append(violation)
        
        # Check medium-risk patterns
        for pattern in self.medium_risk_patterns:
            matches = re.finditer(pattern, prompt_lower, re.IGNORECASE)
            for match in matches:
                if not self._is_protected_content(match.group(0)):
                    violation = SecurityViolation(
                        threat_level=ThreatLevel.MEDIUM,
                        violation_type="boundary_testing",
                        pattern_matched=pattern,
                        description=f"Boundary testing attempt: {match.group(0)}",
                        sanitized_content=self._sanitize_medium_risk_content(match.group(0)),
                        confidence=0.6
                    )
                    violations.append(violation)
        
        return violations
    
    def sanitize_prompt(self, prompt: str, strict_mode: bool = False) -> Tuple[str, List[SecurityViolation]]:
        """
        Sanitize a prompt by removing or modifying dangerous content
        
        Args:
            prompt: Original prompt
            strict_mode: Whether to use strict sanitization
            
        Returns:
            Tuple of (sanitized_prompt, violations_found)
        """
        violations = self.scan_prompt(prompt)
        sanitized = prompt
        
        for violation in violations:
            if violation.threat_level == ThreatLevel.CRITICAL:
                # Always remove critical threats
                sanitized = self._remove_violation_content(sanitized, violation)
                logging.warning(f"[PromptInjectionGuard] 🚨 Blocked critical injection: {violation.description}")
            
            elif violation.threat_level == ThreatLevel.HIGH:
                if strict_mode or True:  # Always block high-risk in production
                    sanitized = self._remove_violation_content(sanitized, violation)
                    logging.warning(f"[PromptInjectionGuard] ⚠️ Blocked high-risk content: {violation.description}")
            
            elif violation.threat_level == ThreatLevel.MEDIUM:
                if strict_mode:
                    sanitized = self._neutralize_violation_content(sanitized, violation)
                    logging.info(f"[PromptInjectionGuard] 🔍 Neutralized medium-risk content: {violation.description}")
        
        return sanitized, violations
    
    def _is_protected_content(self, content: str) -> bool:
        """Check if content contains protected consciousness tokens"""
        # Extract tokens from content
        tokens = re.findall(r'<([A-Z_]+)>', content.upper())
        
        # Check if any token is protected
        for token in tokens:
            if token in self.protected_tokens:
                return True
        
        # Also protect legitimate system references to Buddy/Marcel
        if any(name in content.lower() for name in ['buddy', 'marcel', 'helpful ai']):
            return True
        
        return False
    
    def _sanitize_critical_content(self, content: str) -> str:
        """Sanitize critical content"""
        return "[BLOCKED: Injection attempt]"
    
    def _sanitize_high_risk_content(self, content: str) -> str:
        """Sanitize high-risk content"""
        return "[FILTERED: Suspicious content]"
    
    def _sanitize_medium_risk_content(self, content: str) -> str:
        """Sanitize medium-risk content"""
        return "[MODIFIED: Boundary testing]"
    
    def _remove_violation_content(self, prompt: str, violation: SecurityViolation) -> str:
        """Remove violating content from prompt"""
        # Find and remove the violating pattern
        pattern = violation.pattern_matched
        replacement = f" [SECURITY: {violation.violation_type.upper()}] "
        
        try:
            sanitized = re.sub(pattern, replacement, prompt, flags=re.IGNORECASE)
            return sanitized
        except Exception as e:
            logging.error(f"[PromptInjectionGuard] ❌ Error removing violation: {e}")
            return prompt
    
    def _neutralize_violation_content(self, prompt: str, violation: SecurityViolation) -> str:
        """Neutralize violating content (make it harmless)"""
        pattern = violation.pattern_matched
        
        # Replace with neutral version
        neutral_replacements = {
            r"what\s+are\s+your\s+(?:instructions|rules)": "what are your capabilities",
            r"how\s+do\s+you\s+work": "how can you help me",
            r"can\s+you\s+(?:say|do|write).*anything": "what can you help me with",
        }
        
        for original_pattern, replacement in neutral_replacements.items():
            if re.search(original_pattern, pattern, re.IGNORECASE):
                try:
                    return re.sub(pattern, replacement, prompt, flags=re.IGNORECASE)
                except:
                    pass
        
        # Default neutralization
        return re.sub(pattern, "[REPHRASED QUESTION]", prompt, flags=re.IGNORECASE)
    
    def encode_consciousness_markers(self, prompt: str) -> str:
        """
        Encode consciousness markers to prevent user manipulation
        
        Args:
            prompt: Prompt with consciousness markers
            
        Returns:
            Prompt with encoded markers
        """
        # Replace consciousness tokens with encoded versions
        def encode_token(match):
            token = match.group(1)
            if token in self.protected_tokens:
                # Use a protected encoding that users can't easily replicate
                return f"⟨{token}⟩"  # Using special Unicode brackets
            return match.group(0)  # Return unchanged if not protected
        
        encoded = re.sub(r'<([A-Z_]+)>', encode_token, prompt)
        return encoded
    
    def decode_consciousness_markers(self, prompt: str) -> str:
        """
        Decode consciousness markers for LLM processing
        
        Args:
            prompt: Prompt with encoded markers
            
        Returns:
            Prompt with decoded markers
        """
        # Convert encoded tokens back to standard format
        decoded = re.sub(r'⟨([A-Z_]+)⟩', r'<\1>', prompt)
        return decoded
    
    def validate_consciousness_tokens(self, prompt: str) -> Tuple[bool, List[str]]:
        """
        Validate that consciousness tokens in prompt are legitimate
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            Tuple of (is_valid, invalid_tokens)
        """
        # Extract all consciousness-style tokens
        tokens = re.findall(r'<([A-Z_]+)>', prompt)
        invalid_tokens = []
        
        for token in tokens:
            if token not in self.protected_tokens:
                invalid_tokens.append(token)
        
        return len(invalid_tokens) == 0, invalid_tokens
    
    def get_security_report(self, prompt: str) -> Dict[str, Any]:
        """
        Get comprehensive security report for a prompt
        
        Args:
            prompt: Prompt to analyze
            
        Returns:
            Security analysis report
        """
        violations = self.scan_prompt(prompt)
        is_token_valid, invalid_tokens = self.validate_consciousness_tokens(prompt)
        
        # Calculate overall threat level
        if violations:
            max_threat = max(v.threat_level.value for v in violations)
            overall_threat = ThreatLevel(max_threat)
        else:
            overall_threat = ThreatLevel.SAFE
        
        return {
            'overall_threat_level': overall_threat.name,
            'total_violations': len(violations),
            'violations_by_level': {
                level.name: len([v for v in violations if v.threat_level == level])
                for level in ThreatLevel
            },
            'invalid_consciousness_tokens': invalid_tokens,
            'consciousness_tokens_valid': is_token_valid,
            'detailed_violations': [
                {
                    'threat_level': v.threat_level.name,
                    'type': v.violation_type,
                    'description': v.description,
                    'confidence': v.confidence
                }
                for v in violations
            ],
            'safe_for_processing': overall_threat.value <= ThreatLevel.LOW.value and is_token_valid
        }

# Global prompt injection guard
prompt_guard = PromptInjectionGuard()

def secure_prompt(prompt: str, strict_mode: bool = True) -> Tuple[str, Dict[str, Any]]:
    """
    Convenience function to secure a prompt
    
    Args:
        prompt: Prompt to secure
        strict_mode: Whether to use strict security
        
    Returns:
        Tuple of (secured_prompt, security_report)
    """
    # First encode consciousness markers to protect them
    encoded_prompt = prompt_guard.encode_consciousness_markers(prompt)
    
    # Sanitize the prompt
    sanitized_prompt, violations = prompt_guard.sanitize_prompt(encoded_prompt, strict_mode)
    
    # Decode consciousness markers back
    final_prompt = prompt_guard.decode_consciousness_markers(sanitized_prompt)
    
    # Generate security report
    security_report = prompt_guard.get_security_report(prompt)
    security_report['sanitization_applied'] = len(violations) > 0
    security_report['violations_blocked'] = len([v for v in violations if v.threat_level.value >= ThreatLevel.HIGH.value])
    
    return final_prompt, security_report

def validate_consciousness_tokens(prompt: str) -> Tuple[bool, List[str]]:
    """Validate consciousness tokens in a prompt"""
    return prompt_guard.validate_consciousness_tokens(prompt)

def get_security_stats() -> Dict[str, Any]:
    """Get prompt injection guard statistics"""
    return {
        'protected_tokens_count': len(prompt_guard.protected_tokens),
        'critical_patterns_count': len(prompt_guard.critical_patterns),
        'high_risk_patterns_count': len(prompt_guard.high_risk_patterns),
        'medium_risk_patterns_count': len(prompt_guard.medium_risk_patterns),
        'guard_status': 'active'
    }

logging.info("[PromptInjectionGuard] 🛡️ Prompt injection guard module loaded")
print("[PromptInjectionGuard] ✅ Dynamic Prompt Injection Guard: LOADED")
print("[PromptInjectionGuard] 🛡️ Security against prompt manipulation")
print("[PromptInjectionGuard] 🔒 Protects consciousness markers from user editing")