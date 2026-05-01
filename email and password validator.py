import customtkinter as ctk
from tkinter import messagebox
import graphviz
import os
# Replace this path with where you installed Graphviz
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz\bin'
import string

#PASSWORD VALIDATION
MIN_LENGTH = 8
SPECIAL_CHARS = set(string.punctuation)
PASSWORD_ACCEPT_STATE = {'qLUSD'}
PASSWORD_TRAP_STATE = 'qR'
def get_password_symbol(char: str) -> str:
    if char.islower(): return 'l'
    if char.isupper(): return 'u'
    if char.isdigit(): return 'd'
    if char in SPECIAL_CHARS: return 's'
    return 'o'
PASSWORD_DFA_TABLE = {
    'q0': {'l': 'qL', 'u': 'qU', 'd': 'qD', 's': 'qS', 'o': 'qR'},
    'qL': {'l': 'qL', 'u': 'qLU', 'd': 'qLD', 's': 'qLS', 'o': 'qR'},
    'qU': {'l': 'qLU', 'u': 'qU', 'd': 'qUD', 's': 'qUS', 'o': 'qR'},
    'qD': {'l': 'qLD', 'u': 'qUD', 'd': 'qD', 's': 'qDS', 'o': 'qR'},
    'qS': {'l': 'qLS', 'u': 'qUS', 'd': 'qDS', 's': 'qS', 'o': 'qR'},
    'qLU': {'l': 'qLU', 'u': 'qLU', 'd': 'qLUD', 's': 'qLUS', 'o': 'qR'},
    'qLD': {'l': 'qLD', 'u': 'qLUD', 'd': 'qLD', 's': 'qLDS', 'o': 'qR'},
    'qLS': {'l': 'qLS', 'u': 'qLUS', 'd': 'qLDS', 's': 'qLS', 'o': 'qR'},
    'qUD': {'l': 'qLUD', 'u': 'qUD', 'd': 'qUD', 's': 'qUDS', 'o': 'qR'},
    'qUS': {'l': 'qLUS', 'u': 'qUS', 'd': 'qUDS', 's': 'qUS', 'o': 'qR'},
    'qDS': {'l': 'qLDS', 'u': 'qUDS', 'd': 'qDS', 's': 'qDS', 'o': 'qR'},
    'qLUD': {'l': 'qLUD', 'u': 'qLUD', 'd': 'qLUD', 's': 'qLUSD', 'o': 'qR'},
    'qLUS': {'l': 'qLUS', 'u': 'qLUS', 'd': 'qLUSD', 's': 'qLUS', 'o': 'qR'},
    'qLDS': {'l': 'qLDS', 'u': 'qLUSD', 'd': 'qLDS', 's': 'qLDS', 'o': 'qR'},
    'qUDS': {'l': 'qLUSD', 'u': 'qUDS', 'd': 'qUDS', 's': 'qUDS', 'o': 'qR'},
    'qLUSD': {'l': 'qLUSD', 'u': 'qLUSD', 'd': 'qLUSD', 's': 'qLUSD', 'o': 'qR'},
    'qR': {'l': 'qR', 'u': 'qR', 'd': 'qR', 's': 'qR', 'o': 'qR'}
}
def get_email_symbol(char: str) -> str:
    if char.isalpha(): 
        return 'A'   # Alphabets
    if char.isdigit() or char == '-': 
        return 'AL'  # Numbers or Dash (Alphanumeric for User part)
    if char == '@': return '@'
    if char == '.': return '.'
    return 'O'

