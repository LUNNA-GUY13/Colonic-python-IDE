import sys
import os
import time
import random
import math
import re
import tkinter as tk
from tkinter import filedialog, simpledialog, scrolledtext, messagebox, ttk

# Try to import Numba for optimization
try:
    from numba import jit
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False
    def jit(nopython=False): return lambda f: f # Dummy decorator

class ColonicInterpreter:
    def __init__(self, output_func, input_func, create_window_func=None, draw_pixel_func=None):
        self.points = 0
        self.variables = {}
        self.output_func = output_func
        self.input_func = input_func
        self.create_window_func = create_window_func
        self.draw_pixel_func = draw_pixel_func
        self.code_source = ""
        self.inflation_rate = 1
        self.terraria_mode = False
        self.glitch_mode = False
        self.sonic_mode = False
        self.reset()

    def reset(self):
        self.points = 0
        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.last_input = "0"
        self.inflation_rate = 1
        self.terraria_mode = False
        self.glitch_mode = False
        self.sonic_mode = False

    def log(self, message):
        if self.glitch_mode:
            # Scramble 10% of characters
            chars = list(str(message))
            for i in range(len(chars)):
                if random.random() < 0.1:
                    chars[i] = chr(random.randint(33, 126))
            message = "".join(chars)
        self.output_func(str(message) + "\n")

    def run(self, code):
        self.reset()
        self.code_source = code
        lines = code.split('\n')
        self.execute_block(lines, 0)

    def scan_forward(self, lines, start_pc, start_token_prefix, end_token):
        """Scans forward to find the matching end token, handling nesting."""
        depth = 1
        pc = start_pc + 1
        while pc < len(lines):
            line = lines[pc].strip()
            if line.startswith(start_token_prefix):
                depth += 1
            elif line == end_token:
                depth -= 1
                if depth == 0:
                    return pc
            pc += 1
        return pc

    def execute_block(self, lines, pc, stop_token=None):
        """Recursive parser to execute a block of code."""
        
        while pc < len(lines):
            line = lines[pc].strip()
            line_num = pc

            # Sonic Mode Slowdown
            if self.sonic_mode:
                time.sleep(0.05) # "Run slower"
                # Note: The IDE output lambda handles UI updates to prevent freezing
            
            # 1. Handle Comments (:) 
            if ":" in line:
                line = line.split(":")[0].strip()
            
            if not line:
                pc += 1
                continue
            
            # Check for block end
            if stop_token and line == stop_token:
                return pc

            try:
                # 0. Secrets
                if line == "UPUPDOWNDOWNLEFTRIGHTLEFTRIGHTAB": # Easter Egg (Classic)
                    self.points += 1000000
                    self.log("[SECRET] GOD MODE ENABLED: Infinite Wealth.")
                    pc += 1
                    continue
                elif line == "DOOM64":
                    self.log("[SECRET] DOOM MODE: All outputs are now 'Doomed'.")
                    self.output_func = lambda msg: sys.stdout.write("Doomed\n") # Override low-level
                    pc += 1
                    continue
                elif line == "TERRARIA":
                    self.log("[SECRET] TERRARIA MODE: Randomly generate items instead of points.")
                    self.terraria_mode = True
                    pc += 1
                    continue
                elif line == "[DATA EXPUNGED]":
                    self.log("[SECRET] this is a archived message. PLEASE PLEASE DO NOT TYPE 'MANY TEARS, MANY LAUGHS , 'IN TBOI' WE TRUST'.")
                    pc += 1
                    continue
                elif line == "IN TBOI":
                    self.log("PLAY THE BINDING OF ISAAC: REPENTANCE, IT'S A GREAT GAME AND YOU'LL LOVE IT. LOVE LUNNA-GUY :)")
                    pc += 1
                    continue
                elif line == "HYPERINFLATION":
                    self.log("[SECRET] HYPERINFLATION: Money is worthless (but you get more of it).")
                    self.inflation_rate = 100
                    pc += 1
                    continue
                elif line == "MISSINGNO":
                    self.log("[SECRET] GLITCH MODE ENABLED.")
                    self.glitch_mode = True
                    pc += 1
                    continue
                elif line == "SONIC":
                    self.log("[SECRET] SONIC MODE: GOTTA GO... SLOW? (Points x10!)")
                    self.sonic_mode = True
                    self.inflation_rate *= 10
                    pc += 1
                    continue

                # 2. $! (The Grind) - Earn Points
                if line.startswith("$!") and not line.startswith("$!!"):
                    if self.terraria_mode:
                        self.handle_terraria_grind()
                    else:
                        earned = random.randint(25, 50) * self.inflation_rate
                        self.points += earned
                        self.log(f"[SYSTEM] Worked hard. Earned {earned} $. Total: {self.points}")

                # 3. $!! (The Header) - Initializing
                elif line.startswith("$!!"):
                    self.log("--- COLONIC PROGRAM START ---")

                # 4. ?! "text" (The Interrogator - Prompt)
                elif line.startswith('?!"'):
                    # Safer quote parsing
                    parts = line.split('"')
                    if len(parts) >= 2:
                        text = parts[1]
                        cost = len(text)
                        if self.points >= cost:
                            self.points -= cost
                            user_in = self.input_func(text)
                            self.last_input = user_in if user_in is not None else ""
                        else:
                            self.log(f"BANKRUPTCY ERROR: Need {cost} $ to speak, but only have {self.points}.")
                            break
                    else:
                        self.log(f"SYNTAX ERROR (Line {line_num+1}): Malformed string.")

                # 5. ?! variable (The Interrogator - Assignment)
                elif line.startswith("?!") and '"' not in line and line != "?!!" and not line.startswith("?!!"):
                    var_name = line.replace("?!", "").strip()
                    tax = 10 if var_name in self.variables else 5
                    if self.points >= tax:
                        self.points -= tax
                        self.variables[var_name] = self.last_input
                    else:
                        self.log(f"TAX ERROR: Need {tax} $ to store data.")
                        break

                # 5.5 Modifiers & Standard Library
                elif line.startswith("!upper "):
                    content = line[7:].strip()
                    val = str(self.variables.get(content, content))
                    self.log(f">> {val.upper()}")

                elif line.startswith("!lower "):
                    content = line[7:].strip()
                    val = str(self.variables.get(content, content))
                    self.log(f">> {val.lower()}")

                elif line.startswith("!math."):
                    # Standard Library: Math
                    cmd = line.replace("!math.", "").strip()
                    if cmd == "pi": self.log(f">> {math.pi}")
                    elif cmd == "e": self.log(f">> {math.e}")
                    elif cmd.startswith("sqrt "):
                        arg = cmd.split(" ")[1]
                        val = float(self.variables.get(arg, arg))
                        self.log(f">> {math.sqrt(val)}")
                    else: self.log(">> [MATH LIB ERROR] Unknown function")

                # 6. ! (The Strike - Output)
                elif line.startswith("!") and not any(line.startswith(x) for x in ["!!!", "?!", "!math", "!upper", "!lower", "!$"]):
                    content = line[1:].strip()
                    # Check if it's a variable or literal
                    val = self.variables.get(content, content)
                    self.log(f">> {val}")

                # 7. $ (Wallet Check)
                elif line == "$":
                    self.log(f"[WALLET] Current Balance: {self.points} $")

                # 8. !!! (The X-Ray - Debug)
                elif line == "!!!":
                    self.log(f"--- DEBUG: Points: {self.points} | Vars: {self.variables} ---")

                # 9. ?!! (The Mystery/Gambler)
                elif line == "?!!":
                    if random.choice([True, False]):
                        self.points *= 2 * self.inflation_rate
                        self.log(f"[GAMBLE] Jackpot! Points doubled to {self.points}.")
                    else:
                        self.points = 0
                        self.log("[GAMBLE] House wins. You are broke.")

                # 10. !!!$loops$!!! N
                elif line.startswith("!!!$loops$!!!"):
                    parts = line.split()
                    count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                    loop_start_pc = pc + 1
                    
                    # Find end first to know where to jump after loop
                    end_pc = self.scan_forward(lines, pc, "!!!$loops$!!!", "!!!$end$!!!")
                    
                    # Recursively execute the block N times
                    for _ in range(count):
                        self.execute_block(lines, loop_start_pc, "!!!$end$!!!")
                    
                    pc = end_pc # Skip to end

                # 10.5 Conditional Logic
                elif line.startswith("??") and not line.startswith("??!") and not line.startswith("??!!"):
                    parts = line.split()
                    condition_val = "0"
                    if len(parts) > 1:
                        condition_val = self.variables.get(parts[1], parts[1])
                    
                    is_true = condition_val not in ["0", "", "false", None, 0]

                    # Scan for boundaries
                    else_pc = -1
                    endif_pc = -1
                    depth = 1
                    for i in range(pc + 1, len(lines)):
                        scan_line = lines[i].strip()
                        if scan_line.startswith("??") and not scan_line.startswith("??!") and not scan_line.startswith("??!!"):
                            depth += 1
                        elif scan_line == "??!!":
                            depth -= 1
                            if depth == 0:
                                endif_pc = i
                                break
                        elif scan_line == "??!" and depth == 1:
                            if else_pc == -1: else_pc = i

                    if endif_pc == -1:
                        self.log(f"SYNTAX ERROR (Line {line_num+1}): Missing '??!!' for '??'.")
                        break

                    if is_true:
                        # Execute the 'then' block.
                        stop_token = "??!" if else_pc != -1 else "??!!"
                        self.execute_block(lines, pc + 1, stop_token=stop_token)
                    elif else_pc != -1:
                        # Condition is false, execute the 'else' block.
                        self.execute_block(lines, else_pc + 1, stop_token="??!!")
                    
                    pc = endif_pc # Jump to the end of the if/else structure

                # 10.6 Window Creation
                elif line.startswith("?$!!"):
                    parts = line.split('"')
                    title = parts[1] if len(parts) > 1 else "Colonic Window"
                    dims = parts[2].strip().split()
                    width, height = int(dims[0]), int(dims[1]) if len(dims) > 1 else (400, 200)
                    cost = 250
                    if self.points >= cost and self.create_window_func:
                        self.points -= cost
                        self.create_window_func(title, width, height)
                        self.log(f"[GUI] Created window '{title}'. Cost: {cost} $.")
                    else:
                        self.log(f"GUI ERROR: Need {cost} $ to create a window.")

                # 10.7 File I/O
                elif line.startswith("!file."):
                    parts = line.split()
                    cmd = parts[0]
                    
                    if cmd == "!file.write":
                        # !file.write "filename" "content"
                        # Parse quotes manually
                        qparts = line.split('"')
                        if len(qparts) >= 4:
                            fname = qparts[1]
                            content = qparts[3]
                            try:
                                with open(fname, "w") as f: f.write(content)
                                self.log(f"[FILE] Wrote to {fname}")
                            except Exception as e: self.log(f"[FILE ERROR] {e}")
                    
                    elif cmd == "!file.read":
                        # !file.read "filename" varname
                        qparts = line.split('"')
                        if len(qparts) >= 3:
                            fname = qparts[1]
                            varname = line.split()[-1]
                            try:
                                with open(fname, "r") as f: content = f.read()
                                self.variables[varname] = content
                                self.log(f"[FILE] Read from {fname}")
                            except Exception as e: self.log(f"[FILE ERROR] {e}")

                # 10.8 Pixel Drawing
                elif line.startswith("?$pixel"):
                    # ?$pixel "WindowName" x y "Color"
                    qparts = line.split('"')
                    if len(qparts) >= 4:
                        win_name = qparts[1]
                        color = qparts[3]
                        # Get coords between quotes
                        coords = line.replace(f'"{win_name}"', "").replace(f'"{color}"', "").replace("?$pixel", "").split()
                        if len(coords) >= 2 and self.draw_pixel_func:
                            x, y = int(coords[0]), int(coords[1])
                            self.draw_pixel_func(win_name, x, y, color)

                # 10.9 System Commands
                elif line.startswith("!console"):
                    self.log("[SYSTEM] Launching console...")
                    if os.name == 'nt': os.system("start cmd")
                    else: os.system("x-terminal-emulator")

                elif line.startswith("!compile"):
                    # !compile "filename.py"
                    out_name = line.split('"')[1] if '"' in line else "out.py"
                    self.compile_to_python(out_name)

                elif line.startswith("!plugin"):
                    # !plugin "filename.col"
                    if '"' in line:
                        path = line.split('"')[1]
                        try:
                            if os.path.exists(path):
                                with open(path, "r") as f:
                                    plugin_lines = f.read().split('\n')
                                self.log(f"[SYSTEM] Loading plugin '{path}'...")
                                self.execute_block(plugin_lines, 0)
                                self.log(f"[SYSTEM] Plugin '{path}' loaded.")
                            else:
                                self.log(f"[ERROR] Plugin file '{path}' not found.")
                        except Exception as e:
                            self.log(f"[ERROR] Failed to load plugin: {e}")

                elif line.startswith("!numba.benchmark"):
                    if HAS_NUMBA:
                        self.log("[NUMBA] Running JIT compiled benchmark...")
                        start = time.time()
                        res = self.numba_heavy_task(1000000)
                        self.log(f"[NUMBA] Result: {res} in {time.time()-start:.4f}s")
                    else:
                        self.log("[NUMBA] Library not installed. Running in standard Python mode.")

                # 11. ?????? (Function Definition)
                elif line.startswith("??????"):
                    parts = line.split()
                    func_name = parts[1] if len(parts) > 1 else "anon"
                    args = parts[2:]
                    
                    start_body = pc + 1
                    end_body = self.scan_forward(lines, pc, "??????", "??????!")
                    
                    self.functions[func_name] = {
                        "args": args,
                        "start": start_body,
                        "end_token": "??????!"
                    }
                    pc = end_body # Skip definition

                # 12. call FuncName Args
                elif line.startswith("call "):
                    parts = line.split()
                    if len(parts) > 1:
                        func_name = parts[1]
                        call_args = parts[2:]
                        
                        if func_name in self.functions:
                            func = self.functions[func_name]
                            # Scope Management: simple variable backup (shadowing)
                            saved_vars = self.variables.copy()
                            
                            # Map args
                            for i, arg_name in enumerate(func["args"]):
                                if i < len(call_args):
                                    val = call_args[i]
                                    # Resolve variable if passed as arg
                                    self.variables[arg_name] = self.variables.get(val, val)
                            
                            # Execute
                            self.execute_block(lines, func["start"], func["end_token"])
                            
                            # Restore scope (globals persist modifications, locals die? 
                            # In this simple model, we restore everything to simulate local scope, 
                            # but that means functions can't modify globals. 
                            # Let's keep it simple: functions use a temp scope based on current.)
                            self.variables = saved_vars
                        else:
                            self.log(f"ERROR: Function '{func_name}' not found.")

                # 13. $$$$ (Class Definition)
                elif line.startswith("$$$$"):
                    parts = line.split()
                    class_name = parts[1] if len(parts) > 1 else "UnknownClass"
                    
                    self.log(f"[CLASS] Defining {class_name}...")
                    
                    # Execute body in a fresh scope to capture members
                    parent_vars = self.variables
                    self.variables = {} # New scope for class
                    
                    end_pc = self.execute_block(lines, pc + 1, "$$$$!")
                    
                    # Save class definition
                    self.classes[class_name] = self.variables
                    
                    # Restore and save class reference
                    class_members = self.variables
                    self.variables = parent_vars
                    self.variables[class_name] = class_members # Store class as a dict
                    
                    pc = end_pc

            except Exception as e:
                self.log(f"RUNTIME ERROR (Line {line_num+1}): {e}")
            pc += 1
        return pc

    def handle_terraria_grind(self):
        items = {
            "Copper Coin": 1, "Silver Coin": 5, "Gold Coin": 10, "Platinum Coin": 20,
            "Dirtiest Dirt Block": 50, "Wooden Sword": 10, "Stone Block": 5,
            "Healing Potion": "mul2", "Mana Potion": "mul1.5", "Zenith": 99999,
            "NOTE : [redacted]": "note"
        }
        item_name = random.choice(list(items.keys()))
        val = items[item_name]

        if isinstance(val, int):
            self.points += val
            self.log(f"[SYSTEM] Found a {item_name}! (+{val})")
        elif val == "mul2":
            self.points *= 2
            self.log(f"[SYSTEM] Drank {item_name}. Points doubled!")
        elif val == "mul1.5":
            self.points = int(self.points * 1.5)
            self.log(f"[SYSTEM] Drank {item_name}. Points x1.5!")
        elif val == "note":
            self.log("[SYSTEM] Found a mysterious note...")
            self.log("[NOTE] 'The code is .. it is... is in the... the... the... [DATA EXPUNGED]'")

    @staticmethod
    @jit(nopython=True)
    def numba_heavy_task(n):
        # A task to demonstrate Numba speed (calculating sum of sqrt)
        acc = 0.0
        for i in range(n): acc += math.sqrt(i)
        return acc

    def compile_to_python(self, filename):
        # Creates a standalone python script that includes a mini-interpreter
        py_code = f"""import sys, random, math, tkinter as tk
class StandaloneInterpreter:
    def __init__(self):
        self.points = 0
        self.variables = {{}}
        self.functions = {{}}
    def log(self, msg): print(msg)
    def run(self, code): self.execute(code.split('\\n'), 0)
    def scan(self, lines, pc, start, end):
        d=1; pc+=1
        while pc<len(lines):
            if lines[pc].strip().startswith(start): d+=1
            elif lines[pc].strip()==end: d-=1; 
            if d==0: return pc
            pc+=1
        return pc
    def execute(self, lines, pc, stop=None):
        while pc < len(lines):
            line = lines[pc].strip()
            if not line or ":" in line: 
                pc+=1; continue
            if stop and line==stop: return pc
            # Limited feature set for compiled version
            if line.startswith("$!"): self.points += 10; print(f"Earned 10. Total: {{self.points}}")
            elif line.startswith("!"): 
                c = line[1:].strip()
                print(self.variables.get(c, c))
            elif line.startswith("?!") and '"' not in line:
                v = line.replace("?!","").strip()
                if self.points>=5: 
                    self.points-=5; self.variables[v] = input()
            elif line.startswith('?!"'):
                p = line.split('"')[1]
                if self.points>=len(p):
                    self.points-=len(p); print(p); 
            # Loops
            elif line.startswith("!!!$loops$!!!"):
                c = int(line.split()[1])
                start = pc+1
                end = self.scan(lines, pc, "!!!$loops$!!!", "!!!$end$!!!")
                for _ in range(c): self.execute(lines, start, "!!!$end$!!!")
                pc = end
            pc+=1

code = r'''{self.code_source}'''
if __name__ == "__main__":
    StandaloneInterpreter().run(code)
"""
        try:
            with open(filename, "w") as f:
                f.write(py_code)
            self.log(f"[COMPILER] Compiled to {filename}. Run with 'python {filename}'")
        except Exception as e:
            self.log(f"[COMPILER ERROR] {e}")

class ColonicIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Colonic IDE 'All I See Is Bule' v4 - " + str(random.choice(["What happened to V1 - V3","VS CODE IS WEAK!!", "COLONIC IS NAMED AFTER colons our comment symbol", "COLONIC IS THE BEST!" , "I wuv U User <3 uwu", "This is a very strange IDE", "Why does this exist?", "Don't forget to check the README for syntax!" , "also try terraria or minecraft they are good games", "COLON LIVES MATTER!!", "The Binding of Isaac is a great game and you should play it", "This IDE is a joke, but also kind of a flex", "Don't forget to check the README for syntax!", "This is a very strange IDE", "Why does this exist?", "Don't forget to check the README for syntax! AGAIN!" , "also try i have nothing to say", "COLON LIVES MATTER!!", "RISK OF RAIN 2 is a great game and you should play it" , "WILL THE WHOLE WORLD KNOW YOUR NAMEEEEEEEE? AS WE DANCE WITH DESTINYYY? I HAVE BEEN THERE, I HAVE SEEN IT" , "You feel your sins crawling on your back." , "A terrible night to have Debt." , "Eyes up, Coder." , "The cake is a lie" , "Praise the Sun! L[¯⊥¯]⅃" , "I used to be a programmer like you, then I took a syntax error to the knee." , "'It must have been the wind'"])))
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")
        self.wealth = 0
        self.windows = {} # Store window references: {title: (window, canvas)}
        self.suggestions = None # For IntelliSense

        # Styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#cccccc")
        style.configure("TButton", background="#007acc", foreground="white", borderwidth=0)
        style.map("TButton", background=[("active", "#005f9e")])

        # --- Toolbar ---
        toolbar = tk.Frame(root, bg="#252526", height=30)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(toolbar, text="📂 Load", bg="#333333", fg="white", borderwidth=0, command=self.load_file).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(toolbar, text="💾 Save (100 $)", bg="#333333", fg="white", borderwidth=0, command=self.save_file).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(toolbar, text="▶ RUN", bg="#007acc", fg="white", borderwidth=0, font=("Segoe UI", 9, "bold"), command=self.run_code).pack(side=tk.LEFT, padx=20, pady=2)
        self.lbl_wealth = tk.Label(toolbar, text="Global Wealth: 0 $", bg="#252526", fg="#daa520", font=("Segoe UI", 10, "bold"))
        self.lbl_wealth.pack(side=tk.RIGHT, padx=10)

        # --- Main Layout (Paned Window) ---
        main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#1e1e1e", sashwidth=4, sashrelief=tk.FLAT)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # Sidebar (Explanations)
        sidebar = ttk.Frame(main_pane, style="TFrame")
        main_pane.add(sidebar, minsize=220)
        
        tk.Label(sidebar, text="SYNTAX GUIDE", bg="#252526", fg="#888", font=("Segoe UI", 8, "bold"), anchor="w").pack(fill=tk.X, padx=5, pady=5)

        # --- Syntax Tree ---
        style.configure("Treeview", background="#252526", foreground="#d4d4d4", fieldbackground="#252526", borderwidth=0)
        style.map("Treeview", background=[('selected', '#007acc')])
        self.syntax_tree = ttk.Treeview(sidebar, show="tree", style="Treeview")
        self.syntax_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        items = {
            "Economy": ["$! : Earn points", "$ : Check points"],
            "I/O": ["! : Print var/text", '?!"prompt" : Get input', "!file.read", "!file.write"],
            "Variables": ["?! var : Assign last input"],
            "Logic": ["?? var : If", "??! : Else", "??!! : End If"],
            "Loops": ["!!!$loops$!!! N", "!!!$end$!!!"],
            "Functions": ["?????? name : Def func", "call name : Call func"],
            "GUI": ['?$!! "Title" : New Window', '?$pixel "Win" : Draw'],
            "System": ["!console", "!compile", "!plugin"],
        }
        for category, commands in items.items():
            cat_id = self.syntax_tree.insert("", "end", text=category, open=True)
            for cmd in commands:
                self.syntax_tree.insert(cat_id, "end", text=f"  {cmd}")

        # Right Pane (Editor + Output)
        right_pane = tk.PanedWindow(main_pane, orient=tk.VERTICAL, bg="#1e1e1e", sashwidth=4)
        main_pane.add(right_pane)

        # Code Editor Frame (to hold line numbers + text)
        edit_frame = tk.Frame(right_pane, bg="#1e1e1e")
        right_pane.add(edit_frame, minsize=300)

        # Editor Area
        self.text_area = scrolledtext.ScrolledText(edit_frame, wrap=tk.NONE, font=("Consolas", 12), undo=True,
                                                   bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", selectbackground="#264f78")
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Line Numbers
        self.line_numbers = tk.Text(edit_frame, width=4, padx=4, takefocus=0, border=0, background="#252526", foreground="#858585", state="disabled", font=("Consolas", 12))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind("<ButtonRelease-1>", self.on_text_change)
        self.text_area.bind("<MouseWheel>", self.sync_scroll)
        # Sync scrollbar
        self.text_area.vbar.config(command=self.sync_scroll_bar)

        # Output Area
        out_frame = tk.Frame(right_pane, bg="#1e1e1e")
        right_pane.add(out_frame, minsize=100)
        
        tk.Label(out_frame, text="TERMINAL", bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 8)).pack(anchor="w", padx=5)
        self.output_area = scrolledtext.ScrolledText(out_frame, height=10, bg="#1e1e1e", fg="#cccccc", font=("Consolas", 10), borderwidth=0)
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5)

        # --- Syntax Highlighting ---
        self.text_area.tag_config("comment", foreground="#6a9955", font=("Consolas", 12, "italic"))
        self.text_area.tag_config("money", foreground="#dcdcaa", font=("Consolas", 12, "bold"))
        self.text_area.tag_config("keyword", foreground="#569cd6", font=("Consolas", 12, "bold"))
        self.text_area.tag_config("string", foreground="#ce9178")
        self.text_area.tag_config("lib", foreground="#4ec9b0")
        self.text_area.tag_config("loop", foreground="#c586c0", font=("Consolas", 12, "bold"))
        self.text_area.tag_config("def", foreground="#dcdcaa", font=("Consolas", 12, "bold"))
        self.text_area.tag_config("class", foreground="#4ec9b0", font=("Consolas", 12, "bold"))
        self.text_area.tag_config("cond", foreground="#d16969", font=("Consolas", 12, "bold"))
        self.text_area.tag_config("sys", foreground="#ff00ff", font=("Consolas", 12, "bold"))

        # --- Status Bar ---
        self.status_bar = tk.Label(root, text="Ready", bg="#007acc", fg="white", anchor="w", font=("Segoe UI", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Default Code
        self.text_area.insert(tk.END, """$!! : Program Start
: This is the Colonic IDE, a strange place.
: Earn points with '$!' and spend them on commands.

$! : Earn some starting cash
$!

$ : Check your script's current points

?! "What is your name?"
?! username

?? username
    ! "Greetings, "
    !upper username
??!
    ! "Fine, be that way."
??!!

: Your script's final points will be added to your Global Wealth.
"""
)
        self.on_text_change()

    def sync_scroll(self, event=None):
        self.line_numbers.yview_moveto(self.text_area.yview()[0])
        return "break" # Let default propagate? No, we handle it.
    
    def sync_scroll_bar(self, *args):
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def update_line_numbers(self):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        line_count = self.text_area.index('end-1c').split('.')[0]
        lines = "\n".join(str(i) for i in range(1, int(line_count) + 1))
        self.line_numbers.insert("1.0", lines)
        self.line_numbers.config(state="disabled")
        self.line_numbers.yview_moveto(self.text_area.yview()[0])

    def show_intellisense(self, event):
        # Simple keyword suggestion
        if event.keysym in ["Return", "space", "BackSpace", "Up", "Down"]: return
        
        # Get word at cursor
        idx = self.text_area.index(tk.INSERT)
        line, col = idx.split('.')
        current_line = self.text_area.get(f"{line}.0", idx)
        words = current_line.split()
        if not words: return
        
        last_word = words[-1]
        keywords = ["$!", "$!!", "?!", "?!!", "!!!", "call", "func", "class", "print", "!upper", "!lower", "!file.", "!numba."]
        # (Implementation simplified: In a real IDE this would pop up a Listbox. 
        # For now, we assume the user just wants the line numbers and Numba as main features per prompt constraints)

    def on_text_change(self, event=None):
        self.update_line_numbers()
        if event and event.type == tk.EventType.KeyRelease:
            self.show_intellisense(event) # Placeholder for future expansion
        self.highlight()
        self.update_status_bar()

    def update_status_bar(self):
        try:
            idx = self.text_area.index(tk.INSERT)
            self.status_bar.config(text=f"Ln {idx.split('.')[0]}, Col {idx.split('.')[1]}")
        except: pass

    def highlight(self, event=None):
        for tag in ["comment", "money", "keyword", "string", "lib", "loop", "def", "class", "cond", "sys"]:
            self.text_area.tag_remove(tag, "1.0", tk.END)

        self.apply_regex(r'".*?"', "string")
        self.apply_regex(r"(\$!!|\$!|\$)", "keyword") # Basic money commands
        self.apply_regex(r"(!!!\$loops\$!!!|!!!\$end\$!!!)", "loop")
        self.apply_regex(r"(\?\?!|\?\?!!|\?\?|\?\$!!)", "cond")
        self.apply_regex(r"(\?\?\?\?\?\?!|\?\?\?\?\?\?)", "def")
        self.apply_regex(r"(\$\$\$\$!|\$\$\$\$)", "class")
        self.apply_regex(r"(!console|!compile|!file\.|!\$pixel|!plugin)", "sys")
        self.apply_regex(r"(\?!!|\?!|!!!|!upper|!lower|!)", "money")
        self.apply_regex(r"!math\.[a-zA-Z0-9]+", "lib")
        self.apply_regex(r":.*", "comment") # Comments mask others

    def apply_regex(self, pattern, tag):
        start = "1.0"
        count_var = tk.IntVar()
        while True:
            pos = self.text_area.search(pattern, start, stopindex=tk.END, regexp=True, count=count_var)
            if not pos: break
            self.text_area.tag_add(tag, pos, f"{pos}+{count_var.get()}c")
            start = f"{pos}+{count_var.get()}c"

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Colonic Files", "*.col"), ("All Files", "*.*")])
        if path:
            with open(path, "r") as f:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", f.read())
            self.highlight()

    def save_file(self):
        cost = 100
        ext = ".col"
        content = self.text_area.get("1.0", tk.END)

        if self.wealth >= cost:
            self.wealth -= cost
            self.lbl_wealth.config(text=f"Global Wealth: {self.wealth} $")
        else:
            messagebox.showwarning("Insufficient Funds", f"You need {cost} $ to save properly.\nSaving as corrupt file.")
            ext = ".corrupt"
            content = "".join([chr(random.randint(33, 126)) for _ in content]) # Scramble

        path = filedialog.asksaveasfilename(defaultextension=ext, filetypes=[("Colonic Files", ext)])
        if path:
            with open(path, "w") as f: f.write(content)

    def create_window(self, title, width, height):
        try:
            win = tk.Toplevel(self.root)
            win.title(title)
            win.geometry(f"{width}x{height}")
            canvas = tk.Canvas(win, width=width, height=height, bg="black")
            canvas.pack()
            self.windows[title] = (win, canvas)
        except Exception as e:
            messagebox.showerror("GUI Error", f"Failed to create window: {e}")
            
    def draw_pixel(self, title, x, y, color):
        if title in self.windows:
            win, canvas = self.windows[title]
            try:
                # Draw a 2x2 pixel rectangle for visibility
                canvas.create_rectangle(x, y, x+2, y+2, outline=color, fill=color)
            except: pass

    def run_code(self):
        self.output_area.delete("1.0", tk.END)
        interpreter = ColonicInterpreter(
            lambda t: (self.output_area.insert(tk.END, t), self.output_area.see(tk.END), self.root.update()), # Update UI for Sonic Mode
            lambda p: simpledialog.askstring("Input", p, parent=self.root),
            create_window_func=self.create_window,
            draw_pixel_func=self.draw_pixel
        )
        interpreter.run(self.text_area.get("1.0", tk.END))
        self.wealth += interpreter.points
        self.lbl_wealth.config(text=f"Global Wealth: {self.wealth} $")

if __name__ == "__main__":
    root = tk.Tk()
    ColonicIDE(root)
    root.mainloop()
