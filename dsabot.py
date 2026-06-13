import os
import sys
import math
import json
import random
import time
import threading
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import pyttsx3

# Set default theme styling to dark
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# -------------------------------------------------------------------------
# TEXT TO SPEECH (Threaded & Toggleable)
# -------------------------------------------------------------------------
class TTSManager:
    def __init__(self):
        self.enabled = True
        self._engine_lock = threading.Lock()
        
    def say(self, text):
        if not self.enabled:
            return
        # Run speech synthesis in a background thread to prevent UI freezing
        threading.Thread(target=self._speak_worker, args=(text,), daemon=True).start()

    def _speak_worker(self, text):
        with self._engine_lock:
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 165)
                # Clean up some markdown-like code indicators for cleaner speech
                clean_text = text.replace("`", "").replace("- ", "")
                if len(clean_text) > 300:
                    clean_text = clean_text[:300] + "... and so on."
                engine.say(clean_text)
                engine.runAndWait()
            except Exception:
                pass

tts = TTSManager()

# -------------------------------------------------------------------------
# MOCK / BACKUP DATASET (If json file is missing)
# -------------------------------------------------------------------------
DEFAULT_DATASET = {
    "sorting": {
        "general": {
            "definition": ["Sorting is the process of arranging data in a specific order, typically ascending or descending."],
            "types": ["- Bubble Sort", "- Selection Sort", "- Insertion Sort", "- Merge Sort", "- Quick Sort"]
        },
        "bubble_sort": {
            "explanations": ["Bubble Sort repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order."],
            "time_complexity": ["Worst Case: O(n^2)", "Average Case: O(n^2)", "Best Case: O(n)"],
            "sample_codes": ["def bubbleSort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]"]
        },
        "selection_sort": {
            "explanations": ["Selection Sort divides the input list into two parts: a sorted sublist and an unsorted sublist, repeatedly finding the minimum element."],
            "time_complexity": ["Worst/Avg/Best Case: O(n^2)"],
            "sample_codes": ["# Selection Sort Implementation\nfor i in range(len(A)):\n    min_idx = i\n    for j in range(i+1, len(A)):\n        if A[min_idx] > A[j]: min_idx = j\n    A[i], A[min_idx] = A[min_idx], A[i]"]
        }
    },
    "array": {
        "definition": ["An array is a collection of elements stored at contiguous memory locations."],
        "facts": ["Arrays provide O(1) random access time by index."],
        "applications": ["Used for implementing matrices, lookup tables, and dynamic heaps."],
        "examples": ["Example: arr = [10, 20, 30, 40, 50]"]
    },
    "linked_list": {
        "definition": ["A linked list is a linear data structure where elements are stored in nodes, and each node points to the next."],
        "facts": ["Linked lists have dynamic sizes and ease of insertion/deletion compared to arrays."],
        "applications": ["Used in Undo/Redo operations, OS task schedulers, and Graph adjacency lists."],
        "advantages": ["Dynamic memory allocation; no memory wastage."],
        "disadvantages": ["No random access allowed; extra memory required for pointer fields."],
        "types": {
            "singly_linked_list": {"explanations": ["Nodes only point forward to the next node."], "sample_codes": ["class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None"]},
            "doubly_linked_list": {"explanations": ["Nodes point both to the next node and the previous node."], "sample_codes": ["class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n        self.prev = None"]},
            "circular_linked_list": {"explanations": ["The last node points back to the first node."], "sample_codes": ["# Tail next points back to Head node\ntail.next = head"]},
            "circular_doubly_linked_list": {"explanations": ["The nodes are doubly linked, and the tail next points to head, head prev points to tail."], "sample_codes": ["# Bi-directional circular loops"]}
        }
    }
}

# Load Dataset Safely
try:
    if os.path.exists("datasets/dsa_data.json"):
        with open("datasets/dsa_data.json", "r") as file:
            dsa = json.load(file)
    else:
        dsa = DEFAULT_DATASET
except Exception:
    dsa = DEFAULT_DATASET

sorting = dsa.get("sorting", DEFAULT_DATASET["sorting"])
array = dsa.get("array", DEFAULT_DATASET["array"])
linked_list = dsa.get("linked_list", DEFAULT_DATASET["linked_list"])

