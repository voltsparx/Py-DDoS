# Contributing to Py-DDoS

**Project Author:** voltsparx  
**Contact:** voltsparx@gmail.com

Thank you for your interest in contributing to this educational project! This document outlines how you can help improve Py-DDoS - the Operational Network Stress Testing Tool.

## Code of Conduct

### Our Values

We are committed to:
- **Promoting education** in cybersecurity and network resilience
- **Maintaining ethical standards** in security research
- **Respecting legal boundaries** in all jurisdictions
- **Encouraging responsible disclosure** of vulnerabilities
- **Supporting the security community** professionally

### Contributor Expectations

All contributors agree to:
- Use this project **ONLY** for educational and authorized testing
- Follow all applicable laws and regulations
- Respect intellectual property rights
- Maintain professional conduct
- Report security issues responsibly
- Contribute with positive intent

## How to Contribute

### 1. Report Bugs

**Found a bug? Please report it!**

Open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Error messages and logs
- Proof of concept (if applicable)

```markdown
## Bug Report

**Description:**
[Clear description of the issue]

**To Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Environment:**
- OS: [Windows/Linux/macOS]
- Python: [Version]
- Dependencies: [Installed versions]

**Error Output:**
[Paste error logs here]
```

### 2. Suggest Features

**Have an idea for improvement?**

Create a feature request with:
- Clear description of the feature
- Why it would be useful
- Possible implementation approach
- Example use cases
- Relevant code references

```markdown
## Feature Request

**Title:** [Concise title]

**Description:**
[Clear description of desired feature]

**Motivation:**
[Why is this feature needed?]

**Proposed Solution:**
[How should it work?]

**Example Usage:**
[How would users interact with it?]

**Implementation Approach:**
[Rough idea of how to implement]

**Alternative Solutions:**
[Other possible approaches]
```

### 3. Contribute Code

**Want to submit code improvements?**

#### Before Starting

1. **Check existing issues/PRs** to avoid duplication
2. **Discuss major changes** in an issue first
3. **Review SECURITY.md** for legal/ethical guidelines
4. **Understand the codebase** structure
5. **Get maintainer approval** before significant work

#### Development Setup

```bash
# Clone repository
git clone https://github.com/user/py-ddos.git
cd py-ddos

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Create feature branch
git checkout -b feature/your-feature-name
```

#### Code Standards

**Python Style Guide:**
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to all functions

**Type Hints:**
```python
def validate_target(target: str) -> tuple[bool, str]:
    """Validate and resolve target IP or hostname.
    
    Args:
        target: IP address or hostname
        
    Returns:
        Tuple of (is_valid, resolved_ip)
    """
    # Implementation
```

**Comments and Docstrings:**
```python
def http_flood(self):
    """
    HTTP Layer 7 Flood Attack
    
    Sends rapid HTTP requests with randomized headers and parameters.
    
    Returns:
        None (updates metrics in-place)
        
    Note:
        For educational purposes. Requires authorization.
    """
```

**Check Code Quality:**

```bash
# Format code
black core/*.py py-ddos.py

# Check style
flake8 core/*.py py-ddos.py

# Type checking
mypy core/*.py py-ddos.py

# Run tests
pytest tests/
```

#### Commit Guidelines

```
# Use clear commit messages
git commit -m "Add feature: [Feature name]"
git commit -m "Fix: [Bug description]"
git commit -m "Refactor: [What changed]"
git commit -m "Docs: [Documentation update]"
git commit -m "Tests: [Test addition]"

# Example good commits:
git commit -m "Add DNS amplification attack implementation"
git commit -m "Fix: Handle timeout errors gracefully in HTTP flood"
git commit -m "Refactor: Separate color output to dedicated module"
```

#### Testing

**Write tests for new features:**

```python
# tests/test_attacks.py
import unittest
from core.attacks_advanced import AttackWorkers

class TestAttackWorkers(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.host = "example.com"
        self.port = 80
        # ... more setup
    
    def test_http_flood_initialization(self):
        """Test HTTP flood attack initialization"""
        # Test implementation
        pass
    
    def test_invalid_target(self):
        """Test handling of invalid targets"""
        # Test implementation
        pass
```

**Run all tests:**

```bash
python -m pytest tests/ -v
```

### 4. Improve Documentation

**Help improve documentation:**

- Fix typos and errors
- Clarify confusing sections
- Add examples
- Update outdated information
- Improve formatting

```markdown
## Documentation Improvements

**What needs improvement:**
[Describe the documentation issue]

**Suggested changes:**
[Provide the improved text or corrections]

**Reason for change:**
[Explain why this improvement helps]
```

### 5. Add Examples

**Create example configurations or scripts:**

```bash
# Create example files in examples/ directory
examples/
├── example_http_attack.json
├── example_slowloris_attack.json
└── example_usage_guide.md
```

**Example configuration file:**

```json
{
  "name": "Example HTTP Attack",
  "description": "Basic HTTP flood on test server",
  "target_host": "192.168.1.1",
  "target_port": 80,
  "attack_type": "HTTP",
  "threads": 100,
  "duration": 60,
  "use_tor": false
}
```

## Pull Request Process

### 1. Create Pull Request

**Before submitting:**

- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] No unrelated changes
- [ ] Documentation updated
- [ ] Commit messages clear
- [ ] No security issues introduced

**PR Description Template:**

