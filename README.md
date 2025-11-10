# Ultra Type Pro ⌨️ — Smart Auto Typer for macOS

**Ultra Type Pro** is a modern, GUI-based **Auto Typer** built with **Python + Tkinter**, designed especially for **macOS** (and also works seamlessly on Windows/Linux).

It lets you automatically type text into any app using **customizable global hotkeys** — perfect for productivity, coding demos, or automating repetitive typing tasks.

---

##  Features

-  **Beautiful macOS-style UI** — Built with Tkinter and Apple’s SF Pro design language.  
-  **Multiple Text Sections** — Easily manage and switch between 3 typing sections.  
-  **Global Hotkeys (macOS shortcuts):**  
  - ⌘ **Cmd + Shift + X** → Type Section 1  
  - ⌘ **Cmd + Shift + Y** → Type Section 2  
  - ⌘ **Cmd + Shift + Z** → Type Section 3  
  - **Esc** → Stop typing  
-  **Adjustable Typing Speed** — Set delay between characters (0–200 ms).  
-  **Status Bar & Progress Indicator** — Displays typing progress.  
-  **Threaded Typing** — Keeps UI responsive while typing.  


---

##  Tech Stack

| **Component** | **Usage** |
|----------------|-----------|
| **Python 3.8+** | Core language |
| **Tkinter** | GUI framework |
| **pynput** | Global hotkey detection |
| **threading** | Non-blocking typing |
| **time** | Delay management |

---

##  Installation (macOS)

### 1️ Clone the Repository

```bash
git clone https://github.com/<your-username>/mac-autotyper.git
cd mac-autotyper 
```
##  macOS Permissions Setup (Important!)

To allow **Ultra Type Pro** to control the keyboard and listen for global hotkeys,  
you must grant **two system permissions** to **Visual Studio Code** (or **Python.app** if running directly).

---

###  Step 1: Enable Input Monitoring

1. Open **System Settings → Privacy & Security → Input Monitoring**  
2. Click the **“+”** button  
3. Add **Visual Studio Code** (or **Python.app**)  
4. Restart VS Code if needed  

---

###  Step 2: Enable Accessibility Access

1. Go to **System Settings → Privacy & Security → Accessibility**  
2. Click the **“+”** button  
3. Add **Visual Studio Code** (or **Python.app**)  
4. Enable the toggle   

> ⚠️ **Without these permissions, global hotkeys and typing simulation will not work.**

---