# -------------------------------------------------------------------------
# BOT CORE LOGIC
# -------------------------------------------------------------------------
def detect_intent(user_input):
    text = user_input.lower()
    explain_keywords = ["what is", "explain", "define", "tell me", "about"]

    if "sorting" in text:
        if any(word in text for word in explain_keywords): return ("dsa", "sorting", "definition")
        if "type" in text: return ("dsa", "sorting", "types")
        return ("dsa", "sorting", "definition")
    elif "bubble sort" in text:
        if "time complexity" in text: return ("dsa", "bubble_sort", "time_complexity")
        if "code" in text: return ("dsa", "bubble_sort", "sample_code")
        return ("dsa", "bubble_sort", "explanation")
    elif "selection sort" in text:
        if "time complexity" in text: return ("dsa", "selection_sort", "time_complexity")
        if "code" in text: return ("dsa", "selection_sort", "sample_code")
        return ("dsa", "selection_sort", "explanation")
    elif "insertion sort" in text:
        if "time complexity" in text: return ("dsa", "insertion_sort", "time_complexity")
        if "code" in text: return ("dsa", "insertion_sort", "sample_code")
        return ("dsa", "insertion_sort", "explanation")
    elif "merge sort" in text:
        if "time complexity" in text: return ("dsa", "merge_sort", "time_complexity")
        if "code" in text: return ("dsa", "merge_sort", "sample_code")
        return ("dsa", "merge_sort", "explanation")
    elif "quick sort" in text:
        if "time complexity" in text: return ("dsa", "quick_sort", "time_complexity")
        if "code" in text: return ("dsa", "quick_sort", "sample_code")
        return ("dsa", "quick_sort", "explanation")
    elif "circular doubly linked list" in text:
        if "code" in text: return ("dsa", "linked_list_code", "circular_doubly_linked_list")
        return ("dsa", "linked_list", "circular_doubly_linked_list")
    elif "circular linked list" in text:
        if "code" in text: return ("dsa", "linked_list_code", "circular_linked_list")
        return ("dsa", "linked_list", "circular_linked_list")
    elif "doubly linked list" in text:
        if "code" in text: return ("dsa", "linked_list_code", "doubly_linked_list")
        return ("dsa", "linked_list", "doubly_linked_list")
    elif "singly linked list" in text:
        if "code" in text: return ("dsa", "linked_list_code", "singly_linked_list")
        return ("dsa", "linked_list", "singly_linked_list")
    elif "linked list" in text:
        if "fact" in text: return ("dsa", "linked_list", "facts")
        if "application" in text: return ("dsa", "linked_list", "applications")
        if "advantage" in text: return ("dsa", "linked_list", "advantages")
        if "disadvantage" in text: return ("dsa", "linked_list", "disadvantages")
        if "type" in text: return ("dsa", "linked_list", "types")
        return ("dsa", "linked_list", "definition")
    elif "array" in text:
        if "fact" in text: return ("dsa", "array", "facts")
        if "application" in text: return ("dsa", "array", "applications")
        if "example" in text: return ("dsa", "array", "examples")
        return ("dsa", "array", "definition")
    return ("unknown", "unknown", "unknown")

def generate_text(intent):
    main_domain, topic, subtopic = intent
    if main_domain == "dsa":
        if topic == "sorting":
            if subtopic == "definition": return random.choice(sorting["general"]["definition"])
            if subtopic == "types": return "\n".join(sorting["general"]["types"])
        elif topic in sorting:
            if subtopic == "explanation": return random.choice(sorting[topic]["explanations"])
            if subtopic == "time_complexity": return "\n".join(sorting[topic]["time_complexity"])
            if subtopic == "sample_code": return "\n".join(sorting[topic]["sample_codes"])
        elif topic == "array":
            if subtopic == "definition": return random.choice(array["definition"])
            if subtopic == "facts": return random.choice(array["facts"])
            if subtopic == "applications": return random.choice(array["applications"])
            if subtopic == "examples": return random.choice(array["examples"])
        elif topic == "linked_list":
            if subtopic == "definition": return random.choice(linked_list["definition"])
            if subtopic == "facts": return random.choice(linked_list["facts"])
            if subtopic == "applications": return random.choice(linked_list["applications"])
            if subtopic == "advantages": return random.choice(linked_list["advantages"])
            if subtopic == "disadvantages": return random.choice(linked_list["disadvantages"])
            if subtopic == "types":
                return "Types of Linked Lists:\n- Singly Linked List\n- Doubly Linked List\n- Circular Linked List\n- Circular Doubly Linked List"
            elif subtopic in linked_list.get("types", {}):
                return random.choice(linked_list["types"][subtopic]["explanations"])
        elif topic == "linked_list_code":
            if subtopic in linked_list.get("types", {}):
                return "\n".join(linked_list["types"][subtopic]["sample_codes"])
    return random.choice([
        "I don't know about that topic yet.",
        "Try asking about Sorting, Arrays or Linked Lists.",
        "My dataset doesn't contain that specific request layout."
    ])

