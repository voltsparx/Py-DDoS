# Py-DDoS Simulator

**Py-DDoS Simulator** is an ethical cybersecurity demonstration tool designed for educational purposes and authorized security testing.  
It allows users to simulate various types of DDoS attacks in a controlled environment to understand their impact and test defensive measures.

---

## ⚠️ WARNING

> **This tool is for educational and ethical testing purposes only.**
>
> **Unauthorized use against networks or systems you do not own or have explicit permission to test is illegal.**
>
> Use responsibly and only in environments you own or have written permission to test.

---

## Features

- Multiple attack vectors: HTTP/HTTPS Flood, TCP SYN Flood, UDP Flood, ICMP Flood, Slowloris
- Configurable target, port, threads, and duration
- Optional Tor proxy support for anonymity
- Real-time statistics and colorful UI (with [rich](https://github.com/Textualize/rich))

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Py-DDoS.git
   cd Py-DDoS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

```bash
python py-ddos.py
```

Follow the interactive prompts to configure your test attack.

---

## Example

```text
$ python py-ddos.py

╔══════════════════════════════════════════════════════════════╗
║                 Py-DDoS Simulator v2.0                       ║
║                 Ethical Demonstration Tool                   ║
║                 Author: voltsparx                            ║
║                 Contact: voltsparx@gmail.com                 ║
╚══════════════════════════════════════════════════════════════╝

[... warning and configuration prompts ...]
```

---

## Requirements

- Python 3.7+
- See `requirements.txt` for Python dependencies

---

## License

This project is released under the MIT License.

---

## Author

- **voltsparx**  
  Contact: voltsparx@gmail.com

---

## Disclaimer

The author assumes no liability for misuse of this tool.  
Always obtain proper authorization before conducting
