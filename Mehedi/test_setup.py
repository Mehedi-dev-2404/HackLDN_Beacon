"""
Quick test script for Aura backend components.
Run this after setting up .env to verify everything works.
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 Testing Aura Backend Components\n")

# Test 1: Config and API keys
print("1️⃣ Testing config and API keys...")
try:
    from backend.config import gemini_model, GEMINI_KEY, ELEVEN_KEY
    print("   ✅ Config loaded successfully")
    print(f"   ✅ GEMINI_KEY: {GEMINI_KEY[:10]}...")
    print(f"   ✅ ELEVEN_KEY: {ELEVEN_KEY[:10]}...")
except Exception as e:
    print(f"   ❌ Config failed: {e}")
    sys.exit(1)

# Test 2: Socratic Engine
print("\n2️⃣ Testing Socratic Engine...")
try:
    from intelligence.socratic_engine import socratic_viva
    question = socratic_viva("Python recursion", "I'm not sure")
    print(f"   ✅ Generated question: {question[:100]}...")
except Exception as e:
    print(f"   ❌ Socratic engine failed: {e}")

# Test 3: Career Matcher
print("\n3️⃣ Testing Career Matcher...")
try:
    from intelligence.career_matcher import analyze_career_match
    test_job = """
    Graduate Software Engineer
    Required: Python, JavaScript, problem-solving
    Experience: Junior level
    """
    result = analyze_career_match(test_job)
    print(f"   ✅ Analysis completed: {len(result['technical_skills'])} technical skills found")
except Exception as e:
    print(f"   ❌ Career matcher failed: {e}")

# Test 4: Integrity Guard
print("\n4️⃣ Testing Integrity Guard...")
try:
    from intelligence.integrity_guard import check_academic_integrity
    
    # Test legitimate query
    legit = check_academic_integrity("Can you explain recursion?")
    print(f"   ✅ Legitimate query: {legit['is_acceptable']}")
    
    # Test violation
    violation = check_academic_integrity("Write my essay for me")
    print(f"   ✅ Violation detected: {not violation['is_acceptable']}")
except Exception as e:
    print(f"   ❌ Integrity guard failed: {e}")

# Test 5: Chunker
print("\n5️⃣ Testing Chunker...")
try:
    from intelligence.chunker import chunk_text, chunk_by_sentences
    test_text = "Sentence one. Sentence two. " * 100
    chunks = chunk_text(test_text, max_chunk_size=200)
    print(f"   ✅ Created {len(chunks)} chunks")
except Exception as e:
    print(f"   ❌ Chunker failed: {e}")

print("\n✨ All tests completed!\n")
print("🚀 You can now run: cd backend && python main.py")
