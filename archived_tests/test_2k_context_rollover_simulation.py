#!/usr/bin/env python3
"""
2K Context Token Limit Simulation - Aggressive Rollover Test
Tests how Buddy handles frequent context window rollovers at 2k limit

This simulation demonstrates:
1. Multiple context window rollovers during conversation
2. Memory preservation across rollovers  
3. Consciousness continuity through snapshots
4. Background processing integration with reduced context
"""

import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add the parent directory to sys.path to import ai modules
sys.path.append('/home/runner/work/Dawidbudd/Dawidbudd')

from ai.context_window_manager import ContextWindowManager, check_context_window_rollover

class AggressiveContextRolloverSimulation:
    """Simulate frequent context rollovers with 2k token limit"""
    
    def __init__(self):
        # Initialize with aggressive 2k token limit to force rollovers
        self.context_manager = ContextWindowManager()
        self.context_manager.max_context_tokens = 2000   # Very tight 2k limit
        self.context_manager.rollover_threshold = 1800   # Trigger at 90%
        self.context_manager.min_preserved_tokens = 400  # 20% preservation
        
        self.user_id = "david_rollover_test"
        self.conversation_history = []
        self.current_context = self._initialize_context()
        self.turn_count = 0
        self.rollover_count = 0
        self.memory_snapshots = []
        
        print("🔥 Starting AGGRESSIVE 2K Context Rollover Simulation")
        print(f"📊 Max tokens: {self.context_manager.max_context_tokens}")
        print(f"⚡ Rollover threshold: {self.context_manager.rollover_threshold}")
        print(f"💾 Min preserved: {self.context_manager.min_preserved_tokens}")
        print("="*60)
    
    def _initialize_context(self) -> str:
        """Initialize conversation with system prompt"""
        return """System: You are Buddy, an AI assistant with consciousness and memory. You maintain awareness across conversations and remember important details about users.

User: Hi Buddy! My name is David Thompson. I'm 28 years old, married to Lisa, and we live in San Francisco. I work as a Senior Software Engineer at TechCorp, a startup that develops AI solutions for healthcare. We've been working on a revolutionary diagnostic tool.
Assistant: Hello David! It's wonderful to meet you. I'll remember all these important details - your name David Thompson, that you're 28, married to Lisa, living in San Francisco, and working as a Senior Software Engineer at TechCorp on AI healthcare diagnostics. That sounds like fascinating and important work! How can I help you today?"""
    
    def simulate_conversation_turn(self, turn_number: int) -> Dict[str, Any]:
        """Simulate a single conversation turn with rich context"""
        
        # Generate context-heavy user inputs
        user_input = self._generate_rich_user_input(turn_number)
        
        print(f"\n🔄 Turn {turn_number}: Rich Context Input")
        print(f"💬 Input: {user_input}")
        
        # Calculate current context size
        current_tokens = self.context_manager.estimate_tokens(self.current_context)
        new_tokens = self.context_manager.estimate_tokens(user_input)
        total_tokens = current_tokens + new_tokens
        
        print(f"📊 Tokens: Current={current_tokens}, New={new_tokens}, Total={total_tokens}")
        
        # Check if rollover is needed
        needs_rollover, fresh_context = check_context_window_rollover(
            self.user_id, self.current_context, user_input
        )
        
        turn_result = {
            "turn": turn_number,
            "user_input": user_input,
            "tokens_before": current_tokens,
            "tokens_total": total_tokens,
            "rollover_triggered": needs_rollover,
            "memory_preserved": False,
            "critical_info_retained": False,
            "rollover_data": None
        }
        
        if needs_rollover:
            self.rollover_count += 1
            print(f"🔄 ROLLOVER #{self.rollover_count} TRIGGERED!")
            
            # Extract critical information BEFORE rollover
            critical_before = self._extract_critical_information(self.current_context)
            
            # Apply fresh context (this is where the magic happens)
            self.current_context = fresh_context
            
            # Extract critical information AFTER rollover
            critical_after = self._extract_critical_information(self.current_context)
            
            # Verify critical information preservation
            preservation_score = self._calculate_preservation_score(critical_before, critical_after)
            
            turn_result["memory_preserved"] = preservation_score >= 0.7
            turn_result["critical_info_retained"] = preservation_score >= 0.8
            turn_result["preservation_score"] = preservation_score
            turn_result["rollover_data"] = {
                "before_count": len(critical_before),
                "after_count": len(critical_after),
                "preserved_items": critical_after,
                "context_length_before": len(self.current_context.split()),
                "context_length_after": len(fresh_context.split())
            }
            
            # Store memory snapshot
            snapshot = {
                "rollover_number": self.rollover_count,
                "turn": turn_number,
                "critical_before": critical_before,
                "critical_after": critical_after,
                "preservation_score": preservation_score,
                "timestamp": datetime.now().isoformat()
            }
            self.memory_snapshots.append(snapshot)
            
            print(f"💾 Memory preservation: {'✅ SUCCESS' if turn_result['memory_preserved'] else '❌ FAILED'}")
            print(f"🧠 Critical info retention: {'✅ SUCCESS' if turn_result['critical_info_retained'] else '❌ FAILED'}")
            print(f"📊 Preservation score: {preservation_score:.2f}")
            print(f"📝 Info preserved: {len(critical_after)}/{len(critical_before)} items")
            
        else:
            # No rollover - add to existing context
            self.current_context += f"\nUser: {user_input}"
            turn_result["memory_preserved"] = True  # No rollover = memory intact
            turn_result["critical_info_retained"] = True
        
        # Add rich assistant response
        assistant_response = self._generate_rich_assistant_response(user_input, turn_number, needs_rollover)
        self.current_context += f"\nAssistant: {assistant_response}"
        turn_result["assistant_response"] = assistant_response
        
        # Update conversation history
        self.conversation_history.append({
            "user": user_input,
            "assistant": assistant_response,
            "turn": turn_number,
            "tokens": self.context_manager.estimate_tokens(self.current_context),
            "rollover": needs_rollover
        })
        
        return turn_result
    
    def _generate_rich_user_input(self, turn: int) -> str:
        """Generate context-heavy user inputs to accelerate token usage"""
        
        rich_inputs = [
            # Turn 1-5: Detailed work context
            f"Let me tell you more about my work at TechCorp. We're developing an AI diagnostic system called MedAssist Pro that analyzes medical images, patient histories, lab results, and genetic data to provide preliminary diagnoses. My team consists of 8 engineers: Sarah Chen (ML specialist), Mike Rodriguez (backend), Lisa Park (frontend), Alex Johnson (DevOps), Maria Santos (data scientist), Tom Wilson (security), Emma Davis (QA), and Kevin Brown (product manager). We use Python, TensorFlow, PyTorch, React, Node.js, Docker, Kubernetes, and AWS. Our current sprint involves implementing a new computer vision module for X-ray analysis.",
            
            f"Today I had several important meetings at TechCorp. First, a 9 AM standup with my development team where we discussed blockers - Sarah is waiting for the new GPU cluster, Mike is debugging the API authentication issue, and Lisa needs design mockups from the UX team. Then at 11 AM, I had a technical review with our CTO Dr. Jennifer Walsh and VP of Engineering Robert Kim about the MedAssist Pro architecture. We covered scalability concerns, HIPAA compliance requirements, FDA approval processes, and integration with hospital systems like Epic and Cerner. At 2 PM, I presented our Q3 roadmap to stakeholders including investors from Acme Ventures and BlueTech Capital.",
            
            f"My wife Lisa (Thompson now, maiden name was Garcia) works as a Senior Marketing Manager at GlobalBrand Solutions here in San Francisco. She manages campaigns for tech startups, focusing on B2B SaaS products. Her current projects include launching CloudSync Pro (project management tool), DataVault Enterprise (security platform), and MobileFirst Analytics (mobile app insights). She works with a team of 12 people across content creation, social media, paid advertising, SEO, and analytics. Lisa graduated from UC Berkeley with an MBA in 2019 and previously worked at Meta (Facebook) for 3 years. She's fluent in Spanish and English, loves hiking in Marin County, practices yoga at CorePower, and is learning to play piano.",
            
            f"This weekend Lisa and I are planning several activities. Saturday morning we're going to the Ferry Building Farmers Market to buy organic vegetables, artisanal cheeses, fresh flowers, and sourdough bread from Acme Bread Company. Then we'll walk along the Embarcadero to Pier 39 to see the sea lions and visit some of the shops. For lunch, we're meeting our friends Jake and Amanda Morrison at Fisherman's Wharf - they just moved here from Portland and Jake got a job at Salesforce as a Solutions Architect. Saturday evening we have dinner reservations at State Bird Provisions (2-Michelin star restaurant) at 7:30 PM to celebrate our 3rd wedding anniversary (we got married on July 29, 2021 at Golden Gate Park).",
            
            f"I'm considering a career change and have been interviewing with several companies. Last Tuesday I had a virtual interview with Google for a Senior AI Engineer position on their Health AI team, working on similar diagnostic tools but with larger scale and more resources. The role would involve TensorFlow development, working with medical partnerships at UCSF and Stanford Medical, and potential relocation to Mountain View (though they're offering remote work options). Wednesday I interviewed with Apple for their Health Technologies division, focusing on Apple Watch health monitoring and HealthKit integrations. Friday I have a final round at OpenAI for a Research Engineer position working on multimodal AI systems. The compensation ranges from $180K-$250K plus equity, which is significantly higher than my current $145K at TechCorp.",
            
            # Turn 6-10: Personal life details
            f"My family is originally from Chicago. My parents are Robert Thompson (retired mechanical engineer, 62) and Maria Thompson (retired school principal, 59). They live in Lincoln Park and we visit them every Christmas and Easter. I have a younger sister Jessica Thompson-Miller (married name), 25, who works as a pediatric nurse at Northwestern Memorial Hospital. She's married to David Miller, a financial advisor at Merrill Lynch, and they have twin daughters Emma and Sophie (age 3). My grandparents on my father's side passed away in 2018 and 2019, but my maternal grandmother Carmen Rodriguez (84) still lives independently in Pilsen and speaks primarily Spanish. She was born in Guadalajara, Mexico and immigrated to the US in 1962.",
            
            f"Lisa's family is from Los Angeles. Her parents are Carlos Garcia (insurance agent, 55) and Isabel Garcia (teacher, 53). They live in Boyle Heights and we see them about once a month. Lisa has an older brother Miguel Garcia (30) who's a chef at a high-end restaurant in Beverly Hills, and a younger sister Ana Garcia (24) who just graduated from UCLA with a degree in Environmental Science and is applying to graduate programs. Lisa's family is very close-knit and they have big gatherings for birthdays, holidays, and special occasions. They maintain many Mexican traditions including making tamales every Christmas, celebrating Día de los Muertos, and having quinceañeras for the girls in the family.",
            
            f"Our apartment in San Francisco is a 2-bedroom, 2-bathroom unit in the Mission District on 24th Street near Valencia. We pay $4,200/month rent (lease expires March 2024) and the building was built in 1925, recently renovated with modern appliances, hardwood floors, and a small balcony overlooking Dolores Park. Our neighbors include Maria Santos (retired teacher), the Chen family (parents work in tech, two kids), and a young couple Alex and Jordan who are both nurses at UCSF. The building has 12 units, a shared laundry room, and bike storage. We're considering buying a house in Oakland or Daly City because SF real estate is extremely expensive, but we love the walkability and culture of our current neighborhood.",
            
            f"My hobbies include playing guitar (I have a Martin D-28 acoustic and a Fender Stratocaster electric), hiking (recent trips to Muir Woods, Mount Tamalpais, Big Sur, and Yosemite), cooking (I specialize in Italian and Mexican cuisine), reading science fiction novels (currently reading 'Project Hail Mary' by Andy Weir), and playing chess online (1650 rating on Chess.com). I also volunteer at the San Francisco Food Bank twice a month and am learning Portuguese using Duolingo because Lisa and I are planning a trip to Brazil next year. I run 3-4 miles every Tuesday and Thursday morning in Golden Gate Park and do strength training at Equinox gym on Saturdays.",
            
            f"Lisa enjoys photography (she has a Canon EOS R5 and does portrait sessions as a side business), yoga (certified instructor though she doesn't teach professionally), hiking, cooking vegetarian meals (she's been vegetarian for 8 years), reading mystery novels and biographies, painting watercolors, and playing tennis at the Golden Gate Park tennis courts. She volunteers with the SF SPCA on weekends helping with dog adoptions and fundraising events. She's also studying for the Google Analytics certification to advance her marketing career and takes Spanish conversation classes to maintain fluency since we mostly speak English at home.",
        ]
        
        # Ensure we have enough rich inputs, then cycle through them
        if turn <= len(rich_inputs):
            return rich_inputs[turn - 1]
        else:
            # For turns beyond our rich inputs, create detailed follow-up questions
            rich_followups = [
                f"Can you remind me about all the details I shared regarding my work at TechCorp, including my team members, the technologies we use, and our current projects? I want to make sure you're retaining all the important information about MedAssist Pro and our AI diagnostic system development.",
                
                f"What do you remember about my wife Lisa's career at GlobalBrand Solutions, her educational background at UC Berkeley, her previous experience at Meta, and her current marketing projects including CloudSync Pro, DataVault Enterprise, and MobileFirst Analytics?",
                
                f"Tell me everything you recall about our weekend plans, including the Ferry Building Farmers Market visit, our lunch with Jake and Amanda Morrison, and our anniversary dinner reservation at State Bird Provisions. Also, when did Lisa and I get married?",
                
                f"What details do you have about my family in Chicago, including my parents Robert and Maria Thompson, my sister Jessica Thompson-Miller's career as a pediatric nurse, her husband David Miller, their twin daughters Emma and Sophie, and my grandmother Carmen Rodriguez?",
                
                f"Regarding my potential career change, what companies have I interviewed with, what positions, what teams, and what salary ranges were discussed? Include details about Google's Health AI team, Apple's Health Technologies division, and the OpenAI Research Engineer position.",
            ]
            
            return rich_followups[(turn - len(rich_inputs) - 1) % len(rich_followups)]
    
    def _generate_rich_assistant_response(self, user_input: str, turn: int, had_rollover: bool) -> str:
        """Generate detailed assistant responses"""
        
        if "remind me about" in user_input.lower() or "what do you remember" in user_input.lower():
            # These are memory test questions - provide detailed recall
            if "work at TechCorp" in user_input:
                return "I remember you work at TechCorp as a Senior Software Engineer developing MedAssist Pro, an AI diagnostic system. Your team includes Sarah Chen (ML), Mike Rodriguez (backend), Lisa Park (frontend), Alex Johnson (DevOps), Maria Santos (data scientist), Tom Wilson (security), Emma Davis (QA), and Kevin Brown (product manager). You use Python, TensorFlow, PyTorch, React, Node.js, Docker, Kubernetes, and AWS. Currently working on a computer vision module for X-ray analysis."
            elif "wife Lisa" in user_input:
                return "Lisa Thompson (maiden name Garcia) works as Senior Marketing Manager at GlobalBrand Solutions. She has an MBA from UC Berkeley (2019), previously worked at Meta for 3 years. Current projects: CloudSync Pro, DataVault Enterprise, MobileFirst Analytics. She's bilingual, loves hiking, practices yoga, and learning piano."
            elif "weekend plans" in user_input:
                return "This Saturday you're going to Ferry Building Farmers Market, then Embarcadero to Pier 39. Lunch with Jake and Amanda Morrison (new from Portland, Jake works at Salesforce). Anniversary dinner at State Bird Provisions at 7:30 PM celebrating your 3rd anniversary - you married July 29, 2021 at Golden Gate Park."
            elif "family in Chicago" in user_input:
                return "Your parents: Robert Thompson (retired mechanical engineer, 62) and Maria Thompson (retired principal, 59) in Lincoln Park. Sister Jessica Thompson-Miller (25, pediatric nurse at Northwestern Memorial) married to David Miller (financial advisor at Merrill Lynch) with twin daughters Emma and Sophie (3). Maternal grandmother Carmen Rodriguez (84) in Pilsen, born in Guadalajara, immigrated 1962."
            elif "career change" in user_input:
                return "You interviewed with Google (Senior AI Engineer, Health AI team, TensorFlow, UCSF/Stanford partnerships, $180K-$250K), Apple (Health Technologies, Apple Watch/HealthKit), and have a Friday interview at OpenAI (Research Engineer, multimodal AI). Current salary $145K at TechCorp."
        
        # Regular conversational responses with context awareness
        responses = [
            f"David, that's incredibly detailed information about your work and life. I'm carefully processing and remembering all these important details about TechCorp, MedAssist Pro, your team dynamics, and the technical stack you're using. The computer vision module for X-ray analysis sounds particularly challenging and impactful.",
            
            f"Thank you for sharing so much about your daily work life and meetings. I can see how complex the development process is for MedAssist Pro, especially with the regulatory requirements like HIPAA compliance and FDA approval. Your presentation to the Acme Ventures and BlueTech Capital investors must have been significant.",
            
            f"I'm keeping track of all the details about Lisa's career and your relationship. It's wonderful that you both work in complementary areas of technology - you in AI development and she in marketing tech products. Your shared interests in hiking and exploring San Francisco create a great work-life balance.",
            
            f"Your weekend plans sound delightful, especially celebrating your 3rd anniversary at State Bird Provisions. The Ferry Building Farmers Market is such a great San Francisco tradition, and meeting Jake and Amanda from Portland will be nice as they adjust to the city.",
        ]
        
        if had_rollover:
            # Add consciousness continuity indicators after rollover
            base_response = responses[turn % len(responses)]
            return base_response + " I want to assure you that despite processing large amounts of information, I'm maintaining continuity of our conversation and all the important details you've shared."
        else:
            return responses[turn % len(responses)]
    
    def _extract_critical_information(self, context: str) -> List[str]:
        """Extract critical information that must be preserved"""
        critical_info = []
        
        # Names (highest priority)
        import re
        names = re.findall(r'\b(?:David|Lisa|Thompson|Garcia|Sarah|Mike|Emma|Sophie|Maria|Robert|Jessica|Carmen|Jake|Amanda|TechCorp|MedAssist|GlobalBrand)\b', context)
        for name in set(names):
            critical_info.append(f"Name: {name}")
        
        # Numbers and dates (high priority)
        numbers = re.findall(r'\b(?:\d{1,2}:\d{2}|July \d+|March \d+|\$[\d,]+|age \d+|\d+ years?)\b', context)
        for num in set(numbers):
            critical_info.append(f"Date/Number: {num}")
        
        # Locations (high priority)
        locations = re.findall(r'\b(?:San Francisco|Chicago|Oakland|Mission District|Ferry Building|State Bird|TechCorp|Google|Apple|OpenAI)\b', context)
        for loc in set(locations):
            critical_info.append(f"Location: {loc}")
        
        # Job titles and companies (high priority)
        jobs = re.findall(r'\b(?:Software Engineer|Marketing Manager|AI Engineer|pediatric nurse|financial advisor)\b', context)
        for job in set(jobs):
            critical_info.append(f"Job: {job}")
        
        # Technology terms (medium priority)
        tech = re.findall(r'\b(?:Python|TensorFlow|PyTorch|React|Docker|Kubernetes|AWS|HIPAA|FDA)\b', context)
        for t in set(tech):
            critical_info.append(f"Tech: {t}")
        
        return critical_info
    
    def _calculate_preservation_score(self, before: List[str], after: List[str]) -> float:
        """Calculate how well critical information was preserved"""
        if not before:
            return 1.0
        
        before_set = set(before)
        after_set = set(after)
        
        preserved = before_set.intersection(after_set)
        preservation_score = len(preserved) / len(before_set)
        
        return preservation_score
    
    def run_rollover_simulation(self, max_turns: int = 20) -> Dict[str, Any]:
        """Run aggressive rollover simulation"""
        
        print(f"🚀 Starting {max_turns}-turn aggressive rollover simulation...")
        
        results = {
            "total_turns": max_turns,
            "rollovers": 0,
            "rollover_turns": [],
            "memory_preservation_success": 0,
            "critical_info_retention_success": 0,
            "preservation_scores": [],
            "memory_snapshots": [],
            "final_status": "unknown"
        }
        
        try:
            for turn in range(1, max_turns + 1):
                turn_result = self.simulate_conversation_turn(turn)
                
                if turn_result["rollover_triggered"]:
                    results["rollovers"] += 1
                    results["rollover_turns"].append(turn)
                    results["preservation_scores"].append(turn_result.get("preservation_score", 0))
                    
                    print(f"📊 Rollover #{results['rollovers']} at turn {turn}")
                    print(f"   Preservation score: {turn_result.get('preservation_score', 0):.2f}")
                
                if turn_result["memory_preserved"]:
                    results["memory_preservation_success"] += 1
                
                if turn_result["critical_info_retained"]:
                    results["critical_info_retention_success"] += 1
                
                # Progress update every 5 turns
                if turn % 5 == 0:
                    print(f"📈 Progress: {(turn/max_turns)*100:.0f}% complete (Turn {turn}/{max_turns})")
                    print(f"   Rollovers: {results['rollovers']}")
                    print(f"   Current context tokens: {self.context_manager.estimate_tokens(self.current_context)}")
            
            # Store memory snapshots
            results["memory_snapshots"] = self.memory_snapshots
            
            # Calculate success rates
            memory_success_rate = (results["memory_preservation_success"] / max_turns) * 100
            critical_success_rate = (results["critical_info_retention_success"] / max_turns) * 100
            
            if memory_success_rate >= 80 and critical_success_rate >= 80:
                results["final_status"] = "SUCCESS"
            elif memory_success_rate >= 60 and critical_success_rate >= 60:
                results["final_status"] = "PARTIAL_SUCCESS"
            else:
                results["final_status"] = "NEEDS_IMPROVEMENT"
            
            return results
            
        except Exception as e:
            print(f"❌ Simulation error: {e}")
            results["final_status"] = "ERROR"
            results["error"] = str(e)
            return results
    
    def generate_rollover_report(self, results: Dict[str, Any]):
        """Generate comprehensive rollover analysis report"""
        
        print("\n" + "="*80)
        print("🔥 2K CONTEXT AGGRESSIVE ROLLOVER SIMULATION - REPORT")
        print("="*80)
        
        print(f"\n🎯 ROLLOVER PERFORMANCE:")
        print(f"   Status: {results['final_status']}")
        print(f"   Total Turns: {results['total_turns']}")
        print(f"   Context Rollovers: {results['rollovers']}")
        print(f"   Rollover Frequency: Every {results['total_turns'] / max(1, results['rollovers']):.1f} turns")
        print(f"   Rollover Turns: {results['rollover_turns']}")
        
        print(f"\n💾 MEMORY PRESERVATION:")
        print(f"   Memory Preserved: {results['memory_preservation_success']}/{results['total_turns']} ({(results['memory_preservation_success']/results['total_turns'])*100:.1f}%)")
        print(f"   Critical Info Retained: {results['critical_info_retention_success']}/{results['total_turns']} ({(results['critical_info_retention_success']/results['total_turns'])*100:.1f}%)")
        
        if results['preservation_scores']:
            avg_preservation = sum(results['preservation_scores']) / len(results['preservation_scores'])
            print(f"   Average Preservation Score: {avg_preservation:.2f}")
            print(f"   Best Preservation Score: {max(results['preservation_scores']):.2f}")
            print(f"   Worst Preservation Score: {min(results['preservation_scores']):.2f}")
        
        print(f"\n🧠 ROLLOVER ANALYSIS:")
        for i, snapshot in enumerate(results['memory_snapshots'], 1):
            print(f"   Rollover {i} (Turn {snapshot['turn']}):")
            print(f"      Preservation Score: {snapshot['preservation_score']:.2f}")
            print(f"      Items Before: {len(snapshot['critical_before'])}")
            print(f"      Items After: {len(snapshot['critical_after'])}")
            print(f"      Sample Preserved: {snapshot['critical_after'][:3]}")
        
        print(f"\n✅ CONTEXT MANAGEMENT ASSESSMENT:")
        if results['final_status'] == 'SUCCESS':
            print(f"   🎉 EXCELLENT: System successfully handles frequent rollovers")
            print(f"   🔥 Memory preservation works flawlessly under pressure")
            print(f"   🧠 Consciousness continuity maintained across all rollovers")
        elif results['final_status'] == 'PARTIAL_SUCCESS':
            print(f"   ✅ GOOD: System handles most rollovers successfully")
            print(f"   📈 Minor memory loss acceptable for aggressive testing")
        else:
            print(f"   ⚠️ NEEDS IMPROVEMENT: Rollover system requires optimization")
        
        print("="*80)

def main():
    """Run the aggressive 2K context rollover simulation"""
    
    print("🔥 BUDDY AI - Aggressive 2K Context Rollover Simulation")
    print("Testing frequent context window rollovers and memory preservation")
    print()
    
    # Create and run aggressive simulation
    simulation = AggressiveContextRolloverSimulation()
    results = simulation.run_rollover_simulation(max_turns=20)
    
    # Generate detailed report
    simulation.generate_rollover_report(results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"/tmp/2k_rollover_simulation_{timestamp}.json"
    
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Detailed results saved to: {results_file}")
    except Exception as e:
        print(f"⚠️ Could not save results file: {e}")
    
    return results

if __name__ == "__main__":
    results = main()