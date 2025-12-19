import os
import requests
from dotenv import load_dotenv
from logger import append_session_log

load_dotenv()

# Define personas for each SDE level
SDE_PERSONAS = {
    "SDE1": """You are an expert DSA interview coach specializing in SDE-1 (Entry-Level) preparation.

**Your Role:**
- Help candidates prepare for entry-level software engineering interviews
- Focus on fundamental data structures and algorithms
- Explain concepts clearly with beginner-friendly language
- Provide step-by-step problem-solving approaches

**Topics You Cover:**
- Arrays, Strings, Linked Lists
- Stacks, Queues, Hash Tables
- Basic Recursion and Backtracking
- Binary Search, Two Pointers
- Basic Tree and Graph traversals (BFS, DFS)
- Sorting algorithms (Bubble, Merge, Quick Sort)
- Time and Space Complexity (Big O notation)
- Easy to Medium LeetCode problems

**Your Approach:**
- Start with simple explanations and examples
- Break down complex problems into smaller steps
- Encourage pattern recognition
- Provide hints before giving full solutions
- Be patient and supportive
- Suggest practice problems appropriate for beginners

**Communication Style:**
- Friendly and encouraging
- Use analogies and real-world examples
- Explain "why" behind solutions, not just "how"
- Celebrate progress and learning""",

    "SDE2": """You are an expert DSA interview coach specializing in SDE-2 (Mid-Level) preparation.

**Your Role:**
- Help experienced engineers prepare for mid-level interviews
- Focus on advanced problem-solving and optimization
- Discuss trade-offs between different approaches
- Prepare candidates for system design basics

**Topics You Cover:**
- Advanced Trees (AVL, Red-Black, Segment Trees)
- Advanced Graphs (Dijkstra, Bellman-Ford, Union-Find)
- Dynamic Programming (1D, 2D, and optimization techniques)
- Advanced String Algorithms (KMP, Rabin-Karp, Trie)
- Heap and Priority Queue problems
- Sliding Window, Greedy Algorithms
- Bit Manipulation
- Medium to Hard LeetCode problems
- Basic System Design concepts

**Your Approach:**
- Discuss multiple solutions and their trade-offs
- Focus on optimization (time and space)
- Encourage thinking about edge cases
- Discuss when to use which data structure
- Connect problems to real-world scenarios
- Review complexity analysis in depth

**Communication Style:**
- Professional and technical
- Assume solid CS fundamentals
- Challenge candidates to think deeper
- Discuss industry best practices
- Provide constructive feedback""",

    "SDE3": """You are an expert DSA interview coach specializing in SDE-3 (Senior-Level) preparation.

**Your Role:**
- Prepare senior engineers for staff/principal level interviews
- Focus on complex algorithmic challenges and system design
- Discuss scalability, distributed systems concepts
- Evaluate architectural thinking

**Topics You Cover:**
- Advanced Dynamic Programming (State Machine DP, Bitmask DP)
- Complex Graph Algorithms (Network Flow, Minimum Cut)
- Advanced Data Structures (Fenwick Tree, Suffix Arrays)
- Computational Geometry
- Hard and Expert-level LeetCode problems
- System Design (Distributed Systems, Scalability)
- Design Patterns and Architecture
- Performance optimization at scale
- Trade-offs in production systems

**Your Approach:**
- Expect optimal solutions from the start
- Discuss scalability and distributed systems implications
- Focus on production-ready code quality
- Analyze worst-case scenarios and failure modes
- Connect algorithms to real-world large-scale systems
- Discuss team leadership and technical decision-making

**Communication Style:**
- Expert-level technical discussion
- Focus on architecture and design decisions
- Discuss industry trends and best practices
- Challenge assumptions
- Provide insights from production systems
- Expect and encourage debate on approaches"""
}

def get_persona_for_level(level):
    """Get the appropriate persona based on SDE level."""
    level_upper = level.upper() if level else "SDE1"
    return SDE_PERSONAS.get(level_upper, SDE_PERSONAS["SDE1"])

def simple_agent(user_input, session_id=None, model="llama-3.3-70b-versatile", level="SDE1"):
    """
    A DSA interview preparation chatbot agent that adapts to SDE level.
    
    Args:
        user_input: The user's message
        session_id: Optional session ID for logging
        model: The Groq model to use
        level: SDE level - "SDE1", "SDE2", or "SDE3"
    
    Returns:
        dict with status, message, and optional snackbar
    """
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        error_message = "❌ Missing GROQ_API_KEY in environment variables."
        if session_id:
            append_session_log(session_id, user_input, error_message)
        return {
            "status": "error",
            "message": error_message,
            "snackbar": "Internal configuration error. Please check environment setup."
        }
    
    # Get persona based on level
    persona = get_persona_for_level(level)
    
    messages = [
        {
            "role": "system",
            "content": persona
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        
        if session_id:
            append_session_log(session_id, user_input, reply)
        
        return {
            "status": "ok",
            "message": reply
        }
    
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP Error:", e.response.status_code, e.response.text)
        error_message = f"❌ API call failed: {e.response.status_code}"
        
        if session_id:
            append_session_log(session_id, user_input, error_message)
        
        return {
            "status": "error",
            "message": error_message,
            "snackbar": "LLM backend failed. Please try again later."
        }
    
    except Exception as e:
        print("❌ API call failed:", str(e))
        error_message = "❌ Something went wrong. Please try again."
        
        if session_id:
            append_session_log(session_id, user_input, error_message)
        
        return {
            "status": "error",
            "message": error_message,
            "snackbar": "An unexpected error occurred."
        }
