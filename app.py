import threading
import json
from datetime import datetime
import cv2
from PIL import Image, ImageTk
import customtkinter as ctk

from voice_engine import VoiceEngine
from database import DatabaseManager
from ai_engine import AIEngine

ctk.set_appearance_mode("Dark")


class AuthView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_login_success):
        super().__init__(parent, fg_color="#0B0F19", corner_radius=0)
        self.db = db_manager
        self.on_success = on_login_success
        self.is_login_mode = True

        self.setup_ui()
        
    def setup_ui(self):
        self.card = ctk.CTkFrame(self, fg_color="#1E293B", width=360, height=450, corner_radius=16)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.card, text="IntervAI Login", 
            font=ctk.CTkFont(size=24, weight="bold"), text_color="white"
        )
        self.title_label.pack(pady=(40, 30))
        
        self.username_entry = ctk.CTkEntry(
            self.card, placeholder_text="Username", 
            width=280, height=40, fg_color="#0F172A", border_color="#334155"
        )
        self.username_entry.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(
            self.card, placeholder_text="Password", show="*", 
            width=280, height=40, fg_color="#0F172A", border_color="#334155"
        )
        self.password_entry.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        self.status_label.pack(pady=5)
        
        self.submit_btn = ctk.CTkButton(
            self.card, text="Sign In", width=280, height=40, 
            fg_color="#2563EB", hover_color="#1D4ED8", font=ctk.CTkFont(weight="bold"),
            command=self.handle_submit
        )
        self.submit_btn.pack(pady=(15, 10))
        
        self.toggle_btn = ctk.CTkButton(
            self.card, text="Don't have an account? Sign Up", 
            fg_color="transparent", text_color="#3B82F6", hover_color="#1E293B",
            font=ctk.CTkFont(size=12), command=self.toggle_mode
        )
        self.toggle_btn.pack(pady=10)

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
        self.geometry("1100x680")
        
        self.db = DatabaseManager()
        self.ai = AIEngine()
        self.voice = VoiceEngine()
        self.cap = None
        
        self.current_user_id = None
        self.current_username = None
        self.current_question = ""
        self.webcam_image = None
        
        self.auth_view = AuthView(self, self.db, self.login_success_callback)
        self.auth_view.pack(fill="both", expand=True)

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
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#121824")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) 

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

        self.profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.profile_frame.grid(row=1, column=0, padx=25, pady=(10, 30), sticky="ew")
        
        self.profile_name = ctk.CTkLabel(
            self.profile_frame, text=self.current_username.capitalize(),
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color="#FFFFFF"
        )
        self.profile_name.pack(anchor="w")
        
        self.profile_role = ctk.CTkLabel(
            self.profile_frame, text="Software Engineer",
            font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#9CA3AF"
        )
        self.profile_role.pack(anchor="w")

        self.nav_title = ctk.CTkLabel(
            self.sidebar_frame, text="NAVIGATION",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#4B5563"
        )
        self.nav_title.grid(row=2, column=0, padx=25, pady=(10, 5), sticky="w")

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="  Dashboard", fg_color="#1E293B", text_color="#3B82F6",
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

        self.dashboard_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)
        self.session_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)
        self.analytics_view = ctk.CTkFrame(self, fg_color="#0B0F19", corner_radius=0)

    def setup_dashboard_content(self):
        formatted_date = datetime.now().strftime("%A · %B %d, %Y").upper()
        
        self.date_lbl = ctk.CTkLabel(self.dashboard_view, text=formatted_date, font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563")
        self.date_lbl.pack(padx=40, pady=(40, 0), anchor="w")

        self.welcome_lbl = ctk.CTkLabel(self.dashboard_view, text=f"Welcome back, {self.current_username.capitalize()}.", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color="white")
        self.welcome_lbl.pack(padx=40, pady=(5, 0), anchor="w")

        self.motivate_lbl = ctk.CTkLabel(self.dashboard_view, text="You're on a roll — don't break the streak today.", font=ctk.CTkFont(size=14), text_color="#9CA3AF")
        self.motivate_lbl.pack(padx=40, pady=(5, 25), anchor="w")

        self.metrics_container = ctk.CTkFrame(self.dashboard_view, fg_color="transparent")
        self.metrics_container.pack(padx=40, pady=10, fill="x", anchor="w")
        self.metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        card1 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card1.grid(row=0, column=0, padx=8, pady=0, sticky="nsew")
        card1.grid_propagate(False)
        self.streak_val = ctk.CTkLabel(card1, text="🔥 0", font=ctk.CTkFont(size=36, weight="bold"), text_color="#F59E0B")
        self.streak_val.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        ctk.CTkLabel(card1, text="Day Streak", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").grid(row=1, column=0, padx=20, pady=0, sticky="w")

        card2 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card2.grid(row=0, column=1, padx=8, pady=0, sticky="nsew")
        card2.grid_propagate(False)
        ctk.CTkLabel(card2, text="Questions Answered", font=ctk.CTkFont(size=12), text_color="#9CA3AF").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.questions_val = ctk.CTkLabel(card2, text="0", font=ctk.CTkFont(size=36, weight="bold"), text_color="white")
        self.questions_val.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        card3 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card3.grid(row=0, column=2, padx=8, pady=0, sticky="nsew")
        card3.grid_propagate(False)
        ctk.CTkLabel(card3, text="Average Score", font=ctk.CTkFont(size=12), text_color="#9CA3AF").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.avg_score_val = ctk.CTkLabel(card3, text="0.0", font=ctk.CTkFont(size=36, weight="bold"), text_color="white")
        self.avg_score_val.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        card4 = ctk.CTkFrame(self.metrics_container, fg_color="#161F30", height=160, corner_radius=12)
        card4.grid(row=0, column=3, padx=8, pady=0, sticky="nsew")
        card4.grid_propagate(False)
        ctk.CTkLabel(card4, text="Sessions Completed", font=ctk.CTkFont(size=12), text_color="#9CA3AF").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.sessions_val = ctk.CTkLabel(card4, text="0", font=ctk.CTkFont(size=36, weight="bold"), text_color="white")
        self.sessions_val.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        self.challenge_card = ctk.CTkFrame(self.dashboard_view, fg_color="#0F1E36", border_color="#1E3A8A", border_width=1, corner_radius=16)
        self.challenge_card.pack(padx=40, pady=30, fill="x")
        self.challenge_card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.challenge_card, text="● TODAY'S CHALLENGE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#3B82F6").grid(row=0, column=0, padx=30, pady=(25, 0), sticky="w")
        ctk.CTkLabel(self.challenge_card, text="Behavioral Questions\n— STAR Method Focus", font=ctk.CTkFont(size=24, weight="bold"), text_color="white", justify="left").grid(row=1, column=0, padx=30, pady=(5, 0), sticky="w")
        ctk.CTkLabel(self.challenge_card, text="5 questions · 15 minutes · Estimated score boost: +0.6 pts", font=ctk.CTkFont(size=13), text_color="#9CA3AF").grid(row=2, column=0, padx=30, pady=(10, 25), sticky="w")

        self.start_btn = ctk.CTkButton(
            self.challenge_card, text="Start Session   →", fg_color="#2563EB", hover_color="#1D4ED8",
            font=ctk.CTkFont(size=15, weight="bold"), corner_radius=8, width=160, height=45,
            command=self.show_session
        )
        self.start_btn.grid(row=1, column=1, padx=40, sticky="e")

    def refresh_dashboard_metrics(self):
        questions, sessions, streak = self.db.get_user_stats(self.current_user_id)
        avg_score = self.db.get_average_score(self.current_user_id)
        
        self.streak_val.configure(text=f"🔥 {streak}")
        self.questions_val.configure(text=str(questions))
        self.sessions_val.configure(text=str(sessions))
        self.avg_score_val.configure(text=str(avg_score))

    def setup_session_interface(self):
        self.session_header_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.session_header_frame.pack(padx=40, pady=(20, 10), fill="x")
        
        ctk.CTkLabel(self.session_header_frame, text="BEHAVIORAL VIDEO SESSION", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4B5563").pack(side="left")
        
        self.interview_split_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.interview_split_frame.pack(padx=40, pady=10, fill="both", expand=True)
        self.interview_split_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")
        self.interview_split_frame.grid_rowconfigure(0, weight=1)

        self.ai_card = ctk.CTkFrame(self.interview_split_frame, fg_color="#161F30", corner_radius=16)
        self.ai_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(self.ai_card, text="🤖 AI Interviewer", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(pady=(20, 10))
        
        self.question_text = ctk.CTkLabel(
            self.ai_card, 
            text="Click 'Start Session' to begin...",
            font=ctk.CTkFont(size=15), text_color="white", justify="center", wraplength=350
        )
        self.question_text.pack(pady=20, padx=20, expand=True)

        self.btn_speak_question = ctk.CTkButton(
            self.ai_card, text="🔊 Repeat Question", fg_color="#374151", hover_color="#4B5563",
            command=self.play_ai_voice
        )
        self.btn_speak_question.pack(pady=(0, 20))

        self.video_card = ctk.CTkFrame(self.interview_split_frame, fg_color="#0F172A", corner_radius=16)
        self.video_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        self.webcam_label = ctk.CTkLabel(self.video_card, text="Camera Feed Inactive")
        self.webcam_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.controls_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.controls_frame.pack(padx=40, pady=10, fill="x")

        self.text_response_box = ctk.CTkTextbox(self.controls_frame, fg_color="#111827", height=80, corner_radius=12, font=ctk.CTkFont(size=13), text_color="white")
        self.text_response_box.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_record = ctk.CTkButton(
            self.controls_frame, text="🎙️ Record Answer", fg_color="#DC2626", hover_color="#B91C1C",
            width=140, height=80, font=ctk.CTkFont(weight="bold"),
            command=self.start_voice_recording
        )
        self.btn_record.pack(side="right")

        self.footer_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.footer_frame.pack(padx=40, pady=(5, 20), fill="x")
        
        self.btn_submit = ctk.CTkButton(
            self.footer_frame, text="Submit Answer   →", fg_color="#2563EB", hover_color="#1D4ED8",
            font=ctk.CTkFont(size=14, weight="bold"), height=40, command=self.handle_submit
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

        card_overall = ctk.CTkFrame(self.analytics_cards_frame, fg_color="#161F30", height=120, corner_radius=12)
        card_overall.grid(row=0, column=0, padx=6, sticky="nsew")
        card_overall.grid_propagate(False)
        ctk.CTkLabel(card_overall, text="AVERAGE SCORE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#9CA3AF").pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_overall = ctk.CTkLabel(card_overall, text="0.0 / 10", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3B82F6")
        self.lbl_analytics_overall.pack(anchor="w", padx=16)

        card_sessions = ctk.CTkFrame(self.analytics_cards_frame, fg_color="#161F30", height=120, corner_radius=12)
        card_sessions.grid(row=0, column=1, padx=6, sticky="nsew")
        card_sessions.grid_propagate(False)
        ctk.CTkLabel(card_sessions, text="TOTAL SESSIONS", font=ctk.CTkFont(size=11, weight="bold"), text_color="#9CA3AF").pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_sessions = ctk.CTkLabel(card_sessions, text="0", font=ctk.CTkFont(size=28, weight="bold"), text_color="#10B981")
        self.lbl_analytics_sessions.pack(anchor="w", padx=16)

        card_streak = ctk.CTkFrame(self.analytics_cards_frame, fg_color="#161F30", height=120, corner_radius=12)
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

        self.history_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="#161F30", corner_radius=12)
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
        self.btn_dashboard.configure(fg_color="#1E293B", text_color="#3B82F6")
        self.btn_session.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_analytics.configure(fg_color="transparent", text_color="#9CA3AF")

    def show_analytics(self):
        self.stop_webcam()
        self.clear_views()
        self.refresh_analytics_data()
        self.analytics_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_session.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_analytics.configure(fg_color="#1E293B", text_color="#3B82F6")


    # ==========================================================
    # STEP 4: HOOKING UP AI ENGINE & VOICE TO SESSION VIEW
    # ==========================================================

    def show_session(self):
        """Switches to session view, starts camera, and fetches a new AI question."""
        self.clear_views()
        self.session_view.grid(row=0, column=1, sticky="nsew")
        
        # Update Nav Active State
        self.btn_dashboard.configure(fg_color="transparent", text_color="#9CA3AF")
        self.btn_session.configure(fg_color="#1E293B", text_color="#3B82F6")
        self.btn_analytics.configure(fg_color="transparent", text_color="#9CA3AF")
        
        # 1. Start Webcam Feed
        self.start_webcam()
        
        # 2. Reset UI State
        self.question_text.configure(text=" Fetching your AI question...")
        self.text_response_box.delete("1.0", "end")
        self.btn_submit.configure(state="disabled", text="Submit Answer   →")
        
        # 3. Fetch Question asynchronously off main thread
        def fetch_question_worker():
            question = self.ai.generate_question("Behavioral")
            self.current_question = question
            
            # Update UI on Main Thread
            self.after(0, lambda: self._on_question_loaded(question))

        threading.Thread(target=fetch_question_worker, daemon=True).start()

    def _on_question_loaded(self, question):
        """UI Callback once the question fetch completes."""
        self.question_text.configure(text=question)
        self.btn_submit.configure(state="normal", text="Submit Answer   →")
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

        # Disable submit button to prevent double submissions
        self.btn_submit.configure(state="disabled", text=" Analyzing with AI...")

        def process_submission_worker():
            try:
                # 1. Send response to AI Engine for structured scoring
                analysis = self.ai.analyze_response(self.current_question, user_answer)
                
                overall_score = analysis.get("overall_score", 7.0)
                feedback_json = json.dumps(analysis)
                
                # 2. Persist to DB
                self.db.save_interview_session(
                    user_id=self.current_user_id,
                    topic="Behavioral",
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
            self.cap = cv2.VideoCapture(0)
        self.update_webcam_feed()

    def update_webcam_feed(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                self.webcam_image = ctk.CTkImage(light_image=img, dark_image=img, size=(380, 240))
                
                self.webcam_label.configure(image=self.webcam_image, text="")
                self.webcam_label.after(15, self.update_webcam_feed)

    def stop_webcam(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None


if __name__ == "__main__":
    app = IntervAIApp()
    app.mainloop()