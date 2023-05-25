# Honeypot

Welcome to this repository!

This project is between a medium and high interaction honeypot : external requests won't *actually* interact with an information system but will *pretend* to do so.

How does it works?

Basically, using RegExes, if a requests looks like a valid HTTP protocol GET request, it will match agains a rule and be answered with HTTP content.

If another request looks like a SQL injection tentative on a WordPress, it might be anwered accordingly to simulate a WordPress environment.

We aim to simulate interaction, but there is actually no potentially vulnerable database or filesystem for attackers to exploit.


---

# Getting Started

## Prerequisites

- python3
- python3-pip
- openssl

> **Note** : As of today, deployment has been imagined with Debian-like systems in mind. More portable versions and companion scripts will come later.

```
git clone https://github.com/FenrirSec/honeypot
```

---

# Which protocols are working for the moment?

- [] Telnet :white_check_mark:
- [] POP :white_check_mark:
- [] SMTP :white_check_mark:
- [] POP :white_check_mark:
- [] HTTP :white_check_mark:
- [] ADB :white_check_mark:
- [] SSH :white_check_mark:

---

# Todolist

- Quality of life improvements
- Add more potentially interesting protocols
- Make RSA encryption MiTM proof with honeypot's private key verification
- Make HTTPS management safer with Ingress server certificate pinning
- Add templates to simulate IoT devices