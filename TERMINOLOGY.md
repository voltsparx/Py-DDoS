# TERMINOLOGY

This document defines key terms and concepts used throughout the RedLoad-X project.

---

**Attack Session**: A single run of the DDoS engine, from configuration to completion.

**Worker**: An individual thread or async task responsible for generating attack traffic.

**RPS (Requests Per Second)**: The number of HTTP requests sent per second.

**Flood**: A coordinated set of requests targeting a specific host/port.

**Coordinator**: The component that manages and synchronizes multiple floods.

**Rate Limiter**: Mechanism to control the maximum allowed RPS.

**Async Engine**: The asynchronous attack engine using aiohttp for high concurrency.

**Optional Dependency**: A library (like aiohttp) that is not required for basic operation but enables additional features.

**Structured Logger**: The logging system that outputs events in JSONL format for analysis.

**Dry-Run**: A mode where no real packets are sent, used for testing configuration.

**Warm-Up Phase**: Initial period where attack load ramps up gradually.

**Adaptive Load Control**: Automatic adjustment of attack parameters based on feedback.

**JSONL**: JSON Lines format, where each log entry is a single JSON object per line.

**TokenBucket**: The algorithm used for rate limiting.

**Backward Compatibility**: Guarantee that new versions do not break existing usage.

---

For more details, see the README.md and SECURITY.md files.