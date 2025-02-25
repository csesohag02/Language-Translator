import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import io
import pygame

class LanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self.translator = Translator()
        pygame.mixer.init()
        
        # Format languages with first letter uppercase and short form
        self.language_options = [f"{val.title()} ({key})" for key, val in LANGUAGES.items()]
        
        # Title Label
        ttk.Label(root, text="Language Translator", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Input Text
        self.input_text = tk.Text(root, height=5, width=50)
        self.input_text.pack(pady=5)
        
        # Language Selection Frame
        lang_frame = tk.Frame(root)
        lang_frame.pack(pady=5)
        
        # Source Language Label and Dropdown
        ttk.Label(lang_frame, text="From").grid(row=0, column=0, padx=5, pady=2)
        self.source_lang = ttk.Combobox(lang_frame, values=self.language_options, state="normal")
        self.source_lang.set("English (en)")
        self.source_lang.grid(row=1, column=0, padx=5, pady=2)
        self.source_lang.bind("<KeyRelease>", self.filter_languages)
        
        # Swap Button
        self.swap_button = ttk.Button(lang_frame, text="⇄", command=self.swap_languages)
        self.swap_button.grid(row=1, column=1, padx=5, pady=2)
        
        # Target Language Label and Dropdown
        ttk.Label(lang_frame, text="To").grid(row=0, column=2, padx=5, pady=2)
        self.target_lang = ttk.Combobox(lang_frame, values=self.language_options, state="normal")
        self.target_lang.set("Bengali (bn)")
        self.target_lang.grid(row=1, column=2, padx=5, pady=2)
        self.target_lang.bind("<KeyRelease>", self.filter_languages)
        
        # Translate Button
        ttk.Button(root, text="Translate", command=self.translate_text).pack(pady=5)
        
        # Output Text
        self.output_text = tk.Text(root, height=5, width=50, state="disabled")
        self.output_text.pack(pady=5)
        
        # Copy & TTS Buttons Frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="Copy Text", command=self.copy_text).pack(side="left", padx=50)
        ttk.Button(button_frame, text="Speak", command=self.speak_text).pack(side="right", padx=50)
        
        # Exit Button
        ttk.Button(root, text="Exit", command=self.root.destroy).pack(pady=5)
    
    def swap_languages(self):
        src = self.source_lang.get()
        dest = self.target_lang.get()
        self.source_lang.set(dest)
        self.target_lang.set(src)
    
    def filter_languages(self, event):
        widget = event.widget
        search_text = widget.get().lower()
        filtered_languages = [lang for lang in self.language_options if lang.lower().startswith(search_text)]
        widget["values"] = filtered_languages

    def translate_text(self):
        try:
            text = self.input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter text to translate.")
                return
            
            # Extract language codes from selected values
            src_lang = self.source_lang.get().split(" (")[1][:-1]
            dest_lang = self.target_lang.get().split(" (")[1][:-1]
            
            translated_text = self.translator.translate(text, src=src_lang, dest=dest_lang).text
            
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated_text)
            self.output_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {str(e)}")
    
    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get("1.0", tk.END))
        self.root.update()
        messagebox.showinfo("Copied", "Translated text copied to clipboard!")
    
    def speak_text(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            try:
                # Extract target language code
                dest_lang = self.target_lang.get().split(" (")[1][:-1]
                
                # Generate speech in memory
                tts = gTTS(text=text, lang=dest_lang)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                
                # Play audio using pygame
                pygame.mixer.music.load(audio_fp, 'mp3')
                pygame.mixer.music.play()
            except Exception as e:
                messagebox.showerror("Error", f"Speech synthesis failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No text to speak.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()