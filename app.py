import customtkinter as ctk

# Set global application styling matching your Figma design
ctk.set_appearance_mode("Dark")

class IntervAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IntervAI — Interview Coach")
        self.geometry("1200x700")
        
        # Configure overall grid layout (1 row, 2 columns: Sidebar and Content Canvas)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ----------------------------------------------------
        # 1. FIXED LEFT NAVIGATION SIDEBAR
        # ----------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#121824")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) 

        # App Logo Brand Header
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="I  IntervAI", 
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#FFFFFF"
        )
        self.logo_label.grid(row=0, column=0, padx=25, pady=(25, 5), sticky="w")
        
        self.sub_logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="INTERVIEW COACH", 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#9CA3AF"
        )
        self.sub_logo_label.grid(row=0, column=0, padx=43, pady=(52, 20), sticky="w")

        # User Profile Block
        self.profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.profile_frame.grid(row=1, column=0, padx=25, pady=(10, 30), sticky="ew")
        
        self.profile_name = ctk.CTkLabel(
            self.profile_frame, text="Latifah Osei",
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
            self.sidebar_frame, text="🎙️  Daily Session", fg_color="transparent", text_color="#9CA3AF",
            hover_color="#1E293B", anchor="w", font=ctk.CTkFont(size=14), command=self.show_session
        )
        self.btn_session.grid(row=4, column=0, padx=15, pady=5, sticky="ew")

        self.btn_analytics = ctk.CTkButton(
            self.sidebar_frame, text="📊  Analytics", fg_color="transparent", text_color="#9CA3AF",
            hover_color="#1E293B", anchor="w", font=ctk.CTkFont(size=14), command=self.show_analytics
        )
        self.btn_analytics.grid(row=5, column=0, padx=15, pady=5, sticky="ew")

        # ----------------------------------------------------
        # 2. MAIN CANVAS VIEWS
        # ----------------------------------------------------
        self.dashboard_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)
        self.session_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)
        self.analytics_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)

        self.setup_dashboard_content()
        self.setup_other_placeholders()

        self.show_dashboard()

    # ----------------------------------------------------
    # 3. BUILD THE FIGMA DASHBOARD LAYOUT
    # ----------------------------------------------------
    def setup_dashboard_content(self):
        # Header Greeting Section
        self.date_lbl = ctk.CTkLabel(self.dashboard_view, text="MONDAY · JULY 20, 2026", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563")
        self.date_lbl.pack(padx=40, pady=(40, 0), anchor="w")

        self.welcome_lbl = ctk.CTkLabel(self.dashboard_view, text="Welcome back, Latifah.", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color="white")
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
        card3.grid_propagate(False)
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
        
        # Details inside the banner (using grid inside the pack card)
        self.challenge_card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.challenge_card, text="● TODAY'S CHALLENGE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#3B82F6").grid(row=0, column=0, padx=30, pady=(25, 0), sticky="w")
        
        ctk.CTkLabel(self.challenge_card, text="Behavioral Questions\n— STAR Method Focus", font=ctk.CTkFont(size=24, weight="bold"), text_color="white", justify="left").grid(row=1, column=0, padx=30, pady=(5, 0), sticky="w")
        
        ctk.CTkLabel(self.challenge_card, text="5 questions · 15 minutes · Estimated score boost: +0.6 pts", font=ctk.CTkFont(size=13), text_color="#9CA3AF").grid(row=2, column=0, padx=30, pady=(10, 25), sticky="w")

        # Glowing Blue CTA Button right inside the card
        self.start_btn = ctk.CTkButton(
            self.challenge_card, text="Start Session  →", fg_color="#2563EB", hover_color="#1D4ED8",
            font=ctk.CTkFont(size=15, weight="bold"), corner_radius=8, width=160, height=45,
            command=self.show_session
        )
        self.start_btn.grid(row=1, column=1, padx=40, sticky="e")

    def setup_other_placeholders(self):
        # ----------------------------------------------------
        # FIGMA SCREEN 2: ACTIVE DALY SESSION INTERFACE
        # ----------------------------------------------------
        # Page Header & Progress Metrics Row
        self.session_header_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.session_header_frame.pack(padx=40, pady=(40, 10), fill="x")
        
        ctk.CTkLabel(
            self.session_header_frame, text="BEHAVIORAL SESSION", 
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563"
        ).pack(side="left")
        
        ctk.CTkLabel(
            self.session_header_frame, text="Question 2 of 5", 
            font=ctk.CTkFont(size=13, weight="bold"), text_color="white"
        ).pack(side="right")
        
        # Horizontal Custom Progress Bar Visual Indicator
        self.progress_bar = ctk.CTkProgressBar(self.session_view, height=4, progress_color="#2563EB", fg_color="#1E293B")
        self.progress_bar.pack(padx=40, pady=(0, 25), fill="x")
        self.progress_bar.set(0.4) # Sets progress visual roughly to 40% completed

        # The AI Interviewer Card Container
        self.ai_card = ctk.CTkFrame(self.session_view, fg_color="#161F30", corner_radius=16)
        self.ai_card.pack(padx=40, pady=10, fill="x")
        
        # Grid inside the AI question block for neat visual layout alignment
        self.ai_card.grid_columnconfigure(1, weight=1)
        
        # Mini AI Icon Box Representation
        self.ai_icon_box = ctk.CTkFrame(self.ai_card, width=45, height=45, fg_color="#4338CA", corner_radius=8)
        self.ai_icon_box.grid(row=0, column=0, padx=(25, 15), pady=(25, 10), sticky="nw")
        self.ai_icon_box.grid_propagate(False)
        ctk.CTkLabel(self.ai_icon_box, text="🤖", font=ctk.CTkFont(size=20)).pack(expand=True)
        
        ctk.CTkLabel(
            self.ai_card, text="AI INTERVIEWER", 
            font=ctk.CTkFont(size=10, weight="bold"), text_color="#9CA3AF"
        ).grid(row=0, column=1, pady=(23, 0), sticky="w")
        
        # Dynamic Target Interview Prompt Label Block
        self.question_text = ctk.CTkLabel(
            self.ai_card, 
            text="Tell me about a time you had to deal with a conflict in a team database project. How did you approach the situation, and what was the final outcome for the team?",
            font=ctk.CTkFont(family="Segoe UI", size=16), text_color="white", justify="left", wraplength=700
        )
        self.question_text.grid(row=1, column=1, pady=(5, 20), padx=(0, 25), sticky="w")
        
        # Context Recommendation Visual Hint Block
        ctk.CTkLabel(
            self.ai_card, text="⭐ Tip: Use the STAR format — Situation → Task → Action → Result.",
            font=ctk.CTkFont(size=12), text_color="#F59E0B"
        ).grid(row=2, column=1, pady=(0, 25), sticky="w")

        # User Interactive Typing Box Frame Area Container
        self.input_container = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.input_container.pack(padx=40, pady=20, fill="both", expand=True)
        self.input_container.grid_columnconfigure(0, weight=1)
        self.input_container.grid_rowconfigure(0, weight=1)

        # Huge Multi-line Text Field Element Input Entry Canvas Box
        self.text_response_box = ctk.CTkTextbox(
            self.input_container, fg_color="#111827", border_color="#1F2937", border_width=1,
            corner_radius=12, font=ctk.CTkFont(size=14), text_color="white"
        )
        self.text_response_box.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.text_response_box.insert("0.0", "Type your answer here, or use the microphone to respond...")

        # Side panel container housing the microphone circular control
        self.mic_panel = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.mic_panel.grid(row=0, column=1, sticky="ns")
        
        self.mic_btn = ctk.CTkButton(
            self.mic_panel, text="🎙️", font=ctk.CTkFont(size=24), width=65, height=65,
            corner_radius=32, fg_color="#1F2937", hover_color="#374151"
        )
        self.mic_btn.pack(expand=True, pady=(0, 5))
        
        ctk.CTkLabel(
            self.mic_panel, text="HOLD TO\nRECORD", 
            font=ctk.CTkFont(size=9, weight="bold"), text_color="#9CA3AF", justify="center"
        ).pack()

        # Footer Action Panel Row
        self.footer_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.footer_frame.pack(padx=40, pady=(10, 25), fill="x")
        
        ctk.CTkLabel(self.footer_frame, text="0 words", font=ctk.CTkFont(size=12), text_color="#4B5563").pack(side="left")
        
        self.submit_btn = ctk.CTkButton(
            self.footer_frame, text="Submit Answer  →", fg_color="#2563EB", hover_color="#1D4ED8",
            font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, width=150, height=40,
            command=self.show_analytics
        )
        self.submit_btn.pack(side="right")

        # ----------------------------------------------------
        # FIGMA SCREEN 3 & 4: PERFORMANCE ANALYTICS GRAPHICS
        # ----------------------------------------------------
        # Make the analytics canvas scrollable so all feedback text fits cleanly
        self.scroll_canvas = ctk.CTkScrollableFrame(self.analytics_view, fg_color="transparent")
        self.scroll_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Session Complete Action Header
        self.completion_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.completion_frame.pack(padx=30, pady=(30, 5), fill="x")
        
        ctk.CTkLabel(self.completion_frame, text="SESSION COMPLETE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563").pack(side="left")
        
        self.dash_btn = ctk.CTkButton(self.completion_frame, text="Dashboard", fg_color="#2563EB", hover_color="#1D4ED8", width=100, height=35, font=ctk.CTkFont(size=13, weight="bold"), command=self.show_dashboard)
        self.dash_btn.pack(side="right", padx=5)
        self.retry_btn = ctk.CTkButton(self.completion_frame, text="Try Again", fg_color="transparent", border_color="#374151", border_width=1, text_color="white", hover_color="#1E293B", width=90, height=35, font=ctk.CTkFont(size=13), command=self.show_session)
        self.retry_btn.pack(side="right", padx=5)

        self.review_lbl = ctk.CTkLabel(self.scroll_canvas, text="Performance Review", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color="white")
        self.review_lbl.pack(padx=30, pady=(5, 20), anchor="w")

        # OVERALL PERFORMANCE BLOCK CARD
        self.perf_card = ctk.CTkFrame(self.scroll_canvas, fg_color="#161F30", corner_radius=16)
        self.perf_card.pack(padx=30, pady=10, fill="x")
        self.perf_card.grid_columnconfigure(1, weight=1)

        # Circular Badge Visual Mimic (8/10 Score Container)
        self.badge_box = ctk.CTkFrame(self.perf_card, width=100, height=100, fg_color="transparent", border_color="#2563EB", border_width=6, corner_radius=50)
        self.badge_box.grid(row=0, column=0, rowspan=3, padx=30, pady=30, sticky="nsew")
        self.badge_box.grid_propagate(False)
        ctk.CTkLabel(self.badge_box, text="8", font=ctk.CTkFont(size=32, weight="bold"), text_color="white").pack(pady=(20,0))
        ctk.CTkLabel(self.badge_box, text="/ 10", font=ctk.CTkFont(size=11), text_color="#9CA3AF").pack()

        # Text Summary Critiques
        ctk.CTkLabel(self.perf_card, text="OVERALL PERFORMANCE", font=ctk.CTkFont(size=10, weight="bold"), text_color="#9CA3AF").grid(row=0, column=1, pady=(25, 0), sticky="w")
        ctk.CTkLabel(self.perf_card, text="Strong delivery with room to sharpen pacing.", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").grid(row=1, column=1, pady=(2, 0), sticky="w")
        
        self.summary_desc = ctk.CTkLabel(
            self.perf_card, 
            text="Your STAR structure was solid and technical specificity stood out. Focus on slowing your delivery — interviewers respond better to measured, deliberate pacing.",
            font=ctk.CTkFont(size=13), text_color="#9CA3AF", justify="left", wraplength=650
        )
        self.summary_desc.grid(row=2, column=1, pady=(5, 20), padx=(0, 30), sticky="w")

        # Metric Core Skill Split Grid Layout Subpanel
        self.skills_grid = ctk.CTkFrame(self.perf_card, fg_color="transparent")
        self.skills_grid.grid(row=3, column=0, columnspan=2, padx=30, pady=(0, 25), sticky="ew")
        self.skills_grid.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        # Left Skills Metrics Block
        ctk.CTkLabel(self.skills_grid, text="STAR Method", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self.skills_grid, text="9/10", text_color="#10B981", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="e")
        s1 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#10B981", fg_color="#1E293B")
        s1.grid(row=1, column=0, sticky="ew", pady=(4, 15), padx=(0, 20))
        s1.set(0.9)

        ctk.CTkLabel(self.skills_grid, text="Pacing & Delivery", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w")
        ctk.CTkLabel(self.skills_grid, text="6/10", text_color="#3B82F6", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, sticky="e")
        s2 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#3B82F6", fg_color="#1E293B")
        s2.grid(row=3, column=0, sticky="ew", pady=(4, 5), padx=(0, 20))
        s2.set(0.6)

        # Right Skills Metrics Block
        ctk.CTkLabel(self.skills_grid, text="Technical Clarity", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(self.skills_grid, text="8/10", text_color="#10B981", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=1, sticky="e")
        s3 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#10B981", fg_color="#1E293B")
        s3.grid(row=1, column=1, sticky="ew", pady=(4, 15))
        s3.set(0.8)

        ctk.CTkLabel(self.skills_grid, text="Conciseness", text_color="#9CA3AF", font=ctk.CTkFont(size=12)).grid(row=2, column=1, sticky="w")
        ctk.CTkLabel(self.skills_grid, text="7/10", text_color="#3B82F6", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=1, sticky="e")
        s4 = ctk.CTkProgressBar(self.skills_grid, height=6, progress_color="#3B82F6", fg_color="#1E293B")
        s4.grid(row=3, column=1, sticky="ew", pady=(4, 5))
        s4.set(0.7)

        # SPLIT ANALYSIS COLUMNS (What Went Well vs Room to Improve Layout Container)
        self.split_columns = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.split_columns.pack(padx=30, pady=15, fill="x")
        self.split_columns.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        # Green Column Card (Strengths)
        good_card = ctk.CTkFrame(self.split_columns, fg_color="#061A16", border_color="#064E3B", border_width=1, corner_radius=12)
        good_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(good_card, text="✓  What You Did Well", font=ctk.CTkFont(size=14, weight="bold"), text_color="#10B981").pack(anchor="w", padx=20, pady=20)
        
        bullets_good = "• Strong use of the STAR method — structure was clear from start to finish\n\n• Specific, measurable outcome clearly articulated at the close\n\n• Technical vocabulary around database constraints was precise"
        ctk.CTkLabel(good_card, text=bullets_good, font=ctk.CTkFont(size=12), text_color="#A7F3D0", justify="left", wraplength=400).pack(anchor="w", padx=20, pady=(0, 20))

        # Amber Column Card (Improvements)
        improve_card = ctk.CTkFrame(self.split_columns, fg_color="#1C160C", border_color="#78350F", border_width=1, corner_radius=12)
        improve_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(improve_card, text="!  Room to Improve", font=ctk.CTkFont(size=14, weight="bold"), text_color="#F59E0B").pack(anchor="w", padx=20, pady=20)
        
        bullets_bad = "• Pacing was slightly rushed — slow down on key assertions for emphasis\n\n• The Situation stage was too brief; add 2 more context sentences\n\n• Avoid filler phrases — \"basically\" and \"kind of\" undercut authority"
        ctk.CTkLabel(improve_card, text=bullets_bad, font=ctk.CTkFont(size=12), text_color="#FDE68A", justify="left", wraplength=400).pack(anchor="w", padx=20, pady=(0, 20))

        # AI REWRITE SANDBOX CARD
        self.sandbox_card = ctk.CTkFrame(self.scroll_canvas, fg_color="#111827", border_color="#1F2937", border_width=1, corner_radius=16)
        self.sandbox_card.pack(padx=30, pady=(15, 40), fill="x")
        self.sandbox_card.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        ctk.CTkLabel(self.sandbox_card, text="AI REWRITE SANDBOX", font=ctk.CTkFont(size=10, weight="bold"), text_color="#4B5563").grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")
        
        # Original Answer Layout Box Panel
        ctk.CTkLabel(self.sandbox_card, text="YOUR ANSWER", font=ctk.CTkFont(size=9, weight="bold"), text_color="#EF4444", fg_color="#2D1A1A", corner_radius=4, padx=6, pady=2).grid(row=1, column=0, padx=25, pady=(10, 5), sticky="w")
        orig_txt = '“So basically, there was this conflict with a team member about how we were handling the database schema. I kind of took charge and talked to them and we eventually resolved it and the project went well.”'
        ctk.CTkLabel(self.sandbox_card, text=orig_txt, font=ctk.CTkFont(size=13, slant="italic"), text_color="#6B7280", justify="left", wraplength=400).grid(row=2, column=0, padx=25, pady=(5, 25), sticky="nw")

        # Recommended Senior Candidate Upgrade Box Panel
        ctk.CTkLabel(self.sandbox_card, text="★ SENIOR CANDIDATE", font=ctk.CTkFont(size=9, weight="bold"), text_color="#3B82F6", fg_color="#1E293B", corner_radius=4, padx=6, pady=2).grid(row=1, column=1, padx=25, pady=(10, 5), sticky="w")
        senior_txt = '"In my previous role, our team was split on how to normalize a shared schema... I scheduled a structured design review, preparing a side-by-side trade-off analysis. We adopted a hybrid model that cut query complexity by 40% and shipped on schedule."'
        ctk.CTkLabel(self.sandbox_card, text=senior_txt, font=ctk.CTkFont(size=13), text_color="#E5E7EB", justify="left", wraplength=400).grid(row=2, column=1, padx=25, pady=(5, 25), sticky="nw")

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

    def show_session(self):
        self.clear_views()
        self.session_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_session.configure(fg_color="#1E293B", text_color="#3B82F6")
        self.btn_analytics.configure(fg_color="transparent", text_color="#9CA3AF")

    def show_analytics(self):
        self.clear_views()
        self.analytics_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_session.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_analytics.configure(fg_color="#1E293B", text_color="#3B82F6")

if __name__ == "__main__":
    app = IntervAIApp()
    app.mainloop()