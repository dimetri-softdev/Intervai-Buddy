import json

import customtkinter as ctk

from ui.constants import INTERVIEW_TYPES
from ui.theme import THEME


class AnalyticsViewMixin:
    def setup_analytics_view(self):
        self.scroll_canvas = ctk.CTkScrollableFrame(self.analytics_view, fg_color="transparent")
        self.scroll_canvas.pack(fill="both", expand=True, padx=20, pady=20)

        self.completion_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.completion_frame.pack(fill="x", pady=(10, 5))
        self.review_lbl = ctk.CTkLabel(
            self.completion_frame,
            text="Performance Analytics",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="white",
        )
        self.review_lbl.pack(side="left")

        self.dash_btn = ctk.CTkButton(
            self.completion_frame,
            text="Dashboard",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            width=100,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.show_dashboard,
        )
        self.dash_btn.pack(side="right", padx=5)

        self.retry_btn = ctk.CTkButton(
            self.completion_frame,
            text="New Question",
            fg_color="transparent",
            border_color="#374151",
            border_width=1,
            text_color="white",
            hover_color="#1E293B",
            width=110,
            height=35,
            font=ctk.CTkFont(size=13),
            command=self.show_session,
        )
        self.retry_btn.pack(side="right", padx=5)

        self.analytics_cards_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.analytics_cards_frame.pack(fill="x", pady=(20, 25))
        self.analytics_cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        card_overall = ctk.CTkFrame(
            self.analytics_cards_frame,
            fg_color=THEME["card"],
            height=120,
            corner_radius=10,
            border_width=1,
            border_color=THEME["border"],
        )
        card_overall.grid(row=0, column=0, padx=6, sticky="nsew")
        card_overall.grid_propagate(False)
        ctk.CTkLabel(
            card_overall,
            text="AVERAGE SCORE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_overall = ctk.CTkLabel(
            card_overall,
            text="0.0 / 10",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3B82F6",
        )
        self.lbl_analytics_overall.pack(anchor="w", padx=16)

        card_sessions = ctk.CTkFrame(
            self.analytics_cards_frame,
            fg_color=THEME["card"],
            height=120,
            corner_radius=10,
            border_width=1,
            border_color=THEME["border"],
        )
        card_sessions.grid(row=0, column=1, padx=6, sticky="nsew")
        card_sessions.grid_propagate(False)
        ctk.CTkLabel(
            card_sessions,
            text="TOTAL SESSIONS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_sessions = ctk.CTkLabel(
            card_sessions,
            text="0",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#10B981",
        )
        self.lbl_analytics_sessions.pack(anchor="w", padx=16)

        card_streak = ctk.CTkFrame(
            self.analytics_cards_frame,
            fg_color=THEME["card"],
            height=120,
            corner_radius=10,
            border_width=1,
            border_color=THEME["border"],
        )
        card_streak.grid(row=0, column=2, padx=6, sticky="nsew")
        card_streak.grid_propagate(False)
        ctk.CTkLabel(
            card_streak,
            text="CURRENT STREAK",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=16, pady=(16, 4))
        self.lbl_analytics_streak = ctk.CTkLabel(
            card_streak,
            text="🔥 0 Days",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F59E0B",
        )
        self.lbl_analytics_streak.pack(anchor="w", padx=16)

        ctk.CTkLabel(
            self.scroll_canvas,
            text="Performance by Interview Type",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=THEME["text"],
        ).pack(anchor="w", pady=(2, 12))

        self.type_analytics_frame = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.type_analytics_frame.pack(fill="x", pady=(0, 22))
        self.type_analytics_frame.grid_columnconfigure(
            tuple(range(len(INTERVIEW_TYPES))), weight=1, uniform="type-analytics"
        )
        self.type_analytics_values = {}
        type_accents = {
            "Behavioral": THEME["purple"],
            "Technical": THEME["cyan"],
            "Coding": THEME["green"],
            "System Design": THEME["amber"],
        }
        for column, interview_type in enumerate(INTERVIEW_TYPES):
            type_card = ctk.CTkFrame(
                self.type_analytics_frame,
                fg_color=THEME["card"],
                height=118,
                corner_radius=9,
                border_width=1,
                border_color=THEME["border"],
            )
            type_card.grid(row=0, column=column, padx=5, sticky="nsew")
            type_card.grid_propagate(False)
            ctk.CTkLabel(
                type_card,
                text=interview_type.upper(),
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=type_accents[interview_type],
            ).pack(anchor="w", padx=13, pady=(13, 6))
            average_label = ctk.CTkLabel(
                type_card,
                text="0.0",
                font=ctk.CTkFont(family="Segoe UI", size=25, weight="bold"),
                text_color=THEME["text"],
            )
            average_label.pack(anchor="w", padx=13)
            sessions_label = ctk.CTkLabel(
                type_card,
                text="0 sessions",
                font=ctk.CTkFont(size=10),
                text_color=THEME["muted"],
            )
            sessions_label.pack(anchor="w", padx=13, pady=(0, 10))
            self.type_analytics_values[interview_type] = (average_label, sessions_label)

        ctk.CTkLabel(
            self.scroll_canvas,
            text="Recent Interview Sessions",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white",
        ).pack(anchor="w", pady=(10, 15))

        self.history_frame = ctk.CTkFrame(
            self.scroll_canvas,
            fg_color=THEME["card"],
            corner_radius=10,
            border_width=1,
            border_color=THEME["border"],
        )
        self.history_frame.pack(fill="x", pady=(0, 20))

    def refresh_analytics_data(self):
        data = self.db.get_user_analytics(self.current_user_id)
        self.lbl_analytics_overall.configure(text=f"{data['avg_overall']} / 10")
        self.lbl_analytics_sessions.configure(text=str(data["total_sessions"]))
        self.lbl_analytics_streak.configure(text=f"🔥 {data['current_streak']} Days")

        type_stats = self.db.get_interview_type_analytics(self.current_user_id)
        for interview_type, (average_label, sessions_label) in self.type_analytics_values.items():
            stats = type_stats.get(interview_type, {})
            average_label.configure(text=f"{stats.get('average_score', 0.0):.1f}")
            session_count = stats.get("sessions", 0)
            sessions_label.configure(
                text=f"{session_count} session{'s' if session_count != 1 else ''}"
            )

        for widget in self.history_frame.winfo_children():
            widget.destroy()

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
                text="No completed sessions yet. Start a session to build your history!",
                font=ctk.CTkFont(size=13),
                text_color="#9CA3AF",
            ).pack(pady=20)
            return

        for topic, score, session_date, ai_feedback_str in recent:
            card = ctk.CTkFrame(self.history_frame, fg_color="#0F172A", corner_radius=10)
            card.pack(fill="x", padx=16, pady=8)

            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.pack(fill="x", padx=14, pady=(12, 6))
            ctk.CTkLabel(
                header_row,
                text=topic or "Behavioral Session",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white",
            ).pack(side="left")

            score_val = score if score is not None else 0.0
            score_color = (
                "#10B981" if score_val >= 7.0 else "#F59E0B" if score_val >= 5.0 else "#EF4444"
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

            reason_text = "No explanation available."
            tips_text = "No improvement tips recorded."
            correctness = None
            correctness_feedback = ""
            time_complexity = ""
            space_complexity = ""
            if ai_feedback_str:
                try:
                    feedback_data = json.loads(ai_feedback_str)
                    reason_text = feedback_data.get("score_reason", reason_text)
                    tips_text = feedback_data.get("improvement_tips", tips_text)
                    correctness = feedback_data.get("is_correct")
                    correctness_feedback = feedback_data.get("correctness_feedback", "")
                    time_complexity = feedback_data.get("time_complexity", "")
                    space_complexity = feedback_data.get("space_complexity", "")
                except (TypeError, json.JSONDecodeError):
                    reason_text = ai_feedback_str

            if correctness_feedback:
                status_text = (
                    "Code review: Correct" if correctness is True
                    else "Code review: Issues found" if correctness is False
                    else "Code review: Unable to verify"
                )
                status_color = THEME["green"] if correctness is True else THEME["amber"]
                ctk.CTkLabel(
                    card,
                    text=f"{status_text}  |  {correctness_feedback}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=status_color,
                    wraplength=700,
                    justify="left",
                ).pack(anchor="w", padx=14, pady=(0, 6))
                if time_complexity or space_complexity:
                    ctk.CTkLabel(
                        card,
                        text=f"Time: {time_complexity or 'Unknown'}    Space: {space_complexity or 'Unknown'}",
                        font=ctk.CTkFont(size=11),
                        text_color=THEME["muted"],
                    ).pack(anchor="w", padx=14, pady=(0, 6))

            ctk.CTkLabel(
                card,
                text=f"💡 Why this score: {reason_text}",
                font=ctk.CTkFont(size=12),
                text_color="#CBD5E1",
                wraplength=700,
                justify="left",
            ).pack(anchor="w", padx=14, pady=(2, 4))
            ctk.CTkLabel(
                card,
                text=f"🚀 How to improve: {tips_text}",
                font=ctk.CTkFont(size=12),
                text_color="#60A5FA",
                wraplength=700,
                justify="left",
            ).pack(anchor="w", padx=14, pady=(0, 12))

    def show_analytics(self):
        self.stop_webcam()
        self.clear_views()
        self.refresh_analytics_data()
        self.analytics_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_session.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_analytics.configure(fg_color=THEME["surface_2"], text_color=THEME["primary_2"])
