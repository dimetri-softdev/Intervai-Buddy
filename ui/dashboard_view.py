from datetime import datetime

import customtkinter as ctk

from ui.theme import THEME


class DashboardViewMixin:
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

    def refresh_dashboard_metrics(self):
        questions, sessions, streak = self.db.get_user_stats(self.current_user_id)
        avg_score = self.db.get_average_score(self.current_user_id)

        self.streak_val.configure(text=str(streak))
        self.questions_val.configure(text=str(questions))
        self.sessions_val.configure(text=str(sessions))
        self.avg_score_val.configure(text=str(avg_score))

    def show_dashboard(self):
        self.stop_webcam()
        self.clear_views()
        self.refresh_dashboard_metrics()
        self.dashboard_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color=THEME["surface_2"], text_color=THEME["primary_2"])
        self.btn_session.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_analytics.configure(fg_color="transparent", text_color=THEME["text_soft"])
