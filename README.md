📌 Background

Keyloggers are tools that record keystrokes and sometimes collect additional data such as audio, screenshots, or Wi-Fi credentials.

The two main types:

User-based keyloggers (API level) – common, intercept keyboard signals at user level.

Kernel-based keyloggers (OS level) – rare, complex, harder to detect/remove, often implemented as rootkits.

This project demonstrates a user-level keylogger in Python, exploring attacker techniques while emphasizing confidentiality, integrity, ethical hacking, and detection.

From a defensive view, this work shows how security teams can detect Indicators of Compromise (IoCs) such as hidden directories, renamed processes, or unusual SMTP traffic.

🚀 Project Details

I originally considered both user-level and kernel-level approaches, but macOS restrictions (System Integrity Protection, signed kernel extensions) made kernel-level work impractical.

Instead, I focused on a user-level implementation with extended features:

Keystroke logging

Continuous screenshots

Audio recording

Wi-Fi password retrieval (macOS Keychain)

Data exfiltration via SMTP

🔧 Implementation

Language & Libraries: Python, pynput, Pillow, sounddevice, soundfile, smtplib.

Logging: Captures keystrokes into hidden directory files (keylog.txt).

Screenshots: Captured at regular intervals in a separate thread to prevent blocking.

Audio Recording: Saved as .wav files with timing synced to email delivery.

Wi-Fi Password Retrieval: Used subprocess with macOS networksetup and security commands.

Exfiltration: Periodically sent files via SMTP with MIME attachments.

Stealth: Process renamed (e.g., system-update.py), hidden directory storage, background execution with nohup.

Concurrency: Solved logging/screenshot conflicts using multithreading.

🚧 Limitations

macOS security restrictions (SIP, notarisation, permissions) limited stealth and automation.

Cross-platform support: Windows build partially tested, reduced functionality.

SMTP provider limits: Free tier (200 emails/day, 5 MB attachments).

Detection: User-level keylogger → not stealthy against AV/EDR.

Compilation: macOS executable creation restricted, required Windows environment.

🔮 Future Work

Dynamic SSID-to-account mapping (regex parsing).

Full cross-platform compatibility (Windows/Linux).

Server-based exfiltration (instead of SMTP).

Encryption of stored and transmitted data.

Advanced process concealment (phishing delivery, binary disguise).

⚖️ Ethical Considerations

Developed in a controlled academic environment.

No unauthorized testing performed.

Aimed to understand attacker techniques to strengthen SOC detection.

Highlights defender IoCs: hidden folders, renamed processes, outbound SMTP traffic.

Reinforces responsible use, privacy awareness, and defensive application of malware research.

📚 References

Binary IT – Types of Keyloggers and Examples

Apple Support – System Integrity Protection

GeeksforGeeks – Send Automated Email in Python

Python Docs – os.path.expanduser

Python Docs – subprocess

Python Docs – pynput

SoundDevice – Recording and Playback of Audio

Time Champ – Keylogger Software & Legal Implications

YouTube:

Get WiFi Info on macOS with Python

Create an Advanced Keylogger in Python

David Bombal – Python Remote Keylogger