# -------------------------------------------------------------------------
# CYBERPUNK / HUD COMPONENT INTERFACES
# -------------------------------------------------------------------------
class StarfieldCanvas(tk.Canvas):
    """An efficient animated 2D pipeline displaying an expansive warp field background."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.stars = []
        self.num_stars = 75
        self.bind("<Configure>", self.on_resize)
        self.animation_running = True
        
    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.init_stars()
        
    def init_stars(self):
        self.stars = []
        for _ in range(self.num_stars):
            self.stars.append({
                'x': random.uniform(-self.width/2, self.width/2),
                'y': random.uniform(-self.height/2, self.height/2),
                'z': random.uniform(1, self.width),
                'color': random.choice(["#00f0ff", "#ff007f", "#ffffff", "#7000ff"])
            })

    def animate(self):
        if not self.animation_running or not hasattr(self, 'width'):
            if self.winfo_exists():
                self.after(30, self.animate)
            return
            
        self.delete("all")
        # Draw tech matrix floor grid accent lines
        self.create_line(0, self.height*0.85, self.width, self.height*0.85, fill="#003344", width=1)
        
        cx, cy = self.width / 2, self.height / 2
        for s in self.stars:
            s['z'] -= 4
            if s['z'] <= 0:
                s['z'] = self.width
                s['x'] = random.uniform(-self.width/2, self.width/2)
                s['y'] = random.uniform(-self.height/2, self.height/2)

            # Perspective projection calculation
            k = 400.0 / s['z']
            px = int(s['x'] * k + cx)
            py = int(s['y'] * k + cy)

            if 0 <= px < self.width and 0 <= py < self.height:
                size = max(1, int((1 - s['z']/self.width) * 5))
                self.create_oval(px, py, px+size, py+size, fill=s['color'], outline="")
                
        if self.winfo_exists():
            self.after(25, self.animate)

class HologramRingCanvas(tk.Canvas):
    """Renders a complex rotating 3D vector-ring system with pulsing HUD arcs."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.angle = 0
        self.pulse = 0
        self.bind("<Configure>", lambda e: self.draw())
        
    def draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10: return
        cx, cy = w // 2, h // 2
        
        radius = min(w, h) // 3
        pulse_offset = math.sin(self.pulse) * 8
        r_final = radius + pulse_offset
        
        # Draw nested procedural technology circles
        self.create_oval(cx - r_final, cy - r_final, cx + r_final, cy + r_final, outline="#00f0ff", width=2)
        self.create_oval(cx - r_final + 15, cy - r_final + 15, cx + r_final - 15, cy + r_final - 15, outline="#7000ff", width=1, dash=(10, 10))
        self.create_oval(cx - r_final - 10, cy - r_final - 10, cx + r_final + 10, cy + r_final + 10, outline="#005577", width=1)

        # Dynamic rotating segments
        for i in range(4):
            cur_angle = self.angle + (i * 90)
            rad1 = math.radians(cur_angle)
            rad2 = math.radians(cur_angle + 35)
            
            x1, y1 = cx + (r_final + 5) * math.cos(rad1), cy + (r_final + 5) * math.sin(rad1)
            x2, y2 = cx + (r_final + 5) * math.cos(rad2), cy + (r_final + 5) * math.sin(rad2)
            self.create_line(x1, y1, x2, y2, fill="#ff007f", width=4)
            
        # Geometric cross-hairs
        self.create_line(cx - 20, cy, cx + 20, cy, fill="#00f0ff", width=1)
        self.create_line(cx, cy - 20, cx, cy + 20, fill="#00f0ff", width=1)

    def update_anim(self):
        self.angle = (self.angle + 3) % 360
        self.pulse += 0.1
        self.draw()
        if self.winfo_exists():
            self.after(30, self.update_anim)

