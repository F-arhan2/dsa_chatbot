import tkinter as tk
import customtkinter as ctk
import json
import random
import pyttsx3
import threading
import math
import sys
import os
import webbrowser

# Set up global styling attributes for a Cyberpunk / Iron Man HUD feel
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BG_COLOR = "#0A0B10"          # Ultra dark space/cyberpunk tone
PANEL_COLOR = "#121420"       # Translucent glass-feel background
ACCENT_NEON = "#00F0FF"       # Cyberpunk Cyan / Neon Blue
ACCENT_PINK = "#FF007F"       # Cyberpunk Pink / Magenta
TEXT_MAIN = "#E2E8F0"         # Clean readable near-white text
TEXT_MUTED = "#64748B"        # Sleek grey text

# -------------------------------------------------------------------------
# MANDATORY FILE VALIDATION & DYNAMIC LOADING
# -------------------------------------------------------------------------
DATASET_PATH = "datasets/dsa_data.json"
dsa = {}

def load_dataset():
    global dsa
    if not os.path.exists(DATASET_PATH):
        print(f"[-] CRITICAL CONFIGURATION ERROR: Absolute dependency missing.")
        print(f"    The system requires '{DATASET_PATH}' to initialize.")
        print(f"    Terminating AI Core environment setup pipeline.")
        sys.exit(1)

    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as file:
            dsa = json.load(file)
    except Exception as e:
        print(f"[-] CRITICAL FILE READ ERROR: '{DATASET_PATH}' failed compilation.")
        print(f"    Details: {e}")
        sys.exit(1)

# Initialize dataset structure maps
load_dataset()

# Global TTS state tracker
tts_enabled = True
voice_gender = "male"

def say(text):
    if not tts_enabled:
        return

    def _speak_thread():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            voices = engine.getProperty("voices")

            # Select voice
            if voice_gender == "female":
                for voice in voices:
                    if "female" in voice.name.lower() or "zira" in voice.name.lower():
                        engine.setProperty("voice", voice.id)
                        break
            else:
                for voice in voices:
                    if "male" in voice.name.lower() or "david" in voice.name.lower():
                        engine.setProperty("voice", voice.id)
                        break

            cleaned_text = str(text).split("{")[0].replace("\n", " ").replace(";", " ")
            engine.say(cleaned_text)
            engine.runAndWait()
        except Exception:
            pass

    threading.Thread(target=_speak_thread, daemon=True).start()

# -------------------------------------------------------------------------
# DATASET EXTRACTION, INTENT ENGINE & MODULAR PARSING PIPELINES
# -------------------------------------------------------------------------
def detect_topic(text):
    """
    Scans variations of user inputs to isolate exact target keys within the multi-tier JSON.
    Maps natural variants into the specific structure parameters requested.
    """
    # 2D Array check must precede basic array matching
    if "2d array" in text or "two dimensional array" in text or "matrix" in text:
        return ("Arrays", "2D Array")
    if "array" in text:
        return ("Arrays", "Array")
    
    # Specific Linked List variants mapping rules
    if "circular doubly linked list" in text or "circular doubly" in text:
        return ("Linked Lists", "Circular Doubly Linked List")
    if "circular linked list" in text or "circular list" in text:
        return ("Linked Lists", "Circular Linked List")
    if "doubly linked list" in text or "doubly linked" in text:
        return ("Linked Lists", "Doubly Linked List")
    if "singly linked list" in text or "singly linked" in text:
        return ("Linked Lists", "Singly Linked List")
    if "linked list" in text or "node list" in text:
        return ("Linked Lists", "Singly Linked List")

    # Stacks matching pathways
    if "stack using array" in text or "array stack" in text:
        return ("Stacks", "Stack Using Array")
    if "stack using linked list" in text or "linked list stack" in text:
        return ("Stacks", "Stack Using Linked List")
    if "stack" in text:
        return ("Stacks", "Stack Using Array")

    # Queues verification structures
    if "circular queue" in text:
        return ("Queues", "Circular Queue")
    if "priority queue" in text:
        return ("Queues", "Priority Queue")
    if "simple queue" in text or "linear queue" in text:
        return ("Queues", "Simple Queue")
    if "deque" in text or "double ended queue" in text:
        return ("Queues", "Deque")
    if "queue" in text:
        return ("Queues", "Simple Queue")

    # Searching Algorithms algorithms mappings
    if "linear search" in text or "sequential search" in text:
        return ("Searching Algorithms", "Linear Search")
    if "binary search" in text:
        return ("Searching Algorithms", "Binary Search")

    # Sorting Techniques processing loops
    if "bubble sort" in text:
        return ("Sorting Algorithms", "Bubble Sort")
    if "selection sort" in text:
        return ("Sorting Algorithms", "Selection Sort")
    if "insertion sort" in text:
        return ("Sorting Algorithms", "Insertion Sort")
    if "merge sort" in text:
        return ("Sorting Algorithms", "Merge Sort")
    if "quick sort" in text:
        return ("Sorting Algorithms", "Quick Sort")

    # Common Operations validations
    if "traversal" in text:
        return ("Common Operations", "Traversal")
    if "insertion operation" in text or "insert operation" in text:
        return ("Common Operations", "Insertion")
    if "deletion operation" in text or "delete operation" in text:
        return ("Common Operations", "Deletion")
    if "searching operation" in text or "search operation" in text:
        return ("Common Operations", "Searching")

    # Higher Tier Trees structure checking
    if "binary search tree" in text or "bst" in text:
        return ("Trees", "Binary Search Tree")
    if "binary tree" in text:
        return ("Trees", "Binary Tree")
    if "heap" in text or "max heap" in text or "min heap" in text:
        return ("Trees", "Heap")

    return (None, None)

