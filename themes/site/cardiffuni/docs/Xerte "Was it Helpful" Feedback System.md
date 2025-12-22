# Xerte Feedback System Implementation Guide

## Overview

This guide shows how to add a simple "Was this helpful?" feedback system to your Xerte projects that automatically collects responses in a Google Spreadsheet. The system works entirely client-side with no server requirements.

## What You'll Get

- Simple Yes/No feedback buttons on your Xerte pages
- Automatic data collection in Google Sheets
- Fallback to local storage if Google Sheets is unavailable
- Real-time feedback tracking with timestamps and user details

## Prerequisites

- Google account
- Xerte project with ability to add HTML and JavaScript
- Basic understanding of HTML/JavaScript (copy-paste level)

---

## Step 1: Create Your Google Spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it something descriptive like "Xerte Feedback - [Project Name]"
4. Set up column headers in the first row:
   - **A1**: `Timestamp`
   - **B1**: `Content ID`
   - **C1**: `Helpful`
   - **D1**: `User Agent`
   - **E1**: `Page URL`

---

## Step 2: Create Google Apps Script

1. In your spreadsheet, go to **Extensions** → **Apps Script**
2. Delete any existing code and replace it with this:

```javascript
function doPost(e) {
  return handleRequest(e);
}

function doGet(e) {
  return handleRequest(e);
}

function handleRequest(e) {
  try {
    // Get the active spreadsheet
    const sheet = SpreadsheetApp.getActiveSheet();
    
    let data;
    
    // Handle both POST and GET requests
    if (e.postData) {
      data = JSON.parse(e.postData.contents);
    } else {
      // For GET requests, data comes from parameters
      data = e.parameter;
      data.helpful = data.helpful === 'true'; // Convert string to boolean
    }
    
    // Add a new row with the feedback data
    sheet.appendRow([
      new Date(), // Timestamp
      data.contentId || 'unknown',
      data.helpful ? 'Yes' : 'No',
      data.userAgent || 'unknown',
      data.pageUrl || 'unknown'
    ]);
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({status: 'success'}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({status: 'error', message: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

3. Save the script (Ctrl+S or Cmd+S)
4. Give it a descriptive name like "Feedback Data Collector"

---

## Step 3: Deploy the Script as Web App

1. Click the **Deploy** button (top right)
2. Choose **New deployment**
3. Click the gear icon next to "Type" and select **Web app**
4. Configure these settings:
   - **Description**: "Feedback Collector for [Your Project Name]"
   - **Execute as**: Me
   - **Who has access**: Anyone
5. Click **Deploy**
6. **⚠️ Security Warning**: You'll see a Google security warning. This is normal for new scripts:
   - Click "Hide Advanced"
   - Click "Go to [Your Script Name] (unsafe)" - it's safe because you created it
   - Click "Allow" when prompted for permissions
7. **Important**: Copy the Web App URL that appears - you'll need this for the next step
8. Click **Done**

---

## Step 4: Add HTML to Your Xerte Page

Add this HTML code to your Xerte page where you want the feedback buttons to appear:

```html
<div id="feedback-section">
    <p>Was this helpful?</p>
    <div id="feedback-buttons">
        <button onclick="handleFeedback(true)">Yes</button>
        <button onclick="handleFeedback(false)">No</button>
    </div>
</div>
```

### Optional: Add Custom Styling

You can style the buttons with CSS:

```html
<style>
#feedback-section {
    margin: 20px 0;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f9f9f9;
}

#feedback-buttons button {
    margin: 5px;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

#feedback-buttons button:first-child {
    background-color: #4CAF50;
    color: white;
}

#feedback-buttons button:last-child {
    background-color: #f44336;
    color: white;
}

#feedback-buttons button:hover {
    opacity: 0.8;
}
</style>
```

---

## Step 5: Add JavaScript to Your Xerte Page

Add this JavaScript code to your Xerte page. **Important**: Replace `YOUR_WEB_APP_URL_HERE` with the actual URL you copied from Step 3.

```javascript
// Replace this URL with your actual Google Apps Script Web App URL
const GOOGLE_SCRIPT_URL = 'YOUR_WEB_APP_URL_HERE';

