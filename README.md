### Background

Keyloggers are a type of invasive software (or hardware) that stealthily records and monitors every keystroke you make on a pc or a mobile device. There’s various types of keyloggers. The main types I researched were:

**User-based keyloggers** which operate at the API level are the most common type of keylogger software. Their job is to intercept keyboard signals and send them to the program. This is the type I have implemented with additional functionalities.

**Kernel-based keyloggers** operate at the core of the operating system, making them difficult to detect and remove. They are complex and difficult to write, so they aren't very common. Many kernel-level keyloggers are crafted as rootkits, which can subvert an operating system's kernel and steal data.

Understanding and developing keyloggers ties closely to key cybersecurity principles like **confidentiality**, **integrity**, and **ethical hacking**. Keyloggers can breach confidentiality by capturing sensitive information, such as passwords and private conversations. My project shows how attackers could use user-level keyloggers to compromise this principle, stressing the importance of strong detection methods, thorough system monitoring, and user education to prevent such attacks.

From an **ethical hacking** point of view, my project demonstrates how building and testing keylogger functions can help security professionals improve their defenses. By adding features like audio recording, continuous screenshots, and Wi-Fi password retrieval, I explored multiple potential attack methods that real attackers might use. This provides valuable insight into how to better protect systems from unauthorised data collection.

**Social engineering** is often used to deploy keyloggers, where attackers rely on tricking users into running malicious software. For example, if I had hidden my keylogger in a phishing link or a disguised file, it would show how attackers combine technical skills with psychological tactics to bypass security. 

### Project Details

I had initially thought of creating both a user level and a kernel level keylogger. However, on researching more into the idea of a kernel level keylogger, I realised how tricky it would be to get around, especially working on a mac (see limitations). So I went with a user level keylogger instead with different functionalities. **This project is completely for educational purposes.**

The keylogger I developed can do more than just record keystrokes. Once installed, it also captures audio, takes continuous screenshots, and attempts to retrieve the Wi-Fi password of the connected network. All collected information is then compiled and sent in bulk to my Gmail account using SMTP.

### **Implementation Details**

**Keylogger Implementation**

I built the keylogger using Python's `pynput` library, allowing for the capture of keystrokes at the user level. The captured keystrokes were stored in a buffer and written to a log file (`keylog.txt`) located in a hidden directory for security. 

**Initial Format Issues**: One of the challenges faced was ensuring that the keystrokes were logged in a clean, horizontal format. Initially, the output included newlines or special characters that disrupted readability. I improved this by appending characters directly to a buffer and flushing the buffer after specific key presses (e.g., space, enter), ensuring the output remained continuous and easy to read.

**Snippet**:

![Screenshot 2024-11-04 at 1.24.52 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/4651de9a-9c25-4abc-a258-8ca9f0684c7c/e315ac7a-7a4a-44c0-be57-3a7fc8120fe1/Screenshot_2024-11-04_at_1.24.52_PM.png)

**Screenshot Functionality**

Screenshots were captured using the `Pillow` library's `ImageGrab` module at regular intervals and saved in the hidden directory. (I researched the different practices for implementing screenshot capture in Python and found `Pillow` to be the most robust due to its cross platform support.) The code for capturing screenshots was run in a separate thread to avoid blocking the main program. 

**Challenge**: At first, the program would get stuck in a loop when capturing screenshots, which stopped the keylogger from updating the log in real time. This issue happened because the screenshot capture and keylogging processes were clashing. I fixed this concurrency problem by improving how the threads were managed, making sure the screenshot capture ran in a separate thread without interfering with the keylogger.

**Solution**: I used Python threading to separate the screenshot-taking functionality from the main keylogging process, allowing both operations to run smoothly without conflict.

**Snippet**:

![Screenshot 2024-11-04 at 2.43.28 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/4651de9a-9c25-4abc-a258-8ca9f0684c7c/ba2b2f6e-d9aa-4e9e-9382-efe9196bd8fb/Screenshot_2024-11-04_at_2.43.28_PM.png)

**Audio Recording Functionality**

The audio recording functionality was implemented using the `sounddevice` and `soundfile` libraries. The audio was captured for a set duration and saved as `audio_rec.wav` in the hidden folder.

**Challenge**: While the basic implementation was straightforward, I ran into problems making sure the recording lengths were consistent and avoiding errors with the sampling rates. 

I also had to make sure that the audio recording interval matched the emailing interval; otherwise, the email would be sent before the audio file was finished recording, which meant the audio wouldn't be included in the attachment. This required coordinating the timing of both processes to ensure all files were ready when the email was sent.

**Snippet**:

![Screenshot 2024-11-04 at 2.43.45 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/4651de9a-9c25-4abc-a258-8ca9f0684c7c/222564d3-f47f-4d0b-b6a2-d4bd34187431/Screenshot_2024-11-04_at_2.43.45_PM.png)

**Wi-Fi Password Retrieval**

The Wi-Fi password retrieval feature was the most challenging and time-consuming part of the project. It involved using `subprocess` to run macOS commands (`networksetup` and `security`) to extract stored Wi-Fi passwords from the Keychain. I applied principles from COMP2041, like using shell commands and mapping data effectively, to make this work. The process involved mapping SSIDs to account names to ensure the correct passwords were retrieved.

