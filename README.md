# AdFlowPlayer
A robust, Python-based Digital Signage Media Player for the AdFlow Network. Integrated with VLC engine and PyQt6, featuring auto-syncing API, smart looping, and full manual keyboard controls (Volume, Navigation, Fullscreen).

# 📺 AdFlowPlayer

AdFlow Player is a high-performance digital signage application designed for the AdFlow Network. It features a robust integration of the VLC Multimedia Engine and PyQt6, allowing for seamless video playback with cloud-based playlist management.

### **✨ Key Features:**
* **Cloud Sync (API):** Automatically fetches the latest ad playlist from a remote server (JSON API).
* **Offline Fallback:** If internet is unavailable, it plays a pre-defined local/cached playlist to ensure zero downtime.
* **VLC Core:** Uses the high-performance VLC engine with --quiet mode to suppress system logs.
* **Desktop Optimized:** Full support for Windowed and Fullscreen modes with native Minimize/Maximize/Close controls.
* **Manual Override (Keyboard):** Space (Pause/Play), Right/Left Arrows (Skip), Up/Down Arrows (Volume Control), F / ESC (Toggle Fullscreen).

### **🛠️ Installation & Setup:**
* **Prerequisites:** Python 3.10+ and VLC Media Player (64-bit) must be installed.
* **Install Dependencies:** `pip install PyQt6 python-vlc requests`
* **Running the App:** `python main.py`

### **📦 Building the Executable (.exe):**
To create a standalone desktop application using PyInstaller: `pyinstaller --noconsole --onedir --name "AdFlowPlayer" main.py`  
**Note:** Ensure you distribute the entire `dist/AdFlowPlayer` folder (including the `_internal` folder and DLLs).

### **⚙️ Configuration:**
Inside `main.py`, you can modify `API_URL` (Your server endpoint) and `ad_duration` (The interval in seconds, default is 10s).

### **📂 Project Structure:**
* **main.py:** Core application logic with API & VLC integration.
* **requirements.txt:** List of required Python libraries.
* **AdFlowPlayer.spec:** Build configuration for PyInstaller.
