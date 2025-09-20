Disclaimer: This project is for educational and research purposes only. It was developed to study attacker methodologies, stealth techniques, and detection methods, with the goal of improving defensive awareness in cybersecurity.

**Background**

Keyloggers are tools that record keystrokes and sometimes capture additional data such as screenshots or audio. They can be deployed in attacks through methods like social engineering or phishing.

This project demonstrates how a user-level keylogger can be built in Python, along with added features such as:

Keystroke logging

Continuous screenshots

Audio recording

Wi-Fi password retrieval

Data exfiltration via SMTP

The intent is to explore how attackers operate and, more importantly, how defenders can recognize Indicators of Compromise (IoCs) like hidden directories, renamed processes, or unusual outbound email activity.


**Project Details
**
Implemented with Python (pynput, sounddevice, PIL, smtplib).

Designed to log keystrokes, capture screenshots, and record audio in parallel using multithreading.

Stores files in a hidden directory for stealth.

Exfiltrates data via email using SMTP.

Explored OS-specific limitations (macOS SIP, Keychain permissions, Windows compilation challenges).

**Limitations
**
macOS security restrictions (SIP, notarisation, permissions) limited automation.

Cross-platform support (Windows/Linux) only partially tested.

SMTP provider limits email size/volume (demo service).

User-level keylogger → easier to detect than kernel-level alternatives.

**Future Improvements
**

Cross-platform support (Windows/Linux).

Dynamic SSID-to-Account mapping for Wi-Fi retrieval.

Server-based exfiltration instead of SMTP.

Encryption for logs and transmissions.

Advanced process concealment (disguised binaries / phishing delivery in simulated settings).

**Ethical Considerations
**
This project was conducted in a controlled, academic environment.

No unauthorized systems were tested.

Purpose is to improve understanding of attacker TTPs and defensive strategies.

Key takeaway: defenders can strengthen SOC operations by monitoring IoCs like hidden processes, renamed binaries, and suspicious outbound traffic.

**Skills & Takeaways
**
Python scripting for cybersecurity

Threat research & malware analysis (educational)

Multithreading & concurrency handling

OS security restrictions (macOS SIP, Windows executables)

SOC awareness: identifying attacker stealth methods and IoCs

Ethical awareness in security research