EMAIL_DFA_TABLE = {
    # q0: Username accepts A or AL
    'q0':       {'A': 'qUser', 'AL': 'qUser', '@': 'qR', '.': 'qR', 'O': 'qR'},
    'qUser':    {'A': 'qUser', 'AL': 'qUser', '@': 'qAt', '.': 'qR', 'O': 'qR'},
    
    # qAt: After @, ONLY Alphabet 'A' is allowed for Domain
    'qAt':      {'A': 'qDomain', 'AL': 'qR', '@': 'qR', '.': 'qR', 'O': 'qR'},
    'qDomain':  {'A': 'qDomain', 'AL': 'qR', '@': 'qR', '.': 'qDot', 'O': 'qR'},
    
    # qDot: After dot, 'A' can be Subdomain or TLD (qFinal)
    'qDot':     {'A': 'qFinal', 'AL': 'qR', '@': 'qR', '.': 'qR', 'O': 'qR'}, 
    
    # qFinal (Accept State): If another dot comes, move back to check Subdomain
    'qFinal':   {'A': 'qFinal', 'AL': 'qR', '@': 'qR', '.': 'qDot', 'O': 'qR'},
    
    'qR':       {'A': 'qR', 'AL': 'qR', '@': 'qR', '.': 'qR', 'O': 'qR'}
}
EMAIL_ACCEPTING_STATES = {'qFinal'} 
EMAIL_TRAP_STATE = 'qR'
#DFA VISUALIZATION
def visualize_dfa_run(path: list, input_str: str, is_valid: bool, dfa_table: dict, accepting_states: set, trap_state: str, filename_prefix: str):
    try:
        dot = graphviz.Digraph(
            comment=f'Run: "{input_str}"', 
            graph_attr={'rankdir': 'LR'} 
        )
        all_states = set(dfa_table.keys())
        for state in all_states:
            shape = 'doublecircle' if state in accepting_states else 'circle'
            color = 'black'
            fillcolor = "#69ABDA" 
            if state == trap_state: fillcolor = '#FF0000' 
            elif state in accepting_states: fillcolor = "#8EDFB1" 
            dot.attr('node', shape=shape, style='filled', fillcolor=fillcolor, color=color)
            dot.node(state)
        for current_state, transitions in dfa_table.items():
            for symbol, next_state in transitions.items():
                dot.edge(current_state, next_state, label=symbol, color='#524646', fontcolor='#524646', penwidth='0.5')
        dot.attr('node', shape='none')
        dot.edge('__start', 'q0')
        for src, symbol, dest in path:
            dot.edge(src, dest, label=symbol, color='#FF5722', fontcolor='#FF5722', penwidth='2.5') 
            final_node_color = '#F7DC6F' 
            if dest == trap_state: final_node_color = '#E74C3C' 
            elif dest in accepting_states: final_node_color = '#2ECC71' 
            dot.attr('node', style='filled', fillcolor=final_node_color, color='black', penwidth='3.0')
            dot.node(dest)
        dot.attr('node', style='filled', fillcolor='#F7DC6F', color='black', penwidth='3.0')
        dot.node('q0')
        safe_input = input_str.replace(' ', '_').replace('@', '_at_').replace('.', '_dot_')
        output_filename = f'{filename_prefix}_{safe_input}'
        dot.render(output_filename, view=True, format='png', cleanup=True)
        return True, f"Visualization PNG file saved and opened: {output_filename}.png"
    except graphviz.backend.ExecutableNotFound:
        return False, "ERROR: Graphviz executable not found. Please install Graphviz."
    except Exception as e:
        return False, f"An error occurred during visualization: {e}"
    

