import json
import threading

import cv2
import customtkinter as ctk
from PIL import Image

from ui.theme import THEME


class SessionControllerMixin:
    def show_session(self):
        """Open interview setup so the user can select a type and start."""
        self.stop_webcam()
        self.clear_views()
        self.session_view.grid(row=0, column=1, sticky="nsew")
        self.btn_dashboard.configure(fg_color="transparent", text_color=THEME["text_soft"])
        self.btn_session.configure(fg_color=THEME["surface_2"], text_color=THEME["primary_2"])
        self.btn_analytics.configure(fg_color="transparent", text_color=THEME["text_soft"])

        self.session_request_id += 1
        self.current_question = ""
        self.interview_type_menu.configure(state="normal")
        self.language_menu.configure(state="normal")
        self.on_interview_type_changed(self.interview_type_menu.get())
        self.btn_start_session.configure(state="normal", text="Start Session")
        self.btn_speak_question.configure(state="disabled")
        self.btn_record.configure(state="disabled", text="🎙️ Record Answer")
        self.question_text.configure(text="Choose an interview type, then press Start Session.")
        self.text_response_box.delete("1.0", "end")
        self.btn_submit.configure(state="disabled", text="Submit Answer   →")

    def start_interview_session(self):
        """Start the camera and request a question for the chosen interview type."""
        if self.btn_start_session.cget("state") == "disabled":
            return

        self.current_interview_type = self.interview_type_menu.get()
        self.current_language = (
            self.language_menu.get()
            if self.current_interview_type == "Coding"
            else None
        )
        self.session_request_id += 1
        request_id = self.session_request_id
        self.current_question = ""
        self.btn_start_session.configure(state="disabled", text="Starting...")
        self.interview_type_menu.configure(state="disabled")
        self.language_menu.configure(state="disabled")
        self.btn_speak_question.configure(state="disabled")
        self.btn_record.configure(state="disabled")
        self.btn_submit.configure(state="disabled", text="Submit Answer   →")
        self.text_response_box.delete("1.0", "end")
        self.question_text.configure(
            text=(
                f"Preparing your {self.current_language} coding challenge..."
                if self.current_interview_type == "Coding"
                else f"Preparing your {self.current_interview_type.lower()} interview question..."
            )
        )
        self.start_webcam()

        def fetch_question_worker():
            question = self.ai.generate_question(
                self.current_interview_type, self.current_language
            )
            self.after(0, lambda: self._on_question_loaded(question, request_id))

        threading.Thread(target=fetch_question_worker, daemon=True).start()

    def _on_question_loaded(self, question, request_id):
        """Update the session controls after question generation completes."""
        if request_id != self.session_request_id:
            return

        self.current_question = question
        self.question_text.configure(text=question)
        self.btn_submit.configure(state="normal", text="Submit Answer   →")
        self.btn_speak_question.configure(state="normal")
        if self.current_interview_type != "Coding":
            self.btn_record.configure(state="normal", text="🎙️ Record Answer")
        self.btn_start_session.configure(text="Session Started")
        if self.current_interview_type != "Coding":
            self.play_ai_voice()

    def play_ai_voice(self):
        """Speak the current question on demand or for voice interview types."""
        text = self.current_question
        if text and not text.startswith(" Fetching"):
            threading.Thread(target=lambda: self.voice.speak(text), daemon=True).start()

    def start_voice_recording(self):
        """Transcribe a spoken answer into the response editor."""
        self.btn_record.configure(state="disabled", text=" Listening...", fg_color="#D97706")

        def record_worker():
            transcript = self.voice.listen_and_transcribe()
            self.after(0, lambda: self.on_transcription_complete(transcript))

        threading.Thread(target=record_worker, daemon=True).start()

    def on_transcription_complete(self, transcript):
        self.text_response_box.delete("1.0", "end")
        if transcript:
            self.text_response_box.insert("1.0", transcript)
        else:
            self.text_response_box.insert("1.0", "Could not capture audio. Please type response.")
        self.btn_record.configure(state="normal", text="🎙️ Record Answer", fg_color="#DC2626")

    def handle_submit(self):
        """Evaluate the response, save the session, and open analytics."""
        user_answer = self.text_response_box.get("1.0", "end-1c").strip()
        if not user_answer or not self.current_question or self.current_question.startswith(" Fetching"):
            return

        question = self.current_question
        interview_type = self.current_interview_type
        language = self.current_language
        self.btn_submit.configure(state="disabled", text=" Analyzing with AI...")

        def process_submission_worker():
            try:
                analysis = self.ai.analyze_response(
                    question, user_answer, interview_type, language
                )
                overall_score = analysis.get("overall_score", 7.0)
                feedback_json = json.dumps(analysis)
                self.db.save_interview_session(
                    user_id=self.current_user_id,
                    topic=interview_type,
                    score=overall_score,
                    feedback=feedback_json,
                )
                self.after(0, self.show_analytics)
            except Exception as err:
                print(f"[Error] Failed to process AI submission: {err}")
                self.after(
                    0,
                    lambda: self.btn_submit.configure(
                        state="normal", text="Submit Answer   →"
                    ),
                )

        threading.Thread(target=process_submission_worker, daemon=True).start()

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
