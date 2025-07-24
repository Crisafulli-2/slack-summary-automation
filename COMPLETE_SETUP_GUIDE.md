# Slack Recap Automation - Complete Setup Guide

🚀 **Automated daily Slack workspace recap extraction with Google Sheets integration**

This project automatically scrapes daily recap content from your Slack workspace and saves summarized data to Google Sheets for tracking and analysis.

## ✅ What's Working

- ✅ **Slack Authentication**: Cookie-based authentication system
- ✅ **Selenium Scraper**: JavaScript-rendered content extraction
- ✅ **Google Sheets Integration**: Automated data writing
- ✅ **Content Detection**: Multiple strategies for finding recap content
- ✅ **Debug Capabilities**: Screenshots and page source saving
- ✅ **Error Handling**: Robust error handling and logging

## 📋 Quick Start

### 1. Install Dependencies

```bash
cd /Users/jcris/Projects/Slack
pip3 install -r requirements.txt
```

### 2. Setup Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create Service Account credentials
5. Download `credentials.json` file
6. Place file at: `/Users/jcris/Projects/Slack/credentials.json`

### 3. Install Chrome and ChromeDriver

**macOS (using Homebrew):**
```bash
brew install chromedriver
```

**Linux:**
```bash
sudo apt-get install chromium-chromedriver
```

### 4. Test the System

```bash
cd /Users/jcris/Projects/Slack/src

# Test Slack content extraction only
python3 slack_recap_automation.py
# Choose option 1

# Test Google Sheets integration
python3 test_sheets_integration.py
```

## 🎯 Main Scripts

### `slack_recap_automation.py`
**Complete automation with both scraping and Google Sheets**

```bash
python3 slack_recap_automation.py
```

- **Option 1**: Test extraction only (no Google Sheets)
- **Option 2**: Full automation (requires Google Sheets ID)

### `daily_recap_runner.py`
**Automated daily runner (perfect for cron jobs)**

```bash
# Set your Google Sheets ID in the script, then:
python3 daily_recap_runner.py

# Or pass as argument:
python3 daily_recap_runner.py "your_google_sheets_id_here"

# Or set environment variable:
export GOOGLE_SHEETS_ID="your_google_sheets_id_here"
python3 daily_recap_runner.py
```

### `test_sheets_integration.py`
**Test Google Sheets integration separately**

```bash
python3 test_sheets_integration.py
```

## 📊 Google Sheets Setup

### 1. Create a New Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```

### 2. Share with Service Account

1. Open your Google Sheet
2. Click "Share" button
3. Add your service account email (found in `credentials.json`)
4. Give "Editor" permissions

### 3. Data Structure

The automation creates these columns:
- **A**: Date (YYYY-MM-DD)
- **B**: Timestamp (YYYY-MM-DD HH:MM:SS)
- **C**: Active Channels (number)
- **D**: Total Channels (number)
- **E**: Activity Rate (percentage)
- **F**: Summary (formatted text)
- **G**: Raw Text (pipe-separated recap content)

## ⏰ Daily Automation Setup

### Option 1: Cron (Unix/Linux/macOS)

```bash
# Run setup helper
python3 schedule_automation.py

# Or manually add to crontab:
crontab -e

# Add this line for daily 9 AM execution:
0 9 * * * cd /Users/jcris/Projects/Slack/src && python3 daily_recap_runner.py >> cron_recap.log 2>&1
```

### Option 2: macOS launchd

```bash
python3 schedule_automation.py
# Choose option 2 for launchd setup
```

### Option 3: Manual Daily Execution

```bash
cd /Users/jcris/Projects/Slack/src
python3 daily_recap_runner.py
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Google Sheets ID (optional - can set in script)
GOOGLE_SHEETS_ID=your_google_sheets_id_here

# Chrome paths (optional)
CHROME_BINARY_PATH=/path/to/chrome
CHROMEDRIVER_PATH=/path/to/chromedriver
```

### Authentication Cookies

The Slack authentication cookies are configured in the scripts. If they expire:

1. Log into Slack in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies → slack.com
4. Copy the values for: `d`, `x`, `d-s`, `b`
5. Update the `cookies` dictionary in the automation scripts

## 🐛 Debugging

### Debug Files

The automation creates debug files:
- `debug_extraction_YYYYMMDD_HHMMSS.png` - Screenshots
- `debug_page_source_YYYYMMDD_HHMMSS.html` - Page source
- `cron_recap.log` - Cron execution logs

### Common Issues

**"ChromeDriver not found"**
```bash
# Install ChromeDriver
brew install chromedriver

# Or download manually from:
# https://chromedriver.chromium.org/
```

**"Credentials file not found"**
- Ensure `credentials.json` is in project root
- Check file permissions

**"No recap content found"**
- Check debug screenshots to see what page is loaded
- Verify Slack workspace ID is correct (`T2AAHSB5F`)
- Try running during different times when recap content might be available

**"Google Sheets permission denied"**
- Share the sheet with service account email
- Give "Editor" permissions
- Check the sheet ID is correct

## 📁 Project Structure

```
/Users/jcris/Projects/Slack/
├── credentials.json              # Google API credentials
├── requirements.txt              # Python dependencies
├── .env                         # Environment variables (optional)
├── README.md                    # This file
└── src/
    ├── slack_recap_automation.py    # Main automation script
    ├── daily_recap_runner.py        # Automated daily runner
    ├── test_sheets_integration.py   # Google Sheets testing
    ├── schedule_automation.py       # Cron/launchd setup helper
    ├── setup.py                     # Dependency installer
    ├── selenium_slack_scraper.py    # Original Selenium scraper
    └── google_sheets_real.py        # Google Sheets client
```

## 🎯 Next Steps

1. **Test the complete workflow**: Run `python3 slack_recap_automation.py` and choose option 2
2. **Setup daily automation**: Use `python3 schedule_automation.py` to configure cron
3. **Monitor logs**: Check debug files and cron logs for issues
4. **Customize extraction**: Modify recap keywords in `slack_recap_automation.py` if needed

## 🚀 Success Indicators

- ✅ Chrome browser opens and navigates to Slack
- ✅ Authentication cookies are applied successfully
- ✅ Page loads and JavaScript renders
- ✅ Debug screenshots show Slack workspace content
- ✅ Data is written to Google Sheets with proper formatting
- ✅ Daily automation runs without errors

## 💡 Tips

- **Run tests first**: Always test manually before setting up automation
- **Check debug files**: Screenshots and page source help diagnose issues
- **Monitor regularly**: Check logs and Google Sheets for consistent operation
- **Update cookies**: Refresh authentication cookies if they expire
- **Backup data**: Export Google Sheets data regularly

---

🎉 **Ready to automate your Slack recap tracking!**
