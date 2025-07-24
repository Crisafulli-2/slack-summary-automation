# Slack Daily Recap Automation - Source Files

## Essential Files (Use These)

### 🎯 **`clean_daily_automation.py`** - Main Script
- **Purpose**: Core automation script that extracts Slack recap data and writes to Google Sheets
- **Target Data**: "X of your Y recap channels had new messages on Date"
- **Usage**: Can run interactively or be imported by other scripts
- **Features**: 
  - Extracts channel activity statistics
  - Detects "Delivered with love" status
  - Writes clean data to Google Sheets
  - Robust error handling

### 🔄 **`daily_runner.py`** - Production Runner
- **Purpose**: Production-ready script for automated daily execution
- **Usage**: 
  ```bash
  python3 daily_runner.py "your_google_sheets_id"
  # OR
  export GOOGLE_SHEETS_ID="your_sheet_id" && python3 daily_runner.py
  ```
- **Cron Setup**:
  ```bash
  # Daily at 9 AM
  0 9 * * * cd /Users/jcris/Projects/Slack/src && python3 daily_runner.py >> ../logs/daily_recap.log 2>&1
  ```

### 🧪 **`test_complete_workflow.py`** - Testing Script
- **Purpose**: Test the complete workflow with Google Sheets integration
- **Usage**: `python3 test_complete_workflow.py`
- **Use this to**: Verify everything works before setting up automation

## Supporting Files

### 📊 **`google_sheets_real.py`** - Google Sheets Client
- **Purpose**: Helper class for Google Sheets API operations
- **Used by**: Other scripts for Sheets integration

### 📋 **`slack_recap_automation.py`** - Original Full Script  
- **Purpose**: Original comprehensive script with more features
- **Status**: Working but more complex than needed
- **Use**: If you need additional extraction strategies

### 🕐 **`daily_recap_runner.py`** - Legacy Runner
- **Purpose**: Original daily runner script
- **Status**: May reference old imports
- **Recommendation**: Use `daily_runner.py` instead

## Quick Start

1. **Test extraction only**:
   ```bash
   python3 -c "from clean_daily_automation import CleanSlackAutomation; CleanSlackAutomation().test_extraction_only()"
   ```

2. **Test complete workflow**:
   ```bash
   python3 test_complete_workflow.py
   ```

3. **Run daily automation**:
   ```bash
   python3 daily_runner.py "your_google_sheets_id"
   ```

## Data Format

The automation extracts and saves:
- **Date**: Current date
- **Time**: Extraction time
- **Active Channels**: Number from "X of your Y recap channels"
- **Total Channels**: Total number from pattern
- **Activity Rate**: Calculated percentage
- **Recap Date**: Date mentioned in recap (e.g., "Tuesday, June 10")
- **Delivered with Love**: ✅/❌ based on detection
- **Notes**: Timestamp and automation info

## Success Indicators

✅ **"8 of 10 channels active on Tuesday, June 10"** - Pattern found  
✅ **"Delivered with love: Yes"** - Status detected  
✅ **"Activity Rate: 80.0%"** - Statistics calculated  
✅ **Google Sheets integration working**
