<div align="center">

# Kick Follow Manager

**Export and re-follow all your Kick.com channels automatically**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Chrome](https://img.shields.io/badge/Chrome-Required-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://www.google.com/chrome/)
[![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](LICENSE)

[Demo](https://pkkls.github.io/Kick-follow-Manager) • [Report Bug](../../issues) • [Request Feature](../../issues)

<img width="499" alt="Preview" src="https://github.com/user-attachments/assets/41b1b7ff-4e5f-4d24-af00-eb6a438cd016" />

</div>

---

## ✨ Features

<table>
<tr>
<td>

**🔒 Stealth Mode**  
Uses undetected-chromedriver to bypass bot detection

</td>
<td>

**🌍 Bilingual**  
English / 日本語 menu at startup

</td>
</tr>
<tr>
<td>

**🧹 Smart Parser**  
Auto-cleans duplicates, LIVE tags, headers

</td>
<td>

**📄 Auto Reports**  
Timestamped logs for every run

</td>
</tr>
</table>

## 🚀 Quick Start
```bash
# Install dependencies
pip install undetected-chromedriver selenium

# Run the script
python kick_selenium.py
```

## 📖 Usage Guide

### Step 1: Export your follows

1. Visit `kick.com/following` on your source account
2. Scroll to the bottom of your follows list
3. Copy everything (`Ctrl+A` → `Ctrl+C`)
4. Paste into `kick_follows.txt`

✅ No need to clean the file — the script handles duplicates, LIVE suffixes, headers and blank lines automatically.

### Step 2: Run and follow

The script will:
- Open Chrome in stealth mode
- Prompt you to log in manually
- Process your list and follow each channel
- Generate a detailed report

## 📁 Project Structure
```
kick-follow-manager/
├── kick_selenium.py      # Main script
├── kick_follows.txt      # Your exported follows (one per line)
└── reports/              # Auto-generated reports
```

## ⚙️ Requirements

- Python 3.8 or higher
- Google Chrome (latest version)
- Active Kick.com account

## 📝 Notes

- **No API key needed** — manual login only
- **No data stored** — all processing is local
- **Cross-platform** — Works on Windows, macOS, Linux

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

Made with ❤️ for the Kick community

[⬆ Back to top](#kick-follow-manager)

</div>
