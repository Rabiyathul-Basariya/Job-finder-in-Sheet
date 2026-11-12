/**
 * Google Apps Script for Automated Job Tracker & 24/7 Webhook Sync
 * Target Roles: Associate Product Manager, Product Manager, Business Analyst
 * Candidate: Rabiyathul Basariya B
 * 
 * Instructions to install in Google Sheets:
 * 1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1XgQzSxVp8cXJDbwrrSXTDWOj5xqoHXvLv5xZZQ1Hkmk/edit
 * 2. Click on "Extensions" -> "Apps Script" in the top menu.
 * 3. Replace all existing code with this file.
 * 4. Click Save (Ctrl + S) and Deploy -> Manage Deployments -> Edit -> New Version -> Deploy.
 * 5. Refresh your Google Sheet.
 */

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('🚀 Job Hunter Hub')
    .addItem('1. Format Sheet & Setup Columns', 'setupHeadersAndFormatting')
    .addItem('2. Create Ready-to-Send Gmail Drafts', 'createGmailDrafts')
    .addItem('3. Send Outreach Emails Directly (Live Send)', 'sendLiveEmails')
    .addToUi();
}

/**
 * Handles incoming 24/7 webhooks from autonomous_agent_24x7.py
 */
function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getActiveSheet();
    
    // Check if sheet needs initialization
    if (sheet.getLastRow() === 0) {
      setupHeadersAndFormatting();
    }
    
    var data = JSON.parse(e.postData.contents);
    var todayStr = Utilities.formatDate(new Date(), "GMT+5:30", "yyyy-MM-dd");
    var followupDate = Utilities.formatDate(new Date(new Date().getTime() + 4 * 24 * 60 * 60 * 1000), "GMT+5:30", "yyyy-MM-dd");
    
    sheet.appendRow([
      data.company || "Unknown",
      data.role || "Product Role",
      data.location || "Bengaluru / Remote",
      data.funding || "Growth Stage",
      data.contact_person || "Hiring Team",
      data.email || "careers@" + (data.company || "company").toLowerCase().replace(/\s+/g, '') + ".com",
      data.subject || "Product Role Application",
      data.pitch || "",
      data.followup || "",
      data.ats_match || "Matched",
      "Ready to Send",
      todayStr,
      followupDate,
      data.notes || "Live 24/7 Crawl"
    ]);

    // Apply text wrapping to the newly added row
    var lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1, 1, 14).setWrap(true);

    return ContentService.createTextOutput(JSON.stringify({ status: "success", row: lastRow }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("🚀 Job Hunter 24/7 Live Webhook is active and listening.")
    .setMimeType(ContentService.MimeType.TEXT);
}

function setupHeadersAndFormatting() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.setName("Active Applications");

  var headers = [
    "Company Name",
    "Role Title",
    "Location",
    "Funding Stage / Sector",
    "Target Contact Person",
    "Contact Email / Profile",
    "Outreach Subject",
    "Tailored Cold Pitch (Ready to Send)",
    "Follow-up Template (Day +4)",
    "ATS Match & Keywords",
    "Status",
    "Date Contacted",
    "Follow-up Date",
    "Target Angle / Notes"
  ];

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
  } else {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }

  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground("#1a73e8")
             .setFontColor("#ffffff")
             .setFontWeight("bold")
             .setFontFamily("Roboto")
             .setHorizontalAlignment("center")
             .setWrap(true);

  sheet.setFrozenRows(1);

  sheet.setColumnWidth(1, 150); // Company
  sheet.setColumnWidth(2, 230); // Role
  sheet.setColumnWidth(3, 140); // Location
  sheet.setColumnWidth(4, 180); // Stage
  sheet.setColumnWidth(5, 200); // Contact Person
  sheet.setColumnWidth(6, 220); // Email
  sheet.setColumnWidth(7, 280); // Subject
  sheet.setColumnWidth(8, 400); // Pitch
  sheet.setColumnWidth(9, 350); // Follow-up
  sheet.setColumnWidth(10, 240); // ATS
  sheet.setColumnWidth(11, 140); // Status
  sheet.setColumnWidth(12, 120); // Date Contacted
  sheet.setColumnWidth(13, 130); // Follow-up Date
  sheet.setColumnWidth(14, 300); // Notes

  // Dropdown validation for Status
  var statusRange = sheet.getRange(2, 11, sheet.getMaxRows() - 1, 1);
  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["Ready to Send", "Draft Created", "Email Sent", "Follow-up Sent", "Interview Scheduled", "Offer Received"], true)
    .setAllowInvalid(false)
    .build();
  statusRange.setDataValidation(rule);

  SpreadsheetApp.getUi().alert("✅ Sheet headers, column widths, and status validation successfully configured!");
}

function createGmailDrafts() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var count = 0;

  for (var i = 1; i < data.length; i++) {
    var email = data[i][5];
    var subject = data[i][6];
    var body = data[i][7];
    var status = data[i][10];

    if (status === "Ready to Send" && email && email.indexOf("@") !== -1) {
      GmailApp.createDraft(email, subject, body);
      sheet.getRange(i + 1, 11).setValue("Draft Created");
      count++;
    }
  }

  SpreadsheetApp.getUi().alert("📧 Created " + count + " ready-to-review drafts in your Gmail inbox!");
}

function sendLiveEmails() {
  var ui = SpreadsheetApp.getUi();
  var confirm = ui.alert("Confirm Live Email Send", "Are you sure you want to send all 'Ready to Send' emails directly to recruiters/founders?", ui.ButtonSet.YES_NO);
  if (confirm !== ui.Button.YES) {
    return;
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var count = 0;

  for (var i = 1; i < data.length; i++) {
    var email = data[i][5];
    var subject = data[i][6];
    var body = data[i][7];
    var status = data[i][10];

    if (status === "Ready to Send" && email && email.indexOf("@") !== -1) {
      GmailApp.sendEmail(email, subject, body);
      sheet.getRange(i + 1, 11).setValue("Email Sent");
      count++;
    }
  }

  ui.alert("🚀 Successfully sent " + count + " outreach emails from your Gmail account!");
}