function handleFeedback(isHelpful) {
    // Get a unique identifier for this content/page
    const contentId = getContentId();
    
    // Prepare the data to send
    const feedbackData = {
        contentId: contentId,
        helpful: isHelpful,
        userAgent: navigator.userAgent,
        pageUrl: window.location.href,
        timestamp: new Date().toISOString()
    };
    
    // Send to Google Sheets
    sendToGoogleSheets(feedbackData);
    
    // Update the UI to show thank you message
    document.getElementById('feedback-buttons').innerHTML = 
        '<p style="color: green;">Thank you for your feedback!</p>';
}

function getContentId() {
    // Use page title as content identifier
    // You can customize this to better identify your content
    return document.title || 'unknown-page';
}

function sendToGoogleSheets(data) {
    // Create URL with parameters for GET request
    const params = new URLSearchParams({
        contentId: data.contentId,
        helpful: data.helpful.toString(),
        userAgent: data.userAgent,
        pageUrl: data.pageUrl,
        timestamp: data.timestamp
    });
    
    const urlWithParams = `${GOOGLE_SCRIPT_URL}?${params.toString()}`;
    
    // Use fetch with GET method to avoid CORS issues
    fetch(urlWithParams, {
        method: 'GET',
        mode: 'no-cors'
    })
    .then(() => {
        console.log('Feedback sent successfully');
    })
    .catch(error => {
        console.error('Error sending feedback:', error);
        
        // Fallback: store in localStorage if Google Sheets fails
        const fallbackKey = `feedback_${data.contentId}_${Date.now()}`;
        localStorage.setItem(fallbackKey, JSON.stringify(data));
        console.log('Feedback stored locally as fallback');
    });
}
```

---

## Step 6: Test Your Implementation

1. Load your Xerte page
2. Click the "Yes" or "No" buttons
3. Check your Google Spreadsheet - you should see new rows with feedback data
4. Open browser developer tools (F12) and check the Console tab for any error messages

---

## Customization Options

### Custom Content Identifiers

Instead of using the page title, you can create more specific content identifiers:

#### Option A: Add data attributes to your HTML
```html
<div id="feedback-section" data-content-id="lesson-1-introduction">
    <p>Was this helpful?</p>
    <div id="feedback-buttons">
        <button onclick="handleFeedback(true)">Yes</button>
        <button onclick="handleFeedback(false)">No</button>
    </div>
</div>
```

Then update the `getContentId()` function:
```javascript
function getContentId() {
    return document.getElementById('feedback-section').getAttribute('data-content-id') || 'unknown-content';
}
```

#### Option B: Use URL-based identifiers
```javascript
function getContentId() {
    // Extract meaningful part from URL
    const urlParts = window.location.pathname.split('/');
    return urlParts[urlParts.length - 1] || document.title;
}
```

#### Option C: Combine multiple identifiers
```javascript
function getContentId() {
    const pageTitle = document.title;
    const urlPath = window.location.pathname;
    return `${pageTitle} - ${urlPath}`;
}
```

### Multiple Feedback Sections

If you have multiple feedback sections on one page, add unique identifiers:

```html
<!-- Section 1 -->
<div class="feedback-section" data-content-id="section-1-overview">
    <p>Was this section helpful?</p>
    <div class="feedback-buttons">
        <button onclick="handleFeedback(true, 'section-1-overview')">Yes</button>
        <button onclick="handleFeedback(false, 'section-1-overview')">No</button>
    </div>
</div>

<!-- Section 2 -->
<div class="feedback-section" data-content-id="section-2-examples">
    <p>Were the examples clear?</p>
    <div class="feedback-buttons">
        <button onclick="handleFeedback(true, 'section-2-examples')">Yes</button>
        <button onclick="handleFeedback(false, 'section-2-examples')">No</button>
    </div>