**Challenges**:

- **Understanding Keychain Storage**: I spent time researching how Wi-Fi passwords and credentials are stored and accessed in Keychain Access on a mac.
- **Command Execution and Debugging**: Revising the `subprocess` commands based on security principles learned in prior courses was essential to effectively run and parse outputs. Debugging this part of the project took the longest, but it now works reliably on two known networks.

**Future Improvement**:

- The current implementation uses a hardcoded mapping of SSIDs to accounts, which limits its scalability. This can be addressed in the future by implementing a more dynamic solution to automatically retrieve SSID-to-account mappings. A potential enhancement is using a script that automatically scrapes SSID-to-account mappings from the Keychain. This would allow for more flexibility and support for additional networks. This would have taken a while, so I left it for now. In essence, what I would have done is parse the command output with regex to extract SSID-to-account mappings, so it could be applied to different networks automatically.

**Snippet:**

![Screenshot 2024-11-04 at 1.33.34 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/4651de9a-9c25-4abc-a258-8ca9f0684c7c/6fa23d41-ec2a-4e35-979c-fe9a0bb81159/Screenshot_2024-11-04_at_1.33.34_PM.png)

**Limitation**: This method still required manual permission approvals for accessing Keychain data, limiting automation. Another limitation is that the code is specifically designed for macOS, as it relies on macOS's Keychain Access and commands like `security find-generic-password`. This makes it incompatible with Windows or other non-macOS devices.

**Emailing Functionality**

I set up the functionality for sending emails with attachments using Python's `smtplib` and `email.mime` libraries. This allowed me to send compiled logs and captured data periodically to my Gmail account.

**Challenge**: I needed to research and integrate SMTP server details, which included setting up a Mailtrap account for testing. Finding the appropriate code for securely sending attachments from the website also required additional effort.

**Solution**: I managed to integrate the email-sending code into the project and used threading to automate the process. This helped ensure that the emails were sent without interfering with other parts of the system. 

**Snippet**:

![Screenshot 2024-11-04 at 1.37.12 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/4651de9a-9c25-4abc-a258-8ca9f0684c7c/25f027b2-4d08-42bd-8045-350dae9f6d8a/Screenshot_2024-11-04_at_1.37.12_PM.png)

**How it runs:**

To run my keylogger, I execute it as a background process or compile it into an executable file to deploy on other systems. 

As I researched keylogger detection methods, I came up with ways to hide my program. 

**Key Techniques for Stealth Operations:**

1. Disguising the Process

- **Renaming the Process**: I renamed my main python file to `system-update.py` so whenever it runs in the task manager, it appears to be a computer induced operation instead of a stealthy keylogger.
- **Binary Path Placement**: I store the documents in a hidden directory using  `os.path.join(os.path.expanduser("~"), ".hiddenfolder")` ensures that it remains out of sight during  system checks, and works on all macs irrespective of user path.

2. Running as a Background Process

- I could also run it as a background process on a computer without having to open vscode. I open my terminal and run it as an unending process using the commad **`nohup python3 system-update.py &` ;**This command runs the script in the background and makes sure it continues running even after I close the terminal. The process runs quietly in the background, so I don’t need to worry about it stopping when the terminal is shut.

### **Limitations and problem list:**

- Initially, I was saving all generated files and logs in a hidden folder specific to the user’s home directory on my system, this made it incompatible to run on different devices devices due to hardcoded user paths. To solve this, I used `os.path.expanduser()` . This method allows you to save files in a user's home directory without hardcoding the username.
- **User-Based Keylogger Detection**: My project is a user-level keylogger, which isn’t super hard to detect. I couldn’t build a kernel-level keylogger due to:
    - **System Integrity Protection (SIP)**: This macOS feature blocks root access to key system files.
    - **Signed Kernel Extensions:** macOS needs kernel extensions to be approved and signed with an Apple Developer ID, making kernel-level work almost impossible.
- **Permission Issues on macOS**: The program requires a range of permissions to run effectively on macOS, such as input monitoring and file access permissions. These must be granted manually, which reduces the stealth and ease of use.
- **Cross-Platform Issues**: While I managed to create an executable (.exe) version of the keylogger for a friend’s Windows computer, converting macOS-specific code to work smoothly on Windows was tricky and reduced functionality.
- **Compilation Challenges**: Creating an executable on macOS was a headache due to strict security protocols. I needed a friend with Windows to compile it and turn it into an executable, and had to tweak it by removing mac-specific parts, which was time-consuming.
- **Security Restrictions on macOS**: Sharing and running executable versions on macOS is difficult due to Apple's security measures, such as notarisation requirements and System Integrity Protection (SIP).
- **Disguise Limitations**: My keylogger isn’t disguised as malware, which makes it more detectable. For better hiding, I would need to disguise it as a legitimate-looking link in a phishing email or embed it within another piece of software.
- **SMTP Provider Limitations**: The current SMTP provider is a demo service that limits me to sending 200 emails per day and has a maximum attachment size of 5 MB per email. While this is sufficient for short-term testing, a more robust and scalable solution would require a paid service. The emails were also taking a while to send, which made it harder to debug issues.

