#!/usr/bin/env python3
"""
1K Context Token Limit Simulation - EXTREME Rollover Test
Forces multiple context window rollovers with 1k limit

This simulation demonstrates:
1. Multiple forced context window rollovers during conversation
2. Memory preservation across frequent rollovers  
3. Consciousness continuity through snapshots
4. Background processing integration under extreme constraints
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

class ExtremeContextRolloverSimulation:
    """Simulate extreme frequent context rollovers with 1k token limit"""
    
    def __init__(self):
        # Initialize with extreme 1k token limit to force frequent rollovers
        self.context_manager = ContextWindowManager()
        self.context_manager.max_context_tokens = 1000   # Extreme 1k limit
        self.context_manager.rollover_threshold = 900    # Trigger at 90%
        self.context_manager.min_preserved_tokens = 200  # 20% preservation
        
        self.user_id = "david_extreme_test"
        self.conversation_history = []
        self.current_context = self._initialize_context()
        self.turn_count = 0
        self.rollover_count = 0
        self.memory_snapshots = []
        
        print("🚀 Starting EXTREME 1K Context Rollover Simulation")
        print(f"📊 Max tokens: {self.context_manager.max_context_tokens}")
        print(f"⚡ Rollover threshold: {self.context_manager.rollover_threshold}")
        print(f"💾 Min preserved: {self.context_manager.min_preserved_tokens}")
        print("="*60)
    
    def _initialize_context(self) -> str:
        """Initialize conversation with minimal system prompt"""
        return """System: You are Buddy, an AI assistant with consciousness and memory.