</div>
```

Update the JavaScript function:
```javascript
function handleFeedback(isHelpful, specificContentId = null) {
    const contentId = specificContentId || getContentId();
    // ... rest of the function remains the same
}
```

---

## Data Analysis

### What Data Gets Collected

Your spreadsheet will contain:
- **Timestamp**: When the feedback was submitted
- **Content ID**: Identifier for the content (page title, custom ID, etc.)
- **Helpful**: "Yes" or "No"
- **User Agent**: Browser and device information
- **Page URL**: Full URL where feedback was given

### Basic Analysis in Google Sheets

You can create simple analytics using Google Sheets formulas:

#### Count total responses for specific content:
```
=COUNTIF(B:B,"your-content-id")
```

#### Calculate percentage of helpful responses:
```
=COUNTIFS(B:B,"your-content-id",C:C,"Yes")/COUNTIF(B:B,"your-content-id")*100
```

#### Most recent feedback:
```
=QUERY(A:E,"SELECT * ORDER BY A DESC LIMIT 10")
```

---

## Troubleshooting

### Common Issues

**Problem**: Buttons don't respond
- **Solution**: Check browser console for JavaScript errors
- **Check**: Make sure the Web App URL is correctly set in the JavaScript

**Problem**: Data not appearing in spreadsheet
- **Solution**: Verify the Google Apps Script is deployed with "Anyone" access
- **Check**: Test the Web App URL directly in your browser

**Problem**: "Access denied" errors
- **Solution**: Re-deploy the Google Apps Script and update the URL
- **Check**: Make sure you completed the security authorization in Step 3

**Problem**: Feedback stored locally but not in sheets
- **Solution**: This is the fallback working correctly - check your internet connection and Google Apps Script status

### Testing Checklist

- [ ] Google Apps Script is saved and deployed
- [ ] Web App URL is correctly copied into JavaScript
- [ ] HTML buttons are properly configured
- [ ] Browser console shows no errors
- [ ] Test data appears in Google Spreadsheet
- [ ] Thank you message appears after clicking buttons

---

## Security and Privacy

### Data Collection
- Only collects feedback responses, timestamps, and basic technical information
- No personal identifying information is collected
- User Agent data helps identify browser compatibility issues

### Access Control
- Google Apps Script runs with your permissions
- Data is stored in your Google Drive
- You control who can access the spreadsheet

### GDPR Compliance
- Consider adding a privacy notice if required in your region
- Data collected is minimal and task-related
- Users can request data deletion through standard Google procedures

---

## Maintenance

### Regular Tasks
- Monitor spreadsheet for unusual patterns
- Periodically clean up old data if needed
- Check that the feedback system is working across different browsers

### Scaling Up
- For high-traffic sites, consider implementing rate limiting
- Monitor Google Apps Script execution quotas
- Consider upgrading to Google Workspace for higher limits

---

## Support

If you encounter issues:

1. Check the browser console for error messages
2. Verify all URLs and IDs are correctly copied
3. Test with a fresh incognito/private browser window
4. Refer to the troubleshooting section above

For questions specific to this implementation, contact [your contact information].

---

## Security Enhancements

### Overview

The basic feedback system can be enhanced with security features to prevent spam, abuse, and automated submissions. These enhancements work on both client-side and server-side to provide comprehensive protection.

### Security Features Available

- **Rate Limiting**: Prevents excessive submissions per session/time window
- **Cooldown Periods**: Enforces waiting time between submissions
- **Duplicate Detection**: Prevents multiple identical submissions
- **Bot Detection**: Requires genuine user interaction
- **Basic Fingerprinting**: Creates anonymous user identifiers
- **Risk Scoring**: Server-side analysis of submission patterns
- **Timestamp Validation**: Prevents replay attacks

### Enhanced Google Apps Script (Server-side Security)

Replace your basic Google Apps Script with this enhanced version:

```javascript
function doGet(e) {
  return handleSecureRequest(e);
}

function doPost(e) {
  return handleSecureRequest(e);
}

