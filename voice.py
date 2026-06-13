import random
import json
import pyttsx3

# -----------------------
# Load Dataset
# -----------------------
with open("datasets/dsa_data.json", "r") as file:
    dsa = json.load(file)

# -----------------------
# TTS Engine (initialize once - FIXED)
# -----------------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def say(text):
    engine.say(str(text))
    engine.runAndWait()

# -----------------------
# INTENT CONFIG (NEW ARCHITECTURE)
# -----------------------
INTENTS = {
    "sorting": ["sorting"],
    "bubble_sort": ["bubble sort", "bubble"],
    "selection_sort": ["selection sort"],
    "insertion_sort": ["insertion sort"],
    "merge_sort": ["merge sort"],
    "quick_sort": ["quick sort"],
    "array": ["array"],
    "linked_list": ["linked list", "linkedlist"],
    "operations": ["insert", "delete", "traversal", "search"],
    "greeting": ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
}

# -----------------------
# DETECT INTENT (UPGRADED)
# -----------------------
def detect_intent(text):
    text = text.lower()

    for intent, keywords in INTENTS.items():
        if any(k in text for k in keywords):

            if intent == "greeting":
                if "morning" in text or text == "good morning":
                    return ("greeting", "greeting_data", "good_morning")
                if "afternoon" in text:
                    return ("greeting", "greeting_data", "good_afternoon")
                if "evening" in text:
                    return ("greeting", "greeting_data", "good_evening")
                return ("greeting", "greeting_data", "hello")

            if intent in dsa.get("sorting", {}):
                return ("dsa", intent, detect_subtopic(text))

            if intent in dsa.get("array", {}):
                return ("dsa", "array", detect_subtopic(text))

            if intent in dsa.get("linked_list", {}):
                return ("dsa", "linked_list", detect_subtopic(text))

            if intent == "operations":
                return ("dsa", "operations", detect_subtopic(text))

    return ("unknown", "unknown", "unknown")

# -----------------------
# SUBTOPIC DETECTION (NEW)
# -----------------------
def detect_subtopic(text):
    if "time complexity" in text:
        return "time_complexity"
    if "code" in text:
        return "sample_code"
    if "types" in text:
        return "types"
    if "fact" in text:
        return "facts"
    if "application" in text:
        return "applications"
    if "example" in text:
        return "examples"
    return "explanation"

# -----------------------
# RESPONSE ENGINE (FIXED + CLEAN)
# -----------------------
def generate_text(intent):
    main, topic, sub = intent

    if main == "greeting":
        return random.choice(dsa["greeting_data"][sub])

    if main == "dsa":

        # sorting
        if topic in dsa.get("sorting", {}):
            data = dsa["sorting"][topic]

            if sub in data:
                return random.choice(data[sub])

            return random.choice(data["explanations"])

        # array
        if topic == "array":
            return random.choice(dsa["array"][sub])

        # linked list
        if topic == "linked_list":
            return random.choice(dsa["linked_list"][sub])

        # operations (NEW)
        if topic == "operations":
            return random.choice(dsa["operations"][sub])

    return "I don't know about that topic yet."

# -----------------------
# MAIN LOOP
# -----------------------
print("DSA BOT STARTED (INDUSTRY LEVEL VERSION)")

while True:
    user = input("\nYou: ").lower()

    if user in ["exit", "quit", "bye"]:
        print("Bot: Goodbye!")
        say("Goodbye")
        break

    intent = detect_intent(user)
    response = generate_text(intent)

    print("Bot:", response)
    say(response)