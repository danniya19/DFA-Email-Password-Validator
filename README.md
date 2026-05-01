
# **Team Members**

Daniya Mehmood

Zainab Rafique

# DFA-Based Email and Password Validator

This project is a functional implementation of Deterministic Finite Automata (DFA) to validate the structural integrity of email addresses and the security strength of passwords. It was developed as part of the Automata Theory coursework at the Karachi Institute of Economics and Technology (PAF-KIET).

## Project Overview
The system bridges the gap between mathematical computation models and practical software applications. By utilizing state transition logic, the validator ensures that user inputs strictly adhere to predefined formal language rules.

## Features

### Password Validation
The DFA enforces high-security standards by tracking transitions for specific character sets:
*   Minimum Length: Must be at least 8 characters.
*   Complexity: Requires at least one uppercase letter (A-Z), one lowercase letter (a-z), one digit (0-9), and one special character.
*   Final State: Input is only "Accepted" if the engine lands on a designated final state after processing the string.

### Email Validation
Ensures the input follows the standard protocol (local-part@domain.extension):
*   Validates alphanumeric characters in the local part.
*   Verifies the presence of the @ symbol and a valid domain extension like .com or .org.

## Tech Stack
*   Logic Modeling: JFLAP (for designing DFA state diagrams and transition tables).
*   Programming: Python (to simulate DFA logic and state transitions).
*   Visualization: Graphviz (for generating automated automata diagrams).
*   UI: Tkinter/PyQt (for an interactive graphical validation interface).

## File Structure
*   email and password validator.py: The main Python script containing the DFA logic and GUI.
*   DFA_Models.jff: JFLAP files containing the visual automata designs.
*   Transition_Tables.pdf: Detailed state transition documentation.

## How to Run
1. Clone the repository.
2. Ensure you have Python installed.
3. (Optional) Install Graphviz for visualization:
   ```bash
   pip install graphviz
4.Run the application.

   
Developed as part of the Automata Theory course at PAF-KIET.
