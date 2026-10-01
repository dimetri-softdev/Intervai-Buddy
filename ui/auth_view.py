import customtkinter as ctk

from ui.theme import THEME


class AuthView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_login_success):
        super().__init__(parent, fg_color=THEME["bg"], corner_radius=0)
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
                self.status_label.configure(
                    text="Invalid username or password.", text_color=THEME["red"]
                )
        else:
            success, message = self.db.register_user(username, password)
            if success:
                self.status_label.configure(
                    text="Account created! Switching...", text_color="#10B981"
                )
                self.after(1500, self.toggle_mode)
            else:
                self.status_label.configure(text=message, text_color=THEME["red"])
