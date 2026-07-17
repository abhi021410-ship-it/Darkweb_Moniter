# 🔍 DarkWeb Breach Monitor

**Enterprise-grade dark web breach detection system** – a hackathon project that simulates real-time scanning of breached credentials using a combination of preloaded breach datasets and mock dark web intelligence feeds.

---

## 📌 Project Overview

DarkWeb Breach Monitor is a Flask‑based web application that allows users to check if their email address appears in known data breaches. It mimics the behaviour of real breach‑checking services (like HaveIBeenPwned) by:

- Cross‑referencing emails with a built‑in breach database (preset breach records)
- Scanning a mock CSV dataset (simulating a real leaked dataset)
- Displaying **live threat feeds**, **dark web marketplaces**, and **historical breach news**
- Providing a professional, interactive dashboard with statistics and charts

> **Note:** This is a **proof‑of‑concept** built for a hackathon. In production, it would integrate with real APIs (e.g., HaveIBeenPwned) and actual dark web crawling infrastructure.

---

## ✨ Features

- ✅ **Email Breach Check** – Enter any email and get breach details (realistic demo)
- 🗂️ **Mock Breach Dataset** – Includes a sample CSV file (1200+ records) to simulate real data
- 📊 **Interactive Dashboard** – Stats, live threat feed, active dark web markets
- 📜 **Breach History** – Timeline of major data breaches (Yahoo, Facebook, LinkedIn, etc.)
- 🔄 **Real‑time Updates** – Threat feed refreshes automatically every 30 seconds
- 📱 **Responsive UI** – Works on desktop and mobile

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python, Flask, Flask‑SocketIO |
| **Frontend** | HTML5, CSS3, JavaScript (Chart.js, Socket.IO client) |
| **Data** | CSV (sample breach dataset), JSON (breach news) |
| **Deployment** | GitHub, Render / PythonAnywhere (free tier) |

---

## 📁 Project Architecture
