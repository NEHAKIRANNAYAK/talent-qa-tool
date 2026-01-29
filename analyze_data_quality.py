import requests
import json
from collections import defaultdict
from datetime import datetime

# Configuration
API_URL = "http://34.56.103.200/talent-profiling-service/talent/get-profiles"
AUTH_TOKEN = "835d6dc88b708bc646d6db82c853ef4182fabbd4a8de59c213f2b5ab3ae7d9be"

# Fields to analyze
FIELDS_TO_CHECK = [
    'name', 'email', 'phone', 'experience_years', 'domain', 
    'summary', 'country', 'skills', 'current_role', 
    'current_company', 'current_location'
]

def fetch_all_data():
    """Fetch all profiles from the API with pagination"""
    all_profiles = []
    page = 1
    
    print("🔄 Fetching data from API...")
    
    while True:
        print(f"   Fetching page {page}...")
        
        try:
            response = requests.get(
                f"{API_URL}?limit=500&page={page}",
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {AUTH_TOKEN}'
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            if not data or len(data) == 0:
                break
                
            all_profiles.extend(data)
            page += 1
            
            # Safety limit
            if page > 20:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data: {e}")
            break
    
    print(f"✅ Successfully fetched {len(all_profiles)} profiles")
    return all_profiles

def analyze_data_quality(profiles):
    """Analyze data quality by role"""
    print("\n📊 Analyzing data quality...")
    
    role_stats = defaultdict(lambda: {
        'count': 0,
        'missing_fields': defaultdict(int),
        'total_fields': len(FIELDS_TO_CHECK)
    })
    
    field_stats = defaultdict(lambda: {'missing': 0, 'total': 0})
    
    for profile in profiles:
        data = profile.get('json_structure', {})
        role = data.get('current_role') or 'Unknown Role'
        
        role_stats[role]['count'] += 1
        
        for field in FIELDS_TO_CHECK:
            value = data.get(field)
            is_empty = (
                value is None or 
                value == '' or 
                (isinstance(value, list) and len(value) == 0)
            )
            
            field_stats[field]['total'] += 1
            
            if is_empty:
                role_stats[role]['missing_fields'][field] += 1
                field_stats[field]['missing'] += 1
    
    # Calculate percentages for roles
    role_analysis = []
    for role, stats in role_stats.items():
        total_possible = stats['count'] * stats['total_fields']
        total_missing = sum(stats['missing_fields'].values())
        missing_percentage = (total_missing / total_possible * 100) if total_possible > 0 else 0
        quality_score = 100 - missing_percentage
        
        role_analysis.append({
            'role': role,
            'count': stats['count'],
            'missing_percentage': round(missing_percentage, 1),
            'quality_score': round(quality_score, 1),
            'field_breakdown': dict(stats['missing_fields'])
        })
    
    # Calculate percentages for fields
    field_analysis = []
    for field, stats in field_stats.items():
        missing_percentage = (stats['missing'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        field_analysis.append({
            'field': field,
            'total': stats['total'],
            'missing': stats['missing'],
            'missing_percentage': round(missing_percentage, 1)
        })
    
    return {
        'role_analysis': sorted(role_analysis, key=lambda x: x['count'], reverse=True),
        'field_analysis': sorted(field_analysis, key=lambda x: x['missing_percentage'], reverse=True)
    }

def generate_html_report(profiles, analysis):
    """Generate an interactive HTML report"""
    print("\n📝 Generating HTML report...")
    
    total_profiles = len(profiles)
    unique_roles = len(analysis['role_analysis'])
    avg_quality = sum(r['quality_score'] for r in analysis['role_analysis']) / unique_roles if unique_roles > 0 else 0
    fields_analyzed = len(analysis['field_analysis'])
    
    # Generate role rows
    role_rows = ""
    for item in analysis['role_analysis']:
        quality_class = 'good' if item['quality_score'] >= 80 else 'warning' if item['quality_score'] >= 60 else 'bad'
        role_rows += f"""
            <tr>
                <td><span class="role-badge">{item['role']}</span></td>
                <td>{item['count']}</td>
                <td><span class="percentage {quality_class}">{item['missing_percentage']}%</span></td>
                <td><span class="percentage {quality_class}">{item['quality_score']}%</span></td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill {quality_class}" style="width: {item['quality_score']}%"></div>
                    </div>
                </td>
            </tr>
        """
    
    # Generate field cards
    field_cards = ""
    for field in analysis['field_analysis']:
        quality_class = 'good' if field['missing_percentage'] < 20 else 'warning' if field['missing_percentage'] < 40 else 'bad'
        field_cards += f"""
            <div class="field-card">
                <div class="field-name">{field['field']}</div>
                <div class="field-stats">
                    <span>Missing: {field['missing']} / {field['total']}</span>
                    <span class="percentage {quality_class}">{field['missing_percentage']}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill {quality_class}" style="width: {field['missing_percentage']}%"></div>
                </div>
            </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Quality Analysis Report</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: #0F172A;
            --secondary: #1E293B;
            --accent: #10B981;
            --accent-dark: #059669;
            --danger: #EF4444;
            --warning: #F59E0B;
            --bg: #F8FAFC;
            --card: #FFFFFF;
            --text: #0F172A;
            --text-muted: #64748B;
            --border: #E2E8F0;
            --shadow: rgba(15, 23, 42, 0.08);
        }}
        
        body {{
            font-family: 'DM Sans', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 16px;
            margin-bottom: 40px;
            box-shadow: 0 20px 40px var(--shadow);
            position: relative;
            overflow: hidden;
        }}
        
        header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, transparent 70%);
            border-radius: 50%;
        }}
        
        header h1 {{
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }}
        
        header p {{
            font-size: 18px;
            opacity: 0.85;
            position: relative;
            z-index: 1;
        }}
        
        .meta {{
            background: rgba(255, 255, 255, 0.1);
            padding: 16px 20px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
            position: relative;
            z-index: 1;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}
        
        .stat-card {{
            background: var(--card);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 16px var(--shadow);
            border: 1px solid var(--border);
        }}
        
        .stat-label {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: var(--text);
        }}
        
        .results-table {{
            background: var(--card);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px var(--shadow);
            border: 1px solid var(--border);
            margin-bottom: 32px;
        }}
        
        .table-header {{
            background: var(--primary);
            color: white;
            padding: 20px 24px;
            font-weight: 700;
            font-size: 18px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        thead {{
            background: var(--bg);
        }}
        
        th {{
            padding: 16px 24px;
            text-align: left;
            font-weight: 700;
            color: var(--text);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid var(--border);
        }}
        
        td {{
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            font-size: 15px;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        tbody tr:hover {{
            background: var(--bg);
        }}
        
        .role-badge {{
            display: inline-block;
            padding: 6px 14px;
            background: var(--primary);
            color: white;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        
        .percentage {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 16px;
        }}
        
        .percentage.good {{
            color: var(--accent);
        }}
        
        .percentage.warning {{
            color: var(--warning);
        }}
        
        .percentage.bad {{
            color: var(--danger);
        }}
        
        .progress-bar {{
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        
        .progress-fill.good {{
            background: linear-gradient(90deg, var(--accent), var(--accent-dark));
        }}
        
        .progress-fill.warning {{
            background: linear-gradient(90deg, var(--warning), #D97706);
        }}
        
        .progress-fill.bad {{
            background: linear-gradient(90deg, var(--danger), #DC2626);
        }}
        
        .field-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 24px;
        }}
        
        .field-card {{
            background: var(--bg);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--accent);
        }}
        
        .field-name {{
            font-weight: 700;
            color: var(--text);
            margin-bottom: 12px;
            font-size: 14px;
        }}
        
        .field-stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        
        @media print {{
            body {{
                padding: 20px;
            }}
            
            .stat-card, .results-table {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Talent Data Quality Analysis Report</h1>
            <p>Comprehensive analysis of profile data quality across roles</p>
            <div class="meta">
                Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Profiles</div>
                <div class="stat-value">{total_profiles}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Unique Roles</div>
                <div class="stat-value">{unique_roles}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Data Quality</div>
                <div class="stat-value">{avg_quality:.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Fields Analyzed</div>
                <div class="stat-value">{fields_analyzed}</div>
            </div>
        </div>
        
        <div class="results-table">
            <div class="table-header">
                📊 Data Quality by Role
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Role</th>
                        <th>Profiles</th>
                        <th>Missing %</th>
                        <th>Quality Score</th>
                        <th>Visual</th>
                    </tr>
                </thead>
                <tbody>
                    {role_rows}
                </tbody>
            </table>
        </div>
        
        <div class="results-table">
            <div class="table-header">
                🔍 Field-Level Analysis
            </div>
            <div class="field-details">
                {field_cards}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    print("=" * 60)
    print("🎯 TALENT DATA QUALITY ANALYZER")
    print("=" * 60)
    
    # Step 1: Fetch data
    profiles = fetch_all_data()
    
    if not profiles:
        print("\n❌ No data to analyze. Exiting.")
        return
    
    # Step 2: Analyze data
    analysis = analyze_data_quality(profiles)
    
    # Step 3: Generate report
    html_report = generate_html_report(profiles, analysis)
    
    # Step 4: Save report
    filename = f"data_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"\n✅ Report generated successfully: {filename}")
    print(f"\n📈 Summary:")
    print(f"   • Total Profiles: {len(profiles)}")
    print(f"   • Unique Roles: {len(analysis['role_analysis'])}")
    print(f"   • Average Quality Score: {sum(r['quality_score'] for r in analysis['role_analysis']) / len(analysis['role_analysis']):.1f}%")
    print(f"\n🎉 Open the HTML file in your browser to view the full report!")
    print("=" * 60)

if __name__ == "__main__":
    main()