#GUI
ACCENT_COLOR = "#387D43"     
HOVER_COLOR = "#4CAF50"      
BACK_BUTTON_COLOR = "#607D8B" 
RESET_BUTTON_COLOR = "#FF9800" 
MAIN_BG_COLOR = "#F0F0F0"     
class CustomDfaValidatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue") 
        self.title("DFA Validation System (TOA Project)") 
        APP_WIDTH = 900
        APP_HEIGHT = 700 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = (screen_width // 2) - (APP_WIDTH // 2)
        y_position = (screen_height // 2) - (APP_HEIGHT // 2)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x_position}+{y_position}")
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        self.main_content_frame = ctk.CTkFrame(self, fg_color=MAIN_BG_COLOR) 
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) 
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.current_screen = None
        self.show_selection_screen()
    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None
    def show_selection_screen(self):
        self.clear_screen()
        selection_frame = ctk.CTkFrame(self.main_content_frame, fg_color="white", corner_radius=15)
        selection_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        selection_frame.columnconfigure((0, 1), weight=1)
        self.current_screen = selection_frame
        ctk.CTkLabel(selection_frame, 
                     text="Email and Password Validation\nUsing Deterministic Finite Automata", 
                     font=ctk.CTkFont("Arial", 28, "bold"), text_color=ACCENT_COLOR, 
                     height=100).grid(row=0, column=0, columnspan=2, pady=(100, 100)) 
        ctk.CTkButton(selection_frame, text="Password Validator", 
                      command=lambda: self.show_validator_screen("password"),
                      font=ctk.CTkFont("Arial", 18, "bold"), 
                      fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR, 
                      corner_radius=10, width=250, height=60).grid(row=1, column=0, padx=30, pady=20)
        ctk.CTkButton(selection_frame, text="Email Validator", 
                      command=lambda: self.show_validator_screen("email"),
                      font=ctk.CTkFont("Arial", 18, "bold"), 
                      fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR, 
                      corner_radius=10, width=250, height=60).grid(row=1, column=1, padx=30, pady=20)
    def show_validator_screen(self, validator_type):
        self.clear_screen()
        validator_frame = ctk.CTkFrame(self.main_content_frame, fg_color="white", corner_radius=15)
        validator_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        validator_frame.columnconfigure(0, weight=1)
        self.current_screen = validator_frame
        if validator_type == "password":
            self.create_password_ui(validator_frame)
        else:
            self.create_email_ui(validator_frame)
    def create_password_ui(self, frame):
        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        top_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(top_frame, text="PASSWORD VALIDATOR", 
                     font=ctk.CTkFont("Arial", 20, "bold"), text_color="#333333").grid(row=0, column=0, sticky="w")
        ctk.CTkButton(top_frame, text="Back", command=self.show_selection_screen, 
                      fg_color=BACK_BUTTON_COLOR, hover_color="#455A64", corner_radius=6, width=100, height=35).grid(row=0, column=1, padx=(10, 5), sticky="e")
        ctk.CTkButton(top_frame, text="Reset", command=self.reset_password_screen, 
                      fg_color=RESET_BUTTON_COLOR, hover_color="#E67E22", corner_radius=6, width=100, height=35).grid(row=0, column=2, sticky="e")
        ctk.CTkLabel(frame, text=f"Min Length: {MIN_LENGTH} | Required: Lowercase, Uppercase, Digit, Special", 
                     font=("Arial", 12), text_color="#555555").grid(row=1, column=0, pady=(0, 10), sticky="ew", padx=20)
        input_frame = ctk.CTkFrame(frame, fg_color="#FFFFFF", corner_radius=10, border_width=2, border_color="#DDDDDD") 
        input_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew", padx=20)
        input_frame.columnconfigure(0, weight=1)
        self.password_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter password to verify...", 
                                           font=("Arial", 14), height=45, corner_radius=6, 
                                           fg_color=MAIN_BG_COLOR, text_color="#333333", border_width=0)
        self.password_entry.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.password_button = ctk.CTkButton(input_frame, text="VALIDATE", 
                                             command=self.validate_password, 
                                             font=ctk.CTkFont("Arial", 14, "bold"), 
                                             fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR, 
                                             corner_radius=6, width=120, height=45)
        self.password_button.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="e")
        result_frame = ctk.CTkFrame(frame, fg_color=MAIN_BG_COLOR, corner_radius=10)
        result_frame.grid(row=3, column=0, pady=10, sticky="ew", padx=20)
        self.password_result_label = ctk.CTkLabel(result_frame, text="RESULT: Awaiting Validation", 
                                                 font=("Arial", 16, "bold"), text_color="#333333", padx=10, pady=10)
        self.password_result_label.pack(fill="x")
        self.password_details_text = ctk.CTkTextbox(frame, height=200, corner_radius=10, 
                                                   fg_color="#FFFFFF", text_color="#333333", font=("Consolas", 10))
        self.password_details_text.grid(row=4, column=0, pady=(10, 20), sticky="nsew", padx=20)
        self.password_details_text.insert("0.0", "Details of State Transitions, Failure Reasons, and DFA PNG path will appear here...")
        self.password_details_text.configure(state="disabled")
        frame.grid_rowconfigure(4, weight=1)
    def create_email_ui(self, frame):
        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        top_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(top_frame, text="EMAIL VALIDATOR", 
                     font=ctk.CTkFont("Arial", 20, "bold"), text_color="#333333").grid(row=0, column=0, sticky="w")
        ctk.CTkButton(top_frame, text="Back", command=self.show_selection_screen, 
                      fg_color=BACK_BUTTON_COLOR, hover_color="#455A64", corner_radius=6, width=100, height=35).grid(row=0, column=1, padx=(10, 5), sticky="e")
        ctk.CTkButton(top_frame, text="Reset", command=self.reset_email_screen, 
                      fg_color=RESET_BUTTON_COLOR, hover_color="#E67E22", corner_radius=6, width=100, height=35).grid(row=0, column=2, sticky="e")
        ctk.CTkLabel(frame, text="DFA Syntax Check: LocalPart@Domain.TLD (Structure validation)", 
                     font=("Arial", 12), text_color="#555555").grid(row=1, column=0, pady=(0, 10), sticky="ew", padx=20)
        input_frame = ctk.CTkFrame(frame, fg_color="#FFFFFF", corner_radius=10, border_width=2, border_color="#DDDDDD")
        input_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew", padx=20)
        input_frame.columnconfigure(0, weight=1)
        self.email_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter email to verify...", 
                                        font=("Arial", 14), height=45, corner_radius=6,
                                        fg_color=MAIN_BG_COLOR, text_color="#333333", border_width=0)
        self.email_entry.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.email_button = ctk.CTkButton(input_frame, text="VALIDATE", 
                                          command=self.validate_email, 
                                          font=ctk.CTkFont("Arial", 14, "bold"), 
                                          fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR, 
                                          corner_radius=6, width=120, height=45)
        self.email_button.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="e")
        result_frame = ctk.CTkFrame(frame, fg_color=MAIN_BG_COLOR, corner_radius=10)
        result_frame.grid(row=3, column=0, pady=10, sticky="ew", padx=20)
        self.email_result_label = ctk.CTkLabel(result_frame, text="RESULT: Awaiting Validation", 
                                               font=("Arial", 16, "bold"), text_color="#333333", padx=10, pady=10)
        self.email_result_label.pack(fill="x")
        self.email_details_text = ctk.CTkTextbox(frame, height=200, corner_radius=10,
                                                fg_color="#FFFFFF", text_color="#333333", font=("Consolas", 10))
        self.email_details_text.grid(row=4, column=0, pady=(10, 20), sticky="nsew", padx=20)
        self.email_details_text.insert("0.0", "Details of State Transitions, Failure Reasons, and DFA PNG path will appear here...")
        self.email_details_text.configure(state="disabled")
        frame.grid_rowconfigure(4, weight=1)
    def _update_details(self, textbox, details_list):
        textbox.configure(state="normal")
        textbox.delete('1.0', "end")
        textbox.insert("0.0", "\n".join(details_list))
        textbox.configure(state="disabled")
    def reset_password_screen(self):
        self.password_entry.delete(0, "end")
        self._update_details(self.password_details_text, ["Details of State Transitions, Failure Reasons, and DFA PNG path will appear here..."])
        self.password_result_label.configure(text="RESULT: Awaiting Validation", text_color="#333333")
    def reset_email_screen(self):
        self.email_entry.delete(0, "end")
        self._update_details(self.email_details_text, ["Details of State Transitions, Failure Reasons, and DFA PNG path will appear here..."])
        self.email_result_label.configure(text="RESULT: Awaiting Validation", text_color="#333333")
    def validate_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Input Error", "Password field cannot be empty.")
            return
        current_state = 'q0'
        length = 0
        path = []
        for char in password:
            length += 1
            symbol = get_password_symbol(char)
            try: next_state = PASSWORD_DFA_TABLE[current_state][symbol]
            except KeyError: next_state = PASSWORD_TRAP_STATE
            path.append((current_state, symbol, next_state))
            current_state = next_state
            if current_state == PASSWORD_TRAP_STATE: break
        reached_acceptance_state = (current_state in PASSWORD_ACCEPT_STATE)
        met_length = (length >= MIN_LENGTH)
        is_valid = reached_acceptance_state and met_length
        result_color = '#008000' if is_valid else '#FF0000'
        result_text = f"ACCEPTED" if is_valid else f"REJECTED"
        self.password_result_label.configure(text=f"RESULT: {result_text} (Final State: {current_state})", text_color=result_color)
        details = [f"Input: {password}", f"DFA Final State: {current_state}", "-"*30]
        for src, symbol, dest in path: details.append(f"State: {src} -> Symbol: '{symbol}' -> Next: {dest}")
        details.append("-" * 30)
        details.append(f"LENGTH CHECK: {'PASS' if met_length else 'FAIL'} ({length} / {MIN_LENGTH} required)")
        if not is_valid:
            details.append("\n--- FAILURE REASONS ---")
            if current_state == PASSWORD_TRAP_STATE: details.append("  [CRITICAL] Invalid Character Detected (Symbol 'o').")
            if not met_length: details.append(f"  [LENGTH] Too short ({length} chars).")
            if current_state != PASSWORD_TRAP_STATE and not reached_acceptance_state:
                details.append("  [COMPLEXITY] Missing Categories: (Requires: l, u, d, s)")
        success, msg = visualize_dfa_run(path, password, is_valid, PASSWORD_DFA_TABLE, PASSWORD_ACCEPT_STATE, PASSWORD_TRAP_STATE, 'password_gui_run')
        details.append("-" * 30)
        details.append(msg)
        self._update_details(self.password_details_text, details)
        if not success:
            messagebox.showerror("Visualization Error", msg)
    def validate_email(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showwarning("Input Error", "Email field cannot be empty.")
            return
        current_state = 'q0'
        path = []
        for i, char in enumerate(email):
            symbol = get_email_symbol(char)
            try: next_state = EMAIL_DFA_TABLE[current_state][symbol]
            except KeyError: next_state = EMAIL_TRAP_STATE
            path.append((current_state, symbol, next_state))
            current_state = next_state
            if current_state == EMAIL_TRAP_STATE: break
        is_valid = (current_state in EMAIL_ACCEPTING_STATES)
        result_color = '#008000' if is_valid else '#FF0000'
        result_text = f"ACCEPTED" if is_valid else f"REJECTED"
        self.email_result_label.configure(text=f"RESULT: {result_text} (Final State: {current_state})", text_color=result_color)
        details = [f"Input: {email}", f"DFA Final State: {current_state}", "-"*30]
        for src, symbol, dest in path: details.append(f"State: {src} -> Symbol: '{symbol}' -> Next: {dest}")
        details.append("-" * 30)
        if not is_valid:
            details.append("\n--- FAILURE REASONS ---")
            if current_state == EMAIL_TRAP_STATE: details.append("  [CRITICAL] Invalid character or structural violation (Trap State).")
            elif current_state == 'q0': details.append("  [STRUCTURE] Input is empty.")
            elif current_state not in EMAIL_ACCEPTING_STATES: details.append(f"  [STRUCTURE] Did not reach an accepting state ({current_state}).")
        success, msg = visualize_dfa_run(path, email, is_valid, EMAIL_DFA_TABLE, EMAIL_ACCEPTING_STATES, EMAIL_TRAP_STATE, 'email_gui_run')
        details.append("-" * 30)
        details.append(msg)
        self._update_details(self.email_details_text, details)
        if not success:
            messagebox.showerror("Visualization Error", msg)
if __name__ == "__main__":
    app = CustomDfaValidatorApp()
    app.mainloop()