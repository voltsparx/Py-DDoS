# -*- coding: utf-8 -*-
"""
Professional Report Generator v7.5 - Unified Report Module
Generates comprehensive HTML reports with interactive Chart.js visualizations 
and detailed TXT analysis reports

Supports both legacy (stats-based) and modern (metrics-based) report generation
for full backward compatibility.

Author: voltsparx
Contact: voltsparx@gmail.com

Features:
- Interactive Chart.js v4.0+ graphs (bar, doughnut, pie, line charts)
- Professional HTML design with gradient styling
- Response time analysis and distribution
- HTTP status code breakdown
- Connection state visualization
- Risk assessment and educational insights
- Plain text analysis export for scripting
- Mobile-responsive design
- Print-optimized layout
"""

import os
from pathlib import Path
from datetime import datetime
import json
import statistics
from .colors import Styles, Colors


class ReportGenerator:
    """
    Professional report generation with advanced visualizations
    
    Supports both legacy (stats/RPS samples) and modern (metrics-based) interfaces
    for backward compatibility with existing code.
    
    Attributes:
        reports_dir: Directory path for saving generated reports
    """
    
    def __init__(self, reports_dir="reports"):
        """Initialize report generator with output directory"""
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
    
    # ===== MAIN ENTRY POINTS (Support both interfaces) =====
    
    def generate(self, data1, data2=None, data3=None):
        """
        Generate both HTML and TXT reports
        
        Supports two calling conventions for backward compatibility:
        
        Legacy interface:
            generate(stats, config, rps_samples)
        
        Modern interface:
            generate(metrics_data, config)
        
        Args:
            data1: Either stats dict (legacy) or metrics_data dict (modern)
            data2: Either config dict (legacy) or config dict (modern)
            data3: Either rps_samples list (legacy) or None (modern)
        
        Returns:
            Tuple of (html_path, txt_path) as strings
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Detect which interface is being used
        if data3 is not None:
            # Legacy interface: generate(stats, config, rps_samples)
            stats = data1
            config = data2
            rps_samples = data3
            html_report = self._generate_html_report_legacy(stats, config, rps_samples, timestamp)
            txt_report = self._generate_txt_report_legacy(stats, config, rps_samples, timestamp)
        else:
            # Modern interface: generate(metrics_data, config)
            metrics_data = data1
            config = data2
            html_report = self._generate_html_report_modern(metrics_data, config, timestamp)
            txt_report = self._generate_txt_report_modern(metrics_data, config, timestamp)
        
        # Save both formats
        html_path = self.reports_dir / f"pyddos_report_{timestamp}.html"
        txt_path = self.reports_dir / f"pyddos_report_{timestamp}.txt"
        
        with open(html_path, 'w') as f:
            f.write(html_report)
        
        with open(txt_path, 'w') as f:
            f.write(txt_report)
        
        return str(html_path), str(txt_path)
    
    # ===== MODERN INTERFACE (Metrics-based) =====
    
    def _generate_html_report_modern(self, metrics, config, timestamp):
        """Generate interactive HTML report from metrics data (v7.1+)"""
        
        # Extract metrics
        total_requests = metrics.get('total_requests', 0)
        successful = metrics.get('successful', 0)
        failed = metrics.get('failed', 0)
        success_rate = metrics.get('success_rate', 0)
        rps = metrics.get('rps', 0)
        bandwidth = metrics.get('bandwidth_mbps', 0)
        duration = metrics.get('duration', 0)
        
        rt_stats = metrics.get('response_times', {})
        http_codes = metrics.get('http_codes', {})
        conn_states = metrics.get('connection_states', {})
        
        # Prepare chart data
        response_times_list = [rt_stats.get('min', 0), rt_stats.get('mean', 0), rt_stats.get('max', 0)]
        response_time_labels = ['Min (ms)', 'Avg (ms)', 'Max (ms)']
        
        # Status code chart data
        status_labels = list(http_codes.keys())
        status_data = list(http_codes.values())
        
        # Connection state data
        conn_labels = list(conn_states.keys())
        conn_data = list(conn_states.values())
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Py-DDoS v7.1 Network Stress Test Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.0.0/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px;
            text-align: center;
            border-bottom: 5px solid #764ba2;
        }}
        
        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
            margin: 5px 0;
        }}
        
        .metadata {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .meta-item {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .meta-label {{
            font-weight: 600;
            color: #667eea;
        }}
        
        .meta-value {{
            color: #333;
            font-family: 'Courier New', monospace;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
            page-break-inside: avoid;
        }}
        
        .section-title {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
            text-align: center;
        }}
        
        .metric-card .label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-card .value {{
            font-size: 2.2em;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin-bottom: 40px;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }}
        
        .chart-title {{
            font-size: 1.4em;
            color: #333;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            border-top: 2px solid #e9ecef;
            text-align: center;
            color: #6c757d;
            font-size: 0.95em;
        }}
        
        .footer-info {{
            margin: 10px 0;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
        }}
        
        @media (max-width: 768px) {{
            .metadata {{
                grid-template-columns: 1fr;
            }}
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔴 Py-DDoS v7.1</h1>
            <p>Network Stress Test Report</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Operational Testing Framework | Educational & Authorized Use Only</p>
        </div>
        
        <div class="metadata">
            <div class="meta-item">
                <span class="meta-label">Test Date:</span>
                <span class="meta-value">{timestamp}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Test Type:</span>
                <span class="meta-value">{config.get('attack_type', 'Unknown')}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Target:</span>
                <span class="meta-value">{config.get('target_host', 'N/A')}:{config.get('target_port', 'N/A')}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Duration:</span>
                <span class="meta-value">{duration:.2f}s</span>
            </div>
        </div>
        
        <div class="content">
            <!-- Key Metrics Section -->
            <div class="section">
                <h2 class="section-title">📊 Key Performance Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Total Requests</div>
                        <div class="value">{total_requests:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Success Rate</div>
                        <div class="value">{success_rate:.1f}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Requests/Second</div>
                        <div class="value">{rps:.1f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Bandwidth</div>
                        <div class="value">{bandwidth:.2f} MB/s</div>
                    </div>
                </div>
            </div>
            
            <!-- Response Time Analysis -->
            <div class="section">
                <h2 class="section-title">⏱️ Response Time Analysis</h2>
                <div class="chart-container">
                    <div class="chart-title">Response Time Distribution (Min/Avg/Max)</div>
                    <canvas id="responseTimeChart"></canvas>
                </div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Min Response</div>
                        <div class="value">{rt_stats.get('min', 0):.2f}ms</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Avg Response</div>
                        <div class="value">{rt_stats.get('mean', 0):.2f}ms</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Max Response</div>
                        <div class="value">{rt_stats.get('max', 0):.2f}ms</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Std Dev</div>
                        <div class="value">{rt_stats.get('stdev', 0):.2f}ms</div>
                    </div>
                </div>
            </div>
            
            <!-- HTTP Status Codes -->
            {self._generate_status_chart_html(status_labels, status_data) if status_labels else ""}
            
            <!-- Connection States -->
            {self._generate_connection_chart_html(conn_labels, conn_data) if conn_labels else ""}
            
            <!-- Detailed Results -->
            <div class="section">
                <h2 class="section-title">📈 Detailed Results</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Successful</div>
                        <div class="value">{successful:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Failed</div>
                        <div class="value">{failed:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Total Bytes Sent</div>
                        <div class="value">{metrics.get('total_bytes_sent', 0) / (1024*1024):.2f} MB</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Total Bytes Received</div>
                        <div class="value">{metrics.get('total_bytes_received', 0) / (1024*1024):.2f} MB</div>
                    </div>
                </div>
            </div>
            
            <!-- Configuration Summary -->
            <div class="section">
                <h2 class="section-title">⚙️ Test Configuration</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Threads</div>
                        <div class="value">{config.get('threads', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Attack Type</div>
                        <div class="value">{config.get('attack_type', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">TOR Enabled</div>
                        <div class="value">{'Yes' if config.get('use_tor') else 'No'}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Duration</div>
                        <div class="value">{config.get('duration', 'N/A')}s</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-info">
                <strong>Py-DDoS v7.1 - Operational Network Stress Testing Tool</strong>
            </div>
            <div class="footer-info">
                Author: voltsparx | Contact: voltsparx@gmail.com
            </div>
            <div class="footer-info">
                ⚠️  For Authorized Testing & Educational Purposes Only
            </div>
            <div class="footer-info" style="margin-top: 15px; font-size: 0.85em; color: #999;">
                Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </div>
    
    <script>
        // Response Time Chart
        const rtCtx = document.getElementById('responseTimeChart').getContext('2d');
        new Chart(rtCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(response_time_labels)},
                datasets: [{{
                    label: 'Response Time (ms)',
                    data: {json.dumps(response_times_list)},
                    backgroundColor: [
                        '#28a745',
                        '#667eea',
                        '#dc3545'
                    ],
                    borderColor: [
                        '#1e7e34',
                        '#5568d3',
                        '#c82333'
                    ],
                    borderWidth: 2,
                    borderRadius: 5
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top',
                        labels: {{
                            padding: 15,
                            font: {{ size: 12, weight: 'bold' }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ font: {{ size: 12 }} }},
                        grid: {{ color: '#e9ecef' }}
                    }},
                    x: {{
                        ticks: {{ font: {{ size: 12 }} }},
                        grid: {{ display: false }}
                    }}
                }}
            }}
        }});
        
        {self._generate_status_chart_js(status_labels, status_data) if status_labels else ""}
        {self._generate_connection_chart_js(conn_labels, conn_data) if conn_labels else ""}
    </script>
</body>
</html>
"""
        return html
    
    def _generate_status_chart_html(self, labels, data):
        """Generate HTML for status code chart"""
        if not labels:
            return ""
        return f"""
            <div class="section">
                <h2 class="section-title">🌐 HTTP Status Code Distribution</h2>
                <div class="chart-container">
                    <div class="chart-title">Response Status Codes</div>
                    <canvas id="statusCodeChart"></canvas>
                </div>
            </div>
        """
    
    def _generate_status_chart_js(self, labels, data):
        """Generate JavaScript for status code chart"""
        if not labels:
            return ""
        colors = ['#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6c757d']
        return f"""
        const scCtx = document.getElementById('statusCodeChart').getContext('2d');
        new Chart(scCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps([str(l) for l in labels])},
                datasets: [{{
                    data: {json.dumps(data)},
                    backgroundColor: {json.dumps(colors[:len(labels)])},
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'right',
                        labels: {{ padding: 15, font: {{ size: 12 }} }}
                    }}
                }}
            }}
        }});
        """
    
    def _generate_connection_chart_html(self, labels, data):
        """Generate HTML for connection state chart"""
        if not labels:
            return ""
        return f"""
            <div class="section">
                <h2 class="section-title">🔌 Connection State Analysis</h2>
                <div class="chart-container">
                    <div class="chart-title">Connection Status Distribution</div>
                    <canvas id="connectionChart"></canvas>
                </div>
            </div>
        """
    
    def _generate_connection_chart_js(self, labels, data):
        """Generate JavaScript for connection chart"""
        if not labels:
            return ""
        return f"""
        const connCtx = document.getElementById('connectionChart').getContext('2d');
        new Chart(connCtx, {{
            type: 'pie',
            data: {{
                labels: {json.dumps([str(l) for l in labels])},
                datasets: [{{
                    data: {json.dumps(data)},
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe'],
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{ padding: 15, font: {{ size: 12 }} }}
                    }}
                }}
            }}
        }});
        """
    
    def _generate_txt_report_modern(self, metrics, config, timestamp):
        """Generate plain text analysis report (modern interface)"""
        txt = f"""
{'='*80}
PY-DDOS v7.1 - NETWORK STRESS TEST REPORT
{'='*80}

Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test ID: {timestamp}

Author: voltsparx | Contact: voltsparx@gmail.com
⚠️  FOR AUTHORIZED TESTING & EDUCATIONAL PURPOSES ONLY

{'='*80}
EXECUTIVE SUMMARY
{'='*80}

Test Type:              {config.get('attack_type', 'Unknown')}
Target:                {config.get('target_host', 'N/A')}:{config.get('target_port', 'N/A')}
Duration:              {metrics.get('duration', 0):.2f} seconds
Test Date:             {timestamp}

Total Requests:        {metrics.get('total_requests', 0):,}
Successful:            {metrics.get('successful', 0):,}
Failed:                {metrics.get('failed', 0):,}
Success Rate:          {metrics.get('success_rate', 0):.2f}%

{'='*80}
PERFORMANCE METRICS
{'='*80}

Requests Per Second (RPS):     {metrics.get('rps', 0):.2f}
Bandwidth (MB/s):              {metrics.get('bandwidth_mbps', 0):.2f}
Total Data Sent (MB):          {metrics.get('total_bytes_sent', 0) / (1024*1024):.2f}
Total Data Received (MB):      {metrics.get('total_bytes_received', 0) / (1024*1024):.2f}

{'='*80}
RESPONSE TIME ANALYSIS
{'='*80}

Response Time Stats (milliseconds):
  Minimum:               {metrics['response_times'].get('min', 0):.2f} ms
  Average:               {metrics['response_times'].get('mean', 0):.2f} ms
  Median:                {metrics['response_times'].get('median', 0):.2f} ms
  Maximum:               {metrics['response_times'].get('max', 0):.2f} ms
  Std Deviation:         {metrics['response_times'].get('stdev', 0):.2f} ms

{'='*80}
HTTP STATUS CODE DISTRIBUTION
{'='*80}

"""
        
        http_codes = metrics.get('http_codes', {})
        if http_codes:
            for code, count in sorted(http_codes.items()):
                percentage = (count / metrics.get('total_requests', 1)) * 100
                txt += f"  {code:>4d}: {count:>8,} requests ({percentage:>5.1f}%)\n"
        else:
            txt += "  No HTTP status codes recorded\n"
        
        txt += f"""
{'='*80}
CONNECTION STATE ANALYSIS
{'='*80}

"""
        
        conn_states = metrics.get('connection_states', {})
        if conn_states:
            for state, count in conn_states.items():
                txt += f"  {state:.<30} {count:>8,}\n"
        else:
            txt += "  No connection states recorded\n"
        
        txt += f"""
{'='*80}
TEST CONFIGURATION
{'='*80}

Target Host:           {config.get('target_host', 'N/A')}
Target Port:           {config.get('target_port', 'N/A')}
Thread Count:          {config.get('threads', 'N/A')}
Attack Type:           {config.get('attack_type', 'N/A')}
TOR Enabled:           {'Yes' if config.get('use_tor') else 'No'}
Test Duration:         {config.get('duration', 'N/A')} seconds

{'='*80}
LEGAL DISCLAIMER
{'='*80}

This tool is for AUTHORIZED TESTING and EDUCATIONAL PURPOSES ONLY.
Unauthorized use is ILLEGAL and may result in criminal prosecution.

Always obtain written authorization before testing.
Comply with all applicable laws and regulations.

{'='*80}
End of Report
{'='*80}
"""
        
        return txt
    
    # ===== LEGACY INTERFACE (RPS samples-based) =====
    
    def _generate_html_report_legacy(self, stats, config, rps_samples, timestamp):
        """Generate comprehensive HTML report (legacy interface)"""
        
        # Calculate additional metrics
        rps_avg = statistics.mean(rps_samples) if rps_samples else 0
        rps_peak = max(rps_samples) if rps_samples else 0
        rps_min = min(rps_samples) if rps_samples else 0
        rps_stdev = statistics.stdev(rps_samples) if len(rps_samples) > 1 else 0
        
        # Create RPS chart data for HTML5 canvas
        rps_data = json.dumps(rps_samples)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Py-DDoS v7.1 Attack Report - {config.get('attack_type', 'Unknown')}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.0.0/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            border-bottom: 4px solid #764ba2;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin: 30px 0;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .config-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .config-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .config-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            font-family: 'Courier New', monospace;
        }}
        
        .config-table tr:hover {{
            background: #f5f7ff;
        }}
        
        .config-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .success {{
            color: #10b981;
            font-weight: bold;
        }}
        
        .warning {{
            color: #f59e0b;
            font-weight: bold;
        }}
        
        .footer {{
            background: #f9fafb;
            padding: 20px 40px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Py-DDoS v7.1 Network Stress Test Report</h1>
            <p>Professional Penetration Testing Tool - Educational Purpose</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="content">
            <!-- Attack Metrics -->
            <div class="section">
                <div class="section-title">Attack Metrics</div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Total Packets Sent</div>
                        <div class="metric-value">{stats.get('packets_sent', stats.get('total_packets', 0)):,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Bytes Sent</div>
                        <div class="metric-value">{stats.get('bytes_sent', 0):,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average RPS</div>
                        <div class="metric-value">{rps_avg:.2f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Peak RPS</div>
                        <div class="metric-value">{rps_peak:.2f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Min RPS</div>
                        <div class="metric-value">{rps_min:.2f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Std Deviation</div>
                        <div class="metric-value">{rps_stdev:.2f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Attack Duration</div>
                        <div class="metric-value">{stats.get('duration', 0):.1f}s</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Success Rate</div>
                        <div class="metric-value">{stats.get('success_rate', 0):.1f}%</div>
                    </div>
                </div>
            </div>
            
            <!-- RPS Chart -->
            {self._generate_rps_chart_html(rps_samples) if rps_samples else ''}
            
            <!-- Configuration -->
            <div class="section">
                <div class="section-title">Attack Configuration</div>
                <table class="config-table">
                    <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>Target Host</td>
                        <td>{config.get('target_input', config.get('target_host', 'N/A'))}</td>
                    </tr>
                    <tr>
                        <td>Target Port</td>
                        <td>{config.get('target_port', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td>Attack Type</td>
                        <td><span class="success">{config.get('attack_type', 'N/A')}</span></td>
                    </tr>
                    <tr>
                        <td>Thread Count</td>
                        <td>{config.get('threads', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td>Duration</td>
                        <td>{config.get('duration', 'N/A')}s</td>
                    </tr>
                    <tr>
                        <td>TOR Enabled</td>
                        <td>{'<span class="warning">Yes</span>' if config.get('use_tor') else 'No'}</td>
                    </tr>
                </table>
            </div>
            
            <!-- Success/Error Stats -->
            <div class="section">
                <div class="section-title">Success Metrics</div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Successful Packets</div>
                        <div class="metric-value success">{stats.get('success_count', 0):,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Failed Packets</div>
                        <div class="metric-value warning">{stats.get('error_count', 0):,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Packets</div>
                        <div class="metric-value">{stats.get('success_count', 0) + stats.get('error_count', 0):,}</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Py-DDoS v7.1 | Educational & Authorized Testing Only | {datetime.now().strftime('%Y-%m-%d')}</p>
            <p>Author: voltsparx | Report ID: {timestamp}</p>
        </div>
    </div>
    
    <script>
        // Initialize charts when page loads
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initCharts);
        }} else {{
            initCharts();
        }}
        
        function initCharts() {{
            const rpsCanvas = document.getElementById('rpsChart');
            if (rpsCanvas) {{
                new Chart(rpsCanvas, {{
                    type: 'line',
                    data: {{
                        labels: Array.from({{length: {len(rps_samples)}}}, (_, i) => i + 1),
                        datasets: [{{
                            label: 'Requests Per Second',
                            data: {rps_data},
                            borderColor: '#667eea',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 0,
                            pointHoverRadius: 8
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: true,
                                labels: {{
                                    usePointStyle: true,
                                    font: {{size: 12}}
                                }}
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    color: 'rgba(0,0,0,0.05)'
                                }}
                            }},
                            x: {{
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    display: false
                                }}
                            }}
                        }}
                    }}
                }});
            }}
        }}
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_rps_chart_html(self, rps_samples):
        """Generate chart HTML"""
        if not rps_samples:
            return ""
        
        return """
            <div class="section">
                <div class="section-title">Real-time RPS Chart</div>
                <div class="chart-container">
                    <canvas id="rpsChart"></canvas>
                </div>
            </div>
        """
    
    def _generate_txt_report_legacy(self, stats, config, rps_samples, timestamp):
        """Generate comprehensive TXT/CLI report (legacy interface)"""
        
        # Calculate additional metrics
        rps_avg = statistics.mean(rps_samples) if rps_samples else 0
        rps_peak = max(rps_samples) if rps_samples else 0
        rps_min = min(rps_samples) if rps_samples else 0
        rps_stdev = statistics.stdev(rps_samples) if len(rps_samples) > 1 else 0
        
        report = f"""
{'='*80}
PY-DDOS v7.1 NETWORK STRESS TEST REPORT
{'='*80}

Author: voltsparx
Contact: voltsparx@gmail.com

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report ID: {timestamp}

{'='*80}
ATTACK METRICS
{'='*80}

Total Packets Sent:     {stats.get('packets_sent', stats.get('total_packets', 0)):>20,}
Total Bytes Sent:       {stats.get('bytes_sent', 0):>20,}
Attack Duration:        {stats.get('duration', 0):>20.2f} seconds

RPS Statistics:
  Average RPS:          {rps_avg:>20.2f}
  Peak RPS:             {rps_peak:>20.2f}
  Minimum RPS:          {rps_min:>20.2f}
  Std Deviation:        {rps_stdev:>20.2f}

{'='*80}
SUCCESS METRICS
{'='*80}

Successful Packets:     {stats.get('success_count', 0):>20,}
Failed Packets:         {stats.get('error_count', 0):>20,}
Total Processed:        {stats.get('success_count', 0) + stats.get('error_count', 0):>20,}
Success Rate:           {stats.get('success_rate', 0):>20.2f}%

{'='*80}
ATTACK CONFIGURATION
{'='*80}

Target Host:            {config.get('target_input', config.get('target_host', 'N/A')):>20}
Target Port:            {config.get('target_port', 'N/A'):>20}
Attack Type:            {config.get('attack_type', 'N/A'):>20}
Thread Count:           {config.get('threads', 'N/A'):>20}
Duration:               {config.get('duration', 'N/A'):>20} seconds
TOR Enabled:            {('Yes' if config.get('use_tor') else 'No'):>20}

{'='*80}
RPS TIMELINE
{'='*80}

Time (s)    |  RPS      |  Status
{'─'*80}
"""
        
        # Add RPS timeline
        for i, rps in enumerate(rps_samples[:100]):  # Show first 100 samples
            bar = '█' * int(rps / max(rps_samples) * 20) if rps_samples else ''
            status = 'Normal' if rps > rps_avg * 0.5 else 'Low'
            report += f"{i:>6}      |  {rps:>7.2f}  |  {bar:<20} {status}\n"
        
        if len(rps_samples) > 100:
            report += f"... ({len(rps_samples) - 100} more samples)\n"
        
        report += f"""
{'='*80}
LEGAL DISCLAIMER
{'='*80}

This tool is for AUTHORIZED TESTING and EDUCATIONAL PURPOSES ONLY.
Unauthorized use is ILLEGAL and may result in criminal prosecution.

Always obtain written authorization before testing.
Comply with all applicable laws and regulations.

{'='*80}
End of Report
{'='*80}
"""
        
        return report


__all__ = ['ReportGenerator']