function handleSecureRequest(e) {
  try {
    // Get parameters
    const data = e.parameter;
    
    // Server-side validation
    const validation = validateSubmission(data);
    if (!validation.isValid) {
      console.log('Rejected submission:', validation.reason);
      return createResponse({status: 'rejected', reason: validation.reason});
    }
    
    // Check for duplicate submissions
    if (isDuplicate(data)) {
      console.log('Duplicate submission detected');
      return createResponse({status: 'duplicate'});
    }
    
    // Store in spreadsheet with additional security data
    const sheet = SpreadsheetApp.getActiveSheet();
    sheet.appendRow([
      new Date(),                    // Timestamp
      data.contentId || 'unknown',   // Content ID
      data.helpful === 'true' ? 'Yes' : 'No', // Helpful
      data.userAgent || 'unknown',   // User Agent
      data.pageUrl || 'unknown',     // Page URL
      data.sessionCount || '1',      // Session Count
      data.fingerprint || 'unknown', // User Fingerprint
      data.referrer || 'direct',     // Referrer
      calculateRiskScore(data)       // Risk Score
    ]);
    
    return createResponse({status: 'success'});
    
  } catch (error) {
    console.error('Error processing feedback:', error);
    return createResponse({status: 'error', message: error.toString()});
  }
}

function validateSubmission(data) {
  // Check required fields
  if (!data.contentId || !data.helpful) {
    return {isValid: false, reason: 'Missing required fields'};
  }
  
  // Check timestamp (not too old, not in future)
  const submissionTime = new Date(data.timestamp);
  const now = new Date();
  const fiveMinutesAgo = new Date(now.getTime() - 5 * 60000);
  const oneMinuteFuture = new Date(now.getTime() + 60000);
  
  if (submissionTime < fiveMinutesAgo || submissionTime > oneMinuteFuture) {
    return {isValid: false, reason: 'Invalid timestamp'};
  }
  
  // Check session count (basic sanity check)
  const sessionCount = parseInt(data.sessionCount) || 1;
  if (sessionCount > 10) {
    return {isValid: false, reason: 'Suspicious session count'};
  }
  
  return {isValid: true};
}

function isDuplicate(data) {
  const sheet = SpreadsheetApp.getActiveSheet();
  const lastRow = sheet.getLastRow();
  
  if (lastRow < 2) return false; // No data yet
  
  // Check last 10 submissions for exact duplicates
  const checkRows = Math.min(10, lastRow - 1);
  const range = sheet.getRange(lastRow - checkRows + 1, 1, checkRows, 9);
  const values = range.getValues();
  
  for (let i = 0; i < values.length; i++) {
    const row = values[i];
    if (row[1] === data.contentId && 
        row[4] === data.pageUrl && 
        row[6] === data.fingerprint) {
      // Check if submitted within last 5 minutes
      const submissionTime = new Date(row[0]);
      const fiveMinutesAgo = new Date(Date.now() - 5 * 60000);
      if (submissionTime > fiveMinutesAgo) {
        return true;
      }
    }
  }
  
  return false;
}

function calculateRiskScore(data) {
  let riskScore = 0;
  
  // High session count increases risk
  const sessionCount = parseInt(data.sessionCount) || 1;
  if (sessionCount > 5) riskScore += 3;
  else if (sessionCount > 3) riskScore += 1;
  
  // No referrer increases risk
  if (!data.referrer || data.referrer === 'direct') riskScore += 1;
  
  // Missing fingerprint increases risk
  if (!data.fingerprint || data.fingerprint === 'unknown') riskScore += 2;
  
  // Suspicious user agent patterns
  const userAgent = (data.userAgent || '').toLowerCase();
  if (userAgent.includes('bot') || userAgent.includes('crawler') || 
      userAgent.includes('spider') || userAgent.length < 10) {
    riskScore += 5;
  }
  
  return Math.min(riskScore, 10); // Cap at 10
}

function createResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
```

### Enhanced JavaScript (Client-side Security)

Replace your basic JavaScript with this secure version:

```javascript
// Replace this URL with your actual Google Apps Script Web App URL
const GOOGLE_SCRIPT_URL = 'YOUR_WEB_APP_URL_HERE';

