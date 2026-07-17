
### 🔄 How It Works

1. **User** enters an email in the search box.
2. **Frontend** sends a POST request to `/check` with the email.
3. **Backend**:
   - First checks the **built‑in database** (BREACH_DATABASE) for known test emails.
   - Then scans the **CSV dataset** (simulates a real breach dump) – this introduces a **8‑12 second delay** to mimic real‑time scanning.
   - If no match, it generates **random realistic breach data** (for demo purposes).
4. **Response** is returned with breach details, risk score, remediation steps, and dark web mentions.
5. **Frontend** renders the results with animations and interactive cards.

> The **8‑12 second delay** is intentional – it gives the impression of a thorough scan across multiple dark web sources.

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository** (or download the ZIP):
   ```bash
   git clone https://github.com/YOUR_USERNAME/darkweb-monitor.git
   cd darkweb-monitor
