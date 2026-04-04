import sys
import vlc
import time
import requests  # API requests er jonno
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer

class AdFlowPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- 1. Settings ---
        self.setWindowTitle("AdFlowPlayer")
        self.resize(1280, 720)
        
        # API URL (Attach server link)
        self.API_URL = "https://api.jsonbin.io/v3/b/your-bin-id" 
        self.ad_duration = 10
        
        self.ads = [
    "https://vjs.zencdn.net/v/oceans.mp4",
    "https://www.w3schools.com/html/mov_bbb.mp4",
    "https://www.w3schools.com/html/movie.mp4"
                   ] 
        self.current_index = 0

        # --- 2. VLC Setup (With --quiet to hide stale cache errors) ---
        self.instance = vlc.Instance('--no-video-title-show', '--mouse-hide-timeout=0', '--quiet')
        self.mediaplayer = self.instance.media_player_new()

        # --- 3. GUI Layout ---
        self.video_container = QWidget()
        self.setCentralWidget(self.video_container)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.video_container.setLayout(self.layout)

        if sys.platform == "win32":
            self.mediaplayer.set_hwnd(self.video_container.winId())
        else:
            self.mediaplayer.set_xwindow(self.video_container.winId())

        # --- 4. Timers ---
        # Ad Switch Timer
        self.switch_timer = QTimer()
        self.switch_timer.timeout.connect(self.play_next_ad)

        # API Sync Timer (5 minute por por server check korbe)
        self.api_timer = QTimer()
        self.api_timer.timeout.connect(self.fetch_api_playlist)
        self.api_timer.start(300000) 

        # Start
        self.fetch_api_playlist() 
        self.play_ad()

    def fetch_api_playlist(self):
        """Server theke data anar logic"""
        print("🔄 Syncing with Server...")
        try:
            response = requests.get(self.API_URL, timeout=5)
            if response.status_code == 200:
                # JSON data structure onujayi record > ads check korchi
                data = response.json()
                new_ads = data.get("record", {}).get("ads", [])
                if new_ads:
                    self.ads = new_ads
                    print(f"✅ Sync Complete. Total Ads: {len(self.ads)}")
            else:
                print("⚠️ Server returned error, using default playlist.")
        except Exception as e:
            print(f"🌐 Offline Mode: Using local ads list.")

    def play_ad(self):
        if not self.ads: return
        url = self.ads[self.current_index]
        media = self.instance.media_new(url)
        self.mediaplayer.set_media(media)
        self.mediaplayer.play()
        
        # Timer restart
        self.switch_timer.start(self.ad_duration * 1000) 
        print(f"📺 Playing Ad {self.current_index + 1}: {url}")

    def play_next_ad(self):
        self.current_index = (self.current_index + 1) % len(self.ads)
        self.play_ad()

    def play_prev_ad(self):
        self.current_index = (self.current_index - 1) % len(self.ads)
        self.play_ad()

    # --- Keyboard Controls ---
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_F:
            if self.isFullScreen(): self.showNormal()
            else: self.showFullScreen()
        elif key == Qt.Key.Key_Escape:
            self.showNormal()
        elif key == Qt.Key.Key_Space:
            if self.mediaplayer.is_playing():
                self.mediaplayer.pause()
                self.switch_timer.stop()
                print("⏸️ Paused")
            else:
                self.mediaplayer.play()
                self.switch_timer.start()
                print("▶️ Resumed")
        elif key == Qt.Key.Key_Right:
            self.play_next_ad()
        elif key == Qt.Key.Key_Left:
            self.play_prev_ad()
        elif key == Qt.Key.Key_Up:
            vol = min(self.mediaplayer.audio_get_volume() + 5, 100)
            self.mediaplayer.audio_set_volume(vol)
        elif key == Qt.Key.Key_Down:
            vol = max(self.mediaplayer.audio_get_volume() - 5, 0)
            self.mediaplayer.audio_set_volume(vol)

    def closeEvent(self, event):
        self.mediaplayer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = AdFlowPlayer()
    player.show()
    sys.exit(app.exec())