# 🎵 **Py Video to Audio**
Ein **MP4-zu-Audio-Konverter-Tool**, das MP4-Dateien in verschiedene Audioformate umwandelt, inklusive **MP3, WAV**.  
Ideal für schnelle Konvertierungen mit einer **intuitiven GUI** dank **PySide6** und **FFmpeg**! 🎶

---

### ✨ **Features**
✅ **Einfaches Drag & Drop** für MP4-Dateien  
✅ **Wähle dein Audioformat:** MP3 oder WAV  
✅ **Individuelle Bitrate & Samplingrate-Einstellungen**  
✅ **Fortschrittsanzeige für laufende Konvertierungen**  
✅ **Abbrechen-Funktion für laufende Prozesse**  
✅ **Popup-Bestätigung bei Dateiüberschreibung**  
✅ **Multithreading für reaktionsschnelle GUI**  

---

### 🛠 **Installation**
1️⃣ **FFmpeg installieren:**  
- **Linux:**  
  ```bash
  sudo apt install ffmpeg
  ```
- **Windows:**  
  Lade FFmpeg von [ffmpeg.org](https://ffmpeg.org) herunter und füge es zu deinem **PATH** hinzu.

2️⃣ **Python-Abhängigkeiten installieren:**  
```bash
pip install -r requirements.txt
```

3️⃣ **Projekt klonen:**  
```bash
git clone https://github.com/cherzlieb/py-video-to-audio.git
cd py-video-to-audio
```

### 🚀 **Benutzung**

4️⃣ **Venv starten:**  
```bash
source .venv/bin/activate
```

**Tool starten:**  
```bash
python main.py
```
5️⃣ **MP4-Dateien auswählen**  
6️⃣ **Zielordner festlegen**  
7️⃣ **Audioformat & Qualität einstellen**  
8️⃣ **Konvertierung starten & Fortschritt beobachten**  
9️⃣ **Falls nötig: Abbrechen**  

---

### 📝 **Technologien**
🔹 **PySide6** → GUI mit Qt  
🔹 **FFmpeg** → Audio-Konvertierung  
🔹 **Multithreading mit QThread** → Verhindert GUI-Blockaden  
🔹 **Python 3.x** → Für maximale Kompatibilität  

---

### 🛠 **To-Do / Weiterentwicklungen**
🔹 **Batch-Verarbeitung für mehrere Ordner**  
🔹 **Fehlermeldungen & Logging verbessern**  
🔹 **Möglichkeit für benutzerdefinierte FFmpeg-Kommandos**  
🔹 **UI-Optimierungen für bessere Bedienbarkeit**  

---

## 📜 Lizenz
Dieses Projekt steht unter der [MIT License](https://github.com/cherzlieb/py-video-to-audio/blob/main/LICENSE).


