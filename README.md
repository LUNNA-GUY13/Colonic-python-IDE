#  Colonic IDE & Language

Welcome to COLONICAL, a Language with a fricking awesome IDE. This project is for the people who like brainf**k but wish it was just ... more capitalist? (and also had a built-in IDE and with cheat codes), then this counts I guess.(ALSO it's nothing like brainf##k)

## What is this?

`COLONICAL.PY` is a single Python script that runs a complete Integrated Development Environment (IDE) for a custom-designed, esoteric programming language called "Colonic". The language is unique in that most operations cost "points" ($), which you must earn by "working" within your script.

The project is a demonstration of:
- A recursive descent parser(which is decent enough).
- A simple bytecode-less interpreter.
- Building a GUI application with Python's `tkinter`.
- ~~PAIN~~ FUN (yes totally fun).

## Features

- **Esoteric Language:** A unique syntax based on symbols like `$!`, `?!`, and `!!!`.
- **Built-in Economy:** Scripts have their own "points" `($)` which reset on each run. Your IDE has a persistent "Global Wealth" which accumulates points from successful script runs.
- **Full-Featured IDE:**
    - Dark mode, VS Code-inspired theme.
    - Syntax highlighting.
    - Line numbers.
    - A comprehensive Syntax Guide sidebar.(which is just Text on a side bar).
    - An integrated terminal to see script output.
    - which looks like : <img width="1919" height="1025" alt="IDE EXAMPLE" src="https://github.com/user-attachments/assets/f0886d9d-3454-4b23-b77b-c419554eb69b" />
 
- **GUI Creation:** Use commands within your script to create new windows and draw pixels.
- **System & File I/O:** Interact with the file system and launch a system console.
- **Plugins:** Load other `.col` scripts as libraries.
- **Compiler:** A `!compile` command that packages your script into a standalone Python file.
- **Secret Cheat Codes:** Discover hidden commands for special effects and advantages.

## How to Run

You need Python 3.x and Tkinter (which is usually included with Python)(HYPER OPTIONAL : `pip install numba` for some features :) ).

1.  Save the `COLONICAL.PY` script.
2.  Run it from your terminal:
    ```bash
    python COLONICAL.PY
    ```

## How to Create a Standalone Executable (.exe)(ON JOD WHY????)

You can package the IDE into a single `.exe` file on Windows, making it easy to share and run without needing a Python installation.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the PyInstaller command:**
    Navigate to the directory where you saved `COLONICAL.PY` and run the following command:
    ```bash
    pyinstaller --onefile --windowed --icon=NONE COLONICAL.PY
    ```
    - `--onefile`: Bundles everything into a single executable file.
    - `--windowed`: Prevents a console window from appearing in the background when you run the app.
    - `--icon=NONE`: Prevents a default icon from being used.
    
3.  **Find your .exe:**
    PyInstaller will create a `dist` folder. Inside, you will find `COLONICAL.exe`.
    (why am i explaining pyinstaller again??)
## Basic Syntax Overview

| Command | Description |
|---|---|
| `$!!` | **Header:** Marks the start of the program (optional). |
| `$!` | **Grind:** Earns a random amount of points (e.g., 25-50). |
| `$` | **Wallet:** Prints the script's current point balance. |
| `?!"prompt"` | **Prompt:** Asks the user for input. Costs points based on prompt length. |
| `?! var` | **Assign:** Stores the last user input into `var`. Costs a small tax. |
| `! var` | **Print:** Prints the value of a variable or a literal string. |
| `?? var` | **If:** Starts a conditional block. Executes if `var` is not 0 or empty. |
| `??!` | **Else:** The `else` part of a conditional block. |
| `??!!` | **End If:** Ends a conditional block. |
| `!!!$loops$!!! N` | **Loop:** Starts a block that will repeat `N` times. |
| `!!!$end$!!!` | **End Loop:** Marks the end of a loop block. |
| `?????? name` | **Function:** Defines a function. |
| `call name` | **Call:** Calls a previously defined function. |
| `?$!! "Title"` | **Window:** Creates a new GUI window. Costs points. |
| `!plugin "f.col"` | **Plugin:** Loads and runs another `.col` script. |
| `!compile "output.py"` | **Compile:** Compiles the current script into a standalone Python file. |
|`:`|**Comment:** It's used for comments in code.|
|HAVE FUN!|OR ROAST IT ;)|
