# Honeypot 🕵️‍♂️

Welcome to our Honeypot repository! This project is designed as a medium to high interaction honeypot: external requests won't actually interact with a real information system but will convincingly pretend to do so.

## How Does It Work? 🤔

Basically, using RegExes, if a requests looks like a valid HTTP protocol GET request, it will match agains a rule and be answered with HTTP content.

If another request looks like a SQL injection tentative on a WordPress, it might be anwered accordingly to simulate a WordPress environment.

We aim to simulate interaction, but there is actually no potentially vulnerable database or filesystem for attackers to exploit.

---

## Getting Started 🚀

### Prerequisites

- python3
- python3-pip
- openssl

> **Note**: Deployment is currently optimized for Debian-like systems. More portable versions and companion scripts are in development.

```bash
git clone https://github.com/FenrirSec/honeypot
```

---

## Docker Deployment

```bash
docker run --rm lupinfr/honeypot
```

---

## Supported Protocols ✅

- Telnet 
- POP 
- SMTP 
- HTTP 
- ADB 
- SSH 

---

## Todolist 📝

- Quality of life improvements
- Add more interesting protocols
- Make RSA encryption MiTM proof with honeypot's private key verification
- Make HTTPS management safer with Ingress server certificate pinning
- Add templates to simulate IoT devices

Dive in, explore, and help us create a more deceptive and expansive honeypot! 🔍
