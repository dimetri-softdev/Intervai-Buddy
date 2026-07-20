import customtkinter as ctk
import threading
import random
from database import DatabaseManager
from ai_engine import AIEngine

# Set global application styling matching your Figma design
ctk.set_appearance_mode("Dark")


class AuthView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_login_success):
        super().__init__(parent, fg_color="#0B0F19", corner_radius=0)
        self.db = db_manager
        self.on_success = on_login_success
        self.is_login_mode = True

        self.setup_ui()  # <-- FIXED: Pointing to setup_ui instead of build_ui
        
    def setup_ui(self):
        # Center container card
        self.card = ctk.CTkFrame(self, fg_color="#1E293B", width=360, height=450, corner_radius=16)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False)

        # Title
        self.title_label = ctk.CTkLabel(
            self.card, text="IntervAI Login", 
            font=ctk.CTkFont(size=24, weight="bold"), text_color="white"
        )
        self.title_label.pack(pady=(40, 30))
        
        # Username Input
        self.username_entry = ctk.CTkEntry(
            self.card, placeholder_text="Username", 
            width=280, height=40, fg_color="#0F172A", border_color="#334155"
        )
        self.username_entry.pack(pady=10)
        
        # Password Input
        self.password_entry = ctk.CTkEntry(
            self.card, placeholder_text="Password", show="*", 
            width=280, height=40, fg_color="#0F172A", border_color="#334155"
        )
        self.password_entry.pack(pady=10)
        
        # Error/Status Message
        self.status_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        self.status_label.pack(pady=5)
        
        # Submit Button
        self.submit_btn = ctk.CTkButton(
            self.card, text="Sign In", width=280, height=40, 
            fg_color="#2563EB", hover_color="#1D4ED8", font=ctk.CTkFont(weight="bold"),
            command=self.handle_submit
        )
        self.submit_btn.pack(pady=(15, 10))
        
        # Mode Switch Toggle Button
        self.toggle_btn = ctk.CTkButton(
            self.card, text="Don't have an account? Sign Up", 
            fg_color="transparent", text_color="#3B82F6", hover_color="#1E293B",
            font=ctk.CTkFont(size=12), command=self.toggle_mode
        )
        self.toggle_btn.pack(pady=10)

    # FIXED: Methods are now properly indented inside AuthView
    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        self.status_label.configure(text="")
        if self.is_login_mode:
            self.title_label.configure(text="IntervAI Login")
            self.submit_btn.configure(text="Sign In")
            self.toggle_btn.configure(text="Don't have an account? Sign Up")
        else:
            self.title_label.configure(text="Create Account")
            self.submit_btn.configure(text="Sign Up")
            self.toggle_btn.configure(text="Already have an account? Sign In")

    def handle_submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.is_login_mode:
            success, user_id = self.db.authenticate_user(username, password)
            if success:
                self.status_label.configure(text="Success!", text_color="#10B981")
                self.on_success(user_id, username)
            else:
                self.status_label.configure(text="Invalid username or password.", text_color="#EF4444")
        else:
            success, message = self.db.register_user(username, password)
            if success:
                self.status_label.configure(text="Account created! Switching...", text_color="#10B981")
                self.after(1500, self.toggle_mode)
            else:
                 self.status_label.configure(text=message, text_color="#EF4444")


class IntervAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IntervAI - Smart Interview Prep")
        self.geometry("1100x680")
        
        # 1. Initialize your managers
        self.db = DatabaseManager()
        self.db.create_auth_tables() 
        self.ai = AIEngine()
        
        # 2. Track who is logged in
        self.current_user_id = None
        self.current_username = None
        
        # 3. Load the Login Screen on full screen immediately
        self.auth_view = AuthView(self, self.db, self.login_success_callback)
        self.auth_view.pack(fill="both", expand=True)

    def login_success_callback(self, user_id, username):
        """This runs automatically the split-second the user hits 'Sign In' successfully"""
        self.current_user_id = user_id
        self.current_username = username
        
        # Destroy the login screen so it disappears completely
        self.auth_view.destroy()
        
        # Now, and only now, build out the actual dashboard!
        self.initialize_main_app_layout()

    def initialize_main_app_layout(self):
        # Configure overall grid layout (1 row, 2 columns: Sidebar and Content Canvas)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Build subcomponents and content views
        self.setup_sidebar()
        self.setup_dashboard_content()
        self.setup_other_placeholders()
        
        # Force default view update
        self.show_dashboard()

    def setup_sidebar(self):
        # ----------------------------------------------------
        # 1. FIXED LEFT NAVIGATION SIDEBAR
        # ----------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#121824")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) 

        # App Logo Brand Header
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="I   IntervAI", 
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#FFFFFF"
        )
        self.logo_label.grid(row=0, column=0, padx=25, pady=(25, 5), sticky="w")
        
        self.sub_logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="INTERVIEW COACH", 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#9CA3AF"
        )
        self.sub_logo_label.grid(row=0, column=0, padx=43, pady=(52, 20), sticky="w")

        # User Profile Block - Dynamically welcome the authenticated user
        self.profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.profile_frame.grid(row=1, column=0, padx=25, pady=(10, 30), sticky="ew")
        
        self.profile_name = ctk.CTkLabel(
            self.profile_frame, text=self.current_username.capitalize(),  # <-- DYNAMIC USER INJECTION
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color="#FFFFFF"
        )
        self.profile_name.pack(anchor="w")
        
        self.profile_role = ctk.CTkLabel(
            self.profile_frame, text="Software Engineer",
            font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#9CA3AF"
        )
        self.profile_role.pack(anchor="w")

        # Navigation Header
        self.nav_title = ctk.CTkLabel(
            self.sidebar_frame, text="NAVIGATION",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#4B5563"
        )
        self.nav_title.grid(row=2, column=0, padx=25, pady=(10, 5), sticky="w")

        # Navigation Menu Buttons
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="   Dashboard", fg_color="#1E293B", text_color="#3B82F6",
            hover_color="#27272A", anchor="w", font=ctk.CTkFont(size=14), command=self.show_dashboard
        )
        self.btn_dashboard.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        self.btn_session = ctk.CTkButton(
            self.sidebar_frame, text="🎙️   Daily Session", fg_color="transparent", text_color="#9CA3AF",
            hover_color="#1E293B", anchor="w", font=ctk.CTkFont(size=14), command=self.show_session
        )
        self.btn_session.grid(row=4, column=0, padx=15, pady=5, sticky="ew")

        self.btn_analytics = ctk.CTkButton(
            self.sidebar_frame, text="📊   Analytics", fg_color="transparent", text_color="#9CA3AF",
            hover_color="#1E293B", anchor="w", font=ctk.CTkFont(size=14), command=self.show_analytics
        )
        self.btn_analytics.grid(row=5, column=0, padx=15, pady=5, sticky="ew")

        # ----------------------------------------------------
        # 2. MAIN CANVAS VIEWS
        # ----------------------------------------------------
        self.dashboard_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)
        self.session_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)
        self.analytics_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)

    def setup_dashboard_content(self):
        # Header Greeting Section
        self.date_lbl = ctk.CTkLabel(self.dashboard_view, text="MONDAY · JULY 20, 2026", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563")
        self.date_lbl.pack(padx=40, pady=(40, 0), anchor="w")

        self.welcome_lbl = ctk.CTkLabel(self.dashboard_view, text=f"Welcome back, {self.current_username.capitalize()}.", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color="white")
        self.welcome_lbl.pack(padx=40, pady=(5, 0), anchor="w")

        self.motivate_lbl = ctk.CTkLabel(self.dashboard_view, text="You're on a roll — don't break the streak today.", font=ctk.CTkFont(size=14), text_color="#9CA3AF")
        self.motivate_lbl.pack(padx=40, pady=(5, 25), anchor="w")

        # METRICS GRID CONTAINER (Row of 4 Cards)
        self.metrics_container = ctk.CTkFrame(self.dashboard_view, fg_color="transparent")
        self.metrics_container.pack(padx=40, pady=10, fill="x", anchor="w")
        self.metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        # Card 1: Day Streak
        card1 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card1.grid(row=0, column=0, padx=8, pady=0, sticky="nsew")
        card1.grid_propagate(False)
        ctk.CTkLabel(card1, text="🔥 5", font=ctk.CTkFont(size=36, weight="bold"), text_color="#F59E0B").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        ctk.CTkLabel(card1, text="Day Streak", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").grid(row=1, column=0, padx=20, pady=0, sticky="w")
        ctk.CTkLabel(card1, text="Personal best: 12 days 🏆", font=ctk.CTkFont(size=11), text_color="#9CA3AF").grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")

        # Card 2: Questions Answered
        card2 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card2.grid(row=0, column=1, padx=8, pady=0, sticky="nsew")
        card2.grid_propagate(False)
        ctk.CTkLabel(card2, text="Questions Answered", font=ctk.CTkFont(size=12), text_color="#9CA3AF").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        ctk.CTkLabel(card2, text="247", font=ctk.CTkFont(size=36, weight="bold"), text_color="white").grid(row=1, column=0, padx=20, pady=0, sticky="w")
        ctk.CTkLabel(card2, text="+12 today", font=ctk.CTkFont(size=12, weight="bold"), text_color="#10B981").grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        # Card 3: Average Score
        card3 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card3.grid(row=0, column=2, padx=8, pady=0, sticky="nsew")
        card3.grid_propagate(False)
        ctk.CTkLabel(card3, text="Average Score", font=ctk.CTkFont(size=12), text_color="#9CA3AF").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        ctk.CTkLabel(card3, text="7.8", font=ctk.CTkFont(size=36, weight="bold"), text_color="white").grid(row=1, column=0, padx=20, pady=0, sticky="w")
        ctk.CTkLabel(card3, text="↑ 0.4 this week", font=ctk.CTkFont(size=12, weight="bold"), text_color="#10B981").grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        # Card 4: Sessions Completed
        card4 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card4.grid(row=0, column=3, padx=8, pady=0, sticky="nsew")
        card4.grid_propagate(False)
        ctk.CTkLabel(card4, text="Sessions Completed", font=ctk.CTkFont(size=12), text_color="#9CA3AF").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        ctk.CTkLabel(card4, text="34", font=ctk.CTkFont(size=36, weight="bold"), text_color="white").grid(row=1, column=0, padx=20, pady=0, sticky="w")
        ctk.CTkLabel(card4, text="3 this week", font=ctk.CTkFont(size=12, weight="bold"), text_color="#10B981").grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        # TODAY'S CHALLENGE BANNER CARD
        self.challenge_card = ctk.CTkFrame(self.dashboard_view, fg_color="#0F1E36", border_color="#1E3A8A", border_width=1, corner_radius=16)
        self.challenge_card.pack(padx=40, pady=30, fill="x")
        
        self.challenge_card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.challenge_card, text="● TODAY'S CHALLENGE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#3B82F6").grid(row=0, column=0, padx=30, pady=(25, 0), sticky="w")
        ctk.CTkLabel(self.challenge_card, text="Behavioral Questions\n— STAR Method Focus", font=ctk.CTkFont(size=24, weight="bold"), text_color="white", justify="left").grid(row=1, column=0, padx=30, pady=(5, 0), sticky="w")
        ctk.CTkLabel(self.challenge_card, text="5 questions · 15 minutes · Estimated score boost: +0.6 pts", font=ctk.CTkFont(size=13), text_color="#9CA3AF").grid(row=2, column=0, padx=30, pady=(10, 25), sticky="w")

        self.start_btn = ctk.CTkButton(
            self.challenge_card, text="Start Session  →", fg_color="#2563EB", hover_color="#1D4ED8",
            font=ctk.CTkFont(size=15, weight="bold"), corner_radius=8, width=160, height=45,
            command=self.show_session
        )
        self.start_btn.grid(row=1, column=1, padx=40, sticky="e")

    def setup_other_placeholders(self):
        # ----------------------------------------------------
        # FIGMA SCREEN 2: ACTIVE DAILY SESSION INTERFACE
        # ----------------------------------------------------
        self.session_header_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.session_header_frame.pack(padx=40, pady=(40, 10), fill="x")
        
        ctk.CTkLabel(self.session_header_frame, text="BEHAVIORAL SESSION", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563").pack(side="left")
        ctk.CTkLabel(self.session_header_frame, text="Question 2 of 5", font=ctk.CTkFont(size=13, weight="bold"), text_color="white").pack(side="right")
        
        self.progress_bar = ctk.CTkProgressBar(self.session_view, height=4, progress_color="#2563EB", fg_color="#1E293B")
        self.progress_bar.pack(padx=40, pady=(0, 25), fill="x")
        self.progress_bar.set(0.4)

        self.ai_card = ctk.CTkFrame(self.session_view, fg_color="#161F30", corner_radius=16)
        self.ai_card.pack(padx=40, pady=10, fill="x")
        self.ai_card.grid_columnconfigure(1, weight=1)
        
        self.ai_icon_box = ctk.CTkFrame(self.ai_card, width=45, height=45, fg_color="#4338CA", corner_radius=8)
        self.ai_icon_box.grid(row=0, column=0, padx=(25, 15), pady=(25, 10), sticky="nw")
        self.ai_icon_box.grid_propagate(False)
        ctk.CTkLabel(self.ai_icon_box, text="🤖", font=ctk.CTkFont(size=20)).pack(expand=True)
        
        ctk.CTkLabel(self.ai_card, text="AI INTERVIEWER", font=ctk.CTkFont(size=10, weight="bold"), text_color="#9CA3AF").grid(row=0, column=1, pady=(23, 0), sticky="w")
        
        self.question_text = ctk.CTkLabel(
            self.ai_card, 
            text="Tell me about a time you had to deal with a conflict in a team database project. How did you approach the situation, and what was the final outcome for the team?",
            font=ctk.CTkFont(family="Segoe UI", size=16), text_color="white", justify="left", wraplength=700
        )
        self.question_text.grid(row=1, column=1, pady=(5, 20), padx=(0, 25), sticky="w")
        
        ctk.CTkLabel(self.ai_card, text="⭐ Tip: Use the STAR format — Situation → Task → Action → Result.", font=ctk.CTkFont(size=12), text_color="#F59E0B").grid(row=2, column=1, pady=(0, 25), sticky="w")

        self.input_container = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.input_container.pack(padx=40, pady=20, fill="both", expand=True)
        self.input_container.grid_columnconfigure(0, weight=1)
        self.input_container.grid_rowconfigure(0, weight=1)

        self.text_response_box = ctk.CTkTextbox(self.input_container, fg_color="#111827", border_color="#1F2937", border_width=1, corner_radius=12, font=ctk.CTkFont(size=14), text_color="white")
        self.text_response_box.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.text_response_box.insert("0.0", "Type your answer here...")

        self.mic_panel = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.mic_panel.grid(row=0, column=1, sticky="ns")
        
        self.mic_btn = ctk.CTkButton(self.mic_panel, text="🎙️", font=ctk.CTkFont(size=24), width=65, height=65, corner_radius=32, fg_color="#1F2937", hover_color="#374151")
        self.mic_btn.pack(expand=True, pady=(0, 5))
        ctk.CTkLabel(self.mic_panel, text="HOLD TO\nRECORD", font=ctk.CTkFont(size=9, weight="bold"), text_color="#9CA3AF", justify="center").pack()

        self.footer_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.footer_frame.pack(padx=40, pady=(10, 25), fill="x")
        ctk.CTkLabel(self.footer_frame, text="0 words", font=ctk.CTkFont(size=12), text_color="#4B5563").pack(side="left")
        
        self.submit_btn = ctk.CTkButton(self.footer_frame, text="Submit Answer  →", fg_color="#2563EB", hover_color="#1D4ED8", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, width=150, height=40, command=self.handle_submit)
        self.submit_btn.pack(side="right")

        # ----------------------------------------------------
        # FIGMA SCREEN 3 & 4: PERFORMANCE ANALYTICS GRAPHICS
        # ----------------------------------------------------
        self.scroll_canvas = ctk.CTkScrollableFrame(self.analytics_view, fg_color="transparent")
        self.scroll_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.completion_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.completion_frame.pack(padx=30, pady=(30, 5), fill="x")
        ctk.CTkLabel(self.completion_frame, text="SESSION COMPLETE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563").pack(side="left")
        
        self.dash_btn = ctk.CTkButton(self.completion_frame, text="Dashboard", fg_color="#2563EB", hover_color="#1D4ED8", width=100, height=35, font=ctk.CTkFont(size=13, weight="bold"), command=self.show_dashboard)
        self.dash_btn.pack(side="right", padx=5)
        self.retry_btn = ctk.CTkButton(self.completion_frame, text="Try Again", fg_color="transparent", border_color="#374151", border_width=1, text_color="white", hover_color="#1E293B", width=90, height=35, font=ctk.CTkFont(size=13), command=self.show_session)
        self.retry_btn.pack(side="right", padx=5)

        self.review_lbl = ctk.CTkLabel(self.scroll_canvas, text="Performance Review", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color="white")
        self.review_lbl.pack(padx=30, pady=(5, 20), anchor="w")

        self.perf_card = ctk.CTkFrame(self.scroll_canvas, fg_color="#161F30", corner_radius=16)
        self.perf_card.pack(padx=30, pady=10, fill="x")
        self.perf_card.grid_columnconfigure(1, weight=1)

        self.badge_box = ctk.CTkFrame(self.perf_card, width=100, height=100, fg_color="transparent", border_color="#2563EB", border_width=6, corner_radius=50)
        self.badge_box.grid(row=0, column=0, rowspan=3, padx=30, pady=30, sticky="nsew")
        self.badge_box.grid_propagate(False)
        ctk.CTkLabel(self.badge_box, text="8", font=ctk.CTkFont(size=32, weight="bold"), text_color="white").pack(pady=(20,0))
        ctk.CTkLabel(self.badge_box, text="/ 10", font=ctk.CTkFont(size=11), text_color="#9CA3AF").pack()

        ctk.CTkLabel(self.perf_card, text="OVERALL PERFORMANCE", font=ctk.CTkFont(size=10, weight="bold"), text_color="#9CA3AF").grid(row=0, column=1, pady=(25, 0), sticky="w")
        ctk.CTkLabel(self.perf_card, text="Strong delivery with room to sharpen pacing.", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").grid(row=1, column=1, pady=(2, 0), sticky="w")
        
        self.summary_desc = ctk.CTkLabel(self.perf_card, text="Your STAR structure was solid and technical specificity stood out.", font=ctk.CTkFont(size=13), text_color="#9CA3AF", justify="left", wraplength=650)
        self.summary_desc.grid(row=2, column=1, pady=(5, 20), padx=(0, 30), sticky="w")

        self.skills_grid = ctk.CTkFrame(self.perf_card, fg_color="transparent")
        self.skills_grid.grid(row=3, column=0, columnspan=2, padx=30, pady=(0, 25), sticky="ew")
        self.skills_grid.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        ctk.CTkLabel(self.skills_grid, text="STAR Method", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w")
        self.s1 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#10B981", fg_color="#1E293B")
        self.s1.grid(row=1, column=0, sticky="ew", pady=(4, 15), padx=(0, 20))
        self.s1.set(0.9)

        ctk.CTkLabel(self.skills_grid, text="Pacing & Delivery", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w")
        self.s2 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#3B82F6", fg_color="#1E293B")
        self.s2.grid(row=3, column=0, sticky="ew", pady=(4, 5), padx=(0, 20))
        self.s2.set(0.6)

        ctk.CTkLabel(self.skills_grid, text="Technical Clarity", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w")
        self.s3 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#10B981", fg_color="#1E293B")
        self.s3.grid(row=1, column=1, sticky="ew", pady=(4, 15))
        self.s3.set(0.8)

        ctk.CTkLabel(self.skills_grid, text="Conciseness", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=2, column=1, sticky="w")
        self.s4 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#3B82F6", fg_color="#1E293B")
        self.s4.grid(row=3, column=1, sticky="ew", pady=(4, 5))
        self.s4.set(0.7)

        self.split_columns = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.split_columns.pack(padx=30, pady=15, fill="x")
        self.split_columns.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        self.good_card = ctk.CTkFrame(self.split_columns, fg_color="#061A16", border_color="#064E3B", border_width=1, corner_radius=12)
        self.good_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(self.good_card, text="✓   What You Did Well", font=ctk.CTkFont(size=14, weight="bold"), text_color="#10B981").pack(anchor="w", padx=20, pady=20)
        bullets_good = "• Strong use of the STAR method\n\n• Precise database metric communication"
        ctk.CTkLabel(self.good_card, text=bullets_good, font=ctk.CTkFont(size=12), text_color="#A7F3D0", justify="left", wraplength=400).pack(anchor="w", padx=20, pady=(0, 20))

        self.improve_card = ctk.CTkFrame(self.split_columns, fg_color="#1C160C", border_color="#78350F", border_width=1, corner_radius=12)
        self.improve_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(self.improve_card, text="!   Room to Improve", font=ctk.CTkFont(size=14, weight="bold"), text_color="#F59E0B").pack(anchor="w", padx=20, pady=20)
        bullets_bad = "• Pacing was slightly rushed\n\n• Eliminate structural filler words"
        ctk.CTkLabel(self.improve_card, text=bullets_bad, font=ctk.CTkFont(size=12), text_color="#FDE68A", justify="left", wraplength=400).pack(anchor="w", padx=20, pady=(0, 20))

        self.sandbox_card = ctk.CTkFrame(self.scroll_canvas, fg_color="#111827", border_color="#1F2937", border_width=1, corner_radius=16)
        self.sandbox_card.pack(padx=30, pady=(15, 40), fill="x")
        self.sandbox_card.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        ctk.CTkLabel(self.sandbox_card, text="AI REWRITE SANDBOX", font=ctk.CTkFont(size=10, weight="bold"), text_color="#4B5563").grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")

    # ----------------------------------------------------
    # 4. VIEW PAGE ROUTING NAVIGATION LOGIC
    # ----------------------------------------------------
    def clear_views(self):
        self.dashboard_view.grid_forget()
        self.session_view.grid_forget()
        self.analytics_view.grid_forget()

    def show_dashboard(self):
        self.clear_views()
        self.dashboard_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="#1E293B", text_color="#3B82F6")
        self.btn_session.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_analytics.configure(fg_color="transparent", text_color="#9CA3AF")

    def show_analytics(self):
        self.clear_views()
        self.analytics_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_session.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_analytics.configure(fg_color="#1E293B", text_color="#3B82F6")

    def handle_submit(self):
        # Placeholder handler for session submission pipelines
        self.show_analytics()

    def show_session(self):
        self.clear_views()
        self.session_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_session.configure(fg_color="#1E293B", text_color="#3B82F6")
        self.btn_analytics.configure(fg_color="transparent", text_color="#9CA3AF")
        
        self.question_text.configure(text="Fetching a fresh challenge from the AI...")
        self.text_response_box.delete("1.0", "end") 
        
        local_backups = [
            "Tell me about a time you had to deal with a conflict in a team database project. How did you approach the situation, and what was the final outcome?",
            "Describe a challenging technical problem you faced recently. How did you diagnose it, and what solution did you implement?",
            "Tell me about a time you had to adapt to a sudden change in a project's requirements or priorities. How did you handle the transition?"
        ]

        def fetch_task():
            has_completed = False

            def target_call():
                nonlocal has_completed
                try:
                    question = self.ai.generate_question("Behavioral")
                    if not has_completed:
                        has_completed = True
                        self.current_question = question
                        self.after(0, lambda: self.question_text.configure(text=self.current_question))
                except Exception:
                    pass

            api_thread = threading.Thread(target=target_call, daemon=True)
            api_thread.start()
            api_thread.join(timeout=4.0)

            if not has_completed:
                has_completed = True
                self.current_question = random.choice(local_backups)
                self.after(0, lambda: self.question_text.configure(text=self.current_question))

        threading.Thread(target=fetch_task, daemon=True).start()


if __name__ == "__main__":
    app = IntervAIApp()
    app.mainloop()