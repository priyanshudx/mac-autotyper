
#Ultra Type Pro ⌨️ — Smart Auto Typer for macOS

Ultra Type Pro is a modern GUI-based Auto Typer built with Python + Tkinter, designed especially for macOS (and also works on Windows/Linux).
It lets you automatically type text into any window using customizable global hotkeys — perfect for productivity, coding demos, or automating repetitive typing tasks.

🚀 Features

✅ Beautiful macOS-style UI: Built with Tkinter and Apple’s SF Pro design language.
✅ Multiple Text Sections: Create and switch between 3 typing sections easily.
✅ Global Hotkeys:

⌘ Cmd + Shift + X → Type Section 1

⌘ Cmd + Shift + Y → Type Section 2

⌘ Cmd + Shift + Z → Type Section 3

Esc → Stop typing
✅ Custom Typing Speed: Adjustable delay between characters (0–200ms).
✅ Status Bar & Progress Indicator.
✅ Threaded Typing: Keeps UI responsive while typing.
✅ Cross-Platform Support: macOS, Windows, and Linux compatible.

Tech Stack
Component	Usage
Python 3.8+	Core language
Tkinter	GUI framework
pynput	Global hotkey detection
threading	For non-blocking typing
time	Delay management
💻 Installation
1️⃣ Clone the repository
git clone https://github.com/<your-username>/mac-autotyper.git
cd mac-autotyper

2️⃣ Install dependencies
pip install pynput


Tkinter is included by default in most Python distributions.

macOS Permissions Setup (Very Important)

To allow Ultra Type Pro to control the keyboard and listen for global hotkeys,
you must grant two permissions to Visual Studio Code (or Python):

🧾 Step 1: Enable Input Monitoring

Open System Settings → Privacy & Security → Input Monitoring

Click the “+” button

Add Visual Studio Code (or Python.app, depending on what you use to run it)

Restart VS Code if needed

🧾 Step 2: Enable Accessibility Access

Go to System Settings → Privacy & Security → Accessibility

Click the “+” icon

Add Visual Studio Code (or Python.app)

Enable the toggle next to it ✅

⚠️ Without these permissions, global hotkeys and typing simulation won’t work.

🧭 Usage

Launch the app:

python autotyper.py


You’ll see the Ultra Type Pro interface with three text sections.

Type or paste text in any section.

Adjust the typing delay (in milliseconds per character).

Switch to any app (like Notes, Browser, Terminal, etc.).

Use the hotkeys:

Cmd + Shift + X → Type Section 1

Cmd + Shift + Y → Type Section 2

Cmd + Shift + Z → Type Section 3

Esc → Stop typing instantly
