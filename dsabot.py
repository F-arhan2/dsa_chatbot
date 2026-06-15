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
# MANDATORY FILE VALIDATION (Explicitly utilizes user provided dataset)
# -------------------------------------------------------------------------
DATASET_PATH = "datasets/dsa_data.json"

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

# Global TTS state tracker
tts_enabled = True

def say(text):
    """Executes clean non-blocking Text-To-Speech calls."""
    if not tts_enabled:
        return
    def _speak_thread():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            # Filter structural brackets out of speak stream to prevent robot artifacts
            cleaned_text = str(text).split("{")[0].replace("\n", " ").replace(";", " ")
            engine.say(cleaned_text[:150]) 
            engine.runAndWait()
        except Exception:
            pass
    threading.Thread(target=_speak_thread, daemon=True).start()

def get_response(user_input):
    """Processes natural language keyword strings and maps directly onto the user's JSON keys."""
    text = user_input.lower().strip()
    
    try:
        
        # Greetings Match
        if text in ["hi", "hello", "hey"]:
            return random.choice(dsa["greeting_data"]["hello"])
        if text in ["good morning", "gm"]:
            return random.choice(dsa["greeting_data"]["good_morning"])
        if text in ["good afternoon", "ga"]:
            return random.choice(dsa["greeting_data"]["good_afternoon"])
        if text in ["good evening", "ge"]:
            return random.choice(dsa["greeting_data"]["good_evening"])

        # Sorting Sub-matrix Matches
        if any(word in text for word in ["what is sorting", "define sorting", "explain sorting", "tell me about sorting"]):
            return random.choice(dsa["sorting"]["general"]["definition"])
        if "types of sorting" in text or "sorting types" in text:
            return "Available matrix algorithms:\n" + "\n".join([f" • {item}" for item in dsa["sorting"]["general"]["types"]])

        # Dynamic Extraction Map Helper for Sorting Techniques
        for algo in ["bubble_sort", "selection_sort", "insertion_sort", "merge_sort", "quick_sort"]:
            readable_algo = algo.replace("_", " ")
            if readable_algo in text:
                if "complexity" in text or "time" in text:
                    return f"[{readable_algo.upper()} TIME SCALES]:\n" + "\n".join(dsa["sorting"][algo]["time_complexity"])
                if "code" in text or "syntax" in text or "program" in text:
                    return f"// {readable_algo.upper()} STRUCTURAL IMPLEMENTATION:\n" + "\n".join(dsa["sorting"][algo]["sample_codes"])
                return random.choice(dsa["sorting"][algo]["explanations"])

        # Linked List Variant Parsers (Deep Nesting Parsing)
        if "linked list" in text or "node list" in text:
            # Check detailed specific variant models first
            if "circular doubly" in text:
                target = dsa["linked_list"]["types"]["circular_doubly_linked_list"]
                if "code" in text: return "\n".join(target["sample_codes"])
                return random.choice(target["explanations"])
            if "circular" in text:
                target = dsa["linked_list"]["types"]["circular_linked_list"]
                if "code" in text: return "\n".join(target["sample_codes"])
                return random.choice(target["explanations"])
            if "doubly" in text:
                target = dsa["linked_list"]["types"]["doubly_linked_list"]
                if "code" in text: return "\n".join(target["sample_codes"])
                return random.choice(target["explanations"])
            if "singly" in text:
                target = dsa["linked_list"]["types"]["singly_linked_list"]
                if "code" in text: return "\n".join(target["sample_codes"])
                return random.choice(target["explanations"])
                
            # Base linked list matches
            if "fact" in text:
                return random.choice(dsa["linked_list"]["facts"])
            if "application" in text or "use case" in text:
                return "Linked List real-world matrices:\n" + "\n".join([f" -> {item}" for item in dsa["linked_list"]["applications"]])
            if "advantage" in text:
                return "PROSECUTION ADVANTAGES:\n" + "\n".join([f" [+] {item}" for item in dsa["linked_list"]["advantages"]])
            if "disadvantage" in text or "flaw" in text:
                return "SYSTEM LIMITATIONS:\n" + "\n".join([f" [-] {item}" for item in dsa["linked_list"]["disadvantages"]])
            return random.choice(dsa["linked_list"]["definition"])

        # Linear Array Matches
        if "array" in text:
            if "fact" in text:
                return random.choice(dsa["array"]["facts"])
            if "application" in text or "use" in text:
                return "Array allocations:\n" + "\n".join([f" • {item}" for item in dsa["array"]["applications"]])
            if "example" in text:
                return "Matrix instance sample: " + random.choice(dsa["array"]["examples"])
            return random.choice(dsa["array"]["definition"])

        # Dynamic Operations Framework Matches
        if "operation" in text or "actions" in text:
            return "Supported Matrix Mutations:\n- Insertion Tasks\n- Deletion Tasks\n- Traversal\n- Searching Routines"
        if "insertion" in text:
            return "Insertion Protocols:\n" + "\n".join([f" * {item}" for item in dsa["operations"]["insertion"]])
        if "deletion" in text:
            return "Deletion Protocols:\n" + "\n".join([f" * {item}" for item in dsa["operations"]["deletion"]])
        if "traversal" in text:
            return "\n".join(dsa["operations"]["traversal"])
        if "search" in text:
            return "\n".join(dsa["operations"]["searching"])

    except KeyError as e:
        return f"[MATRIX SYNTAX FAULT]: Target index token path path key {e} cannot be mapped onto active .json structure."
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

    return "System unable to resolve keyword. Query target data categories: [Sorting, Arrays, Linked Lists, Operations]."


class ModernDSABotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DSA BOT ")
        self.geometry("1400x800")
        self.configure(fg_color=BG_COLOR)
        
        # Responsive master grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.splash_frame = None
        self.main_container = None
        
        # Deploy futuristic splash screen instantly
        self.init_splash_screen()

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
        cx, cy = w / 2, h / 0.415
        
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
        
        self.after(400, lambda: self.append_chat_bubble("SYSTEM", "AI Frame synchronized with datasets/dsa_data.json configuration node. Diagnostic loops running clean."))

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
        
        lbl_sec = ctk.CTkLabel(left_panel, text="TERMINAL SUB-SECTIONS", font=ctk.CTkFont(family="Consolas", size=11), text_color=TEXT_MUTED)
        lbl_sec.pack(anchor="w", padx=20, pady=(20, 15))
        
        # Core Navigation targets
        nav_items = [
            ("Dashboard Cluster", "hello"),
            ("Sorting Matrix", "types of sorting"),
            ("Linear Arrays", "array allocation definition"),
            ("Linked Nodes", "linked list definition")
        ]
        self.nav_buttons = []
        
        for idx, (label, query) in enumerate(nav_items):
            is_selected = (idx == 0)
            btn = ctk.CTkButton(
                left_panel, text=label, anchor="w", height=45,
                font=ctk.CTkFont(family="Consolas", size=13),
                fg_color="#1E293B" if is_selected else "transparent",
                text_color=ACCENT_NEON if is_selected else TEXT_MAIN,
                border_width=1 if is_selected else 0,
                border_color=ACCENT_NEON,
                hover_color="#1E293B",
                command=lambda l=label, q=query: self.handle_nav_click(l, q)
            )
            btn.pack(fill="x", padx=15, pady=6)
            self.nav_buttons.append(btn)
            
        sys_lbl = ctk.CTkLabel(left_panel, text="PERIPHERAL CHANNELS", font=ctk.CTkFont(family="Consolas", size=11), text_color=TEXT_MUTED)
        sys_lbl.pack(anchor="w", padx=20, pady=(40, 10))
        
        self.tts_switch = ctk.CTkSwitch(
            left_panel, text="Vocalize Matrix Streams", font=ctk.CTkFont(family="Consolas", size=12),
            text_color=TEXT_MAIN, progress_color=ACCENT_NEON, command=self.toggle_tts
        )
        self.tts_switch.pack(anchor="w", padx=20, pady=10)
        self.tts_switch.select()
        
        clear_btn = ctk.CTkButton(
            left_panel, text="Flush Console Buffers", font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#7F1D1D", hover_color="#991B1B", text_color=TEXT_MAIN, command=self.clear_chat_log
        )
        clear_btn.pack(fill="x", padx=15, pady=30, side="bottom")

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
            input_container, placeholder_text="Inject matrix instruction string... (e.g., 'circular linked list explanations')",
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
        
        src_tag = "[NODE ACCESS USER]" if is_user else "[AI TERMINAL TRACE]"
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

    def clear_chat_log(self):
        for child in self.chat_scroll.winfo_children():
            child.destroy()
        self.append_chat_bubble("SYSTEM", "Display pipeline vectors systematically flushed.")

    # ==========================================
    # RIGHT PANEL MODULE (MACRO INTERCEPT CARDS)
    # ==========================================
    def build_right_panel(self):
        right_panel = ctk.CTkFrame(self.main_container, fg_color=PANEL_COLOR, corner_radius=0, border_width=1, border_color="#1E293B")
        right_panel.grid(row=1, column=2, sticky="nsew", padx=(1,0), pady=(1,0))
        
        lbl_sec = ctk.CTkLabel(right_panel, text="KNOWLEDGE MACRO TRACERS", font=ctk.CTkFont(family="Consolas", size=11), text_color=TEXT_MUTED)
        lbl_sec.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Interactive Macros mapped directly to distinct user data segments
        cards_data = [
            ("Bubble Sort Explanation", "What is bubble sort explanation"),
            ("Bubble Sort Code Syntax", "Bubble sort sample codes"),
            ("Selection Sort Matrix", "Selection sort explanation"),
            ("Insertion Sort Blueprint", "Insertion sort sample codes"),
            ("Merge Sort Log Scales", "Merge sort time complexity"),
            ("Quick Sort Core Speed", "Quick sort time complexity"),
            ("Singly Linked List Node", "singly linked list explanations"),
            ("Doubly Pointer Chains", "doubly linked list sample codes"),
            ("Circular Pointer Wraps", "circular linked list explanations"),
            ("Array Cache Benefits", "array facts"),
            ("Matrix Array Operations", "insertion operations")
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


if __name__ == "__main__":
    app = ModernDSABotApp()
    app.mainloop()