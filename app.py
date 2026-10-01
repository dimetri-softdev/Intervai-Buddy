import threading
import json
from datetime import datetime
from ui.auth_view import AuthView
from ui.constants import INTERVIEW_LANGUAGES, INTERVIEW_TYPES
from ui.main_window import IntervAIApp


if __name__ == "__main__":
    app = IntervAIApp()
    app.mainloop()