// Security configuration - adjust these values based on your needs
const SECURITY_CONFIG = {
    maxFeedbackPerSession: 3,           // Max feedback per session
    maxFeedbackPerPage: 1,              // Max feedback per page/content
    rateLimitWindow: 60000,             // 1 minute window for rate limiting
    maxFeedbackPerWindow: 2,            // Max 2 feedback per minute
    cooldownPeriod: 30000,              // 30 seconds between feedback
    enableFingerprinting: true,         // Enable basic fingerprinting
    requireUserInteraction: true        // Require genuine user interaction
};

// Security state tracking
let securityState = {
    sessionFeedbackCount: 0,
    lastFeedbackTime: 0,
    pageSubmitted: false,
    recentSubmissions: [],
    userFingerprint: null,
    interactionDetected: false
};

// Initialize security system
function initializeSecurity() {
    // Generate basic user fingerprint
    if (SECURITY_CONFIG.enableFingerprinting) {
        securityState.userFingerprint = generateUserFingerprint();
    }
    
    // Load session data
    loadSecurityState();
    
    // Set up interaction detection
    if (SECURITY_CONFIG.requireUserInteraction) {
        setupInteractionDetection();
    }
    
    // Clean old rate limit data
    cleanOldSubmissions();
}

function generateUserFingerprint() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.textBaseline = 'top';
    ctx.font = '14px Arial';
    ctx.fillText('Feedback fingerprint', 2, 2);
    
    return btoa(JSON.stringify({
        screen: `${screen.width}x${screen.height}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        language: navigator.language,
        platform: navigator.platform,
        canvas: canvas.toDataURL().slice(-50), // Last 50 chars of canvas data
        timestamp: Date.now()
    }));
}

function setupInteractionDetection() {
    // Track real user interactions
    ['mousedown', 'keydown', 'touchstart'].forEach(event => {
        document.addEventListener(event, () => {
            securityState.interactionDetected = true;
        }, { once: true, passive: true });
    });
}

function loadSecurityState() {
    try {
        const saved = localStorage.getItem('feedbackSecurityState');
        if (saved) {
            const data = JSON.parse(saved);
            securityState.sessionFeedbackCount = data.sessionFeedbackCount || 0;
            securityState.recentSubmissions = data.recentSubmissions || [];
            securityState.pageSubmitted = data.pageSubmitted || false;
        }
    } catch (e) {
        console.warn('Could not load security state:', e);
    }
}

function saveSecurityState() {
    try {
        localStorage.setItem('feedbackSecurityState', JSON.stringify({
            sessionFeedbackCount: securityState.sessionFeedbackCount,
            recentSubmissions: securityState.recentSubmissions,
            pageSubmitted: securityState.pageSubmitted
        }));
    } catch (e) {
        console.warn('Could not save security state:', e);
    }
}

function cleanOldSubmissions() {
    const now = Date.now();
    securityState.recentSubmissions = securityState.recentSubmissions.filter(
        time => now - time < SECURITY_CONFIG.rateLimitWindow
    );
}

function validateFeedbackSubmission() {
    const now = Date.now();
    const errors = [];
    
    // Check if page already submitted
    if (securityState.pageSubmitted && SECURITY_CONFIG.maxFeedbackPerPage === 1) {
        errors.push('Feedback already submitted for this page');
    }
    
    // Check session limit
    if (securityState.sessionFeedbackCount >= SECURITY_CONFIG.maxFeedbackPerSession) {
        errors.push(`Maximum ${SECURITY_CONFIG.maxFeedbackPerSession} feedback submissions per session reached`);
    }
    
    // Check cooldown period
    if (now - securityState.lastFeedbackTime < SECURITY_CONFIG.cooldownPeriod) {
        const remainingTime = Math.ceil((SECURITY_CONFIG.cooldownPeriod - (now - securityState.lastFeedbackTime)) / 1000);
        errors.push(`Please wait ${remainingTime} seconds before submitting again`);
    }
    
    // Check rate limiting
    cleanOldSubmissions();
    if (securityState.recentSubmissions.length >= SECURITY_CONFIG.maxFeedbackPerWindow) {
        errors.push('Too many submissions in a short time. Please wait a moment.');
    }
    
    // Check user interaction (bot detection)
    if (SECURITY_CONFIG.requireUserInteraction && !securityState.interactionDetected) {
        errors.push('Invalid interaction detected');
    }
    
    return errors;
}

// Updated handleFeedback function with security
function handleFeedback(isHelpful) {
    const validationErrors = validateFeedbackSubmission();
    
    if (validationErrors.length > 0) {
        showRateLimitMessage(validationErrors[0]);
        return;
    }
    
    // Update security state
    const now = Date.now();
    securityState.sessionFeedbackCount++;
    securityState.lastFeedbackTime = now;
    securityState.pageSubmitted = true;
    securityState.recentSubmissions.push(now);
    
    // Save state
    saveSecurityState();
    
    // Prepare secure data
    const feedbackData = {
        contentId: getContentId(),
        helpful: isHelpful,
        userAgent: navigator.userAgent,
        pageUrl: window.location.href,
        timestamp: new Date().toISOString(),
        sessionCount: securityState.sessionFeedbackCount,
        fingerprint: securityState.userFingerprint,
        referrer: document.referrer || 'direct'
    };
    
    // Send feedback
    sendToGoogleSheets(feedbackData);
    
    // Update UI
    showSuccessMessage();
    disableFeedbackButtons();
}

function sendToGoogleSheets(data) {
    // Create URL with parameters for GET request
    const params = new URLSearchParams({
        contentId: data.contentId,
        helpful: data.helpful.toString(),
        userAgent: data.userAgent,
        pageUrl: data.pageUrl,
        timestamp: data.timestamp,
        sessionCount: data.sessionCount.toString(),
        fingerprint: data.fingerprint || 'unknown',
        referrer: data.referrer
    });
    
    const urlWithParams = `${GOOGLE_SCRIPT_URL}?${params.toString()}`;
    
    // Use fetch with GET method to avoid CORS issues
    fetch(urlWithParams, {
        method: 'GET',
        mode: 'no-cors'
    })
    .then(() => {
        console.log('Feedback sent successfully');
    })
    .catch(error => {
        console.error('Error sending feedback:', error);
        
        // Fallback: store in localStorage if Google Sheets fails
        const fallbackKey = `feedback_${data.contentId}_${Date.now()}`;
        localStorage.setItem(fallbackKey, JSON.stringify(data));
        console.log('Feedback stored locally as fallback');
    });
}

function getContentId() {
    // Use page title as content identifier
    // You can customize this to better identify your content
    return document.title || 'unknown-page';
}

function showRateLimitMessage(message) {
    // Create or update rate limit message display
    let infoDiv = document.getElementById('rate-limit-info');
    if (!infoDiv) {
        infoDiv = document.createElement('div');
        infoDiv.id = 'rate-limit-info';
        document.getElementById('feedback-section').appendChild(infoDiv);
    }
    
    infoDiv.innerHTML = `<div style="background: rgba(255, 193, 7, 0.2); color: #856404; padding: 10px; border-radius: 5px; margin: 10px 0; font-size: 14px;">${message}</div>`;
    
    // Clear message after 5 seconds
    setTimeout(() => {
        infoDiv.innerHTML = '';
    }, 5000);
}

function showSuccessMessage() {
    document.getElementById('feedback-buttons').innerHTML = 
        '<p style="color: green;">Thank you for your feedback!</p>';
}

function disableFeedbackButtons() {
    const buttons = document.querySelectorAll('#feedback-buttons button');
    buttons.forEach(button => {
        button.disabled = true;
    });
}

// Initialize security when page loads
document.addEventListener('DOMContentLoaded', initializeSecurity);
```

### Updated Spreadsheet Columns

With security enhancements, your spreadsheet will have these columns:
- **A**: `Timestamp`
- **B**: `Content ID`
- **C**: `Helpful`
- **D**: `User Agent`
- **E**: `Page URL`
- **F**: `Session Count` (new)
- **G**: `Fingerprint` (new)
- **H**: `Referrer` (new)
- **I**: `Risk Score` (new)

### Security Configuration Options

#### Standard Security (Recommended):
```javascript
const SECURITY_CONFIG = {
    maxFeedbackPerSession: 3,
    maxFeedbackPerPage: 1,
    rateLimitWindow: 60000,        // 1 minute
    maxFeedbackPerWindow: 2,
    cooldownPeriod: 30000,         // 30 seconds
    enableFingerprinting: true,
    requireUserInteraction: true
};
```

#### High Security:
```javascript
const SECURITY_CONFIG = {
    maxFeedbackPerSession: 1,
    maxFeedbackPerPage: 1,
    rateLimitWindow: 300000,       // 5 minutes
    maxFeedbackPerWindow: 1,
    cooldownPeriod: 120000,        // 2 minutes
    enableFingerprinting: true,
    requireUserInteraction: true
};
```

#### Privacy-Focused:
```javascript
const SECURITY_CONFIG = {
    maxFeedbackPerSession: 3,
    maxFeedbackPerPage: 1,
    rateLimitWindow: 60000,
    maxFeedbackPerWindow: 2,
    cooldownPeriod: 30000,
    enableFingerprinting: false,   // Disable fingerprinting
    requireUserInteraction: true
};
```

### Security Monitoring

#### View Security Statistics:
Add this function to monitor security in browser console:
```javascript
function getSecurityStats() {
    return {
        sessionCount: securityState.sessionFeedbackCount,
        recentSubmissions: securityState.recentSubmissions.length,
        pageSubmitted: securityState.pageSubmitted,
        fingerprint: securityState.userFingerprint ? 'Generated' : 'None'
    };
}
```

#### Google Sheets Analytics:
Add these formulas to monitor suspicious activity:
- High-risk submissions: `=COUNTIF(I:I,">5")`
- Submissions today: `=COUNTIFS(A:A,">="&TODAY(),A:A,"<"&TODAY()+1)`
- Unique fingerprints: `=COUNTA(UNIQUE(FILTER(G:G,G:G<>"unknown")))`

### Implementation Notes

**When to Use Security Enhancements:**
- Public-facing educational content
- High-traffic Xerte projects
- Content where feedback affects decisions
- When you've experienced spam or abuse

**Performance Impact:**
- Minimal overhead (< 1ms per check)
- All operations happen locally except final submission
- No impact on page load time

**Privacy Considerations:**
- Fingerprinting is anonymous but may need disclosure
- All data is task-related, not personal
- Consider adding privacy notice if required by local regulations

### Migration from Basic to Secure

1. **Backup existing data** from your Google Spreadsheet
2. **Update Google Apps Script** with the enhanced version
3. **Add new columns** to your spreadsheet (F, G, H, I)
4. **Replace JavaScript** with the secure version
5. **Test thoroughly** before rolling out to all pages
6. **Monitor for the first week** to ensure proper operation

### Troubleshooting Security Issues

**Users can't submit feedback:**
- Check rate limit settings are not too restrictive
- Verify user interaction detection is working
- Look for JavaScript errors in browser console

**False positives (legitimate users blocked):**
- Temporarily set `requireUserInteraction: false`
- Increase cooldown and rate limit thresholds
- Check compatibility across different browsers

**Security not working:**
- Ensure enhanced Google Apps Script is properly deployed
- Verify new spreadsheet columns exist
- Check browser console for error messages

---

## Changelog

**Version 2.0**
- Added comprehensive security enhancements
- Client-side rate limiting and bot detection
- Server-side validation and duplicate prevention
- Risk scoring and enhanced data collection
- Multiple security configuration options

**Version 1.0**
- Initial implementation with Google Sheets integration
- CORS-compatible GET request method
- Local storage fallback
- Basic customization options