### **Future Developments**

- **Dynamic SSID-to-Account Mapping**: I want to improve the Wi-Fi password retrieval feature by adding a script that automatically pulls SSID-to-account mappings from `security` command outputs using regex. This would make the process more adaptable and remove the need for hardcoded information.
- **Cross-Platform Compatibility**: I plan to modify the code so it can run on Windows and Linux by using alternatives to macOS modules. This would help ensure all features, like keylogging, taking screenshots, and recording audio, work properly on different operating systems.
- **Advanced Process Concealment**: I’m looking into making the keylogger more hidden by embedding it into phishing emails or disguising it within another harmless-looking program. This would help bypass detection from users and antivirus software.
- **Server-Based Data Transfer**: Instead of sending files via email, I want to explore renting a server where data can be sent directly. This would allow me to manage larger files, avoid email limits, and make data transfer more efficient and secure.
- **Encryption:** Implementing encryption in the future is another key goal. This would protect the data during transmission and storage, ensuring that sensitive information remains secure even if intercepted.

### **Ethical Issues and Considerations**

Developing a keylogger required me to think about the ethical and legal implications involved, especially since this type of software can capture private data without the user knowing. Here are the key points I kept in mind:

- **Privacy Concerns**: Keyloggers can record sensitive data like passwords and personal messages, which raises major privacy issues. Collecting data without consent is both unethical and potentially dangerous.
- **User Consent**: Ethically, any software like this should include clear user consent. My project doesn’t have a consent feature, which would be an issue if used without proper authorisation.
- **Risk of Misuse**: Although my project is for educational purposes, it’s important to recognise that keyloggers can be abused for harmful reasons, leading to data theft or unwanted surveillance. This type of project should only be used in legal, controlled settings.
- **Security and Responsibility**: I made sure to use and demonstrate this tool in a secure, monitored environment to avoid unauthorised use or copying of the code.
- **Educational Purpose**: The project’s goal was to learn and raise awareness about security vulnerabilities, not to misuse them. It stressed the importance of responsible practices to strengthen cybersecurity defenses.

### Conclusion

Doing this project was indeed a great learning experience. Facing the above challenges pushed me to find creative solutions and adapt my project as I went along. For example, I learnt a lot about macOS permissions and how to work within them. Debugging the concurrency issues taught me how to use multithreading to keep everything running smoothly. This process definitely improved my problem-solving skills and made me more confident with practical coding techniques.

I also made sure to act professionally by doing thorough research, documenting my work clearly, and being open to feedback by peers. I took ethical considerations seriously, focusing on educational use and responsible handling of this kind of software. These steps showed my growth and ability to balance technical challenges with an awareness of real-world cybersecurity concerns. All in all, I feel fortunate to have an opportunity of working on a project like this.

### **References**

1. Binary IT. *Types of Keyloggers and Examples*. Available at: https://binaryit.com.au/types-of-keyloggers-and-examples/. Accessed: 24 October 2024.
2. Apple Support. *Understanding System Integrity Protection on your Mac*. Available at: https://support.apple.com/en-au/guide/deployment/depa5fb8376f/web. Accessed: 25 October 2024.
3. GeeksforGeeks. *How to Send Automated Email Messages in Python*. Available at: https://www.geeksforgeeks.org/how-to-send-automated-email-messages-in-python/. Accessed: 28 October 2024.
4. Python Documentation. *os.path.expanduser()*. Available at: https://docs.python.org/3/library/os.path.html#os.path.expanduser. Accessed: 1 November 2024.
5. Python Documentation. *subprocess – Subprocess Management*. Available at: https://docs.python.org/3/library/subprocess.html. Accessed: 1 November 2024.
6. Python Documentation. *pynput – Monitor and Control Input Devices*. Available at: https://pynput.readthedocs.io/en/latest/. Accessed: 2 November 2024.
7. SoundDevice Library. *Recording and Playback of Audio*. Available at: https://python-sounddevice.readthedocs.io/en/0.4.5/. Accessed: 28 October 2024.
8. Time Champ. *Keylogger Software and Legal Implications for Maximizing Security*. Available at: https://www.timechamp.io/blogs/keylogger-software-and-legal-implications-for-maximizing-security/. Accessed: 4 November 2024.

**youtube videos:**

1. Keith, the Coder (2017). *Get Wifi Information with Python on Mac OSx*. [online] YouTube. Available at: https://www.youtube.com/watch?v=EKmq0TBRSSo. Accessed 28 October 2024.
2. www.youtube.com. (n.d.). *Create an Advanced Keylogger in Python - Crash Course*. [online] Available at: https://www.youtube.com/watch?v=25um032xgrw. Accessed 29 October 2024
3. David Bombal (2022). *Warning! Python Remote Keylogger (this is really too easy!)*. [online] YouTube. Available at: https://www.youtube.com/watch?v=LBM3EzBXhdY Accessed 29 October 2024.
