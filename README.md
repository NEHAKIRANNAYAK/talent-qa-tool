# 📊 Talent Data Quality Analyzer

> Automated API data quality analysis tool that fetches talent profiles, analyzes data completeness by role, and generates comprehensive visual reports.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Overview

This project automates the analysis of talent profile data quality by fetching data from an API, segregating profiles by job role, and calculating the percentage of missing or incorrect values in each field. The output is a beautiful, interactive HTML report with visual indicators and detailed statistics.

### Key Features

✅ **Automated Data Collection** - Fetches all profiles from API with pagination support  
✅ **Role-Based Analysis** - Segregates data by current job role  
✅ **Field-Level Insights** - Analyzes 11 critical profile fields  
✅ **Visual Reports** - Color-coded quality scores with progress bars  
✅ **Scalable** - Handles thousands of profiles efficiently  
✅ **Easy to Use** - Simple command-line execution

---

## 📋 Table of Contents

- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [Output](#-output)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎥 Demo

The analyzer generates an interactive HTML report with:

- **Summary Cards**: Total profiles, unique roles, average quality score
- **Role Analysis Table**: Quality scores for each job role with visual indicators
- **Field Breakdown**: Missing data percentages for each profile field
- **Color Coding**: Green (>80%), Yellow (60-80%), Red (<60%)

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection (for API access)

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/talent-data-quality-analyzer.git
cd talent-data-quality-analyzer
```

2. **Install required dependencies**

```bash
pip install requests
```

That's it! You're ready to run the analyzer.

---

## 💻 Usage

### Basic Usage

Run the script from the command line:

```bash
python analyze_data_quality.py
```

The script will:
1. Connect to the API endpoint
2. Fetch all talent profiles (with pagination)
3. Analyze data quality by role
4. Generate an HTML report with timestamp
5. Display summary statistics in the terminal

### Expected Output

```
============================================================
🎯 TALENT DATA QUALITY ANALYZER
============================================================
🔄 Fetching data from API...
   Fetching page 1...
   Fetching page 2...
✅ Successfully fetched 847 profiles

📊 Analyzing data quality...

📝 Generating HTML report...

✅ Report generated successfully: data_quality_report_20260129_150523.html

📈 Summary:
   • Total Profiles: 847
   • Unique Roles: 23
   • Average Quality Score: 76.3%

🎉 Open the HTML file in your browser to view the full report!
============================================================
```

### Viewing the Report

Open the generated HTML file in any web browser:

- **Windows**: Double-click the file
- **Mac**: Right-click → Open With → Browser
- **Linux**: `xdg-open data_quality_report_*.html`

---

## 🔧 How It Works

### Workflow

```
┌─────────────────┐
│  API Endpoint   │
└────────┬────────┘
         │ Fetch Data (Paginated)
         ▼
┌─────────────────┐
│  Data Collection│
│   (Python)      │
└────────┬────────┘
         │ Raw JSON Profiles
         ▼
┌─────────────────┐
│  Analysis Engine│
│ - Group by Role │
│ - Check Fields  │
│ - Calculate %   │
└────────┬────────┘
         │ Statistics
         ▼
┌─────────────────┐
│ Report Generator│
│   (HTML/CSS)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visual Report  │
│   (Browser)     │
└─────────────────┘
```

### Analysis Process

1. **Data Fetching**
   - Connects to API with Bearer token authentication
   - Handles pagination (500 records per page)
   - Aggregates all profiles into a single dataset

2. **Data Segregation**
   - Groups profiles by `current_role` field
   - Creates role-specific statistics

3. **Field Analysis**
   - Checks 11 critical fields per profile:
     - `name`, `email`, `phone`
     - `experience_years`, `domain`
     - `summary`, `country`
     - `skills`, `current_role`
     - `current_company`, `current_location`
   - Identifies missing, null, or empty values
   - Calculates percentages

4. **Quality Scoring**
   - Quality Score = 100% - Missing Data %
   - Color-coded indicators for quick assessment

5. **Report Generation**
   - Creates interactive HTML with embedded CSS
   - Responsive design for all devices
   - Timestamp for tracking

---

## ⚙️ Configuration

### API Settings

Edit the following variables in `analyze_data_quality.py`:

```python
# API Configuration
API_URL = "http://your-api-endpoint/talent/get-profiles"
AUTH_TOKEN = "your-bearer-token-here"
```

### Fields to Analyze

Modify the `FIELDS_TO_CHECK` list to analyze different fields:

```python
FIELDS_TO_CHECK = [
    'name', 'email', 'phone', 'experience_years', 
    'domain', 'summary', 'country', 'skills', 
    'current_role', 'current_company', 'current_location'
]
```

### Pagination Limit

Adjust the records per page (default: 500):

```python
response = requests.get(
    f"{API_URL}?limit=500&page={page}",  # Change 500 to desired limit
    ...
)
```

---

## 📊 Output

### Report Contents

The generated HTML report includes:

#### 1. Summary Statistics
- Total number of profiles analyzed
- Number of unique job roles
- Average data quality score
- Number of fields analyzed

#### 2. Role-Based Quality Table
- Job role names
- Profile count per role
- Missing data percentage
- Quality score (0-100%)
- Visual progress bars

#### 3. Field-Level Analysis
- Field names
- Total records
- Missing count
- Missing percentage
- Visual indicators

### Sample Report Structure

```
╔══════════════════════════════════════════╗
║   Talent Data Quality Analysis Report    ║
╠══════════════════════════════════════════╣
║                                          ║
║  Total Profiles: 847                     ║
║  Unique Roles: 23                        ║
║  Avg Quality: 76.3%                      ║
║  Fields Analyzed: 11                     ║
║                                          ║
╠══════════════════════════════════════════╣
║  📊 Data Quality by Role                 ║
╠══════════════════════════════════════════╣
║  Role            | Count | Quality      ║
║  Software Eng.   | 234   | ████░ 82%    ║
║  Data Analyst    | 156   | ███░░ 68%    ║
║  ...                                     ║
╠══════════════════════════════════════════╣
║  🔍 Field-Level Analysis                 ║
╠══════════════════════════════════════════╣
║  email           | Missing: 45 (5.3%)   ║
║  domain          | Missing: 234 (27.6%) ║
║  ...                                     ║
╚══════════════════════════════════════════╝
```

---

## 🛠️ Tech Stack

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core programming language | 3.7+ |
| **requests** | HTTP client for API calls | Latest |
| **json** | Data parsing | Built-in |
| **collections** | Data structures (defaultdict) | Built-in |
| **datetime** | Timestamp generation | Built-in |

### Output Technologies

| Technology | Purpose |
|------------|---------|
| **HTML5** | Report structure |
| **CSS3** | Styling and layout |
| **JavaScript** | (Optional) Future interactivity |

### Design Features

- **Responsive Design**: Works on desktop, tablet, mobile
- **Color Coding**: Visual quality indicators
- **Progress Bars**: Animated quality visualization
- **Professional Styling**: Clean, modern interface

---

## 📁 Project Structure

```
talent-data-quality-analyzer/
│
├── analyze_data_quality.py     # Main script
├── README.md                    # This file
├── LICENSE                      # License information
├── requirements.txt             # Python dependencies
│
├── output/                      # Generated reports
│   └── data_quality_report_*.html
│
└── docs/                        # Documentation
    └── Project_Summary_Report.md
```

---

## 🔍 Example Use Cases

### 1. Monthly Quality Audits
Run the analyzer monthly to track data quality improvements over time.

### 2. Onboarding New Data Sources
Validate data quality when integrating new talent sources.

### 3. Prioritizing Data Collection
Identify which roles or fields need the most attention.

### 4. Stakeholder Reporting
Share visual reports with non-technical stakeholders.

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'requests'`  
**Solution:** Install requests: `pip install requests`

**Issue:** `Error: Failed to fetch`  
**Solution:** Check your API URL and authentication token

**Issue:** `Permission denied`  
**Solution:** Ensure you have write permissions in the directory

**Issue:** Report shows 0 profiles  
**Solution:** Verify API endpoint is returning data

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Update README for new features
- Test thoroughly before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Project Maintainer:** Your Name  
**Email:** your.email@example.com  
**GitHub:** [@yourusername](https://github.com/yourusername)

---

## 🎉 Acknowledgments

- Thanks to the team for API access and support
- Inspired by data quality best practices
- Built with ❤️ for better data insights

---

## 🗺️ Roadmap

### Future Enhancements

- [ ] Email integration for automated reports
- [ ] Historical tracking and trend analysis
- [ ] Excel/CSV export options
- [ ] Advanced field validation (email format, phone patterns)
- [ ] Dashboard integration
- [ ] Scheduled execution (cron jobs)
- [ ] Multi-language support
- [ ] API rate limiting handling
- [ ] Database storage for historical data
- [ ] Comparison reports (before/after)

---

## 📚 Additional Resources

- [Python Requests Documentation](https://docs.python-requests.org/)
- [HTML Report Best Practices](https://www.w3.org/TR/html52/)
- [Data Quality Metrics Guide](https://example.com/data-quality)

---

