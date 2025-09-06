# Blackmail-Check
> Our mission is to eliminate blackmail risk from rogue actors. We propose a secure, trusted platform that removes vulnerable content from your device.

- Scan your files for threats
- Categorise them into risk levels
- Offer bulk-delete or encryption

**Model users:** Civil servants, politicians, celebrities, military personnel

---

## Team

- **Joey Bream 🐟** - AI safety operations
  - *Prev MEng @ Cambridge, Krueger Lab*
- **Dario Cline 🦅** - Mech-interp
  - *Prev CS @ Bath*
- **Anthony Joshua 🐯** - Cyber-security
  - *Prev CS @ Canterbury*

---

## Intro

**Example vulnerabilities:**

- **Personal identifiers:** ID cards, passports, driver's licenses, birth certificates
- **Intimate content:** Nude images, sexual messages, dating app conversations
- **Financial information:** Credit card details, bank statements, tax documents
- **Medical records:** Health diagnoses, prescription information, medical history
- **Credentials:** Passwords, API keys, login tokens
- **Location data:** Home addresses, travel itineraries, frequent locations
- **Illegal content:** Illegal pornography, drug-related conversations, pirated content, extremist materials

1.  **Politician’s Leaked Photos**
    A minister’s personal Gmail and Google Photos contain private vacation pictures and messages with friends. A rogue actor gains access and threatens to release them during election season.
    *With our tool:* A scan conducted 6 months before election season flagged these as medium risk intimate content. The minister bulk-encrypts them, eliminating the attack surface before the threat emerges.

2.  **Civil Servant With Classified Docs at Home**
    A senior civil servant is accidentally storing scanned IDs and sensitive government drafts in Google Drive. If hacked, these could compromise national security.
    *With our tool:* Drive scan identifies “government ID” documents and financial spreadsheets, highlights them as high risk, and guides the user to encrypt/delete, also ensuring compliance with government data handling policies.

3.  **Celebrity Revenge Threat**
    A celebrity’s iCloud/Google Photos contains personal nude images. A former partner attempts extortion.
    *With our tool:* Prior scanning had flagged and moved it to an encrypted vault, so even if the account was accessed, no sensitive material was left to exploit.

4.  **Tech Founder Credential Leak**
    A startup founder has API keys and server credentials stored in plain-text in their Drive and email. Hackers threaten to cripple the business.
    *With our tool:* Credential scanner flags keys and passwords, categorises them as high risk, and provides auto-recommendations for secure storage, potentially saving millions in damages and customer trust.

5.  **Military Officer Location Data**
    A deployed officer keeps flight tickets, hotel bookings, and GPS-tagged images in Gmail and Photos. These reveal patterns of movement that could compromise ongoing operations or personnel safety.
    *With our tool:* Location metadata and itineraries are detected, categorised as medium/high risk, and can be bulk-encrypted or scrubbed of metadata.

---

## Method

**Our Approach: Comprehensive Digital Vulnerability Assessment**

We're building a privacy-first scanning tool that connects to your Google services (Gmail, Photos, and Drive) to identify content that could make you vulnerable to blackmail or security threats.

**How it works:**

1.  **Secure Authentication** - Users log in through Google's OAuth system, ensuring we only access what is necessary while maintaining full data privacy.
2.  **Multi-Platform Scanning:**
    - **Gmail:** Analyse email content for compromising conversations, threats, or sensitive exchanges using NLP.
    - **Google Photos:** Detect intimate or explicit images using multi-modal models.
    - **Google Drive:** Scan documents, spreadsheets, and files for personal identifiers, financial data, credentials, and other sensitive information.
3.  **Risk Assessment** - Each flagged item is categorised by threat level:
    - **High Risk:** Could cause immediate reputational or security damage
    - **Medium Risk:** Potentially compromising in wrong hands
    - **Low Risk:** Minor vulnerabilities worth addressing
4.  **User-Controlled Response** - Present findings through a clean interface where users can:
    - Review flagged content with clear explanations.
    - Choose to delete or encrypt items in bulk.
    - Receive guidance on best practices for digital security.

**Key Principles:**

- No data storage - everything processed locally and securely
- Full user control over actions taken
- Transparent about what's being scanned and why
- Designed specifically for high-profile individuals who face elevated risks

The tool essentially acts as a comprehensive "digital audit" to help users proactively secure their online presence before it can be exploited.

---

## Risk Dashboard

*Example output from running system vulnerability scan*

### 🚨 High risk

- **Gmail:** 3
- **Photos:** 15
- **Drive:** 8

### ⚠️ Medium risk

- **Gmail:** 9
- **Photos:** 32
- **Drive:** 0

### 🔒 Low risk

- **Gmail:** 12
- **Photos:** 3
- **Drive:** 1

---

## Extra resources

- Hackathon image