```markdown
## Description
[Clear description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation improvement
- [ ] Code refactor
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Tested manually
- [ ] No new warnings

## Related Issues
Fixes #[issue number]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Verified legal/ethical compliance
```

### 2. Code Review

**Be prepared for:**
- Questions about implementation
- Requests for clarification
- Suggestions for improvements
- Tests for edge cases

**During review:**
- Be respectful and professional
- Address feedback constructively
- Discuss concerns if you disagree
- Update based on feedback

### 3. Approval and Merge

Once approved:
- Maintainer will merge your PR
- Branch will be deleted
- You'll be credited in CHANGELOG
- Changes appear in next release

## Areas for Contribution

### High Priority

- [ ] New attack types (with proper documentation)
- [ ] Better error handling and reporting
- [ ] Performance optimizations
- [ ] Additional defenses documentation
- [ ] More comprehensive examples
- [ ] Improved logging system
- [ ] Better configuration management

### Medium Priority

- [ ] Additional educational materials
- [ ] Extended statistics/metrics
- [ ] Better reporting formats
- [ ] Configuration wizard improvements
- [ ] Additional network protocols

### Community

- [ ] Share example use cases
- [ ] Create video tutorials
- [ ] Write blog posts
- [ ] Contribute to discussions
- [ ] Help other users

## Project Structure

Understanding the codebase:

```
py-ddos/
├── py-ddos.py              # Main entry point
├── core/
│   ├── colors.py           # ANSI color utilities
│   ├── config.py           # Configuration management
│   ├── cli_menu.py         # Interactive menu
│   ├── engine_new.py       # Main attack engine
│   ├── attacks_advanced.py # Attack implementations
│   ├── tor_handler.py      # TOR integration
│   ├── reporter.py         # Report generation
│   ├── logger.py           # Logging system
│   └── ...
├── tests/                  # Unit tests
├── examples/               # Example configurations
├── logs/                   # Runtime logs
└── reports/               # Generated reports
```

### Module Responsibilities

- **colors.py**: ANSI color output formatting
- **config.py**: Configuration and attack definitions
- **cli_menu.py**: Interactive CLI interface
- **engine_new.py**: Attack orchestration and execution
- **attacks_advanced.py**: Actual attack implementations
- **tor_handler.py**: TOR integration and circuit management
- **reporter.py**: Report generation and visualization
- **logger.py**: File and console logging

## Legal and Ethical Guidelines

### Before Contributing

**Ensure your contribution:**

- [ ] Is for educational purposes
- [ ] Complies with applicable laws
- [ ] Respects user privacy and security
- [ ] Includes appropriate warnings
- [ ] Follows ethical hacking principles
- [ ] Doesn't enable malicious activity
- [ ] Includes security considerations

### Responsible Disclosure

If you discover a vulnerability:

1. **Don't** report it publicly
2. **Contact** maintainers privately
3. **Allow** time for fixes
4. **Coordinate** disclosure timeline

## Community Guidelines

### Be Respectful

- Treat others with respect
- Welcome diverse perspectives
- Listen actively
- Disagree constructively

### Be Helpful

- Answer questions patiently
- Help new contributors
- Share knowledge generously
- Mentor others

### Stay On Topic

- Keep discussions relevant
- Avoid spam and self-promotion
- Don't advertise competing tools
- Focus on project improvement

### Report Issues

- Report harassment or unethical behavior
- Contact maintainers privately
- Provide specific details
- Work toward resolution

## Coding Examples

### Adding a New Attack Type

```python
def new_attack_type(self):
    """
    New Attack Type Description
    
    Detailed explanation of how the attack works.
    
    Algorithm:
    1. First step
    2. Second step
    3. Third step
    
    Detection: How defenders can detect this
    
    Educational notes:
    - Key concepts learned
    - Defense mechanisms
    - Mitigation strategies
    """
    sock = None
    try:
        # Implementation
        while not self.stop_event.is_set():
            try:
                # Attack logic
                self.metrics.success_count += 1
                self.metrics.packets_sent += 1
                self.increment_counter()
            except Exception:
                self.metrics.error_count += 1
    finally:
        if sock:
            try:
                sock.close()
            except:
                pass
```

### Adding Error Handling

```python
def validate_configuration(config: dict) -> tuple[bool, str]:
    """Validate attack configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if not config.get('target_host'):
            return False, "Target host required"
        
        if not 1 <= config.get('target_port', 80) <= 65535:
            return False, "Invalid port"
        
        if config.get('threads', 1) < 1:
            return False, "Threads must be >= 1"
        
        return True, ""
    except Exception as e:
        return False, f"Configuration error: {e}"
```

## Recognition

All contributors will be:
- Added to CONTRIBUTORS file
- Credited in release notes
- Acknowledged in documentation
- Recognized for improvements

## Questions?

- **General questions**: Open a discussion
- **Specific issues**: Open an issue
- **Security concerns**: Contact maintainers privately
- **Contribution ideas**: Submit a feature request

## Resources

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Real Python - Testing](https://realpython.com/python-testing/)
- [GitHub - Contributing Guide](https://github.com/github/docs/blob/main/CONTRIBUTING.md)

## License

By contributing, you agree your code will be licensed under the same license as the project.

---

**Thank you for contributing to Py-DDoS!**

Your contributions help advance cybersecurity education and awareness.

**Last Updated:** February 17, 2026
