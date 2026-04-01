Kick-follow-Manager
Export and re-follow all your Kick.com channels on a new account — automatically, with stealth Chrome and smart paste parsing.
🌐 Project Page
👉 pkkls.github.io/Kick-follow-Manager

✨ Features

🕵️ Stealth Chrome — uses undetected-chromedriver, bypasses bot detection
🌍 Bilingual UI — English / 日本語 menu at startup
🧹 Smart parser — paste anything (raw copy, artifact format, duplicates, LIVE suffixes) and the script cleans it automatically
🔒 No token needed — you log in manually, no API key or credentials stored
📄 Auto report — generates a timestamped .txt report after each run (followed / already / failed)
🖥️ Cross-platform — Windows, macOS, Linux


📦 Files
FileDescriptionkick_selenium.pyMain script (stealth Chrome + bilingual UI)kick_follows.txtYour exported follows list (one channel per line)

🚀 Quick Start
bashpip install undetected-chromedriver selenium
python kick_selenium.py

📋 How to export your follows

Go to kick.com/following on your source account
Scroll all the way to the bottom of your list
Press Ctrl+A then Ctrl+C to select and copy everything
Paste the result into kick_follows.txt


✅ No need to clean the file — the script handles duplicates, LIVE suffixes, headers and blank lines automatically.


📋 Requirements

Python 3.8+
Google Chrome installed (version auto-detected)


🖼️ Preview
<img width="499" height="512" alt="Kick Follow Manager preview" src="https://github.com/user-attachments/assets/41b1b7ff-4e5f-4d24-af00-eb6a438cd016" />
