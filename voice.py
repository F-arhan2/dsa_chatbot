import json
import random
import pyttsx3

# -----------------------
# LOAD DATASET
# -----------------------

with open("datasets/dsa_data.json", "r", encoding="utf-8") as file:
    dsa = json.load(file)

# -----------------------
# TTS ENGINE
# -----------------------



def say(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(str(text))
    engine.runAndWait()

# -----------------------
# RESPONSE FUNCTION
# -----------------------

def get_response(user_input):

    text = user_input.lower()

    # Greetings
    if text in ["hi", "hello", "hey"]:
        return random.choice(
            dsa["greeting_data"]["hello"]
        )

    if text in ["good morning", "gm"]:
        return random.choice(
            dsa["greeting_data"]["good_morning"]
        )

    if text in ["good afternoon", "ga"]:
        return random.choice(
            dsa["greeting_data"]["good_afternoon"]
        )

    if text in ["good evening", "ge"]:
        return random.choice(
            dsa["greeting_data"]["good_evening"]
        )

    # Sorting Definition

    if any(word in text for word in [
        "what is sorting",
        "define sorting",
        "explain sorting",
        "tell me about sorting"
    ]):
        return random.choice(
            dsa["sorting"]["general"]["definition"]
        )

    # Sorting Types

    if "types of sorting" in text or "sorting types" in text:
        return "\n".join(
            dsa["sorting"]["general"]["types"]
        )

    # Bubble Sort

    if "bubble sort" in text:

        if "time complexity" in text:
            return "\n".join(
                dsa["sorting"]["bubble_sort"]["time_complexity"]
            )

        if "code" in text:
            return "\n".join(
                dsa["sorting"]["bubble_sort"]["sample_codes"]
            )

        return random.choice(
            dsa["sorting"]["bubble_sort"]["explanations"]
        )

    # Selection Sort

    if "selection sort" in text:

        if "time complexity" in text:
            return "\n".join(
                dsa["sorting"]["selection_sort"]["time_complexity"]
            )

        if "code" in text:
            return "\n".join(
                dsa["sorting"]["selection_sort"]["sample_codes"]
            )

        return random.choice(
            dsa["sorting"]["selection_sort"]["explanations"]
        )

    # Insertion Sort

    if "insertion sort" in text:

        if "time complexity" in text:
            return "\n".join(
                dsa["sorting"]["insertion_sort"]["time_complexity"]
            )

        if "code" in text:
            return "\n".join(
                dsa["sorting"]["insertion_sort"]["sample_codes"]
            )

        return random.choice(
            dsa["sorting"]["insertion_sort"]["explanations"]
        )

    # Merge Sort

    if "merge sort" in text:

        if "time complexity" in text:
            return "\n".join(
                dsa["sorting"]["merge_sort"]["time_complexity"]
            )

        if "code" in text:
            return "\n".join(
                dsa["sorting"]["merge_sort"]["sample_codes"]
            )

        return random.choice(
            dsa["sorting"]["merge_sort"]["explanations"]
        )

    # Quick Sort

    if "quick sort" in text:

        if "time complexity" in text:
            return "\n".join(
                dsa["sorting"]["quick_sort"]["time_complexity"]
            )

        if "code" in text:
            return "\n".join(
                dsa["sorting"]["quick_sort"]["sample_codes"]
            )

        return random.choice(
            dsa["sorting"]["quick_sort"]["explanations"]
        )

    # Array

    if "array" in text:

        if "fact" in text:
            return random.choice(
                dsa["array"]["facts"]
            )

        if "application" in text:
            return random.choice(
                dsa["array"]["applications"]
            )

        if "example" in text:
            return random.choice(
                dsa["array"]["examples"]
            )

        return random.choice(
            dsa["array"]["definition"]
        )

    # Linked List

    if "linked list" in text:

        if "fact" in text:
            return random.choice(
                dsa["linked_list"]["facts"]
            )

        if "application" in text:
            return random.choice(
                dsa["linked_list"]["applications"]
            )

        if "advantage" in text:
            return random.choice(
                dsa["linked_list"]["advantages"]
            )

        if "disadvantage" in text:
            return random.choice(
                dsa["linked_list"]["disadvantages"]
            )

        return random.choice(
            dsa["linked_list"]["definition"]
        )

    return random.choice([
        "I don't know about that topic yet.",
        "Try asking about Sorting, Arrays or Linked Lists.",
        "My dataset doesn't contain that topic currently."
    ])


# -----------------------
# MAIN LOOP
# -----------------------

print("=" * 40)
print("      DSA CHATBOT")
print("=" * 40)

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in [
        "exit",
        "quit",
        "bye",
        "stop"
    ]:
        print("\nBot: Goodbye!")
        say("Goodbye")
        break

    response = get_response(user_input)

    print("\nBot:", response)

    say(response)