"""
=====================================================================
TASK 1: LANGUAGE TRANSLATION TOOL
=====================================================================
CodeAlpha - Artificial Intelligence Internship

Description:
    A desktop GUI application that lets the user type text, choose a
    source & target language, and get an instant translation.
    Includes: Copy-to-clipboard button and Text-to-Speech (optional
    features mentioned in the task sheet).

How it works:
    1. User Interface        -> built with Tkinter (ttk widgets)
    2. Translation API       -> deep_translator's GoogleTranslator
                                 (wraps the free Google Translate
                                 endpoint, no API key required)
    3. Send text to API      -> GoogleTranslator(...).translate(text)
    4. Display translation   -> shown in a read-only text box
    5. Optional extras       -> Copy button (clipboard) +
                                 Text-to-Speech using pyttsx3

-------------------------------------------------------------------
INSTALLATION (run once):
    pip install deep-translator pyttsx3

RUN:
    python task1_language_translation_tool.py
-------------------------------------------------------------------
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ---- Translation backend -------------------------------------------------
try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

# ---- Optional Text-to-Speech ----------------------------------------------
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


# A representative subset of languages supported by Google Translate.
# (deep_translator.GoogleTranslator.get_supported_languages() can be used
#  to fetch the full live list if internet access is available.)
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Hindi": "hi",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Turkish": "tr",
    "Portuguese": "pt",
    "Italian": "it",
}


class TranslatorApp(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title("AI Language Translation Tool  |  CodeAlpha")
        self.geometry("640x520")
        self.minsize(560, 480)
        self.configure(bg="#f4f6fb")

        self.tts_engine = pyttsx3.init() if TTS_AVAILABLE else None

        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", background="#f4f6fb", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TCombobox", font=("Segoe UI", 10))

        header = ttk.Label(self, text="🌐 AI Language Translation Tool", style="Header.TLabel")
        header.pack(pady=(15, 5))

        # ---- language selectors ----
        lang_frame = ttk.Frame(self)
        lang_frame.pack(pady=5)

        ttk.Label(lang_frame, text="From:").grid(row=0, column=0, padx=5)
        self.src_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.keys()),
                                      state="readonly", width=20)
        self.src_lang.set("Auto Detect")
        self.src_lang.grid(row=0, column=1, padx=5)

        swap_btn = ttk.Button(lang_frame, text="⇄", width=3, command=self._swap_languages)
        swap_btn.grid(row=0, column=2, padx=5)

        ttk.Label(lang_frame, text="To:").grid(row=0, column=3, padx=5)
        self.tgt_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.keys()),
                                      state="readonly", width=20)
        self.tgt_lang.set("Urdu")
        self.tgt_lang.grid(row=0, column=4, padx=5)

        # ---- input box ----
        ttk.Label(self, text="Enter text:").pack(anchor="w", padx=20, pady=(15, 0))
        self.input_box = tk.Text(self, height=8, wrap="word", font=("Segoe UI", 11),
                                  relief="solid", borderwidth=1)
        self.input_box.pack(fill="x", padx=20, pady=5)

        # ---- action buttons ----
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)

        ttk.Button(btn_frame, text="Translate ▶", command=self.translate_text).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_all).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="📋 Copy Result", command=self.copy_result).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="🔊 Speak Result", command=self.speak_result).grid(row=0, column=3, padx=5)

        # ---- output box ----
        ttk.Label(self, text="Translation:").pack(anchor="w", padx=20, pady=(10, 0))
        self.output_box = tk.Text(self, height=8, wrap="word", font=("Segoe UI", 11),
                                   relief="solid", borderwidth=1, state="disabled",
                                   bg="#eef3ff")
        self.output_box.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        if not TRANSLATOR_AVAILABLE:
            messagebox.showwarning(
                "Missing dependency",
                "The 'deep_translator' package is not installed.\n\n"
                "Run:  pip install deep-translator\n\n"
                "The app will still open, but translation will not work "
                "until the package is installed."
            )

    # -------------------------------------------------------------- logic
    def _swap_languages(self):
        src, tgt = self.src_lang.get(), self.tgt_lang.get()
        if src == "Auto Detect":
            messagebox.showinfo("Can't swap", "Choose a specific source language first.")
            return
        self.src_lang.set(tgt)
        self.tgt_lang.set(src)

    def translate_text(self):
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Empty input", "Please type some text to translate.")
            return
        if not TRANSLATOR_AVAILABLE:
            messagebox.showerror("Missing dependency", "Install 'deep_translator' first:\n\npip install deep-translator")
            return

        src_code = LANGUAGES[self.src_lang.get()]
        tgt_code = LANGUAGES[self.tgt_lang.get()]

        try:
            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
        except Exception as exc:
            messagebox.showerror("Translation failed", f"Could not translate text.\n\nDetails: {exc}")
            return

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", translated)
        self.output_box.config(state="disabled")

    def clear_all(self):
        self.input_box.delete("1.0", "end")
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.config(state="disabled")

    def copy_result(self):
        result = self.output_box.get("1.0", "end").strip()
        if not result:
            messagebox.showinfo("Nothing to copy", "Translate some text first.")
            return
        self.clipboard_clear()
        self.clipboard_append(result)
        messagebox.showinfo("Copied", "Translation copied to clipboard!")

    def speak_result(self):
        result = self.output_box.get("1.0", "end").strip()
        if not result:
            messagebox.showinfo("Nothing to speak", "Translate some text first.")
            return
        if not TTS_AVAILABLE:
            messagebox.showerror("Missing dependency", "Install 'pyttsx3' first:\n\npip install pyttsx3")
            return
        self.tts_engine.say(result)
        self.tts_engine.runAndWait()


if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