def detect_intent(text):
    """
    Determines exactly which sub-attribute token parameter is requested from the data matrix block.
    """
    if "definition" in text or "what is" in text or "define" in text:
        return "definition"
    if "explain" in text or "explanation" in text or "tell me about" in text:
        return "explanations"
    if "fact" in text:
        return "facts"
    if "advantage" in text or "pro" in text:
        return "advantages"
    if "disadvantage" in text or "con" in text or "flaw" in text or "limitation" in text:
        return "disadvantages"
    if "application" in text or "use case" in text or "real world" in text:
        return "applications"
    if "complexity" in text or "time complexity" in text or "space complexity" in text:
        return "time_complexity"
    if "code" in text or "java" in text or "program" in text or "runnable" in text:
        return "sample_code"
    if "interview" in text or "questions" in text:
        return "interview_questions"
    if "example" in text or "sample data" in text:
        return "examples"
    
    # Fallback default parameter rule if nothing explicit maps
    return "definition"

def format_response(topic_name, intent, data_block):
    """
    Formats the processed data elements into human-readable outputs instead of raw elements.
    Converts multi-line code structures or formats bullet blocks.
    """
    header = f"Topic: {topic_name}\nSection: {intent.replace('_', ' ').title()}\n\n"    
    if intent == "definition":
        bullets = "\n".join([f"• {point}" for point in data_block])
        return f"{header}{bullets}"
        
    elif intent == "explanations":
        paragraph = " ".join(data_block)
        return f"{header}{paragraph}"
        
    elif intent in ["facts", "advantages", "disadvantages", "interview_questions"]:
        bullets = "\n".join([f"• {point}" for point in data_block])
        return f"{header}{bullets}"
        
    elif intent == "applications":
        bullets = "\n".join([f"→ {point}" for point in data_block])
        return f"{header}{bullets}"
        
    elif intent == "examples":
        bullets = "\n".join([f"e.g., {point}" for point in data_block])
        return f"{header}{bullets}"
        
    elif intent == "time_complexity":
        if isinstance(data_block, dict):
            lines = []
            for key, val in data_block.items():
                lines.append(f"• {key.replace('_', ' ').title()}: {val}")
            return header + "\n".join(lines)
        return f"{header}• Metric Profile: {data_block}"
        
    elif intent == "sample_code":
        # Returns the raw unformatted multi-line block with spacing indicators untouched
        return f"Topic: {topic_name} (COMPLETE JAVA SPECIFICATION)\n{'-'*60}\n{data_block}"

    return str(data_block)

