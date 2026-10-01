import threading
import json
from datetime import datetime

import cv2
from PIL import Image
import customtkinter as ctk

from ui.theme import THEME
from voice_engine import VoiceEngine
from database import DatabaseManager
from ai_engine import AIEngine

ctk.set_appearance_mode("Dark")

INTERVIEW_TYPES = ("Behavioral", "Technical", "Coding", "System Design")


class AuthView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_login_success):
        super().__init__(parent, fg_color="#0B0F19", corner_radius=0)
        self.db = db_manager
        self.on_success = on_login_success
        self.is_login_mode = True

        self.setup_ui()
        
    def setup_ui(self):
        self.configure(fg_color=THEME["bg"])

        self.card = ctk.CTkFrame(
            self,
            fg_color=THEME["panel"],
            width=1040,
            height=560,
            corner_radius=16,
            border_width=1,
            border_color=THEME["border"],
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False)
        self.card.grid_columnconfigure(0, weight=4, uniform="auth")
        self.card.grid_columnconfigure(1, weight=6, uniform="auth")
        self.card.grid_rowconfigure(0, weight=1)

        self.brand_panel = ctk.CTkFrame(self.card, fg_color="#121E30", corner_radius=12)
        self.brand_panel.grid(row=0, column=0, padx=(8, 4), pady=8, sticky="nsew")

        self.brand_bar = ctk.CTkFrame(self.brand_panel, fg_color="transparent")
        self.brand_bar.pack(anchor="w", padx=30, pady=(30, 0))

        self.brand_icon = ctk.CTkLabel(
            self.brand_bar,
            text="I",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=THEME["text"],
            width=36,
            height=36,
            fg_color=THEME["primary"],
            corner_radius=9,
        )
        self.brand_icon.pack(side="left", padx=(0, 10))

        self.brand_name = ctk.CTkLabel(
            self.brand_bar,
            text="IntervAI",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=THEME["text"],
        )
        self.brand_name.pack(side="left")

        ctk.CTkLabel(
            self.brand_panel,
            text="INTERVIEW PRACTICE, REIMAGINED",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["primary_2"],
        ).pack(anchor="w", padx=32, pady=(76, 14))
        ctk.CTkLabel(
            self.brand_panel,
            text="Walk into your\nnext interview\nwith confidence.",
            font=ctk.CTkFont(family="Segoe UI", size=31, weight="bold"),
            text_color=THEME["text"],
            justify="left",
        ).pack(anchor="w", padx=30)
        ctk.CTkLabel(
            self.brand_panel,
            text="Practice real answers with an AI coach that listens, responds, and helps you improve.",
            font=ctk.CTkFont(size=13),
            text_color=THEME["text_soft"],
            wraplength=305,
            justify="left",
        ).pack(anchor="w", padx=32, pady=(18, 0))

        self.practice_badge = ctk.CTkFrame(self.brand_panel, fg_color="#1B2A40", corner_radius=8)
        self.practice_badge.pack(side="bottom", fill="x", padx=24, pady=24)
        ctk.CTkLabel(
            self.practice_badge,
            text="VOICE  /  VIDEO  /  PERSONALIZED FEEDBACK",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["text_soft"],
        ).pack(padx=14, pady=14, anchor="w")

        self.form_panel = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_panel.grid(row=0, column=1, padx=(38, 54), pady=34, sticky="nsew")

        ctk.CTkLabel(
            self.form_panel,
            text="YOUR WORKSPACE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["muted"],
        ).pack(anchor="w", pady=(24, 12))
        self.title_label = ctk.CTkLabel(
            self.form_panel,
            text="Welcome back",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=THEME["text"],
        )
        self.title_label.pack(anchor="w")

        self.subtitle = ctk.CTkLabel(
            self.form_panel,
            text="Sign in to continue your interview prep.",
            font=ctk.CTkFont(size=13),
            text_color=THEME["muted"],
        )
        self.subtitle.pack(anchor="w", pady=(6, 24))

        self.username_entry = ctk.CTkEntry(
            self.form_panel,
            placeholder_text="Username",
            height=46,
            fg_color=THEME["bg_2"],
            border_color=THEME["border"],
            text_color=THEME["text"],
            placeholder_text_color=THEME["muted"],
            corner_radius=8,
        )
        self.username_entry.pack(fill="x", pady=7)

        self.password_entry = ctk.CTkEntry(
            self.form_panel,
            placeholder_text="Password",
            show="*",
            height=46,
            fg_color=THEME["bg_2"],
            border_color=THEME["border"],
            text_color=THEME["text"],
            placeholder_text_color=THEME["muted"],
            corner_radius=8,
        )
        self.password_entry.pack(fill="x", pady=7)

        self.status_label = ctk.CTkLabel(
            self.form_panel,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=THEME["red"],
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

        self.submit_btn = ctk.CTkButton(
            self.form_panel,
            text="Sign In",
            height=46,
            fg_color=THEME["primary"],
            hover_color="#2E6DD0",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.handle_submit,
            corner_radius=8,
        )
        self.submit_btn.pack(fill="x", pady=(18, 8))

        self.toggle_btn = ctk.CTkButton(
            self.form_panel,
            text="Don't have an account? Sign Up",
            fg_color="transparent",
            text_color=THEME["primary_2"],
            hover_color=THEME["surface_2"],
            font=ctk.CTkFont(size=12),
            command=self.toggle_mode,
        )
        self.toggle_btn.pack(anchor="w", pady=4)

    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        self.status_label.configure(text="")
        if self.is_login_mode:
            self.title_label.configure(text="Welcome back")
            self.subtitle.configure(text="Sign in to continue your interview prep.")
            self.submit_btn.configure(text="Sign In")
            self.toggle_btn.configure(text="Don't have an account? Sign Up")
        else:
            self.title_label.configure(text="Create your account")
            self.subtitle.configure(text="Start building confidence for your next interview.")
            self.submit_btn.configure(text="Sign Up")
            self.toggle_btn.configure(text="Already have an account? Sign In")

    def handle_submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
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
        self.geometry("1365x700")
        self.minsize(1120, 640)
        self.configure(fg_color=THEME["bg"])

        self.db = DatabaseManager()
        self.ai = AIEngine()
        self.voice = VoiceEngine()
        self.cap = None

        self.current_user_id = None
        self.current_username = None
        self.current_question = ""
        self.current_interview_type = "Behavioral"
        self.session_request_id = 0
        self.webcam_image = None

        self.auth_view = AuthView(self, self.db, self.login_success_callback)
        self.auth_view.pack(fill="both", expand=True)

    def setup_dashboard_content(self):
        formatted_date = datetime.now().strftime("%A · %B %d, %Y").upper()

        self.dashboard_scroll = ctk.CTkScrollableFrame(
            self.dashboard_view,
            fg_color="transparent",
            scrollbar_button_color=THEME["border"],
            scrollbar_button_hover_color=THEME["muted"],
        )
        self.dashboard_scroll.pack(fill="both", expand=True, padx=28, pady=18)

        self.dashboard_header = ctk.CTkFrame(self.dashboard_scroll, fg_color="transparent")
        self.dashboard_header.pack(fill="x", pady=(8, 20))
        self.dashboard_header.grid_columnconfigure(0, weight=1)

        header_copy = ctk.CTkFrame(self.dashboard_header, fg_color="transparent")
        header_copy.grid(row=0, column=0, sticky="w")
        self.date_lbl = ctk.CTkLabel(
            header_copy,
            text=formatted_date,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["muted"],
        )
        self.date_lbl.pack(anchor="w", pady=(0, 6))
        self.welcome_lbl = ctk.CTkLabel(
            header_copy,
            text=f"Welcome back, {self.current_username.capitalize()}.",
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
            text_color=THEME["text"],
        )
        self.welcome_lbl.pack(anchor="w")
        self.motivate_lbl = ctk.CTkLabel(
            header_copy,
            text="Your next great interview starts with one good answer.",
            font=ctk.CTkFont(size=13),
            text_color=THEME["text_soft"],
        )
        self.motivate_lbl.pack(anchor="w", pady=(4, 0))

        self.metrics_container = ctk.CTkFrame(self.dashboard_scroll, fg_color="transparent")
        self.metrics_container.pack(fill="x", pady=(0, 18))
        self.metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="metric")

        metric_specs = (
            ("DAY STREAK", "0", "Active practice days", THEME["amber"], "streak_val"),
            ("QUESTIONS ANSWERED", "0", "Answers submitted", THEME["cyan"], "questions_val"),
            ("AVERAGE SCORE", "0.0", "Across your sessions", THEME["green"], "avg_score_val"),
            ("SESSIONS COMPLETED", "0", "Practice sessions", THEME["primary_2"], "sessions_val"),
        )
        for column, (label, value, hint, accent, attribute) in enumerate(metric_specs):
            metric_card = ctk.CTkFrame(
                self.metrics_container,
                fg_color=THEME["card"],
                height=126,
                corner_radius=10,
                border_width=1,
                border_color=THEME["border"],
            )
            metric_card.grid(row=0, column=column, padx=6, sticky="nsew")
            metric_card.grid_propagate(False)
            ctk.CTkFrame(
                metric_card,
                width=3,
                height=32,
                fg_color=accent,
                corner_radius=2,
            ).pack(anchor="w", padx=16, pady=(15, 0))
            ctk.CTkLabel(
                metric_card,
                text=label,
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=THEME["muted"],
            ).place(x=28, y=17)
            value_label = ctk.CTkLabel(
                metric_card,
                text=value,
                font=ctk.CTkFont(family="Segoe UI", size=29, weight="bold"),
                text_color=THEME["text"],
            )
            value_label.pack(anchor="w", padx=16, pady=(3, 0))
            setattr(self, attribute, value_label)
            ctk.CTkLabel(
                metric_card,
                text=hint,
                font=ctk.CTkFont(size=10),
                text_color=THEME["muted"],
            ).pack(anchor="w", padx=16, pady=(0, 12))

        self.dashboard_feature_row = ctk.CTkFrame(self.dashboard_scroll, fg_color="transparent")
        self.dashboard_feature_row.pack(fill="x")
        self.dashboard_feature_row.grid_columnconfigure(0, weight=3, uniform="feature")
        self.dashboard_feature_row.grid_columnconfigure(1, weight=2, uniform="feature")

        self.challenge_card = ctk.CTkFrame(
            self.dashboard_feature_row,
            fg_color="#14213A",
            border_color="#263B5B",
            border_width=1,
            corner_radius=12,
            height=264,
        )
        self.challenge_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        self.challenge_card.grid_propagate(False)
        ctk.CTkLabel(
            self.challenge_card,
            text="TODAY'S PRACTICE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["primary_2"],
        ).pack(anchor="w", padx=24, pady=(22, 12))
        ctk.CTkLabel(
            self.challenge_card,
            text="Behavioral interview",
            font=ctk.CTkFont(family="Segoe UI", size=23, weight="bold"),
            text_color=THEME["text"],
        ).pack(anchor="w", padx=24)
        ctk.CTkLabel(
            self.challenge_card,
            text="Build a clear story, then show the impact you made.",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_soft"],
        ).pack(anchor="w", padx=24, pady=(7, 18))

        practice_meta = ctk.CTkFrame(self.challenge_card, fg_color="transparent")
        practice_meta.pack(anchor="w", padx=20)
        for text in ("5 QUESTIONS", "15 MINUTES", "STAR METHOD"):
            ctk.CTkLabel(
                practice_meta,
                text=text,
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=THEME["text_soft"],
                fg_color="#1D2D46",
                corner_radius=6,
                padx=10,
                pady=7,
            ).pack(side="left", padx=4)

        ctk.CTkFrame(
            self.challenge_card,
            height=1,
            fg_color="#263B5B",
        ).pack(fill="x", padx=24, pady=(18, 12))
        ctk.CTkLabel(
            self.challenge_card,
            text="A focused 15-minute session tailored to your next interview.",
            font=ctk.CTkFont(size=11),
            text_color=THEME["muted"],
        ).pack(anchor="w", padx=24)

        self.star_card = ctk.CTkFrame(
            self.dashboard_feature_row,
            fg_color=THEME["card"],
            border_color=THEME["border"],
            border_width=1,
            corner_radius=12,
            height=264,
        )
        self.star_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        self.star_card.grid_propagate(False)
        ctk.CTkLabel(
            self.star_card,
            text="ANSWER FRAMEWORK",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["muted"],
        ).pack(anchor="w", padx=20, pady=(22, 14))

        star_steps = (
            ("S", "Situation", "Set the scene"),
            ("T", "Task", "Name your goal"),
            ("A", "Action", "Explain your choices"),
            ("R", "Result", "Share the outcome"),
        )
        for letter, title, description in star_steps:
            step_row = ctk.CTkFrame(self.star_card, fg_color="transparent")
            step_row.pack(fill="x", padx=18, pady=5)
            ctk.CTkLabel(
                step_row,
                text=letter,
                width=28,
                height=28,
                fg_color="#1E2B3F",
                text_color=THEME["primary_2"],
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=7,
            ).pack(side="left")
            step_copy = ctk.CTkFrame(step_row, fg_color="transparent")
            step_copy.pack(side="left", padx=(10, 0))
            ctk.CTkLabel(
                step_copy,
                text=title,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=THEME["text"],
            ).pack(anchor="w")
            ctk.CTkLabel(
                step_copy,
                text=description,
                font=ctk.CTkFont(size=9),
                text_color=THEME["muted"],
            ).pack(anchor="w", pady=(1, 0))

    def login_success_callback(self, user_id, username):
        self.current_user_id = user_id
        self.current_username = username
        
        self.auth_view.destroy()
        self.initialize_main_app_layout()

    def initialize_main_app_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.setup_sidebar()
        self.setup_dashboard_content()
        self.setup_session_interface()
        self.setup_analytics_view()
        
        self.show_dashboard()

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=THEME["sidebar"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.logo_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.logo_container.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.logo_icon = ctk.CTkLabel(
            self.logo_container,
            text="I",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=28,
            height=28,
            fg_color="#4F46E5",
            corner_radius=8,
            text_color="white",
        )
        self.logo_icon.pack(side="left")

        self.logo_label = ctk.CTkLabel(
            self.logo_container, text="IntervAI",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#FFFFFF"
        )
        self.logo_label.pack(side="left", padx=(12, 0))

        self.sub_logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="INTERVIEW COACH",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#9CA3AF"
        )
        self.sub_logo_label.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        self.profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.profile_frame.grid(row=2, column=0, padx=20, pady=(0, 18), sticky="ew")

        self.profile_avatar = ctk.CTkLabel(
            self.profile_frame,
            text=self.current_username[0].upper() if self.current_username else "L",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=28,
            height=28,
            fg_color="#8B5CF6",
            corner_radius=14,
            text_color="white",
        )
        self.profile_avatar.pack(side="left")

        self.profile_details = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        self.profile_details.pack(side="left", padx=(12, 0), anchor="w")

        self.profile_name = ctk.CTkLabel(
            self.profile_details, text=self.current_username.capitalize() if self.current_username else "Latifah Osei",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=THEME["text"]
        )
        self.profile_name.pack(anchor="w")

        self.profile_role = ctk.CTkLabel(
            self.profile_details, text="Software Engineer",
            font=ctk.CTkFont(family="Segoe UI", size=11), text_color=THEME["muted"]
        )
        self.profile_role.pack(anchor="w", pady=(2, 0))

        self.nav_title = ctk.CTkLabel(
            self.sidebar_frame, text="NAVIGATION",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color=THEME["muted"]
        )
        self.nav_title.grid(row=3, column=0, padx=24, pady=(8, 8), sticky="w")

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="  Dashboard", fg_color=THEME["surface_2"], text_color=THEME["primary_2"],
            hover_color=THEME["surface_2"], anchor="w", font=ctk.CTkFont(size=14), command=self.show_dashboard,
            height=40, corner_radius=8
        )
        self.btn_dashboard.grid(row=4, column=0, padx=15, pady=3, sticky="ew")

        self.btn_session = ctk.CTkButton(
            self.sidebar_frame, text="🎙️  Daily Session", fg_color="transparent", text_color=THEME["text_soft"],
            hover_color=THEME["surface_2"], anchor="w", font=ctk.CTkFont(size=14), command=self.show_session,
            height=40, corner_radius=8
        )
        self.btn_session.grid(row=5, column=0, padx=15, pady=3, sticky="ew")

        self.btn_analytics = ctk.CTkButton(
            self.sidebar_frame, text="📊  Analytics", fg_color="transparent", text_color=THEME["text_soft"],
            hover_color=THEME["surface_2"], anchor="w", font=ctk.CTkFont(size=14), command=self.show_analytics,
            height=40, corner_radius=8
        )
        self.btn_analytics.grid(row=6, column=0, padx=15, pady=3, sticky="ew")

        self.dashboard_view = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)
        self.session_view = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)
        self.analytics_view = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)

    def refresh_dashboard_metrics(self):
        questions, sessions, streak = self.db.get_user_stats(self.current_user_id)
        avg_score = self.db.get_average_score(self.current_user_id)
        
        self.streak_val.configure(text=str(streak))
        self.questions_val.configure(text=str(questions))
        self.sessions_val.configure(text=str(sessions))
        self.avg_score_val.configure(text=str(avg_score))

    def setup_session_interface(self):
        self.session_header_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.session_header_frame.pack(padx=32, pady=(28, 12), fill="x")
        
        ctk.CTkLabel(
            self.session_header_frame,
            text="INTERVIEW SESSION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=THEME["muted"],
        ).pack(side="left")

        self.btn_start_session = ctk.CTkButton(
            self.session_header_frame,
            text="Start Session",
            fg_color=THEME["primary"],
            hover_color="#2E6DD0",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=142,
            height=36,
            command=self.start_interview_session,
        )
        self.btn_start_session.pack(side="right")

        self.interview_type_menu = ctk.CTkOptionMenu(
            self.session_header_frame,
            values=list(INTERVIEW_TYPES),
            fg_color=THEME["surface_2"],
            button_color=THEME["primary"],
            button_hover_color="#2E6DD0",
            dropdown_fg_color=THEME["panel"],
            text_color=THEME["text"],
            width=160,
            height=36,
        )
        self.interview_type_menu.set(self.current_interview_type)
        self.interview_type_menu.pack(side="right", padx=(0, 10))

        ctk.CTkLabel(
            self.session_header_frame,
            text="INTERVIEW TYPE",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=THEME["muted"],
        ).pack(side="right", padx=(0, 8))
        
        self.interview_split_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.interview_split_frame.pack(padx=32, pady=8, fill="both", expand=True)
        self.interview_split_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")
        self.interview_split_frame.grid_rowconfigure(0, weight=1)

        self.ai_card = ctk.CTkFrame(self.interview_split_frame, fg_color=THEME["card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.ai_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(self.ai_card, text="🤖 AI Interviewer", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(pady=(20, 10))
        
        self.question_text = ctk.CTkLabel(
            self.ai_card, 
            text="Choose an interview type, then press Start Session.",
            font=ctk.CTkFont(size=15), text_color="white", justify="center", wraplength=350
        )
        self.question_text.pack(pady=20, padx=20, expand=True)

        self.btn_speak_question = ctk.CTkButton(
            self.ai_card, text="🔊 Repeat Question", fg_color="#374151", hover_color="#4B5563",
            command=self.play_ai_voice, state="disabled"
        )
        self.btn_speak_question.pack(pady=(0, 20))

        self.video_card = ctk.CTkFrame(self.interview_split_frame, fg_color="#080F1C", corner_radius=12, border_width=1, border_color=THEME["border"])
        self.video_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        self.webcam_label = ctk.CTkLabel(self.video_card, text="Camera Feed Inactive")
        self.webcam_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.controls_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.controls_frame.pack(padx=32, pady=8, fill="x")

        self.text_response_box = ctk.CTkTextbox(self.controls_frame, fg_color="#111827", height=80, corner_radius=12, font=ctk.CTkFont(size=13), text_color="white")
        self.text_response_box.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_record = ctk.CTkButton(
            self.controls_frame, text="🎙️ Record Answer", fg_color="#DC2626", hover_color="#B91C1C",
            width=140, height=80, font=ctk.CTkFont(weight="bold"),
            command=self.start_voice_recording, state="disabled"
        )
        self.btn_record.pack(side="right")

        self.footer_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.footer_frame.pack(padx=32, pady=(5, 20), fill="x")
        
        self.btn_submit = ctk.CTkButton(
            self.footer_frame, text="Submit Answer   →", fg_color="#2563EB", hover_color="#1D4ED8",
            font=ctk.CTkFont(size=14, weight="bold"), height=40, command=self.handle_submit,
            state="disabled"
        )
        self.btn_submit.pack(side="right")

    def setup_analytics_view(self):
        self.scroll_canvas = ctk.CTkScrollableFrame(self.analytics_view, fg_color="transparent")
        self.scroll_canvas.pack(fill="both", expand=True, padx=20, pady=20)

        self.completion_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.completion_frame.pack(fill="x", pady=(10, 5))
        
        self.review_lbl = ctk.CTkLabel(
            self.completion_frame, 
            text="Performance Analytics", 
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"), 
            text_color="white"
        )
        self.review_lbl.pack(side="left")

        self.dash_btn = ctk.CTkButton(
            self.completion_frame, text="Dashboard", fg_color="#2563EB", hover_color="#1D4ED8", 
            width=100, height=35, font=ctk.CTkFont(size=13, weight="bold"), command=self.show_dashboard
        )
        self.dash_btn.pack(side="right", padx=5)

        self.retry_btn = ctk.CTkButton(
            self.completion_frame, text="New Question", fg_color="transparent", border_color="#374151", 
            border_width=1, text_color="white", hover_color="#1E293B", width=110, height=35, 
            font=ctk.CTkFont(size=13), command=self.show_session
        )
        self.retry_btn.pack(side="right", padx=5)

        self.analytics_cards_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.analytics_cards_frame.pack(fill="x", pady=(20, 25))
        self.analytics_cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        card_overall = ctk.CTkFrame(self.analytics_cards_frame, fg_color=THEME["card"], height=120, corner_radius=10, border_width=1, border_color=THEME["border"])
        card_overall.grid(row=0, column=0, padx=6, sticky="nsew")
        card_overall.grid_propagate(False)
        ctk.CTkLabel(card_overall, text="AVERAGE SCORE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#9CA3AF").pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_overall = ctk.CTkLabel(card_overall, text="0.0 / 10", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3B82F6")
        self.lbl_analytics_overall.pack(anchor="w", padx=16)

        card_sessions = ctk.CTkFrame(self.analytics_cards_frame, fg_color=THEME["card"], height=120, corner_radius=10, border_width=1, border_color=THEME["border"])
        card_sessions.grid(row=0, column=1, padx=6, sticky="nsew")
        card_sessions.grid_propagate(False)
        ctk.CTkLabel(card_sessions, text="TOTAL SESSIONS", font=ctk.CTkFont(size=11, weight="bold"), text_color="#9CA3AF").pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_sessions = ctk.CTkLabel(card_sessions, text="0", font=ctk.CTkFont(size=28, weight="bold"), text_color="#10B981")
        self.lbl_analytics_sessions.pack(anchor="w", padx=16)

        card_streak = ctk.CTkFrame(self.analytics_cards_frame, fg_color=THEME["card"], height=120, corner_radius=10, border_width=1, border_color=THEME["border"])
        card_streak.grid(row=0, column=2, padx=6, sticky="nsew")
        card_streak.grid_propagate(False)
        ctk.CTkLabel(card_streak, text="CURRENT STREAK", font=ctk.CTkFont(size=11, weight="bold"), text_color="#9CA3AF").pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_streak = ctk.CTkLabel(card_streak, text="🔥 0 Days", font=ctk.CTkFont(size=28, weight="bold"), text_color="#F59E0B")
        self.lbl_analytics_streak.pack(anchor="w", padx=16)

        ctk.CTkLabel(
            self.scroll_canvas, 
            text="Recent Interview Sessions", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), 
            text_color="white"
        ).pack(anchor="w", pady=(10, 15))

        self.history_frame = ctk.CTkFrame(self.scroll_canvas, fg_color=THEME["card"], corner_radius=10, border_width=1, border_color=THEME["border"])
        self.history_frame.pack(fill="x", pady=(0, 20))


    def refresh_analytics_data(self):
        data = self.db.get_user_analytics(self.current_user_id)

        self.lbl_analytics_overall.configure(text=f"{data['avg_overall']} / 10")
        self.lbl_analytics_sessions.configure(text=str(data["total_sessions"]))
        self.lbl_analytics_streak.configure(
            text=f"🔥 {data['current_streak']} Days"
        )

        # Clear existing entries
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        # Query recent session records with full feedback JSON
        self.db.cursor.execute(
            """
            SELECT topic, overall_score, session_date, ai_feedback 
            FROM interview_history 
            WHERE user_id = ?
            ORDER BY id DESC 
            LIMIT 5
        """,
            (self.current_user_id,),
        )
        recent = self.db.cursor.fetchall()

        if not recent:
            ctk.CTkLabel(
                self.history_frame,
                text=(
                    "No completed sessions yet. Start a session to build your"
                    " history!"
                ),
                font=ctk.CTkFont(size=13),
                text_color="#9CA3AF",
            ).pack(pady=20)
            return

        for topic, score, session_date, ai_feedback_str in recent:
            # Main card container
            card = ctk.CTkFrame(
                self.history_frame, fg_color="#0F172A", corner_radius=10
            )
            card.pack(fill="x", padx=16, pady=8)

            # Header Row (Topic, Date, Score)
            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.pack(fill="x", padx=14, pady=(12, 6))

            display_topic = topic if topic else "Behavioral Session"
            ctk.CTkLabel(
                header_row,
                text=display_topic,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white",
            ).pack(side="left")

            score_val = score if score is not None else 0.0
            score_color = (
                "#10B981"
                if score_val >= 7.0
                else ("#F59E0B" if score_val >= 5.0 else "#EF4444")
            )

            ctk.CTkLabel(
                header_row,
                text=f"Score: {score_val}/10",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=score_color,
            ).pack(side="right", padx=(10, 0))
            if session_date:
                ctk.CTkLabel(
                    header_row,
                    text=str(session_date)[:10],
                    font=ctk.CTkFont(size=12),
                    text_color="#9CA3AF",
                ).pack(side="right")

            # Parse AI Feedback JSON
            reason_text = "No explanation available."
            tips_text = "No improvement tips recorded."

            if ai_feedback_str:
                try:
                    feedback_data = json.loads(ai_feedback_str)
                    reason_text = feedback_data.get("score_reason", reason_text)
                    tips_text = feedback_data.get("improvement_tips", tips_text)
                except Exception:
                    reason_text = ai_feedback_str  # Fallback if stored as raw text

            # Score Breakdown Section
            ctk.CTkLabel(
                card,
                text=f"💡 Why this score: {reason_text}",
                font=ctk.CTkFont(size=12),
                text_color="#CBD5E1",
                wraplength=700,
                justify="left",
            ).pack(anchor="w", padx=14, pady=(2, 4))

            # Improvement Tips Section
            ctk.CTkLabel(
                card,
                text=f"🚀 How to improve: {tips_text}",
                font=ctk.CTkFont(size=12),
                text_color="#60A5FA",
                wraplength=700,
                justify="left",
            ).pack(anchor="w", padx=14, pady=(0, 12))


    def clear_views(self):
        self.dashboard_view.grid_forget()
        self.session_view.grid_forget()
        self.analytics_view.grid_forget()

    def show_dashboard(self):
        self.stop_webcam()
        self.clear_views()
        self.refresh_dashboard_metrics()
        self.dashboard_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color=THEME["surface_2"], text_color=THEME["primary_2"])
        self.btn_session.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_analytics.configure(fg_color="transparent", text_color=THEME["text_soft"])

    def show_analytics(self):
        self.stop_webcam()
        self.clear_views()
        self.refresh_analytics_data()
        self.analytics_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_session.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_analytics.configure(fg_color=THEME["surface_2"], text_color=THEME["primary_2"])


    # ==========================================================
    # STEP 4: HOOKING UP AI ENGINE & VOICE TO SESSION VIEW
    # ==========================================================

    def show_session(self):
        """Opens the session setup so the user can choose a type and start."""
        self.stop_webcam()
        self.clear_views()
        self.session_view.grid(row=0, column=1, sticky="nsew")
        
        # Update Nav Active State
        self.btn_dashboard.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_session.configure(fg_color=THEME["surface_2"], text_color=THEME["primary_2"])
        self.btn_analytics.configure(fg_color="transparent", text_color=THEME["text_soft"])
        
        self.session_request_id += 1
        self.current_question = ""
        self.interview_type_menu.configure(state="normal")
        self.btn_start_session.configure(state="normal", text="Start Session")
        self.btn_speak_question.configure(state="disabled")
        self.btn_record.configure(state="disabled", text="🎙️ Record Answer")
        self.question_text.configure(text="Choose an interview type, then press Start Session.")
        self.text_response_box.delete("1.0", "end")
        self.btn_submit.configure(state="disabled", text="Submit Answer   →")

    def start_interview_session(self):
        """Starts the camera and requests a question for the chosen interview type."""
        if self.btn_start_session.cget("state") == "disabled":
            return

        self.current_interview_type = self.interview_type_menu.get()
        self.session_request_id += 1
        request_id = self.session_request_id
        self.current_question = ""
        self.btn_start_session.configure(state="disabled", text="Starting...")
        self.interview_type_menu.configure(state="disabled")
        self.btn_speak_question.configure(state="disabled")
        self.btn_record.configure(state="disabled")
        self.btn_submit.configure(state="disabled", text="Submit Answer   →")
        self.text_response_box.delete("1.0", "end")
        self.question_text.configure(
            text=f"Preparing your {self.current_interview_type.lower()} interview question..."
        )
        self.start_webcam()

        def fetch_question_worker():
            question = self.ai.generate_question(self.current_interview_type)
            self.after(0, lambda: self._on_question_loaded(question, request_id))

        threading.Thread(target=fetch_question_worker, daemon=True).start()

    def _on_question_loaded(self, question, request_id):
        """UI Callback once the question fetch completes."""
        if request_id != self.session_request_id:
            return

        self.current_question = question
        self.question_text.configure(text=question)
        self.btn_submit.configure(state="normal", text="Submit Answer   →")
        self.btn_speak_question.configure(state="normal")
        self.btn_record.configure(state="normal", text="🎙️ Record Answer")
        self.btn_start_session.configure(text="Session Started")
        # Automatically read question aloud via TTS
        self.play_ai_voice()

    def play_ai_voice(self):
        """Triggers text-to-speech for the active question."""
        text = self.current_question
        if text and not text.startswith(" Fetching"):
            threading.Thread(target=lambda: self.voice.speak(text), daemon=True).start()

    def start_voice_recording(self):
        """Listens through microphone and transcribes answer into text box."""
        self.btn_record.configure(state="disabled", text=" Listening...", fg_color="#D97706")
        
        def record_worker():
            # Voice Engine transcribes speech to text
            transcript = self.voice.listen_and_transcribe()
            self.after(0, lambda: self.on_transcription_complete(transcript))

        threading.Thread(target=record_worker, daemon=True).start()

    def on_transcription_complete(self, transcript):
        """Appends transcribed text directly into user response textbox."""
        self.text_response_box.delete("1.0", "end")
        if transcript:
            self.text_response_box.insert("1.0", transcript)
        else:
            self.text_response_box.insert("1.0", "Could not capture audio. Please type response.")
            
        self.btn_record.configure(state="normal", text="🎙️ Record Answer", fg_color="#DC2626")

    def handle_submit(self):
        """Sends question + answer to AI Engine for analysis, saves to DB, shifts to Analytics."""
        user_answer = self.text_response_box.get("1.0", "end-1c").strip()
        
        if not user_answer or not self.current_question or self.current_question.startswith(" Fetching"):
            return

        question = self.current_question
        interview_type = self.current_interview_type

        # Disable submit button to prevent double submissions
        self.btn_submit.configure(state="disabled", text=" Analyzing with AI...")

        def process_submission_worker():
            try:
                # 1. Send response to AI Engine for structured scoring
                analysis = self.ai.analyze_response(question, user_answer, interview_type)
                
                overall_score = analysis.get("overall_score", 7.0)
                feedback_json = json.dumps(analysis)
                
                # 2. Persist to DB
                self.db.save_interview_session(
                    user_id=self.current_user_id,
                    topic=interview_type,
                    score=overall_score,
                    feedback=feedback_json
                )
                
                # 3. Transition cleanly to Analytics View on main thread
                self.after(0, self.show_analytics)

            except Exception as err:
                print(f"[Error] Failed to process AI submission: {err}")
                self.after(0, lambda: self.btn_submit.configure(state="normal", text="Submit Answer   →"))

        threading.Thread(target=process_submission_worker, daemon=True).start()

    # ==========================================================
    # CAMERA CONTROLS
    # ==========================================================

    def start_webcam(self):
        if self.cap is None or not self.cap.isOpened():
            self.stop_webcam()
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.stop_webcam()
                self.show_camera_unavailable()
                return
        self.update_webcam_feed()

    def update_webcam_feed(self):
        if self.cap is None or not self.cap.isOpened():
            self.stop_webcam()
            self.show_camera_unavailable()
            return

        ret, frame = self.cap.read()
        if not ret or frame is None:
            self.stop_webcam()
            self.show_camera_unavailable()
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        self.webcam_image = ctk.CTkImage(light_image=img, dark_image=img, size=(380, 240))

        self.webcam_label.configure(image=self.webcam_image, text="")
        self.webcam_label.after(15, self.update_webcam_feed)

    def show_camera_unavailable(self):
        if hasattr(self, "webcam_label") and self.webcam_label.winfo_exists():
            self.webcam_label.configure(
                image=None,
                text="Camera unavailable\nYou can still type or record your answer.",
                text_color=THEME["muted"],
            )
        self.webcam_image = None

    def stop_webcam(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None


if __name__ == "__main__":
    app = IntervAIApp()
    app.mainloop()