---
name: puppeteer-stealth
description: Bypass bot detection on protected websites using puppeteer-extra with stealth plugin
author: opencode
version: 1.0.0
tags: [puppeteer, web-scraping, bot-detection, stealth, automation]
---

# Puppeteer Stealth - Bypass Bot Detection

Use this skill when you need to scrape or automate websites that block automated browsers.

## When to Use

Use this skill when:
- Website shows "We are sorry, but [site] was not able to complete your request"
- Getting `net::ERR_HTTP2_PROTOCOL_ERROR` or `403 Forbidden`
- Website detects and blocks headless Chrome/Puppeteer/Selenium
- Standard browser automation tools fail with blocking messages

## The Working Solution

### Installation

```bash
npm install puppeteer-extra puppeteer-extra-plugin-stealth
```

### Basic Usage

```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage'
    ]
  });
  
  const page = await browser.newPage();
  
  await page.goto('https://target-website.com', { 
    waitUntil: 'domcontentloaded',
    timeout: 60000 
  });
  
  // Wait for content to load
  await new Promise(r => setTimeout(r, 15000));
  
  const content = await page.content();
  // ... do something with content
  
  await browser.close();
})();
```

### Advanced: Custom Stealth Options

```javascript
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const stealth = StealthPlugin();

// Disable specific evasions if needed
stealth.enabledEvasions.delete('chrome.app');
stealth.enabledEvasions.delete('chrome.csi');

puppeteer.use(stealth);
```

## Methods That DON'T Work

### 1. Standard Browserless Docker
```bash
# Using browserless/chrome container
docker run -p 3000:3000 browserless/chrome:latest
curl -X POST http://localhost:3000/chrome/screenshot?token=xxx -d '{"url":"https://site.com"}'
# Result: 404 or ERR_HTTP2_PROTOCOL_ERROR
```

### 2. CDP User-Agent Override Only
```javascript
const client = await page.target().createCDPSession();
await client.send('Network.setUserAgentOverride', { 
  userAgent: 'Mozilla/5.0...' 
});
// Result: Site still detects automation
```

### 3. Basic Chrome Flags
```javascript
args: [
  '--disable-blink-features=AutomationControlled',
  '--headless=new'
]
// Result: Many sites detect this
```

### 4. Mobile User-Agent
```javascript
userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0...)'
// Result: Sites show mobile blocking page
```

### 5. Incognito Context
```javascript
const context = await browser.createIncognitoBrowserContext();
// Result: Doesn't help with detection
```

## Why Sites Block Standard Automation

1. **navigator.webdriver** - Chrome exposes `window.navigator.webdriver === true`
2. **Missing Chrome runtime** - Headless Chrome lacks Chrome-specific properties
3. **HTTP/2 Protocol Issues** - Improper TLS/ALPN negotiation
4. **TLS Fingerprinting** - Client sends different TLS parameters than real browser
5. **Behavioral Analysis** - No mouse movements, instant page loads
6. **IP Reputation** - Data center IPs get flagged
7. **Canvas/WebGL Fingerprinting** - Different rendering signatures

The stealth plugin patches ~30+ detection points automatically.

## Websites Tested

| Website | Status | Notes |
|---------|--------|-------|
| united.com | ✅ Works | Requires stealth plugin |
| google.com | ✅ Works | Works without stealth |
| delta.com | ✅ Works | Works without stealth |
| southwest.com | ✅ Works | Works without stealth |
| americanairlines.com | ✅ Works | Works without stealth |
| amazon.com | ⚠️ Partial | May need additional tricks |
| ticketmaster.com | ⚠️ Partial | May need proxy |

## Docker Alternative (if local puppeteer not available)

```dockerfile
FROM node:18-alpine

RUN apk add --no-cache chromium chromium-chromedriver ca-certificates

RUN npm install -g puppeteer-extra puppeteer-extra-plugin-stealth

WORKDIR /app
COPY . .

CMD ["node", "your-script.js"]
```

## Troubleshooting

### Still Getting Blocked?

1. **Add more delays:**
```javascript
await page.waitForSelector('body'); // Wait for DOM
await new Promise(r => setTimeout(r, 5000)); // Extra wait
```

2. **Try different viewport:**
```javascript
await page.setViewport({ width: 1920, height: 1080 });
```

3. **Enable logging:**
```javascript
const browser = await puppeteer.launch({
  headless: true,
  dumpio: true, // Shows browser console
  // ...
});
```

4. **Check what's being detected:**
```javascript
await page.evaluate(() => {
  console.log('webdriver:', navigator.webdriver);
  console.log('plugins:', navigator.plugins);
  console.log('languages:', navigator.languages);
});
```

### Performance Tips

- Use `headless: true` (faster than headed mode)
- Reuse browser instance across requests
- Set appropriate timeouts
- Consider using proxy for IP rotation

## Complete Example: Flight Price Checker

See `flight-checker.js` in this project for a working example that:
1. Launches stealth browser
2. Navigates to United Airlines
3. Extracts flight prices
4. Compares with previous prices
5. Sends email notification on price drop
