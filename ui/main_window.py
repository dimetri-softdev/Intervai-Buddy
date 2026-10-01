import customtkinter as ctk

from ai_engine import AIEngine
from database import DatabaseManager
from ui.analytics_view import AnalyticsViewMixin
from ui.auth_view import AuthView
from ui.dashboard_view import DashboardViewMixin
from ui.session_controller import SessionControllerMixin
from ui.session_view import SessionViewMixin
from ui.theme import THEME
from voice_engine import VoiceEngine

ctk.set_appearance_mode("Dark")


class IntervAIApp(
    DashboardViewMixin,
    AnalyticsViewMixin,
    SessionViewMixin,
    SessionControllerMixin,
    ctk.CTk,
):
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
        self.current_language = None
        self.session_request_id = 0
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
        self.sidebar_frame = ctk.CTkFrame(
            self, width=240, corner_radius=0, fg_color=THEME["sidebar"]
        )
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
            fg_color=THEME["primary"],
            corner_radius=8,
            text_color="white",
        )
        self.logo_icon.pack(side="left")
        self.logo_label = ctk.CTkLabel(
            self.logo_container,
            text="IntervAI",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=THEME["text"],
        )
        self.logo_label.pack(side="left", padx=(12, 0))

        ctk.CTkLabel(
            self.sidebar_frame,
            text="INTERVIEW COACH",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=THEME["muted"],
        ).grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        self.profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.profile_frame.grid(row=2, column=0, padx=20, pady=(0, 18), sticky="ew")
        self.profile_avatar = ctk.CTkLabel(
            self.profile_frame,
            text=self.current_username[0].upper() if self.current_username else "L",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=28,
            height=28,
            fg_color=THEME["purple"],
            corner_radius=14,
            text_color="white",
        )
        self.profile_avatar.pack(side="left")
        self.profile_details = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        self.profile_details.pack(side="left", padx=(12, 0), anchor="w")
        self.profile_name = ctk.CTkLabel(
            self.profile_details,
            text=self.current_username.capitalize() if self.current_username else "Latifah Osei",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=THEME["text"],
        )
        self.profile_name.pack(anchor="w")
        self.profile_role = ctk.CTkLabel(
            self.profile_details,
            text="Software Engineer",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=THEME["muted"],
        )
        self.profile_role.pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            self.sidebar_frame,
            text="NAVIGATION",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=THEME["muted"],
        ).grid(row=3, column=0, padx=24, pady=(8, 8), sticky="w")

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame,
            text="  Dashboard",
            fg_color=THEME["surface_2"],
            text_color=THEME["primary_2"],
            hover_color=THEME["surface_2"],
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=self.show_dashboard,
            height=40,
            corner_radius=8,
        )
        self.btn_dashboard.grid(row=4, column=0, padx=15, pady=3, sticky="ew")
        self.btn_session = ctk.CTkButton(
            self.sidebar_frame,
            text="🎙️  Daily Session",
            fg_color="transparent",
            text_color=THEME["text_soft"],
            hover_color=THEME["surface_2"],
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=self.show_session,
            height=40,
            corner_radius=8,
        )
        self.btn_session.grid(row=5, column=0, padx=15, pady=3, sticky="ew")
        self.btn_analytics = ctk.CTkButton(
            self.sidebar_frame,
            text="📊  Analytics",
            fg_color="transparent",
            text_color=THEME["text_soft"],
            hover_color=THEME["surface_2"],
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=self.show_analytics,
            height=40,
            corner_radius=8,
        )
        self.btn_analytics.grid(row=6, column=0, padx=15, pady=3, sticky="ew")

        self.dashboard_view = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)
        self.session_view = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)
        self.analytics_view = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)

    def clear_views(self):
        self.dashboard_view.grid_forget()
        self.session_view.grid_forget()
        self.analytics_view.grid_forget()