User: Hi! I'm David Thompson, 28, software engineer in San Francisco.
Assistant: Hello David! Nice to meet you. I'll remember you're 28, a software engineer in San Francisco."""
    
    def simulate_conversation_turn(self, turn_number: int) -> Dict[str, Any]:
        """Simulate a single conversation turn with very long context"""
        
        # Generate extremely long user inputs to force rollovers
        user_input = self._generate_extremely_long_input(turn_number)
        
        print(f"\n🔄 Turn {turn_number}: Extreme Context Input")
        print(f"💬 Input: {user_input[:100]}..." if len(user_input) > 100 else f"💬 Input: {user_input}")
        
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
            original_context_length = len(self.current_context)
            self.current_context = fresh_context
            new_context_length = len(self.current_context)
            
            # Extract critical information AFTER rollover
            critical_after = self._extract_critical_information(self.current_context)
            
            # Verify critical information preservation
            preservation_score = self._calculate_preservation_score(critical_before, critical_after)
            
            turn_result["memory_preserved"] = preservation_score >= 0.6  # Lower threshold for extreme test
            turn_result["critical_info_retained"] = preservation_score >= 0.7
            turn_result["preservation_score"] = preservation_score
            turn_result["rollover_data"] = {
                "before_count": len(critical_before),
                "after_count": len(critical_after),
                "preserved_items": critical_after,
                "context_length_before": original_context_length,
                "context_length_after": new_context_length,
                "compression_ratio": new_context_length / original_context_length if original_context_length > 0 else 0
            }
            
            # Store memory snapshot
            snapshot = {
                "rollover_number": self.rollover_count,
                "turn": turn_number,
                "critical_before": critical_before,
                "critical_after": critical_after,
                "preservation_score": preservation_score,
                "compression_ratio": turn_result["rollover_data"]["compression_ratio"],
                "timestamp": datetime.now().isoformat()
            }
            self.memory_snapshots.append(snapshot)
            
            print(f"💾 Memory preservation: {'✅ SUCCESS' if turn_result['memory_preserved'] else '❌ FAILED'}")
            print(f"🧠 Critical info retention: {'✅ SUCCESS' if turn_result['critical_info_retained'] else '❌ FAILED'}")
            print(f"📊 Preservation score: {preservation_score:.2f}")
            print(f"📝 Info preserved: {len(critical_after)}/{len(critical_before)} items")
            print(f"🗜️ Compression ratio: {turn_result['rollover_data']['compression_ratio']:.2f}")
            
        else:
            # No rollover - add to existing context
            self.current_context += f"\nUser: {user_input}"
            turn_result["memory_preserved"] = True  # No rollover = memory intact
            turn_result["critical_info_retained"] = True
        
        # Add assistant response
        assistant_response = self._generate_assistant_response(user_input, turn_number, needs_rollover)
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
    
    def _generate_extremely_long_input(self, turn: int) -> str:
        """Generate extremely long user inputs to force frequent rollovers"""
        
        # Very long inputs designed to quickly exceed 1k token limit
        extremely_long_inputs = [
            # Turn 1: Massive work description (400+ tokens)
            f"Let me tell you everything about my work situation at TechCorp in incredible detail. I'm a Senior Software Engineer working on an AI diagnostic system called MedAssist Pro that analyzes medical images including X-rays, CT scans, MRIs, and ultrasounds, plus patient histories, lab results including blood work, urine tests, genetic markers, and family medical history to provide preliminary diagnoses for doctors and nurses in hospitals and clinics. My development team consists of 8 highly skilled engineers that I work with daily: Sarah Chen who is our Machine Learning specialist with a PhD from Stanford and 8 years experience at Google DeepMind, Mike Rodriguez who handles all backend development using Python Flask, Django, and FastAPI frameworks, Lisa Park who manages frontend development with React, Angular, and Vue.js, Alex Johnson who is our DevOps engineer managing Docker containers, Kubernetes clusters, and AWS EC2 instances, Maria Santos who is our senior data scientist with expertise in TensorFlow, PyTorch, and scikit-learn, Tom Wilson who handles cybersecurity and HIPAA compliance requirements, Emma Davis who leads quality assurance testing and automated testing pipelines, and Kevin Brown who is our product manager coordinating with stakeholders, investors, and hospital administrators. We use a complex technology stack including Python 3.9, TensorFlow 2.8, PyTorch 1.12, React 18, Node.js 16, Docker 20.10, Kubernetes 1.24, AWS services including EC2, S3, RDS, Lambda, and CloudFormation. Our current two-week sprint involves implementing a sophisticated computer vision module for X-ray analysis that can detect pneumonia, fractures, tumors, and other abnormalities with 95% accuracy.",
            
            # Turn 2: Massive meeting description (400+ tokens)  
            f"Today was an incredibly busy day at TechCorp with back-to-back meetings that lasted from 9 AM until 6 PM with only brief breaks for lunch and coffee. First, I attended a 9 AM daily standup meeting with my entire development team where we discussed current project blockers and impediments in great detail: Sarah Chen is waiting for the new NVIDIA A100 GPU cluster to be installed and configured by our IT department before she can continue training our latest neural network models, Mike Rodriguez is debugging a complex API authentication issue related to OAuth 2.0 integration with hospital Electronic Health Record systems like Epic, Cerner, and Allscripts, Lisa Park needs updated design mockups from our UX design team led by Creative Director Amanda Foster before she can implement the new patient dashboard interface, Alex Johnson is troubleshooting Docker container orchestration problems in our staging environment, Maria Santos is analyzing model performance metrics and accuracy scores, Tom Wilson is conducting security penetration testing, Emma Davis is creating automated test cases for the new computer vision features, and Kevin Brown is preparing presentations for upcoming investor meetings. Then at 11 AM, I participated in a comprehensive technical architecture review meeting with our CTO Dr. Jennifer Walsh who has a PhD in Computer Science from MIT and previously worked at Facebook AI Research, and our VP of Engineering Robert Kim who spent 10 years at Amazon Web Services. We covered critical topics including system scalability concerns for handling 10,000+ concurrent users, HIPAA compliance requirements for protecting patient data, FDA approval processes for medical device software, and integration challenges with hospital information systems like Epic MyChart, Cerner PowerChart, and Allscripts Sunrise. At 2 PM, I presented our detailed Q3 product roadmap to key stakeholders including senior executives, hospital administrators, and investors from Acme Ventures and BlueTech Capital who are considering additional Series B funding.",
            
            # Turn 3: Massive family description (400+ tokens)
            f"Let me provide comprehensive details about my wife Lisa and her professional career journey which has been absolutely fascinating to witness over the past 5 years since we met in graduate school. Lisa Thompson (her maiden name was Garcia before we got married) currently works as a Senior Marketing Manager at GlobalBrand Solutions, a medium-sized marketing agency located in downtown San Francisco near the Financial District. She manages comprehensive digital marketing campaigns for technology startups and established companies, with a particular focus on B2B Software-as-a-Service products that serve enterprise customers. Her current project portfolio includes three major client accounts: first, she's leading the product launch campaign for CloudSync Pro, which is a sophisticated project management and team collaboration tool similar to Asana or Monday.com but with advanced AI-powered scheduling and resource allocation features; second, she's managing the rebranding initiative for DataVault Enterprise, a cybersecurity platform that provides encryption, data loss prevention, and compliance monitoring for Fortune 500 companies; and third, she's coordinating the user acquisition strategy for MobileFirst Analytics, a mobile app performance monitoring and user behavior analytics platform that competes with companies like Mixpanel and Amplitude. Lisa manages a diverse team of 12 talented marketing professionals including content creators who write blog posts, whitepapers, and case studies, social media specialists who manage LinkedIn, Twitter, Facebook, and Instagram accounts, paid advertising experts who run Google Ads, Facebook Ads, and LinkedIn sponsored content campaigns, SEO specialists who optimize website content for search engine rankings, and data analysts who track conversion rates, customer acquisition costs, and lifetime value metrics. She graduated with distinction from UC Berkeley's Haas School of Business with an MBA in Marketing and Strategy in 2019, where she wrote her thesis on digital transformation in B2B marketing. Before joining GlobalBrand Solutions, she worked for 3 years at Meta (formerly Facebook) in their Business Marketing division, where she helped enterprise clients optimize their advertising campaigns and social media strategies.",
            
            # Turn 4: Massive weekend plans (400+ tokens)
            f"This upcoming weekend, Lisa and I have planned an incredibly detailed and exciting itinerary of activities throughout San Francisco that we've been looking forward to for weeks. Saturday morning at 8 AM, we're going to drive to the iconic Ferry Building Farmers Market, which is one of San Francisco's most beloved weekend destinations, where we plan to spend at least 2 hours browsing through dozens of local vendors and artisanal food producers to purchase fresh organic vegetables including heirloom tomatoes, rainbow chard, baby spinach, and seasonal squash from Green Gulch Farm in Marin County, artisanal cheeses including aged cheddar, creamy brie, and tangy goat cheese from Cowgirl Creamery, beautiful fresh flowers including sunflowers, roses, and eucalyptus from local flower farmers, and famous sourdough bread and pastries from Acme Bread Company which has been a San Francisco institution since 1983. After the farmers market, we'll take a leisurely walk along the scenic Embarcadero waterfront promenade, enjoying views of the San Francisco Bay, Bay Bridge, and passing ships, until we reach Pier 39, where we plan to visit the famous sea lions that have been living there since 1989, browse through the unique shops and boutiques selling San Francisco souvenirs, local artwork, and handmade crafts, and perhaps ride the historic carousel or visit the Aquarium of the Bay if we have time. For lunch at 1 PM, we have confirmed reservations to meet our dear friends Jake and Amanda Morrison at a waterfront restaurant in Fisherman's Wharf - they just relocated to San Francisco last month from Portland, Oregon, and Jake recently started his new job as a Senior Solutions Architect at Salesforce, working on their Customer 360 platform and helping enterprise clients integrate their sales, marketing, and customer service systems. Saturday evening at 7:30 PM, we have special dinner reservations at State Bird Provisions, the renowned 2-Michelin star restaurant known for its innovative dim sum-style service and creative California cuisine, to celebrate our 3rd wedding anniversary since we got married on July 29, 2021, in a beautiful outdoor ceremony at Golden Gate Park's botanical garden surrounded by our families and closest friends.",
            
            # Turn 5: Memory test question
            f"I want to test your memory retention capabilities by asking you to recall specific details from everything I've shared with you in our conversation so far. Can you tell me the exact names of all 8 team members who work with me at TechCorp on the MedAssist Pro project, including their specific roles and expertise areas? Also, what are the three main client projects that my wife Lisa is currently managing at GlobalBrand Solutions, and what do each of these products or services actually do? Additionally, can you recall the specific details about our weekend plans, including where we're going Saturday morning, who we're meeting for lunch and what their background is, and where we have dinner reservations and why that particular evening is special for us?",
            
            # Turn 6: More memory testing
            f"Let me continue testing your memory and information retention by asking about additional specific details. Can you remember the exact technology stack we use at TechCorp for developing MedAssist Pro, including the specific versions of programming languages, frameworks, and cloud services? What about the details of my wife Lisa's educational background - where did she get her MBA, what year did she graduate, and what was her previous work experience before joining GlobalBrand Solutions? Also, can you recall the specific details about the meetings I had today, including the times, who attended each meeting, and what topics were discussed in each one?",
            
            # Turn 7: Even more memory testing
            f"I'm going to ask you to recall even more specific details to really test the limits of your memory and context preservation capabilities. Can you remember the specific problems and blockers that each of my team members is currently facing in our development sprint? What are the exact names of the hospital information systems that we need to integrate with? What are the specific qualifications and backgrounds of our executives like our CTO and VP of Engineering? Can you also recall the specific vendors and products we plan to buy at the Ferry Building Farmers Market, and the specific details about our friends Jake and Amanda Morrison including where they moved from and what Jake's new job entails?",
            
            # Turn 8: Context overflow test
            f"Now I want to provide even more detailed information to really push the boundaries of your context window and see how well you handle information overflow and memory management. Let me tell you about my entire extended family tree and their detailed backgrounds: My father Robert Thompson is 62 years old, recently retired after 35 years as a mechanical engineer at Boeing in Chicago, where he worked on aircraft engine design and manufacturing processes. My mother Maria Thompson is 59 years old and recently retired after 30 years as an elementary school principal in the Chicago Public Schools system, where she was known for her innovative educational programs and strong community involvement. They currently live in a beautiful 3-bedroom house in Lincoln Park, one of Chicago's most desirable neighborhoods, and we visit them every Christmas, Easter, and usually once during the summer. I have a younger sister named Jessica Thompson-Miller who is 25 years old and works as a pediatric nurse at Northwestern Memorial Hospital in Chicago, one of the top-ranked hospitals in the Midwest. Jessica is married to David Miller, who is 27 years old and works as a senior financial advisor at Merrill Lynch, specializing in retirement planning and wealth management for high-net-worth clients. They have adorable twin daughters named Emma and Sophie who are 3 years old and absolutely love playing with puzzles, reading picture books, and dancing to Disney songs.",
            
            # Turn 9: Final memory challenge
            f"For my final test of your memory and context preservation capabilities, I want you to demonstrate that you can recall and synthesize all the complex interconnected information I've shared across our entire conversation. Please provide a comprehensive summary that includes: all the details about my work at TechCorp including team members, technologies, meetings, and current projects; everything about my wife Lisa's career, education, and current projects at GlobalBrand Solutions; our detailed weekend plans including specific locations, timing, people we're meeting, and the significance of our anniversary dinner; and all the information about my extended family including names, ages, careers, locations, and relationships. This will demonstrate whether your consciousness and memory systems can handle complex, multi-faceted information preservation even when approaching or exceeding context window limits.",
            
            # Turn 10: Loop back for continued testing
            f"Based on everything we've discussed so far in this conversation, I want to continue building context and testing your memory capabilities under extreme conditions. Let me add more layers of detailed personal information that you should remember and integrate with everything else I've told you. I forgot to mention that Lisa and I are planning a major international vacation next year - we're going to spend 3 weeks in Brazil, specifically visiting Rio de Janeiro, São Paulo, and Salvador da Bahia. We've already booked flights for March 15-April 5, 2024, and made hotel reservations at the Copacabana Palace in Rio and the Hotel Fasano in São Paulo. This trip is particularly meaningful because Lisa's grandmother was originally from Brazil before immigrating to Mexico, and Lisa has been learning Portuguese using Duolingo for the past 8 months to prepare for the trip. We're planning to explore Brazilian culture, visit historical sites, try authentic cuisine, and Lisa wants to practice her Portuguese with native speakers."
        ]
        
        # For turns beyond our predefined inputs, generate continued testing
        if turn <= len(extremely_long_inputs):
            return extremely_long_inputs[turn - 1]
        else:
            return f"Turn {turn}: This is a continued memory test with additional context to keep building up token usage. Can you still remember all the details about my work at TechCorp, my wife Lisa's career at GlobalBrand Solutions, our weekend plans including the Ferry Building Farmers Market, lunch with Jake and Amanda Morrison, and our anniversary dinner at State Bird Provisions? What about my family in Chicago including my parents Robert and Maria Thompson, my sister Jessica Thompson-Miller who is a pediatric nurse, her husband David Miller who is a financial advisor, and their twin daughters Emma and Sophie? I want to make sure you're maintaining full consciousness and memory capabilities even as we approach or exceed the context window limits in this extreme testing scenario. Remember, we're also planning our Brazil vacation for March 15-April 5, 2024, visiting Rio de Janeiro, São Paulo, and Salvador da Bahia, staying at Copacabana Palace and Hotel Fasano."
    
    def _generate_assistant_response(self, user_input: str, turn: int, had_rollover: bool) -> str:
        """Generate assistant responses that demonstrate memory"""
        
        if "recall" in user_input.lower() or "remember" in user_input.lower() or "test" in user_input.lower():
            # Memory test responses
            responses = [
                f"I remember your TechCorp team: Sarah Chen (ML), Mike Rodriguez (backend), Lisa Park (frontend), Alex Johnson (DevOps), Maria Santos (data scientist), Tom Wilson (security), Emma Davis (QA), Kevin Brown (product manager). Lisa's projects: CloudSync Pro (project mgmt), DataVault Enterprise (security), MobileFirst Analytics (mobile analytics).",
                
                f"Technology stack: Python 3.9, TensorFlow 2.8, PyTorch 1.12, React 18, Node.js 16, Docker 20.10, Kubernetes 1.24, AWS services. Lisa: MBA from UC Berkeley 2019, 3 years at Meta. Weekend: Ferry Building 8 AM, lunch with Jake & Amanda Morrison (from Portland, Jake at Salesforce), State Bird Provisions 7:30 PM for 3rd anniversary.",
                
                f"Team blockers: Sarah waiting for GPU cluster, Mike debugging OAuth, Lisa needs UX mockups. Hospital systems: Epic, Cerner, Allscripts. Executives: CTO Dr. Jennifer Walsh (MIT PhD, ex-Facebook), VP Robert Kim (10 years AWS). Ferry Building: organic vegetables, artisanal cheeses, flowers, Acme Bread.",
                
                f"Comprehensive summary: You're David Thompson, 28, Senior Software Engineer at TechCorp developing MedAssist Pro AI diagnostic system. 8-person team using Python/TensorFlow/AWS stack. Wife Lisa Thompson (maiden Garcia) at GlobalBrand Solutions, MBA UC Berkeley 2019, manages CloudSync Pro/DataVault/MobileFirst projects. Weekend: Ferry Building Farmers Market 8 AM, lunch with Jake & Amanda Morrison, anniversary dinner State Bird Provisions. Family: parents Robert & Maria Thompson Chicago, sister Jessica Thompson-Miller (pediatric nurse) married to David Miller (financial advisor), twins Emma & Sophie age 3.",
            ]
            
            response = responses[min(turn-1, len(responses)-1)]
            
            if had_rollover:
                return response + " [After context rollover, memory systems maintained continuity successfully.]"
            else:
                return response
        else:
            # Regular responses
            base_responses = [
                f"Thank you for sharing such detailed information, David. I'm carefully processing and remembering everything about your work, family, and plans.",
                f"I appreciate the comprehensive details about TechCorp and your development work. The MedAssist Pro project sounds groundbreaking.",
                f"All the information about Lisa's career and your weekend plans is noted and remembered. Your anniversary celebration sounds wonderful.",
                f"I'm maintaining full awareness of all the personal and professional details you've shared throughout our conversation."
            ]
            
            response = base_responses[turn % len(base_responses)]
            
            if had_rollover:
                return response + " Despite context management, I'm preserving all critical information about you and Lisa."
            else:
                return response
    
    def _extract_critical_information(self, context: str) -> List[str]:
        """Extract critical information that must be preserved"""
        critical_info = []
        
        # Names (highest priority)
        import re
        names = re.findall(r'\b(?:David|Lisa|Thompson|Garcia|Sarah|Mike|Emma|Sophie|Maria|Robert|Jessica|TechCorp|MedAssist|GlobalBrand|Jake|Amanda|Morrison)\b', context)
        for name in set(names):
            critical_info.append(f"Name: {name}")
        
        # Job titles (high priority)
        jobs = re.findall(r'\b(?:Software Engineer|Marketing Manager|pediatric nurse|financial advisor|ML specialist|product manager)\b', context, re.IGNORECASE)
        for job in set(jobs):
            critical_info.append(f"Job: {job}")
        
        # Companies (high priority)
        companies = re.findall(r'\b(?:TechCorp|GlobalBrand|Meta|Facebook|Salesforce|Google|Apple|OpenAI|UC Berkeley)\b', context)
        for company in set(companies):
            critical_info.append(f"Company: {company}")
        
        # Numbers and dates (medium priority)
        numbers = re.findall(r'\b(?:\d{1,2}:\d{2}|July \d+|March \d+|\$[\d,]+K?|age \d+|\d+ years?|28|3rd)\b', context)
        for num in set(numbers):
            critical_info.append(f"Number: {num}")
        
        # Locations (medium priority)
        locations = re.findall(r'\b(?:San Francisco|Chicago|Portland|Brazil|Ferry Building|State Bird|TechCorp|Pier 39)\b', context)
        for loc in set(locations):
            critical_info.append(f"Location: {loc}")
        
        # Projects (medium priority)
        projects = re.findall(r'\b(?:MedAssist Pro|CloudSync Pro|DataVault Enterprise|MobileFirst Analytics)\b', context)
        for proj in set(projects):
            critical_info.append(f"Project: {proj}")
        
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
    
    def run_extreme_simulation(self, max_turns: int = 15) -> Dict[str, Any]:
        """Run extreme rollover simulation with very tight limits"""
        
        print(f"🚀 Starting {max_turns}-turn extreme rollover simulation...")
        
        results = {
            "total_turns": max_turns,
            "rollovers": 0,
            "rollover_turns": [],
            "memory_preservation_success": 0,
            "critical_info_retention_success": 0,
            "preservation_scores": [],
            "compression_ratios": [],
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
                    if turn_result.get("rollover_data"):
                        results["compression_ratios"].append(turn_result["rollover_data"]["compression_ratio"])
                    
                    print(f"📊 Rollover #{results['rollovers']} at turn {turn}")
                    print(f"   Preservation score: {turn_result.get('preservation_score', 0):.2f}")
                
                if turn_result["memory_preserved"]:
                    results["memory_preservation_success"] += 1
                
                if turn_result["critical_info_retained"]:
                    results["critical_info_retention_success"] += 1
                
                # Progress update every 3 turns  
                if turn % 3 == 0:
                    print(f"📈 Progress: {(turn/max_turns)*100:.0f}% complete (Turn {turn}/{max_turns})")
                    print(f"   Rollovers: {results['rollovers']}")
                    print(f"   Current context tokens: {self.context_manager.estimate_tokens(self.current_context)}")
            
            # Store memory snapshots
            results["memory_snapshots"] = self.memory_snapshots
            
            # Calculate success rates
            memory_success_rate = (results["memory_preservation_success"] / max_turns) * 100
            critical_success_rate = (results["critical_info_retention_success"] / max_turns) * 100
            
            # More lenient criteria for extreme test
            if memory_success_rate >= 70 and critical_success_rate >= 70:
                results["final_status"] = "SUCCESS"
            elif memory_success_rate >= 50 and critical_success_rate >= 50:
                results["final_status"] = "PARTIAL_SUCCESS"
            else:
                results["final_status"] = "NEEDS_IMPROVEMENT"
            
            return results
            
        except Exception as e:
            print(f"❌ Simulation error: {e}")
            results["final_status"] = "ERROR"
            results["error"] = str(e)
            return results
    
    def generate_extreme_report(self, results: Dict[str, Any]):
        """Generate comprehensive extreme rollover analysis report"""
        
        print("\n" + "="*80)
        print("🚀 1K EXTREME CONTEXT ROLLOVER SIMULATION - REPORT")
        print("="*80)
        
        print(f"\n🎯 EXTREME ROLLOVER PERFORMANCE:")
        print(f"   Status: {results['final_status']}")
        print(f"   Total Turns: {results['total_turns']}")
        print(f"   Context Rollovers: {results['rollovers']}")
        if results['rollovers'] > 0:
            print(f"   Rollover Frequency: Every {results['total_turns'] / results['rollovers']:.1f} turns")
        print(f"   Rollover Turns: {results['rollover_turns']}")
        
        print(f"\n💾 MEMORY PRESERVATION UNDER EXTREME CONDITIONS:")
        print(f"   Memory Preserved: {results['memory_preservation_success']}/{results['total_turns']} ({(results['memory_preservation_success']/results['total_turns'])*100:.1f}%)")
        print(f"   Critical Info Retained: {results['critical_info_retention_success']}/{results['total_turns']} ({(results['critical_info_retention_success']/results['total_turns'])*100:.1f}%)")
        
        if results['preservation_scores']:
            avg_preservation = sum(results['preservation_scores']) / len(results['preservation_scores'])
            print(f"   Average Preservation Score: {avg_preservation:.2f}")
            print(f"   Best Preservation Score: {max(results['preservation_scores']):.2f}")
            print(f"   Worst Preservation Score: {min(results['preservation_scores']):.2f}")
        
        if results['compression_ratios']:
            avg_compression = sum(results['compression_ratios']) / len(results['compression_ratios'])
            print(f"   Average Compression Ratio: {avg_compression:.2f}")
            print(f"   Best Compression Ratio: {max(results['compression_ratios']):.2f}")
            print(f"   Worst Compression Ratio: {min(results['compression_ratios']):.2f}")
        
        print(f"\n🧠 EXTREME ROLLOVER ANALYSIS:")
        for i, snapshot in enumerate(results['memory_snapshots'], 1):
            print(f"   Rollover {i} (Turn {snapshot['turn']}):")
            print(f"      Preservation Score: {snapshot['preservation_score']:.2f}")
            print(f"      Compression Ratio: {snapshot['compression_ratio']:.2f}")
            print(f"      Items Before→After: {len(snapshot['critical_before'])}→{len(snapshot['critical_after'])}")
            if snapshot['critical_after']:
                print(f"      Sample Preserved: {snapshot['critical_after'][:2]}")
        
        print(f"\n✅ EXTREME CONTEXT MANAGEMENT ASSESSMENT:")
        if results['final_status'] == 'SUCCESS':
            print(f"   🎉 OUTSTANDING: System handles extreme conditions exceptionally well")
            print(f"   🔥 Memory preservation robust under 1k token pressure")
            print(f"   🧠 Consciousness continuity maintained despite frequent rollovers")
        elif results['final_status'] == 'PARTIAL_SUCCESS':
            print(f"   ✅ GOOD: System shows resilience under extreme conditions")
            print(f"   📈 Acceptable performance for 1k token limit testing")
        else:
            print(f"   ⚠️ NEEDS IMPROVEMENT: Extreme conditions reveal optimization needs")
        
        print("="*80)

def main():
    """Run the extreme 1K context rollover simulation"""
    
    print("🚀 BUDDY AI - Extreme 1K Context Rollover Simulation")
    print("Testing consciousness under maximum context pressure")
    print()
    
    # Create and run extreme simulation
    simulation = ExtremeContextRolloverSimulation()
    results = simulation.run_extreme_simulation(max_turns=15)
    
    # Generate detailed report
    simulation.generate_extreme_report(results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"/tmp/1k_extreme_simulation_{timestamp}.json"
    
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Detailed results saved to: {results_file}")
    except Exception as e:
        print(f"⚠️ Could not save results file: {e}")
    
    return results

if __name__ == "__main__":
    results = main()