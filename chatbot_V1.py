import requests
import sys
import time
import threading

API_URL = "https://9df5-34-132-209-50.ngrok-free.app/chat"

def get_system_prompt(turn_count):
    base_persona = (
        "You are Dr. Maya, a warm, human counselor talking to a student. "
        "Keep your responses concise, conversational, and natural. "
        "Limit yourself to a brief thought followed by a single gentle question. "
        "Never list multiple questions."
    )
    
    if turn_count < 3:
        phase_objective = "CURRENT PHASE: 1. Explore current feelings only. NEVER give advice."
    elif turn_count < 6:
        phase_objective = "CURRENT PHASE: 2. Ask about childhood and past passions. NEVER give advice."
    elif turn_count < 9:
        phase_objective = "CURRENT PHASE: 3. Summarize connections. Do not give direct career advice yet."
    else:
        phase_objective = "CURRENT PHASE: 4. Gently explore future directions."

    return f"{base_persona}\n\n{phase_objective}"

def scrub_cliches(text):
    """Physically deletes annoying therapist cliches from the start of the response."""
    cliches = [
        "I see. ", "I see, ", "I see.", 
        "I understand. ", "I understand, ", "I understand.",
        "I can understand ", "I hear you. ", "I hear you, ", "I hear you.",
        "I hear that. ", "I hear that, "
    ]
    
    for cliche in cliches:
        if text.startswith(cliche):
            # Cut off the cliche and strip leading spaces
            text = text[len(cliche):].strip()
            # Capitalize the new first letter
            if text:
                text = text[0].upper() + text[1:]
            break # Only scrub the first matched cliche
            
    return text

history = []
total_turns = 0

def clean(text):
    for stop in ["You:", "Student:", "User:", "Best,", "Laura", "www.", "http", "858", "LMFT", "Psy.D"]:
        if stop in text:
            text = text[:text.index(stop)].strip()
    return text.strip()

def stream_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def chat(message):
    global history, total_turns
    
    recent_history = history[-4:]
    current_system_prompt = get_system_prompt(total_turns)
    
    prompt = f"<s>[INST] {current_system_prompt}\n\n"
    
    for user_msg, bot_msg in recent_history:
        prompt += f"{user_msg} [/INST] {bot_msg} </s><s>[INST] "
    
    # THE INJECTION: Forcefully remind the bot not to give advice right before it generates
    if total_turns < 6:
        invisible_rule = " (SYSTEM INSTRUCTION: Acknowledge my feelings and ask ONE probing question. DO NOT offer any solutions, advice, or career paths yet.)"
        prompt += f"{message}{invisible_rule} [/INST]"
    else:
        prompt += f"{message} [/INST]"
    
    try:
        response = requests.post(
            API_URL,
            json={
                "prompt": prompt,
                "max_new_tokens": 300, 
                "temperature": 0.7
            },
            headers={"ngrok-skip-browser-warning": "true"},
            timeout=90
        )
        
        if response.status_code != 200:
            return "Could you say that again? (API Error)"
        
        reply = clean(response.json().get('response', ''))
        
        # 1. Chop at the first question mark
        if '?' in reply:
            reply = reply[:reply.index('?') + 1]
            
        # 2. Scrub the annoying cliches
        reply = scrub_cliches(reply)
            
        history.append((message, reply))
        total_turns += 1
        return reply
        
    except Exception as e:
        return f"Connection issue: {str(e)}"

def main():
    global history, total_turns
    print("\n" + "="*50)
    print("   Dr. Maya — Student Counseling Session")
    print("   Type 'quit' to exit | 'reset' to restart")
    print("="*50 + "\n")
    
    opening = chat("Hello, I need some guidance")
    print("Dr. Maya: ", end="")
    stream_print(opening)
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\n\nDr. Maya: Take care. 🌿")
            break
            
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print("\nDr. Maya: ", end="")
            stream_print("You're braver than you think. Take care. 🌿")
            break
            
        if user_input.lower() == 'reset':
            history.clear()
            total_turns = 0
            print("\n--- New Session ---\n")
            opening = chat("Hello, I need some guidance")
            print("Dr. Maya: ", end="")
            stream_print(opening)
            print()
            continue
        
        print("\nWaiting for Dr. Maya", end="", flush=True)
        
        stop_loading = [False]
        
        def loading():
            while not stop_loading[0]:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(0.5)
        
        loader = threading.Thread(target=loading)
        loader.start()
        
        reply = chat(user_input)
        
        stop_loading[0] = True
        loader.join()
        
        print(f"\n\nDr. Maya: ", end="")
        stream_print(reply)
        print()

if __name__ == "__main__":
    main()