# -------------------------------------------------------------------------
# MAIN CORE CONTAINER INTERFACE
# -------------------------------------------------------------------------
class DSABotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DSA AI CORE CHATBOT")
        self.geometry("1400x800")
        self.configure(fg_color="#0a0a12")
        
        # Main Layout Reference State Variables
        self.current_filter_category = "all"
        self.is_ready = False
        
        # Build System Splash Layer View Overlay
        self.build_splash_screen()

    # -------------------------------------------------------------------------
    # ANIMATED SPLASH VIEW LAYER
    # -------------------------------------------------------------------------
    def build_splash_screen(self):
        self.splash_frame = ctk.CTkFrame(self, fg_color="#06060c")
        self.splash_frame.pack(fill="both", expand=True)
        
        # Layering Starfield Component inside Splash Layout Frame
        self.splash_stars = StarfieldCanvas(self.splash_frame, bg="#06060c")
        self.splash_stars.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Tech Frame Holder Container
        self.ring_container = ctk.CTkFrame(self.splash_frame, width=300, height=300, fg_color="transparent")
        self.ring_container.place(relx=0.5, rely=0.4, anchor="center")
        
        self.holo_ring = HologramRingCanvas(self.ring_container, bg="#06060c")
        self.holo_ring.pack(fill="both", expand=True)
        
        # Central HUD Overlay Text Strings
        self.logo_label = ctk.CTkLabel(
            self.splash_frame, text="DSA BOT", 
            font=ctk.CTkFont(family="Courier New", size=54, weight="bold"),
            text_color="#00f0ff"
        )
        self.logo_label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.status_label = ctk.CTkLabel(
            self.splash_frame, text="BOOT SEQUENCER STARTING...", 
            font=ctk.CTkFont(family="Courier New", size=16),
            text_color="#ff007f"
        )
        self.status_label.place(relx=0.5, rely=0.68, anchor="center")
        
        # Progress Metric Segment Component Bar
        self.pbar = ctk.CTkProgressBar(self.splash_frame, width=450, height=6, fg_color="#111122", progress_color="#00f0ff")
        self.pbar.set(0)
        self.pbar.place(relx=0.5, rely=0.74, anchor="center")
        
        # Start Engine Runtime Background Animations Loops
        self.splash_stars.animate()
        self.holo_ring.update_anim()
        
        # Fire background Initialization Thread Sequencer Sequence Routine Task
        threading.Thread(target=self.run_initialization_sequence, daemon=True).start()

    def run_initialization_sequence(self):
        steps = [
            (0.15, "INITIALIZING AI CORE...", "System online."),
            (0.40, "ESTABLISHING NEURAL LINK CONNECTORS...", "Data stream synchronized."),
            (0.65, "LOADING DSA KNOWLEDGE DATASETS...", "Structures parsed successfully."),
            (0.85, "GENERATING PROCEDURAL HUD UI ENVIRONMENT...", "All engines ready."),
            (1.00, "READY", "Welcome commander.")
        ]
        
        # Sound voice indicator cue trigger simulated
        tts.say("DSA system initialization sequence activated.")
        
        for progress, status_text, audio_cue in steps:
            time.sleep(random.uniform(0.6, 1.0))
            self.update_splash_ui(progress, status_text)
            
        time.sleep(0.4)
        self.after(0, self.transition_to_dashboard)

    def update_splash_ui(self, progress, text):
        self.after(0, lambda: self.pbar.set(progress))
        self.after(0, lambda: self.status_label.configure(text=text))

    def transition_to_dashboard(self):
        # Shutting Down Splash Animations Canvas Frames Cleanly
        self.splash_stars.animation_running = False
        self.splash_frame.destroy()
        
        # Fire Application Interface Initialization Construction Layout Core
        self.build_main_dashboard()
        tts.say("System operational. Welcome.")

    # -------------------------------------------------------------------------
    # MAIN APPLICATION HUD DASHBOARD ARCHITECTURE VIEW
    # -------------------------------------------------------------------------
    def build_main_dashboard(self):
        self.is_ready = True
        
        # Outer Base Layer Matrix Background
        self.bg_canvas = StarfieldCanvas(self, bg="#080810")
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_canvas.animate()
        
        # Create Main Application Scaffold Structured Frame Containers Layout Grid Maps
        self.create_top_bar()
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)
        
        self.create_left_panel()
        self.create_center_chat_panel()
        self.create_right_panel()

    # -------------------------------------------------------------------------
    # TOP HEADER PANEL SECTION
    # -------------------------------------------------------------------------
    def create_top_bar(self):
        self.top_bar = ctk.CTkFrame(self, height=65, fg_color="#0c0c1a", border_width=1, border_color="#00f0ff")
        self.top_bar.place(relx=0, rely=0, relwidth=1)
        
        title_lbl = ctk.CTkLabel(
            self.top_bar, text="🤖 DSA AI QUANTUM ASSISTANT // HUD_v2.6", 
            font=ctk.CTkFont(family="Courier New", size=20, weight="bold"),
            text_color="#00f0ff"
        )
        title_lbl.place(relx=0.02, rely=0.5, anchor="w")
        
        # Pulse Ambient Connection Core Indicator
        self.pulse_frame = ctk.CTkFrame(self.top_bar, width=14, height=14, corner_radius=7, fg_color="#00ff66")
        self.pulse_frame.place(relx=0.88, rely=0.5, anchor="center")
        
        self.status_str_lbl = ctk.CTkLabel(
            self.top_bar, text="SYSTEM: ONLINE", 
            font=ctk.CTkFont(family="Courier New", size=13, weight="bold"),
            text_color="#00ff66"
        )
        self.status_str_lbl.place(relx=0.9, rely=0.5, anchor="w")
        
        self.animate_status_pulse(0)

    def animate_status_pulse(self, step):
        if not self.is_ready or not self.pulse_frame.winfo_exists(): return
        alpha = (math.sin(step) + 1) / 2
        green_intensity = int(150 + (105 * alpha))
        color = f"#00{green_intensity:02x}44"
        self.pulse_frame.configure(fg_color="#00ff66" if alpha > 0.4 else "#005522")
        self.after(120, lambda: self.animate_status_pulse(step + 0.25))

    # -------------------------------------------------------------------------
    # LEFT PANEL NAVIGATION ELEMENTS
    # -------------------------------------------------------------------------
    def create_left_panel(self):
        self.left_panel = ctk.CTkFrame(self.main_container, width=240, fg_color="#090915", border_width=1, border_color="#7000ff")
        self.left_panel.place(relx=0, rely=0, relwidth=0.17, relheight=1)
        
        lbl_nav = ctk.CTkLabel(
            self.left_panel, text="CORE MODULES", 
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold"), text_color="#ff007f"
        )
        lbl_nav.pack(pady=20, anchor="w", padx=20)
        
        modules = [
            ("📊 Dashboard", "all"),
            ("🔄 Sorting", "sorting"),
            ("🔢 Arrays", "array"),
            ("🔗 Linked Lists", "linked_list"),
        ]
        
        self.nav_buttons = {}
        for text, category in modules:
            btn = ctk.CTkButton(
                self.left_panel, text=text, font=ctk.CTkFont(family="Courier New", size=14),
                height=45, fg_color="transparent", text_color="#ffffff", anchor="w",
                hover_color="#1a1a3a", border_width=1, border_color="#222244",
                command=lambda c=category: self.filter_knowledge_cards(c)
            )
            btn.pack(fill="x", padx=15, pady=8)
            self.nav_buttons[category] = btn
            
        self.filter_knowledge_cards("all")
        
        # Audio Engine Control Mechanism Toggle System Widget Block
        self.tts_toggle = ctk.CTkCheckBox(
            self.left_panel, text="AI VOICE HARNESS", font=ctk.CTkFont(family="Courier New", size=11),
            text_color="#00f0ff", fg_color="#00f0ff", hover_color="#00a0cc",
            command=self.toggle_voice_engine
        )
        self.tts_toggle.select()
        self.tts_toggle.pack(side="bottom", fill="x", padx=20, pady=30)

    def toggle_voice_engine(self):
        tts.enabled = bool(self.tts_toggle.get())

    def filter_knowledge_cards(self, category):
        self.current_filter_category = category
        for cat, btn in self.nav_buttons.items():
            if cat == category:
                btn.configure(fg_color="#7000ff", border_color="#00f0ff", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", border_color="#222244", text_color="#b0b0d0")
                
        if hasattr(self, 'right_panel') and self.right_panel.winfo_exists():
            self.render_knowledge_quick_cards()

    # -------------------------------------------------------------------------
    # CENTRAL TERMINAL SYSTEM (CHAT INTERFACE VIEW)
    # -------------------------------------------------------------------------
    def create_center_chat_panel(self):
        self.center_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.center_panel.place(relx=0.17, rely=0, relwidth=0.60, relheight=1)
        
        # Scrollable Layout Space View Area Configuration
        self.chat_display = ctk.CTkScrollableFrame(
            self.center_panel, fg_color="#070712", 
            border_width=1, border_color="#00f0ff"
        )
        self.chat_display.place(relx=0.02, rely=0.03, relwidth=0.96, relheight=0.82)
        
        # Footer Action Field Prompt Matrix Area Block Frame
        self.input_frame = ctk.CTkFrame(self.center_panel, fg_color="transparent")
        self.input_frame.place(relx=0.02, rely=0.87, relwidth=0.96, relheight=0.10)
        
        self.entry_field = ctk.CTkEntry(
            self.input_frame, placeholder_text="Execute secure natural language query...",
            font=ctk.CTkFont(family="Courier New", size=14),
            fg_color="#0c0c1f", border_color="#7000ff", text_color="#ffffff",
            placeholder_text_color="#555577"
        )
        self.entry_field.place(relx=0, rely=0, relwidth=0.76, relheight=0.8)
        self.entry_field.bind("<Return>", lambda event: self.process_user_message())
        
        send_btn = ctk.CTkButton(
            self.input_frame, text="TRANSMIT >>", font=ctk.CTkFont(family="Courier New", size=13, weight="bold"),
            fg_color="#00f0ff", text_color="#000000", hover_color="#ff007f",
            command=self.process_user_message
        )
        send_btn.place(relx=0.78, rely=0, relwidth=0.11, relheight=0.8)
        
        clear_btn = ctk.CTkButton(
            self.input_frame, text="CLR LOG", font=ctk.CTkFont(family="Courier New", size=13, weight="bold"),
            fg_color="#221133", text_color="#ff007f", hover_color="#441122", border_width=1, border_color="#ff007f",
            command=self.clear_chat_logs
        )
        clear_btn.place(relx=0.90, rely=0, relwidth=0.10, relheight=0.8)
        
        self.render_system_bubble("AI Assistant Node Initialized. Target telemetry items to review specifications.")

    def render_user_bubble(self, phrase_string):
        bubble = ctk.CTkFrame(self.chat_display, fg_color="#161633", border_width=1, border_color="#7000ff")
        bubble.pack(anchor="e", padx=10, pady=6, fill="x", expand=True)
        
        lbl = ctk.CTkLabel(
            bubble, text=f"USER // {phrase_string}", font=ctk.CTkFont(family="Courier New", size=13),
            text_color="#00f0ff", justify="left", anchor="w", wraplength=550
        )
        lbl.pack(padx=15, pady=10, fill="x")
        self.smooth_scroll_to_bottom()

    def render_system_bubble(self, message_body):
        bubble = ctk.CTkFrame(self.chat_display, fg_color="#0b1c24", border_width=1, border_color="#00ff66")
        bubble.pack(anchor="w", padx=10, pady=6, fill="x", expand=True)
        
        lbl = ctk.CTkLabel(
            bubble, text=f"BOT_RESPONSE //\n\n{message_body}", font=ctk.CTkFont(family="Courier New", size=13),
            text_color="#ffffff", justify="left", anchor="w", wraplength=550
        )
        lbl.pack(padx=15, pady=10, fill="x")
        self.smooth_scroll_to_bottom()

    def smooth_scroll_to_bottom(self):
        self.chat_display._parent_canvas.yview_moveto(1.0)

    def clear_chat_logs(self):
        for widget in self.chat_display.winfo_children():
            widget.destroy()
        self.render_system_bubble("Core buffers cleared. System standing by.")

    def process_user_message(self, explicit_prompt=None):
        query = explicit_prompt if explicit_prompt else self.entry_field.get().strip()
        if not query: return
        
        if not explicit_prompt:
            self.entry_field.delete(0, tk.END)
            
        self.render_user_bubble(query)
        
        # Emulate processing pipeline layout block delay via a smooth generator
        intent = detect_intent(query)
        resolved_response = generate_text(intent)
        
        self.after(300, lambda: self.render_system_bubble(resolved_response))
        self.after(350, lambda: tts.say(resolved_response))

    # -------------------------------------------------------------------------
    # RIGHT SIDEBAR PANEL - KNOWLEDGE DATABANK
    # -------------------------------------------------------------------------
    def create_right_panel(self):
        self.right_panel = ctk.CTkFrame(self.main_container, fg_color="#090915", border_width=1, border_color="#7000ff")
        self.right_panel.place(relx=0.77, rely=0, relwidth=0.23, relheight=1)
        
        lbl_deck = ctk.CTkLabel(
            self.right_panel, text="TELEMETRY TELEPAD", 
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold"), text_color="#ff007f"
        )
        lbl_deck.pack(pady=20, anchor="w", padx=20)
        
        # Scrollable container container for dataset cards
        self.deck_container = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent")
        self.deck_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.render_knowledge_quick_cards()

    def render_knowledge_quick_cards(self):
        # Clear out current items inside card container
        for widget in self.deck_container.winfo_children():
            widget.destroy()
            
        # Target Cards Library Definition Meta-Map Array System 
        cards_pool = [
            {"title": "Bubble Sort Explanations", "prompt": "Explain bubble sort details", "cat": "sorting"},
            {"title": "Bubble Sort Complexity", "prompt": "What is the time complexity of bubble sort?", "cat": "sorting"},
            {"title": "Bubble Sort Code", "prompt": "Give me bubble sort sample code", "cat": "sorting"},
            {"title": "Selection Sort Details", "prompt": "Explain selection sort algorithm details", "cat": "sorting"},
            {"title": "Selection Sort Code", "prompt": "Show me sample code for selection sort", "cat": "sorting"},
            {"title": "Insertion Sort Info", "prompt": "Explain insertion sort structure", "cat": "sorting"},
            {"title": "Merge Sort Engine", "prompt": "Explain merge sort workflow", "cat": "sorting"},
            {"title": "Quick Sort Blueprint", "prompt": "Explain quick sort setup", "cat": "sorting"},
            {"title": "Array Structures Info", "prompt": "What is an array data structure?", "cat": "array"},
            {"title": "Array Data Facts", "prompt": "Give me a fact about array systems", "cat": "array"},
            {"title": "Linked List Elements", "prompt": "Explain what is a linked list structure", "cat": "linked_list"},
            {"title": "Singly Linked List Code", "prompt": "Show code for singly linked list setup", "cat": "linked_list"},
            {"title": "Doubly Linked List Map", "prompt": "Explain doubly linked list characteristics", "cat": "linked_list"},
            {"title": "Circular Double Code Loop", "prompt": "Give code for circular doubly linked list", "cat": "linked_list"},
        ]
        
        # Parse items based on navigational selector filter state definitions
        for design_meta in cards_pool:
            if self.current_filter_category != "all" and design_meta["cat"] != self.current_filter_category:
                continue
                
            card_frame = ctk.CTkFrame(self.deck_container, fg_color="#121226", border_width=1, border_color="#333366")
            card_frame.pack(fill="x", pady=8, padx=5)
            
            card_lbl = ctk.CTkLabel(
                card_frame, text=design_meta["title"].upper(), 
                font=ctk.CTkFont(family="Courier New", size=11, weight="bold"),
                text_color="#00f0ff", justify="left"
            )
            card_lbl.pack(anchor="w", padx=12, pady=(10, 5))
            
            trigger_action_btn = ctk.CTkButton(
                card_frame, text="DEPLOY QUERY", font=ctk.CTkFont(family="Courier New", size=10, weight="bold"),
                height=24, fg_color="#221144", hover_color="#ff007f", text_color="#ffffff",
                command=lambda text_prompt=design_meta["prompt"]: self.process_user_message(text_prompt)
            )
            trigger_action_btn.pack(fill="x", padx=12, pady=(0, 10))

# -------------------------------------------------------------------------
# RUNTIME ENGINE INITIALIZATION BOOTSTRAPPER
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = DSABotApp()
    app.mainloop()