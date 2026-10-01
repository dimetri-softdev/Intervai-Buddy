import customtkinter as ctk

from ui.constants import INTERVIEW_LANGUAGES, INTERVIEW_TYPES
from ui.theme import THEME


class SessionViewMixin:
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
            command=self.on_interview_type_changed,
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

        self.ai_card = ctk.CTkFrame(
            self.interview_split_frame,
            fg_color=THEME["card"],
            corner_radius=12,
            border_width=1,
            border_color=THEME["border"],
        )
        self.ai_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(
            self.ai_card,
            text="🤖 AI Interviewer",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
        ).pack(pady=(20, 10))

        self.question_text = ctk.CTkLabel(
            self.ai_card,
            text="Choose an interview type, then press Start Session.",
            font=ctk.CTkFont(size=15),
            text_color="white",
            justify="center",
            wraplength=350,
        )
        self.question_text.pack(pady=20, padx=20, expand=True)

        self.btn_speak_question = ctk.CTkButton(
            self.ai_card,
            text="🔊 Repeat Question",
            fg_color="#374151",
            hover_color="#4B5563",
            command=self.play_ai_voice,
            state="disabled",
        )
        self.btn_speak_question.pack(pady=(0, 20))

        self.video_card = ctk.CTkFrame(
            self.interview_split_frame,
            fg_color="#080F1C",
            corner_radius=12,
            border_width=1,
            border_color=THEME["border"],
        )
        self.video_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        self.webcam_label = ctk.CTkLabel(self.video_card, text="Camera Feed Inactive")
        self.webcam_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.controls_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.controls_frame.pack(padx=32, pady=8, fill="x")
        self.response_header = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.response_header.pack(fill="x", pady=(0, 6))
        self.response_mode_label = ctk.CTkLabel(
            self.response_header,
            text="YOUR RESPONSE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["muted"],
        )
        self.response_mode_label.pack(side="left")
        self.response_hint_label = ctk.CTkLabel(
            self.response_header,
            text="Type or record your answer",
            font=ctk.CTkFont(size=10),
            text_color=THEME["muted"],
        )
        self.response_hint_label.pack(side="left", padx=(10, 0))

        self.language_selector = ctk.CTkFrame(self.response_header, fg_color="transparent")
        ctk.CTkLabel(
            self.language_selector,
            text="LANGUAGE",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=THEME["muted"],
        ).pack(side="left", padx=(0, 8))
        self.language_menu = ctk.CTkOptionMenu(
            self.language_selector,
            values=list(INTERVIEW_LANGUAGES),
            fg_color=THEME["surface_2"],
            button_color=THEME["primary"],
            button_hover_color="#2E6DD0",
            dropdown_fg_color=THEME["panel"],
            text_color=THEME["text"],
            width=130,
            height=30,
        )
        self.language_menu.set("Python")
        self.language_menu.pack(side="left")

        self.response_input_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.response_input_frame.pack(fill="x")
        self.text_response_box = ctk.CTkTextbox(
            self.response_input_frame,
            fg_color=THEME["bg_2"],
            height=80,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=THEME["text"],
            border_width=1,
            border_color=THEME["border"],
        )
        self.text_response_box.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_record = ctk.CTkButton(
            self.response_input_frame,
            text="🎙️ Record Answer",
            fg_color="#DC2626",
            hover_color="#B91C1C",
            width=140,
            height=80,
            font=ctk.CTkFont(weight="bold"),
            command=self.start_voice_recording,
            state="disabled",
        )
        self.btn_record.pack(side="right")
        self.on_interview_type_changed(self.current_interview_type)

        self.footer_frame = ctk.CTkFrame(self.session_view, fg_color="transparent")
        self.footer_frame.pack(padx=32, pady=(5, 20), fill="x")
        self.btn_submit = ctk.CTkButton(
            self.footer_frame,
            text="Submit Answer   →",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.handle_submit,
            state="disabled",
        )
        self.btn_submit.pack(side="right")

    def on_interview_type_changed(self, interview_type):
        self.current_interview_type = interview_type
        is_coding = interview_type == "Coding"
        self.response_mode_label.configure(
            text="YOUR CODE" if is_coding else "YOUR RESPONSE"
        )
        self.response_hint_label.configure(
            text=(
                "Reviewed for correctness, edge cases, and complexity"
                if is_coding
                else "Type or record your answer"
            )
        )
        if is_coding:
            self.language_selector.pack(side="right")
            self.text_response_box.configure(
                font=ctk.CTkFont(family="Consolas", size=13),
                height=220,
            )
            self.btn_record.pack_forget()
        else:
            self.language_selector.pack_forget()
            self.text_response_box.configure(
                font=ctk.CTkFont(family="Segoe UI", size=13),
                height=80,
            )
            if not self.btn_record.winfo_manager():
                self.btn_record.pack(side="right")
