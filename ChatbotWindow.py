import customtkinter
import google.generativeai as genai
import threading

class ChatbotWindow:
    def __init__(self):
        self.window = None
        self.api_key = "nope :D"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def show(self):
        self.window = customtkinter.CTkToplevel()
        self.window.title("Hospital Chatbot")
        self.window.geometry("700x500")

        self.textbox = customtkinter.CTkTextbox(self.window, height=300, width=650)
        self.textbox.configure(state="disabled")
        self.textbox.pack(pady=10)

        self.entry = customtkinter.CTkEntry(self.window, width=500)
        self.entry.pack(pady=5)

        self.ask_button = customtkinter.CTkButton(
            self.window, text="Ask", command=self.ask_question_threaded
        )
        self.ask_button.pack(pady=5)

    def ask_question_threaded(self):
        threading.Thread(target=self.ask_question).start()

    def ask_question(self):
        question = self.entry.get()
        self.window.after(0, lambda: self.insert_text(f"You: {question}\n"))
        self.window.after(0, lambda: self.insert_text("Bot: (loading...)\n"))
        self.entry.delete(0, 'end')

        try:
            response = self.model.generate_content(question)
            answer = response.text.strip()
        except Exception as e:
            answer = f"[Error] {str(e)}"

        def update_ui():
            self.textbox.configure(state="normal")
            lines = self.textbox.get("1.0", "end").splitlines()
            if lines and lines[-1] == "Bot: (loading...)":
                self.textbox.delete("end-2l", "end")
            self.textbox.insert("end", f"Bot: {answer}\n\n")
            self.textbox.configure(state="disabled")

        self.window.after(0, update_ui)

    def insert_text(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text)
        self.textbox.configure(state="disabled")