import os
import sys
import re  # Import regex for cleaning
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure we're in project directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
os.chdir(project_dir)

# Add src to path
sys.path.append(script_dir)

from crew import crew
from email_service import EmailSubscriber

def generate_report():
    """Run the analyst crew and return combined report"""
    print("\n🚀 Starting Thai digital landscape analysis...")
    print(f"Model: ollama/qwen2.5:3b-instruct-q4_0")
    print("=" * 60)
    
    try:
        # Execute crew
        crew_output = crew.kickoff()
        
        # === THE FIX: Stitching outputs manually ===
        # CrewAI stores individual task results in 'tasks_output' list
        # Index 0 = Task 1 (English), Index 1 = Task 2 (Thai)
        
        english_part = crew_output.tasks_output[0].raw
        thai_part = crew_output.tasks_output[1].raw
        
        # Combine them with the separator
        full_report = f"{english_part}\n\n---\n\n{thai_part}"
        
        print("\n✓ Report generation complete (English + Thai merged)!")
        return full_report
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        # ... (keep your existing error handling)
        sys.exit(1)

def clean_report_format(report):
    """
    Clean the report to enforce proper formatting:
    1. Remove markdown code fences
    2. STRIP Chinese characters (don't delete whole lines)
    3. Make all headers bold
    4. Ensure clean separator between English and Thai sections
    """
    import re
    
    print("\n🧹 Cleaning report format...")
    
    # 1. Remove markdown code fences
    report = re.sub(r'^```markdown\s*\n?', '', report, flags=re.MULTILINE)
    report = re.sub(r'\n?```\s*$', '', report)

    # 2. Process lines (Safer Chinese Removal)
    lines = report.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Detect Chinese characters
        if re.search(r'[\u4e00-\u9fff]', line):
            # OPTION A: If line is > 50% Chinese, assume it's garbage and skip it
            chinese_char_count = len(re.findall(r'[\u4e00-\u9fff]', line))
            if chinese_char_count > len(line) * 0.5:
                continue 
            
            # OPTION B: Otherwise, just strip the Chinese chars and keep the English
            # This saves lines like "Source: Company (中文)"
            line = re.sub(r'[\u4e00-\u9fff]', '', line)
        
        cleaned_lines.append(line)
    
    report = '\n'.join(cleaned_lines)
    
    # 3. Make all headers bold (English & Thai)
    # Matches # Header and turns it into # **Header**
    report = re.sub(r'^(#+) ([^\*\n]+)$', r'\1 **\2**', report, flags=re.MULTILINE)
    
    # 4. Ensure clean separator for BOTH English "THAI REPORT" and Thai "รายงาน..." headers
    # This regex looks for common headers used for the Thai section
    thai_header_pattern = r'\n(#+ \**(?:\s*THAI REPORT|THAI VERSION|รายงาน|สรุป)\**[^\n]*)'
    
    if re.search(thai_header_pattern, report, re.IGNORECASE):
        report = re.sub(
            thai_header_pattern,
            r'\n\n---\n\n\1', # Add separator before the match
            report,
            flags=re.IGNORECASE
        )

    # 5. Clean up duplicate separators (---)
    report = re.sub(r'(\n\s*---\s*\n)+', r'\n\n---\n\n', report)
    
    print("✓ Report cleaned and formatted")
    return report.strip()

def main():
    # 1. Generate the raw report
    raw_report = generate_report()
    
    # 2. Clean and format the report
    cleaned_report = clean_report_format(raw_report)
    
    # 3. Save cleaned version
    with open("latest_report.md", "w") as f:
        f.write(cleaned_report)
    print("\n💾 Cleaned report saved to latest_report.md")
    
    # 4. Initialize subscriber service
    subscriber_service = EmailSubscriber()
    
    # 5. Add test subscriber (remove this in production)
    test_email = "pramirtha@gmail.com"  # CHANGE THIS
    if subscriber_service.add_subscriber(test_email, name="Test User"):
        print(f"✓ Added subscriber: {test_email}")
    
    # 6. Send cleaned report
    print("\n📧 Sending reports...")
    subscriber_service.send_report(
        cleaned_report,
        subject="Thai Digital Landscape Weekly Brief"
    )
    
    print("\n🎉 All tasks completed successfully!")

if __name__ == "__main__":
    main()
