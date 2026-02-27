# RedLoad-X v8.0 - Operational Network Stress Testing Tool

*Originally released as **Py-DDoS**; project was rebranded to RedLoad-X with v7.5 for clarity and improved scope.*

**Author:** voltsparx  
**Contact:** voltsparx@gmail.com  
**Version:** 8.0  

---

## ⚠️ LEGAL DISCLAIMER

**THIS TOOL IS FOR AUTHORIZED TESTING AND EDUCATIONAL PURPOSES ONLY**

Unauthorized access to computer systems is **ILLEGAL** under laws including:
- **Computer Fraud and Abuse Act (CFAA)** - United States
- **Computer Misuse Act** - United Kingdom
- **Similar laws in virtually all countries**

**You are legally responsible for:**
- Obtaining explicit written authorization before testing
- Ensuring legitimate security testing purposes
- Complying with all applicable laws in your jurisdiction

**Misuse may result in:**
- Criminal prosecution and imprisonment
- Civil liability and substantial fines
- Career destruction and permanent record

**Author (voltsparx) assumes NO LIABILITY for misuse of this tool.**

---

## Table of Contents

1. [Overview](#overview)
2. [What's New in v8.0](#whats-new-in-v80)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Features](#features)
6. [Attack Types](#attack-types)
7. [Usage Guide](#usage-guide)
8. [Safety Systems](#safety-systems)
9. [Metrics & Reporting](#metrics--reporting)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [Development](#development)
13. [Contributing](#contributing)
14. [References](#references)

---

## Overview

**RedLoad-X** is a network stress testing tool for security professionals and students. It enables authorized testing of network resilience across multiple OSI layers with robust safety mechanisms, real-time metrics collection, and interactive reporting.

### Key Characteristics
- ✅ **8 Attack Vectors** - Multiple OSI layers (L3-L7)
- ✅ **Layered Safety** - Multi-layer protection with audit trails
- ✅ **Real-Time Metrics** - 30+ data points tracked automatically
- ✅ **Detailed Reports** - Interactive HTML charts + analysis
- ✅ **Educational Framework** - Detailed learning resources
- ✅ **TOR Integration** - Optional anonymity layer
- ✅ **Dual Interface** - Interactive menu + CLI + Programmatic
- ✅ **Extensive Logging** - Audit trails for compliance

---

## What's New in v8.0

### v8.0 Release Notes

The 8.0 release consolidates the previous 7.5.1 changes and marks a major
milestone.  Highlights include:

- Added **warn-only safety mode** (`--warn-only-locks`) allowing warnings without
  blocking operations (ideal for demonstrations).
- Added unit tests for safety lock behaviours.
- Updated documentation and metadata to reflect the new version.

### 1. Enhanced Safety Locks System
- **Audit Trail Logging** - Every security check is logged with timestamp
- **Resource Impact Estimation** - Predicts CPU/memory usage before execution
- **Risk Assessment Reports** - Comprehensive analysis before running attack
- **Granular Control** - Enable/disable individual safety checks
- **Enhanced Authorization** - Multi-step verification for external targets
- **Script-Friendly Mode** - auto_confirm for automation/CI

**Protections Include:**
- High thread count warnings (CPU impact detection)
- Long duration alerts (prevents runaway tests)
- External target authorization (written permission required)
- TOR implications warnings
- Customizable thresholds

### 2. Real-Time Metrics Collection (NEW)
**Core Module:** `core/metrics.py`

Automatically tracks 30+ metrics throughout test execution:
- Requests per second (RPS)
- Success/failure rates
- HTTP status code distribution
- Response time statistics (min/max/mean/median/stdev)
- Bandwidth consumption (MB/s)
- Connection state analysis
- Time-series data for graphing
- Automatic educational insights

### 3. Improved Reporting System (NEW)
**Core Module:** `core/reporter_v2.py`

Generates detailed reports with interactive visualizations:

**HTML Reports Feature:**
- Interactive Chart.js graphs (v4.0)
- Response time distribution charts
- HTTP status code breakdown (doughnut)
- Connection state analysis (pie chart)
- Responsive mobile-friendly design
- Gradient styling
- Print-optimized layout
- Embedded CSS (no external files needed)

**TXT Reports Feature:**
- Comprehensive metrics analysis
- Status code distribution
- Educational insights
- Configuration details
- Plain-text for grepping/parsing
- Legal disclaimers

420+ lines of conversational guide including:
- 30-second quick start
- Architecture overview
- Core module explanations
- Code examples
- Troubleshooting guide
- Development notes
- Security disclaimer
- Learning resources

### 4. Code Quality Enhancements

All 18 code quality issues fixed:
- ✅ Duplicate methods removed (~150 lines)
- ✅ API mismatches resolved
- ✅ Missing imports added
- ✅ Memory leaks fixed (bounded RPS history)
- ✅ IP validation improved (using ipaddress module)
- ✅ CPU-aware threading (cores * 200)
- ✅ Exception handling improved (specific exceptions)
- ✅ Authorization enforcement added
- ✅ Attack type safety (Enum prevents typos)
- ✅ Configuration validation (comprehensive 42-line check)

---

## Installation

### Requirements
- **Python 3.8+**
- **Windows, Linux, or macOS**
- **pip** (Python package manager)

### Step 1: Clone Repository

```bash
git clone https://github.com/voltsparx/RedLoad-X.git
cd RedLoad-X  # rename directory after clone if desired
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python redload-x.py --version  # or python py-ddos.py for compatibility
python redload-x.py --help     # or python py-ddos.py for compatibility
```

### Requirements.txt

```
requests>=2.28.0
rich>=13.0.0
matplotlib>=3.5.0
scapy>=2.5.0
stem>=1.8.0
urllib3>=1.26.0
```

---

## Quick Start

### Interactive Mode (Recommended for Learning)

```bash
python redload-x.py  # or python py-ddos.py (legacy)
```

**You'll be prompted for:**
1. Target IP/hostname
2. Target port
3. Attack type (HTTP, SLOWLORIS, UDP, SYN, etc.)
4. Number of threads
5. Attack duration
6. TOR anonymity (optional)
7. Safety confirmations
8. Final review before execution

### Command-Line Mode (Scripts & Automation)

```bash
# Basic HTTP flood
python redload-x.py -t example.com -p 80 -a HTTP -d 60 -c 100  # or py-ddos.py for backward compatibility

# Slowloris with TOR
python redload-x.py -t example.com -a SLOWLORIS -d 120 -c 200 --tor

# UDP flood
python redload-x.py -t 192.168.1.1 -a UDP -d 60 -c 500

# SYN flood (requires root/admin)
sudo python redload-x.py -t 192.168.1.1 -a SYN -d 60 -c 1000

# Load configuration
python redload-x.py --config my_test.json

# Save configuration
python redload-x.py -t example.com -a HTTP -c 100 -d 60 --save-config test.json
```
---

## Features

### Attack Types (8 Vectors)

| Attack Type | OSI Layer | Description | Root Required |
|------------|-----------|-------------|---------------|
| **HTTP** | L7 | HTTP GET/POST flood | No |
| **SLOWLORIS** | L7 | Slow client connections | No |
| **SLOWREAD** | L7 | Slow response reading | No |
| **UDP** | L4 | UDP packet flood | No |
| **SYN** | L4 | TCP connection exhaustion | Yes |
| **DNS** | L4 | DNS amplification | No |
| **ICMP** | L3 | ICMP echo flood | Yes |
| **NTP** | L4 | NTP amplification | No |

### Core Features

✅ **Multi-Vector Testing** - Layer 3 through Layer 7 attacks  
✅ **Safety-First Design** - Multi-layer protections enabled by default  
✅ **Real-Time Analytics** - 30+ metrics tracked automatically  
✅ **Detailed Reporting** - Interactive charts + analysis  
✅ **TOR Integration** - Optional anonymity with circuit rotation  
✅ **Dual Interface** - Interactive menu + command-line arguments  
✅ **Configuration Management** - Save/load attack configurations  
✅ **Extensive Logging** - Detailed audit trails  
✅ **Educational Resources** - Learning materials integrated  
✅ **Audit Trails** - Full compliance logging  

---

## Attack Types

### Layer 7 - Application Layer

#### 1. HTTP Flood
**What it does:** Sends rapid HTTP GET/POST requests to overwhelm the web server.

**How it works:**
- Randomized User-Agent strings
- Spoofed X-Forwarded-For headers
- Variable request parameters
- Multiple requests per thread

**Detection:** Standard IDS/WAF detects by request rate, missing cache headers, suspicious user agents.

```bash
python redload-x.py -t example.com -a HTTP -d 60 -c 200
```

#### 2. Slowloris
**What it does:** Keeps HTTP connections alive indefinitely by sending partial requests.

**How it works:**
- Establishes TCP connection
- Sends incomplete HTTP headers
- Periodically sends more headers (never completes)
- Server keeps connection open waiting

**Detection:** Slowloris signatures, incomplete requests, unusual connection duration.

```bash
python redload-x.py -t example.com -a SLOWLORIS -d 120 -c 500
```

#### 3. Slow Read
**What it does:** Reads server response extremely slowly, keeping connection open.

**How it works:**
- Establishes HTTP connection
- Sends valid HTTP request
- Reads response 1 byte per second
- Server waits for completion

**Detection:** Slow read signatures, unusual connection duration, stalled transfers.

```bash
python redload-x.py -t example.com -a SLOWREAD -d 180 -c 300
```

### Layer 4 - Transport Layer

#### 4. UDP Flood
**What it does:** Sends high-volume UDP packets to target.

**How it works:**
- Generates random UDP packets
- Variable payload sizes
- Rapid transmission rate
- No connection establishment

**Detection:** Packet rate analysis, unusual ports, source reputation.

```bash
python redload-x.py -t 192.168.1.1 -p 53 -a UDP -d 60 -c 500
```

#### 5. SYN Flood (Requires Root/Admin)
**What it does:** Floods target with TCP SYN packets with spoofed source IPs.

**How it works:**
- Crafts TCP SYN packets
- Randomizes source IP addresses
- Rapid transmission
- Prevents legitimate connections

```bash
sudo python redload-x.py -t 192.168.1.1 -a SYN -d 60 -c 1000
```

#### 6. DNS Amplification
**What it does:** Exploits DNS servers to amplify traffic toward target.

**How it works:**
- Sends DNS query with spoofed source IP
- DNS server sends large response to target
- Creates traffic amplification (small query → larger response)

```bash
python redload-x.py -t 8.8.8.8 -p 53 -a DNS -d 60 -c 200
```

#### 7. NTP Amplification
**What it does:** Exploits NTP protocol to amplify traffic.

**How it works:**
- Sends NTP MONLIST queries with spoofed source
- NTP servers respond with large MONLIST data
- Target receives amplified traffic

```bash
python redload-x.py -t 192.168.1.1 -p 123 -a NTP -d 60 -c 200
```

### Layer 3 - Network Layer

#### 8. ICMP Flood (Ping Flood - Requires Root/Admin)
**What it does:** Floods target with ICMP echo requests.

**How it works:**
- Generates ICMP echo requests
- Large random payloads
- Rapid transmission rate
- Responses consume bandwidth

```bash
sudo python redload-x.py -t 192.168.1.1 -a ICMP -d 60 -c 500
```

---

## Usage Guide

### Understanding Parameters

```
-t, --target HOST       Target IP or hostname
-p, --port PORT         Target port (default: 80)
-a, --attack TYPE       Attack type (HTTP, SLOWLORIS, UDP, SYN, SLOWREAD, DNS, ICMP, NTP)
-d, --duration SECONDS  Attack duration (default: 60)
-c, --threads COUNT     Number of threads (default: 100)
--tor                   Enable TOR anonymity
--config FILE           Load configuration from JSON
--save-config FILE      Save configuration to JSON
-l, --list-attacks      List all available attacks
-h, --help              Show help message
--version               Show version information
```

### Configuration Files

Create reusable configurations:

**File: `http_test.json`**
```json
{
  "target_host": "192.168.1.1",
  "target_port": 80,
  "attack_type": "HTTP",
  "threads": 100,
  "duration": 60,
  "use_tor": false,
  "authorized": true,
  "authorized_external": true
}
```

**Usage:**
```bash
python redload-x.py --config http_test.json  # legacy: py-ddos.py also works
```

### Examples by Scenario

#### Lab Environment Testing
```bash
python redload-x.py -t 192.168.1.100 -a HTTP -d 30 -c 50
```

#### Authorized Penetration Testing
```bash
# Step 1: Light test
python redload-x.py -t target.internal -a HTTP -d 10 -c 10

# Step 2: Moderate test
python redload-x.py -t target.internal -a HTTP -d 30 -c 50

# Step 3: Full-scale test
python redload-x.py -t target.internal -a HTTP -d 60 -c 200
```

#### Stress Testing Web Server
```bash
python redload-x.py -t example.com -a HTTP -d 120 -c 300
```

#### Testing TOR-Based Attacks
```bash
# Requires TOR daemon running
tor --controlport 9051
python redload-x.py -t example.com -a HTTP --tor -d 60
```

#### Batch Testing Multiple Attacks
```bash
for attack in HTTP SLOWLORIS UDP; do
  python redload-x.py -t example.com -a $attack -d 60 -c 100
  sleep 30
done
```

---

## Safety Systems

### Multi-Layer Protection

#### 1. Thread Count Protection
- **Warning:** > 500 threads
- **Critical:** > 2000 threads
- **Auto-adjustment:** CPU-aware scaling (cores * 200)

#### 2. Duration Limits
- **Warning:** > 10 minutes
- **Critical:** > 1 hour
- **Prevents:** Runaway tests

#### 3. External Target Authorization
- **Requirement:** Explicit written permission for non-local targets
- **Verification:** Multi-step confirmation
- **Logging:** All confirmations recorded

#### 4. TOR Usage Warnings
- **Implication:** Forensic consequences of anonymity
- **Requires:** User confirmation
- **Educational:** Explains implications

#### 5. Resource Impact Estimation
- **CPU Prediction:** Based on thread count
- **Memory Prediction:** Based on request size
- **Bandwidth Prediction:** Based on threads × payload

#### 6. Audit Trail Logging
**File:** `logs/safety_audit.json`

```json
{
  "timestamp": "2026-02-17T15:30:22Z",
  "check": "high_thread_count",
  "result": "PASSED",
  "details": {
    "threads": 500,
    "threshold": 2000,
    "cpu_impact": "medium"
  }
}
```

### Warning-Only Safety Mode

In some cases you may want to see all of the safety warnings without being
forced to acknowledge each one.  Use **warn-only** mode to convert the
interactive prompts into informational messages while still allowing the tool
to proceed:

```bash
# show warnings but never block
python redload-x.py --warn-only-locks
```

The same option can be specified on the CLI during a scripted attack, or it is
activated automatically when the `--warn-only-locks` flag is parsed.

### Disabling Safety Locks (detailed instructions)

```bash
# Requires explicit confirmation
python redload-x.py --no-safety-locks
```

### Customizing Thresholds

```python
from core.safety.safety_locks import SafetyLocks

locks = SafetyLocks()
locks.thresholds['thread_warning'] = 1000
locks.thresholds['duration_critical'] = 7200  # 2 hours
```

---

## Metrics & Reporting

### Real-Time Metrics Collected

During execution, tracks:
- **Request Metrics:** Total, successful, failed count
- **Performance:** RPS, bandwidth (MB/s)
- **Response Times:** Min, max, mean, median, stdev
- **HTTP Codes:** 200, 404, 503, timeout distribution
- **Connection States:** Established, timeout, refused
- **Time-Series:** Data points for graphing

### Report Generation

**Automatic Location:**
- HTML files saved under `reports/html/redloadx_report_YYYYMMDD_HHMMSS.html`
- TXT files saved under `reports/cli/redloadx_report_YYYYMMDD_HHMMSS.txt`

The base `reports` directory will be created automatically and subfolders
`html` and `cli` are used to keep formats separated.

#### HTML Report Contents
- Executive summary card
- Key performance metrics
- Interactive Chart.js graphs
  - RPS over time (line chart)
  - Response time distribution (bar chart)
  - HTTP status codes (doughnut chart)
  - Connection states (pie chart)
- Configuration details table
- Risk assessment section
- Educational insights
- Legal disclaimer
- Standard footer (author, contact, timestamp)

#### TXT Report Contents
- Plain text metrics summary
- Status code distribution table
- Connection state analysis
- Educational insights
- Configuration details
- Legal disclaimers
- Timestamp and author information

### Example Report Analysis

```
TOTAL REQUESTS: 50,000
SUCCESS RATE: 87.5%
AVERAGE RPS: 833.3
PEAK RPS: 1,245
BANDWIDTH: 45.2 MB/s
AVG RESPONSE TIME: 125ms
TARGET STATUS: Degraded performance
```

---

## Configuration

### Configuration File Format

```json
{
  "target_host": "example.com",
  "target_port": 80,
  "attack_type": "HTTP",
  "threads": 100,
  "duration": 60,
  "use_tor": false,
  "authorized": true,
  "authorized_external": true
}
```

### Required Fields
- `target_host` - IP or hostname
- `target_port` - Port number (1-65535)
- `attack_type` - One of: HTTP, SLOWLORIS, UDP, SYN, SLOWREAD, DNS, ICMP, NTP
- `threads` - Thread count (1-50000)
- `duration` - Seconds (1-3600)
- `authorized` - true (confirms understanding)
- `authorized_external` - true (for non-local targets)

### Optional Fields
- `use_tor` - true/false (default: false)

### Saving Configurations

```bash
python redload-x.py -t example.com -a HTTP -c 100 -d 60 --save-config my_config.json
```

---

## Troubleshooting

### Common Issues

#### "Target not found" Error
```
[-] Invalid target: xyz.invalid
```
**Solution:** Use valid IP or resolvable hostname
```bash
python redload-x.py -t 192.168.1.1  # Use IP directly
```

#### "Root required" Error
```
[-] SYN attack requires root/admin privileges
```
**Solution:** Run with sudo/admin privileges
```bash
sudo python redload-x.py -t 192.168.1.1 -a SYN -d 60
```

#### "TOR connection failed"
```
[-] TOR daemon not running on port 9051
```
**Solution:** Start TOR daemon
```bash
tor --controlport 9051
# Or use TOR Browser for automatic startup
```

#### "Port already in use"
```
[-] Address already in use
```
**Solution:** Wait for connections to close or use different port
```bash
python redload-x.py -t target.com -p 8080  # Try different port
```

#### "Scapy import error"
```
ImportError: No module named 'scapy'
```
**Solution:** Install required package
```bash
pip install scapy
```

#### "Safety check failed"
```
[-] High thread count exceeds safe limits
[-] External target requires written authorization
```
**Solution:** Review safety warnings and confirm authorization
```bash
python redload-x.py --no-safety-locks  # Only if truly authorized
```

#### "Low success rate during test"
- **Possible causes:** Target is defending, network issues, wrong port
- **Verification:** Check HTTP response codes in report
- **Solution:** Review target metrics, adjust parameters, verify authorization

#### "Out of memory during test"
- **Cause:** Too many threads keeping connections open
- **Solution:** Reduce thread count
```bash
python redload-x.py -t target.com -c 50 ...  # Instead of 500
```

---

## Development

### Architecture

```
redload-x/
├── redload-x.py              # Entry point with CLI parsing
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── SECURITY.md               # Legal and security framework
├── CONTRIBUTING.md           # Contribution guidelines
│
└── core/
    ├── __init__.py            # Package exports and helpers
    ├── engine/                # Core engine implementation
    │   ├── __init__.py        # RedLoadX class & helpers
    │   ├── async_engine.py    # Async HTTP flood support
    │   ├── rate_limiter.py    # Rate limiting utilities
    │   └── tor_handler.py     # TOR integration for engine
    ├── attacks/               # Attack-specific logic
    │   ├── attack.py          # Worker classes & attack methods
    │   ├── counters.py        # Thread-safe counters
    │   ├── metrics.py         # Legacy metrics helpers
    │   └── __init__.py
    ├── ui/                    # CLI/interactive interface code
    │   ├── banner.py          # ASCII/art and version banner
    │   ├── cli_menu.py        # Interactive menu system
    │   ├── help_menu.py       # Help output
    │   ├── about.py           # About prompts
    │   ├── colors.py          # ANSI color utilities
    │   └── __init__.py
    ├── logging/               # Logging subsystems
    │   ├── logger.py          # Human-readable logger
    │   ├── structured_logger.py # JSON logging
    │   └── __init__.py
    ├── safety/                # Safety lock implementations
    │   └── safety_locks.py
    ├── config/                # Configuration and metadata
    │   ├── config.py
    │   ├── metadata.py
    │   ├── optional_deps.py   # Optional dependency helpers
    │   └── __init__.py
    ├── tests/                 # Unit/integration tests
    │   ├── test_attacks.py
    │   ├── test_aiohttp_errors.py
    │   └── __init__.py
    └── reporter.py            # Unified report generator
```

### Core Modules

#### engine/ package - Attack Orchestration
Contains `RedLoadX` engine and related helpers (rate limiter, TOR handler, async
components). Coordinates attack execution, initializes threads, manages metrics,
generates reports.

**Key Classes/Methods:**
- `RedLoadX.start()` - Begin attack
- `RedLoadX.stop()` - Graceful shutdown
- `RedLoadX.get_metrics()` - Current statistics

#### safety/safety_locks.py - Multi-Layer Safety
Provides comprehensive protection with audit trails, now located under
`core/safety` package.

**Key Methods:**
- `check_all(config)` - Run all checks (honors warn-only mode)
- `print_risk_assessment(config)` - Show risks
- `_save_audit_trail()` - Log audit

**Features:**
- Warn-only mode (`--warn-only-locks`) shows warnings without blocking
- Granular lock enable/disable and thresholds
- Audit trail recording for each decision

#### metrics.py - Real-Time Analytics (NEW)
Collects 30+ metrics automatically.

**Key Methods:**
- `record_request()` - Record individual request
- `get_summary()` - Get metrics summary
- `get_educational_insights()` - Generate learning points

#### reporter_v2.py - Improved Reporting (NEW)
Generates detailed HTML and TXT reports.

**Key Methods:**
- `generate(metrics_data, config)` - Create both report types

### Adding New Features

#### Adding an Attack Type

1. Implement in `attacks.py` or `attacks_advanced.py`:
```python
def attack_my_type(self, target, port, threads, duration):
    # Implementation
    pass
```

2. Register in `engine.py`:
```python
self.attacks = {
    'HTTP': self.attack_http,
    'MY_TYPE': self.attack_my_type,
    # ...
}
```

3. Update argument parser in `redload-x.py`
4. Test thoroughly with safety locks enabled

#### Extending Metrics

```python
metrics.record_request(
    success=True,
    response_time=45.2,
    bytes_sent=1024,
    bytes_received=2048,
    status_code=200,
    connection_state='established',
    # Add custom fields as needed
)
```

### Code Quality Standards

- **Python 3.8+** compatibility
- **Type hints** where applicable
- **Comprehensive error handling** (specific exceptions, not bare except)
- **Detailed comments** for complex logic
- **Security-first** approach
- **Test coverage** before merging
- **Backward compatibility** maintained

---

## Contributing

### Getting Started

1. Read CONTRIBUTING.md
2. Review SECURITY.md for legal compliance
3. Check code quality standards above
4. Test thoroughly with safety locks

### Contribution Process

1. Test your changes thoroughly
2. Document changes clearly
3. Keep conversational tone in comments
4. Run all safety checks
5. Submit with clear explanation

### What We're Looking For

- ✅ Bug fixes
- ✅ Performance improvements
- ✅ New attack types (educational value)
- ✅ Better metrics and reporting
- ✅ Documentation improvements
- ✅ Security enhancements
- ✅ Educational resources

### What We Won't Accept

- ❌ Changes that bypass safety mechanisms
- ❌ Features enabling unauthorized use
- ❌ Code that removes audit trails
- ❌ Modifications that reduce transparency

---

## References

### Protocol Documentation
- [TCP/IP Protocol Suite - RFC 793](https://tools.ietf.org/html/rfc793)
- [ICMP Protocol - RFC 792](https://tools.ietf.org/html/rfc792)
- [DNS Protocol - RFC 1035](https://tools.ietf.org/html/rfc1035)
- [NTP Protocol - RFC 5905](https://tools.ietf.org/html/rfc5905)

### Security Resources
- [OWASP Load Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP DDoS Article](https://owasp.org/www-community/attacks/Denial_of_Service)
- [OWASP Slowloris Attack](https://owasp.org/www-community/attacks/Slowloris)
- [Cloudflare DDoS Learning](https://www.cloudflare.com/learning/ddos/)

### Educational References
- [CompTIA Network+](https://www.comptia.org/)
- [Cisco CCNA](https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html)
- [Darknet Diaries Podcast](https://darknetdiaries.com/)
- [NetworkEngineering Subreddit](https://reddit.com/r/ccna)

---

## File Structure

### Root Directory
```
redload-x/
├── redload-x.py              # Main entry point

# NOTE: legacy `py-ddos` references retained for backward compatibility where noted
├── README.md               # This file
├── SECURITY.md            # Legal/security framework
├── CONTRIBUTING.md        # Contribution guidelines
├── TERMINOLOGY_UPDATE.md  # Consistent naming
├── requirements.txt       # Python dependencies
└── .gitignore            # Git configuration
```

### Core Modules (`core/`)
```
core/
├── __init__.py                # Package initialization
├── engine.py                  # Attack orchestration (ENHANCED)
├── attacks.py                 # Attack wrapper
├── attacks_advanced.py        # 8 attack implementations
├── safety_locks.py            # Safety system (ENHANCED - 280+ lines)
├── metrics.py                 # Metrics collector (NEW - 190+ lines)
├── reporter_v2.py             # Improved reporting (NEW - 450+ lines)
├── reporter.py                # Legacy reporting
├── logger.py                  # Logging system
├── colors.py                  # ANSI colors
├── config.py                  # Configuration
├── banner.py                  # ASCII banner
├── cli_menu.py                # Interactive menu
├── tor_handler.py             # TOR integration
└── __pycache__/               # Python cache
```

### Output Directories
```
logs/
├── redloadx_YYYYMMDD_HHMMSS.log    # Session logs
└── safety_audit.json              # Audit trail

reports/
├── html/
│   └── redloadx_report_*.html       # Interactive reports with charts
└── cli/
    └── redloadx_report_*.txt        # Analysis reports
```

---

## Performance Guidelines

### Recommended Thread Counts

| Attack Type | Recommended | Maximum | Notes |
|------------|------------|---------|-------|
| HTTP | 100-500 | 2000 | Connection limits |
| SLOWLORIS | 200-1000 | 5000 | Keeps connections open |
| UDP | 500-5000 | 50000 | Bandwidth limited |
| SYN | 500-5000 | 50000 | Kernel limited |
| SLOWREAD | 100-500 | 2000 | Resource intensive |
| DNS | 200-1000 | 10000 | Amplification-based |
| ICMP | 500-5000 | 50000 | Kernel limited |
| NTP | 200-1000 | 10000 | Amplification-based |

### Optimization Tips

**For Maximum RPS:**
```bash
# More threads + longer duration
python redload-x.py -t target.com -a UDP -c 5000 -d 300
```

**For Stealth:**
```bash
# Fewer threads + longer duration + TOR
python redload-x.py -t target.com -a SLOWLORIS -c 50 -d 600 --tor
```

**For Bandwidth Testing:**
```bash
# UDP or SYN with high thread count
python redload-x.py -t target.com -a UDP -c 5000 -p 53
```

---

## Educational Value

### Network Fundamentals
- TCP/UDP protocols and mechanics
- HTTP/HTTPS application layer
- DNS and NTP protocol behaviors
- ICMP and ping mechanisms
- OSI model practical application

### Security Concepts
- DDoS attack vectors
- Resource exhaustion techniques
- Application vs. network layer attacks
- Amplification attack mechanics
- Traffic analysis and detection

### System Administration
- Network monitoring and metrics
- Connection pooling and limits
- Server resource management
- Rate limiting strategies
- Firewall rule design

### Penetration Testing
- Attack planning and scoping
- Target reconnaissance
- Impact assessment
- Mitigation validation
- Proper authorization procedures

---

## Support & Contact

**Author:** voltsparx  
**Email:** voltsparx@gmail.com  
**GitHub:** [RedLoad-X](https://github.com/voltsparx/RedLoad-X)

### Getting Help

- **Technical Questions:** Check DEVELOPERS_GUIDE.md
- **Legal Questions:** See SECURITY.md
- **Contributing:** Read CONTRIBUTING.md
- **Terminology:** Review TERMINOLOGY_UPDATE.md
- **Features:** See EDUCATIONAL_FEATURES.md

---

## Version History

### v7.1 (Current - February 17, 2026)
- ✅ Enhanced safety locks with audit trails
- ✅ Real-time metrics collection system
- ✅ Report generation with charts
- ✅ Developer-friendly documentation
- ✅ 18 code quality issues fixed
- ✅ Type safety (Enum)
- ✅ Script-friendly auto_confirm
- ✅ Comprehensive config validation
- ✅ Production-ready with extended features

### v7.0 (February 17, 2026)
- Operational network stress testing tool
- 8 attack vectors across OSI layers
- TOR integration
- Dual interface (CLI + interactive menu)
- Detailed reporting
- Comprehensive logging

---

## License

This tool is provided for **educational and authorized testing purposes only**. Users are responsible for complying with all applicable laws and regulations.

See SECURITY.md for complete legal framework.

---

## Legal Responsibility

You assume **FULL LEGAL RESPONSIBILITY** for:
- Obtaining explicit written authorization
- Complying with all applicable laws
- Staying within authorized scope
- Respecting all legal frameworks
- Understanding consequences of misuse

**Misuse may result in:**
- Criminal prosecution (CFAA §1030)
- Civil liability
- Imprisonment
- Substantial fines
- Permanent criminal record

---

## Disclaimer

This tool is provided **AS-IS** for educational purposes. The author (voltsparx) assumes **NO LIABILITY** for:
- Misuse of this tool
- Unauthorized testing
- Damage caused by testing
- Legal consequences
- Any adverse outcomes

---

**RedLoad-X v7.1** - Network Stress Testing Tool  
**By voltsparx** | voltsparx@gmail.com  
**Released:** February 17, 2026  
**Status:** Production Ready