def get_response(user_input):
    text = user_input.lower().strip()
    
    # Check for close/exit command triggers
    if text in ["exit", "quit", "close", "shutdown", "exit cmd", "bye", "byee"]:
        return "[SYSTEM SHUTDOWN]: De-initializing core UI buffers. Goodbye."

    # Direct Override for  ("Who created you", "Author", "God")
    if any(keyword in text for keyword in ["who created you", "creator", "author", "who is your author", "who is god", "who made you"]):
        return "[Ai Terminal]: I was developed by Farhan Shaikh to help students learn Data Structures and Algorithms"

    if any(keyword in text for keyword in ["god"]):
        return "[Ai Terminal]: For me their is only one god 'Farhan Shaikh' "
    # Direct Override for "What is DSA" (Simple 2-line explanation)
    if text in ["what is dsa", "define dsa", "explain dsa", "dsa"]:
        return "Data Structures and Algorithms (DSA) is a foundational branch of computer science focused on organizing data efficiently and designing step-by-step procedures to solve complex computational problems. Mastering DSA allows developers to write optimized, high-performance software that uses minimal time and memory resources."

    # Open Website Command
    if text.startswith("open "):
        site = text.replace("open ", "").strip()
        if "." not in site:
            site += ".com"
        try:
            webbrowser.open(f"https://{site}")
            return f"Opening {site}..."
        except Exception:
            return f"Unable to open {site}."

    # Process Greeting Sub-checks
    if text in ["hi", "hello", "hey", "greetings"]:
        return "Greetings! Core system data banks operational. Query target data categories: [Arrays, Linked Lists, Stacks, Queues, Searching, Sorting, Trees]."
    if text in ["good morning", "gm", "good afternoon", "good evening"]:
        return f"Hello, welcome back to the terminal framework. Ready to look up target algorithms data."

    # Determine structural target positions
    category, topic = detect_topic(text)
    intent = detect_intent(text)

    # Route request if valid matches are identified within the structure blocks
    if category and topic:
        try:
            # Safely explore the knowledge base block configuration
            kb = dsa.get("dsa_knowledge_base", {})
            target_data = kb.get(category, {}).get(topic, {})
            
            if not target_data:
                return f"[INFO UNMAPPED]: Topic structural reference '{topic}' was found but configuration branches are blank."

            if intent in target_data:
                return format_response(topic, intent, target_data[intent])
            else:
                return f"[FALLBACK PROCESSING]: The node framework path '{topic}' exists, but the parameter '{intent}' is currently unavailable."
        except Exception as e:
            return f"[CORE MAPPING ERROR]: Processing index tracking parameters failed. Reason: {e}"

    # Target data fallback prompt tracking option suggestions
    fallback_msg = (
        "System unable to safely resolve dynamic keywords onto dataset map.\n\n"
        "Supported Query Data Elements:\n"
        "• Arrays: Array, 2D Array\n"
        "• Linked Lists: Singly, Doubly, Circular, Circular Doubly\n"
        "• Stacks & Queues: Simple Queue, Circular Queue, Priority Queue, Deque\n"
        "• Search & Sort: Linear, Binary / Bubble, Selection, Insertion, Merge, Quick\n"
        "• Trees: Binary Tree, BST, Heap\n"
        "• Operations: Traversal, Insertion, Deletion, Searching"
    )
    return fallback_msg


class ModernDSABotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DSA BOT")
        self.geometry("1400x800")
        self.configure(fg_color=BG_COLOR)
        
        # Handle Window standard 'X' close button intercept
        self.protocol("WM_DELETE_WINDOW", self.terminate_system_pipeline)
        
        # Responsive master grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.splash_frame = None
        self.main_container = None
        
        # Deploy futuristic splash screen instantly
        self.init_splash_screen()

    def change_voice(self, choice):
        global voice_gender
        if choice.lower() == "female":
            voice_gender = "female"
        else:
            voice_gender = "male"

        self.append_chat_bubble("SYSTEM", f"Voice changed to {choice}.")

    # ==========================================
    # STARTUP EXPERIENCE (SPLASH MODULE)
    # ==========================================
    def init_splash_screen(self):
        self.splash_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.splash_frame.grid(row=0, column=0, sticky="nsew")
        
        self.splash_canvas = tk.Canvas(self.splash_frame, bg=BG_COLOR, highlightthickness=0)
        self.splash_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Generate floating background vector particles
        self.particles = []
        for _ in range(40):
            self.particles.append({
                "x": random.randint(100, 1300),
                "y": random.randint(100, 700),
                "radius": random.randint(2, 5),
                "dx": random.uniform(-1.2, 1.2),
                "dy": random.uniform(-1.2, 1.2),
                "color": random.choice([ACCENT_NEON, ACCENT_PINK, "#2563EB"])
            })
            
        self.logo_label = ctk.CTkLabel(
            self.splash_frame, text="DSA BOT", font=ctk.CTkFont(family="Consolas", size=76, weight="bold"),
            text_color=ACCENT_NEON
        )
        self.logo_label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.status_label = ctk.CTkLabel(
            self.splash_frame, text="Initializing Cybernetic Hub Framework...", font=ctk.CTkFont(family="Consolas", size=15),
            text_color=TEXT_MUTED
        )
        self.status_label.place(relx=0.5, rely=0.55, anchor="center")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.splash_frame, width=420, height=6, fg_color="#1E293B", progress_color=ACCENT_PINK
        )
        self.progress_bar.place(relx=0.5, rely=0.6, anchor="center")
        self.progress_bar.set(0)
        
        self.ring_angle = 0
        self.animate_splash_canvas()
        
        # Sequential multi-staged timing injection tracking bar values
        self.after(700, lambda: self.update_splash_stage("Parsing Verified datasets/dsa_data.json Structures...", 0.25))
        self.after(1500, lambda: self.update_splash_stage("Compiling Array, Sorting, and Pointer Vectors...", 0.65))
        self.after(2400, lambda: self.update_splash_stage("Booting HUD Dashboard Core Controls...", 0.90))
        self.after(3100, lambda: self.update_splash_stage("Secure Connection Established: Ready", 1.0))
        self.after(3600, self.transition_to_dashboard)

    def animate_splash_canvas(self):
        if not self.splash_frame or not self.splash_frame.winfo_exists():
            return
            
        self.splash_canvas.delete("all")
        w = self.splash_canvas.winfo_width()
        h = self.splash_canvas.winfo_height()
        if w < 10: w, h = 1400, 800
        
        for p in self.particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            if p["x"] < 0 or p["x"] > w: p["dx"] *= -1
            if p["y"] < 0 or p["y"] > h: p["dy"] *= -1
            
            self.splash_canvas.create_oval(
                p["x"]-p["radius"], p["y"]-p["radius"], 
                p["x"]+p["radius"], p["y"]+p["radius"], 
                fill=p["color"], outline=""
            )
            
        self.ring_angle += 0.05
        r = 135
        cx, cy = w / 2, h / 2.415
        
        x1 = cx + r * math.cos(self.ring_angle)
        y1 = cy + r * math.sin(self.ring_angle)
        x2 = cx + r * math.cos(self.ring_angle + math.pi*0.6)
        y2 = cy + r * math.sin(self.ring_angle + math.pi*0.6)
        self.splash_canvas.create_line(x1, y1, x2, y2, fill=ACCENT_NEON, width=2)
        
        x3 = cx + r * math.cos(self.ring_angle + math.pi)
        y3 = cy + r * math.sin(self.ring_angle + math.pi)
        x4 = cx + r * math.cos(self.ring_angle + math.pi * 1.6)
        y4 = cy + r * math.sin(self.ring_angle + math.pi * 1.6)
        self.splash_canvas.create_line(x3, y3, x4, y4, fill=ACCENT_PINK, width=2)
        
        self.after(16, self.animate_splash_canvas)

    def update_splash_stage(self, text, val):
        if self.status_label.winfo_exists():
            self.status_label.configure(text=text)
            self.progress_bar.set(val)

    def transition_to_dashboard(self):
        if self.splash_frame:
            self.splash_frame.destroy()
            self.splash_frame = None
        self.build_main_ui()

    # ==========================================
    # MAIN UI DASHBOARD COMPOSER
    # ==========================================
    def build_main_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1) # Nav Left Panel
        self.main_container.grid_columnconfigure(1, weight=4) # Chat Engine Center Panel
        self.main_container.grid_columnconfigure(2, weight=2) # Macros Panel Right
        
        self.build_top_bar()
        self.build_left_panel()
        self.build_center_panel()
        self.build_right_panel()
        
        self.after(400, lambda: self.append_chat_bubble("SYSTEM", "Hello! I'm your DSA Assistant. Ask me about arrays, linked lists, sorting or custom operations."))

    # ==========================================
    # TOP METRICS HEADER BLOCK
    # ==========================================
    def build_top_bar(self):
        top_bar = ctk.CTkFrame(self.main_container, fg_color=PANEL_COLOR, height=60, corner_radius=0, border_width=1, border_color="#1E293B")
        top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")
        top_bar.grid_propagate(False)
        
        title_lbl = ctk.CTkLabel(top_bar, text="▲ DSA Chat TERMINAL", font=ctk.CTkFont(family="Consolas", size=16, weight="bold"), text_color=TEXT_MAIN)
        title_lbl.pack(side="left", padx=25, pady=15)
        
        self.status_container = ctk.CTkFrame(top_bar, fg_color="transparent")
        self.status_container.pack(side="right", padx=25, pady=15)
        
        self.pulse_dot = ctk.CTkLabel(self.status_container, text="●", font=ctk.CTkFont(size=18), text_color="#10B981")
        self.pulse_dot.pack(side="left", padx=5)
        
        self.status_txt = ctk.CTkLabel(self.status_container, text="CORE COMPILATION STATUS: ONLINE", font=ctk.CTkFont(family="Consolas", size=12), text_color="#10B981")
        self.status_txt.pack(side="left", padx=5)
        
        self.pulse_state = True
        self.toggle_status_pulse()

    def toggle_status_pulse(self):
        if hasattr(self, 'pulse_dot') and self.pulse_dot.winfo_exists():
            self.pulse_state = not self.pulse_state
            color = "#10B981" if self.pulse_state else "#047857"
            self.pulse_dot.configure(text_color=color)
            self.after(750, self.toggle_status_pulse)

    # ==========================================
    # LEFT PANEL MODULE (NAV CONTROLLERS)
    # ==========================================
    def build_left_panel(self):
        left_panel = ctk.CTkFrame(self.main_container, fg_color=PANEL_COLOR, corner_radius=0, border_width=1, border_color="#1E293B")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0,1), pady=(1,0))
        
        lbl_sec = ctk.CTkLabel(left_panel, text="Category Routes", font=ctk.CTkFont(family="Consolas", size=11), text_color=TEXT_MUTED)
        lbl_sec.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Dynamic creation of Navigation maps from localized array targets
        routes_data = [
            ("Linear Array Structural Model", "What is an Array?"),
            ("Two-Dimensional Grids", "Explain 2D Array"),
            ("Connected Lists", "What is Singly Linked List"),
            ("Stack Operations", "Explain Stack Using Array"),
            ("Queue Scheduling Models", "What is Circular Queue"),
            ("Tree Sorting Schemes", "Explain Binary Search Tree")
        ]
        
        self.nav_buttons = []
        for label, query in routes_data:
            btn = ctk.CTkButton(
                left_panel, text=label, font=ctk.CTkFont(family="Consolas", size=12),
                fg_color="transparent", text_color=TEXT_MAIN, anchor="w", height=32,
                hover_color="#1E293B", command=lambda l=label, q=query: self.handle_nav_click(l, q)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.nav_buttons.append(btn)
            
        sys_lbl = ctk.CTkLabel(left_panel, text="Voice Assistant", font=ctk.CTkFont(family="Consolas", size=11), text_color=TEXT_MUTED)
        sys_lbl.pack(anchor="w", padx=20, pady=(40, 10))
        
        self.voice_label = ctk.CTkLabel(
            left_panel, text="Voice Type", font=ctk.CTkFont(family="Consolas", size=12), text_color=TEXT_MAIN
        )
        self.voice_label.pack(anchor="w", padx=20, pady=(10,5))

        self.voice_menu = ctk.CTkOptionMenu(
            left_panel, values=["Male", "Female"], command=self.change_voice
        )
        self.voice_menu.pack(anchor="w", padx=20, pady=(0,10))
        self.voice_menu.set("Male")

        self.tts_switch = ctk.CTkSwitch(
            left_panel, text="Voice Enabled", font=ctk.CTkFont(family="Consolas", size=12),
            text_color=TEXT_MAIN, progress_color=ACCENT_NEON, command=self.toggle_tts
        )
        self.tts_switch.pack(anchor="w", padx=20, pady=10)
        self.tts_switch.select()
        
        clear_btn = ctk.CTkButton(
            left_panel, text="Clear Terminal", font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#7F1D1D", hover_color="#991B1B", text_color=TEXT_MAIN, command=self.clear_chat_log
        )
        clear_btn.pack(fill="x", padx=15, pady=15, side="bottom")

        # Integrated Exit Macro Button
        close_btn = ctk.CTkButton(
            left_panel, text="End Session", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color="#3F3F46", hover_color="#18181B", text_color=ACCENT_PINK, command=self.terminate_system_pipeline
        )
        close_btn.pack(fill="x", padx=15, pady=(0, 10), side="bottom")

    def handle_nav_click(self, selected_label, search_query):
        for btn in self.nav_buttons:
            if btn.cget("text") == selected_label:
                btn.configure(fg_color="#1E293B", text_color=ACCENT_NEON, border_width=1, border_color=ACCENT_NEON)
                self.append_chat_bubble("USER", f"Terminal Focus Route -> {selected_label}")
                self.process_ai_reply(search_query)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_MAIN, border_width=0)

    def toggle_tts(self):
        global tts_enabled
        tts_enabled = bool(self.tts_switch.get())

    # ==========================================
    # CENTER PANEL MODULE (CHAT MATRIX CORES)
    # ==========================================
    def build_center_panel(self):
        center_panel = ctk.CTkFrame(self.main_container, fg_color="transparent", corner_radius=0)
        center_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        center_panel.grid_rowconfigure(0, weight=1)
        center_panel.grid_rowconfigure(1, weight=0)
        center_panel.grid_columnconfigure(0, weight=1)
        
        self.chat_scroll = ctk.CTkScrollableFrame(
            center_panel, fg_color=PANEL_COLOR, border_width=1, border_color="#1E293B"
        )
        self.chat_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        input_container = ctk.CTkFrame(center_panel, fg_color="transparent")
        input_container.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        input_container.grid_columnconfigure(0, weight=1)
        input_container.grid_columnconfigure(1, weight=0)
        
        self.entry_field = ctk.CTkEntry(
            input_container, placeholder_text="Type your question...",
            font=ctk.CTkFont(family="Consolas", size=13), height=50,
            fg_color="#0F172A", border_color="#334155", text_color=TEXT_MAIN, placeholder_text_color="#475569"
        )
        self.entry_field.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_field.bind("<Return>", lambda event: self.submit_user_message())
        
        send_btn = ctk.CTkButton(
            input_container, text="RUN CORE ▶", width=120, height=50,
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color=ACCENT_NEON, text_color="#0F172A", hover_color="#22D3EE",
            command=self.submit_user_message
        )
        send_btn.grid(row=0, column=1, sticky="e")

    def append_chat_bubble(self, sender, text):
        is_user = (sender == "USER")
        align_side = "e" if is_user else "w"
        bubble_bg = "#1E293B" if is_user else "#0F172A"
        border_col = ACCENT_PINK if is_user else ACCENT_NEON
        text_color = TEXT_MAIN if is_user else "#E2E8F0"
        
        outer_row = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        outer_row.pack(fill="x", padx=10, pady=8, anchor=align_side)
        
        bubble = ctk.CTkFrame(
            outer_row, fg_color=bubble_bg, border_width=1, border_color=border_col, corner_radius=8
        )
        bubble.pack(side="right" if is_user else "left", padx=5)
        
        src_tag = "[NODE ACCESS USER]" if is_user else "[AI TERMINAL]"
        tag_color = ACCENT_PINK if is_user else ACCENT_NEON
        
        lbl_tag = ctk.CTkLabel(bubble, text=src_tag, font=ctk.CTkFont(family="Consolas", size=10, weight="bold"), text_color=tag_color)
        lbl_tag.pack(anchor="w", padx=12, pady=(6,2))
        
        msg_lbl = ctk.CTkLabel(
            bubble, text=text, font=ctk.CTkFont(family="Consolas", size=13),
            text_color=text_color, justify="left", wraplength=550
        )
        msg_lbl.pack(anchor="w", padx=12, pady=(0,8))
        
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
        
    def submit_user_message(self):
        query = self.entry_field.get().strip()
        if not query:
            return
        self.entry_field.delete(0, tk.END)
        self.append_chat_bubble("USER", query)
        
        self.after(300, lambda: self.process_ai_reply(query))

    def process_ai_reply(self, query):
        response_text = get_response(query)
        self.append_chat_bubble("BOT", response_text)
        say(response_text)
        
        # Intercept string response to safely terminate window pipeline after displaying exit acknowledgement
        if "[SYSTEM SHUTDOWN]" in response_text:
            self.after(1200, self.terminate_system_pipeline)

    def clear_chat_log(self):
        for child in self.chat_scroll.winfo_children():
            child.destroy()
        self.append_chat_bubble("SYSTEM", "Hello! I'm your AI assistant. How can I help you today?")

    # ==========================================
    # RIGHT PANEL MODULE (MACRO INTERCEPT CARDS)
    # ==========================================
    def build_right_panel(self):
        right_panel = ctk.CTkFrame(self.main_container, fg_color=PANEL_COLOR, corner_radius=0, border_width=1, border_color="#1E293B")
        right_panel.grid(row=1, column=2, sticky="nsew", padx=(1,0), pady=(1,0))
        
        lbl_sec = ctk.CTkLabel(right_panel, text="KNOWLEDGE MACRO TRACERS", font=ctk.CTkFont(family="Consolas", size=11), text_color=TEXT_MUTED)
        lbl_sec.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Extended macro collection capturing multiple permutations across topics and intents
        cards_data = [
            ("What is DSA?", "What is DSA"),
            ("Who created you?", "Who created you?"),
            ("Array Definition", "Give definition of Array"),
            ("Array Applications", "Applications of arrays"),
            ("2D Array Examples", "Give examples of 2D array"),
            ("Singly Linked List Facts", "Give facts about singly linked list"),
            ("Doubly Linked List Code", "Show Java code for doubly linked list"),
            ("Circular List Advantages", "Advantages of circular linked list"),
            ("Circular Doubly Disadvantages", "Disadvantages of circular doubly linked list"),
            ("Stack Interview Questions", "Interview questions on stack using array"),
            ("Simple Queue Complexities", "Time complexity of simple queue"),
            ("Circular Queue Explanation", "Explain circular queue"),
            ("Priority Queue Applications", "Applications of priority queue"),
            ("Deque Disadvantages", "Disadvantages of deque"),
            ("Linear Search Definition", "What is linear search"),
            ("Binary Search Complexity", "Time complexity of binary search"),
            ("Bubble Sort Time Scales", "Time complexity of bubble sort"),
            ("Selection Sort Advantages", "Advantages of selection sort"),
            ("Insertion Sort Execution", "Explain insertion sort"),
            ("Merge Sort Runnable Code", "Show Java code for merge sort"),
            ("Quick Sort Disadvantages", "Disadvantages of quick sort"),
            ("Binary Tree Applications", "Applications of binary tree"),
            ("BST Interview Questions", "Interview questions on binary search tree"),
            ("Heap Internal Allocation", "Give facts about heap"),
            ("Traversal Core Operations", "Explain traversal operations")
        ]
        
        scroll_cards = ctk.CTkScrollableFrame(right_panel, fg_color="transparent")
        scroll_cards.pack(fill="both", expand=True, padx=5, pady=5)
        
        for title, command in cards_data:
            card_frame = ctk.CTkFrame(scroll_cards, fg_color="#1E293B", border_width=1, border_color="#334155", height=65)
            card_frame.pack(fill="x", padx=10, pady=6)
            card_frame.pack_propagate(False)
            
            btn = ctk.CTkButton(
                card_frame, text=f"⚡ {title}", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
                fg_color="transparent", text_color=TEXT_MAIN, anchor="w", hover_color="#27272A",
                command=lambda cmd=command: self.trigger_macro_query(cmd)
            )
            btn.pack(fill="both", expand=True, padx=5, pady=5)

    def trigger_macro_query(self, command_string):
        self.append_chat_bubble("USER", command_string)
        self.after(250, lambda: self.process_ai_reply(command_string))

    # ==========================================
    # EXPLICIT DE-INITIALIZATION SEQUENCE
    # ==========================================
    def terminate_system_pipeline(self):
        """Kills interface widgets safely and flushes process memory."""
        print("[*] Flushing active HUD mainloop threads...")
        print("[+] Secure Matrix Connection Severed. Exiting pipeline runtime.")
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = ModernDSABotApp()
    app.mainloop()