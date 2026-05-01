
# **Team Members**

Daniya Mehmood

Zainab Rafique

# DFA-Based Email and Password Validator

This project is a functional implementation of **Deterministic Finite Automata (DFA)** to validate the structural integrity of email addresses and the security strength of passwords. It was developed as part of the Automata Theory coursework at the **Karachi Institute of Economics and Technology (PAF-KIET)**[cite: 1].

##  Project Overview
The system bridges the gap between mathematical computation models and practical software applications. By utilizing state transition logic, the validator ensures that user inputs strictly adhere to predefined formal language rules[cite: 1].

##  Features

### Password Validation
The DFA enforces high-security standards by tracking transitions for specific character sets:
*   **Minimum Length**: Must be at least 8 characters[cite: 1].
*   **Complexity**: Requires at least one uppercase letter ($A-Z$), one lowercase letter ($a-z$), one digit ($0-9$), and one special character[cite: 1].
*   **Final State**: Input is only "Accepted" if the engine lands on a designated final state after processing the string[cite: 1].

###  Email Validation
Ensures the input follows the standard protocol ($local$-$part@domain.extension$):
*   Validates alphanumeric characters in the local part[cite: 1].
*   Verifies the presence of the `@` symbol and a valid domain extension like `.com` or `.org`[cite: 1].

##  Tech Stack
*   **Logic Modeling**: JFLAP (for designing DFA state diagrams and transition tables)[cite: 1].
*   **Programming**: Python (to simulate DFA logic and state transitions)[cite: 1].
*   **Visualization**: Graphviz (for generating automated automata diagrams)[cite: 1].
*   **UI**: Tkinter/PyQt (for an interactive graphical validation interface)[cite: 1].

##  File Structure
*   `email and password validator.py`: The main Python script containing the DFA logic and GUI[cite: 1].
*   `DFA_Models.jff`: JFLAP files containing the visual automata designs[cite: 1].
*   `Transition_Tables.pdf`: Detailed state transition documentation[cite: 1].

##  How to Run
1. Clone the repository.
2. Ensure you have Python installed.
3. (Optional) Install Graphviz for visualization:
   ```bash
   pip install graphviz
