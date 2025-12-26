# keyword-media-monitor-huen
A lightweight keyword-based web content monitoring tool that periodically collects articles and posts from specified websites for manual review and future NLP analysis.

What we want to build is a very focused internal tool:
it periodically crawls a predefined list of websites (including our own site), collects newly published articles or posts, checks them against a small set of keywords — especially our company name — and stores the matched content for manual review.
The system should update in a certain time(we could design), keep data for one month, and stay as simple and compliant as possible.
There is no need to judge relevance or sentiment automatically. I will review the content manually, and if needed, build a separate NLP program later based on the collected raw data.

# Keyword Media Monitor
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Language](https://img.shields.io/badge/language-Python-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**Internal · Level 1 · Non-Commercial**

---

## Table of Contents

1. [Project Overview](#1-project-overview)  
2. [Project Goals](#2-project-goals)  
3. [Scope & Boundaries](#3-scope--boundaries)  
4. [Target Languages](#4-target-languages)  
5. [Core Functional Requirements](#5-core-functional-requirements)  
   - [Source Configuration](#51-source-configuration)  
   - [Content Collection](#52-content-collection)  
   - [Keyword Matching & Filtering](#53-keyword-matching--filtering)  
   - [Update Frequency & Automation](#54-update-frequency--automation)  
   - [Data Storage & Retention](#55-data-storage--retention)  
   - [Review Interface](#56-review-interface)  
   - [Notification](#57-notification-optional)  
6. [Explicit Exclusions](#6-explicit-exclusions)  
7. [Future Use of Collected Data](#7-future-use-of-collected-data)  
8. [Technical Implementation Guidance](#8-technical-implementation-guidance-simplified)  
9. [Risk & Limitation Statement](#9-risk--limitation-statement)  
10. [Compliance & Ethics](#10-compliance--ethics)  
11. [Ownership & Usage](#11-ownership--usage)  
12. [Acknowledgement](#12-acknowledgement)  
13. [Final Note](#13-final-note)
14. [Suggested Configuration (Example `config.yaml`)](#14-suggested-configuration-example-configyaml)  

---

## 1. Project Overview

This project is an **internal, site-restricted public opinion collection tool** designed to support basic monitoring of overseas (most for hungary and eu area) content related to the company.

The system periodically collects articles or posts **only from user-specified websites**, matches them against predefined keywords (especially the company name), stores the matched content, and presents it for **manual relevance assessment**.

This tool focuses on **content collection and filtering**, potential analysis function needs to be added.

---

## 2. Project Goals

### 2.1 Primary Goals
- Collect public articles/posts from **media websites **
- Identify content mentioning the company or defined keywords
- Provide a continuously updated collection for **manual review**
- Preserve raw content for **future offline cleaning and NLP analysis**

### 2.2 Non-Goals
- Open web discovery
- Automated relevance judgement
- Direct Sentiment analysis or NLP within this system
- Commercial-grade monitoring or completeness guarantees

---

## 3. Scope & Boundaries

### 3.1 In Scope
- Google search and user-added websites (including the company’s own site)
- Publicly accessible pages only
- Articles or posts published on those sites

### 3.2 Out of Scope
- Login-protected or private content
- Circumventing paywalls, CAPTCHAs, or access controls
- Social media private content
- Automated analysis or scoring

---

## 4. Target Languages

- English (mandatory)
- Hungarian (mandatory)

**Language handling**
- Keyword-based matching only
- Case-insensitive

---

## 5. Core Functional Requirements

### 5.1 Source Configuration
- Crawl **only** websites explicitly provided by the user
- List of target websites must be configurable
- No automatic discovery of new domains

### 5.2 Content Collection
- Crawl articles or posts published on the specified websites
- Extract and store:
  - Title
  - URL
  - Publish time (if available)
  - Full text content (raw or near-raw)

### 5.3 Keyword Matching & Filtering
- Match collected content against a configurable keyword list
- Keywords include:
  - Company name (mandatory, highest priority)
  - Project or site names
  - Other user-defined keywords
- Matching rules:
  - Case-insensitive
  - Rule-based only
- Retain content that matches at least one prior keyword
- Record matched keyword(s)
- Manual relevance assessment

### 5.4 Update Frequency & Automation
- Automatic update every **1 hour**
- Each run is independent
- Missed or failed runs do not require backfilling

### 5.5 Data Storage & Retention
- Store matched content in CSV / JSON / SQLite
- Each record: title, source, URL, publish date, matched keywords, full text, collection timestamp
- Automatic cleanup every month (retain data ≤ 30 days)

### 5.6 Review Interface
- Simple list or table view
- Allow viewing matched keywords, opening links, and manual relevance assessment
- Minimal UI, simplicity preferred

### 5.7 Notification (Optional)
- Optional notification when new matched content is collected
- Batching allowed
- No alert SLA required

---

## 6. Explicit Exclusions
- Automated relevance judgement
- Sentiment analysis
- NLP within this system
- Trend/volume analytics
- Dashboards or visualization
- Cross-site discovery
- User roles or permission systems

---

## 7. Future Use of Collected Data
- Input for data cleaning scripts
- Offline NLP or analysis programs
- Out of scope for current system

---

## 8. Technical Implementation Guidance (Simplified)
- Linear workflow: load → crawl → extract → match → store
- Cron or scheduler every 1 hour
- Simple string or regex keyword matching
- Configuration over code
- Partial failures acceptable
- Simplicity and compliance prioritized

---

## 9. Risk & Limitation Statement
- Best-effort basis
- No guarantee of full coverage
- Depends on site structure & availability
- Manual review required

---

## 10. Compliance & Ethics
- Public data only
- No personal data profiling
- Respect site protections & robots.txt

---

## 11. Ownership & Usage
- Internal use only
- Non-commercial
- No service-level guarantees

---

## 12. Acknowledgement
- Contributors acknowledge scope, limitations, manual review requirement, and lightweight internal solution

---

## 13. Final Note
> The objective is a **reliable, simple collection tool** that supports human judgement, not an automated analysis system.

---

## 14. Suggested Configuration (Example `config.yaml`)
```yaml
targets:
  - name: "Company News"
    base_url: "https://company-website.com/news"
    type: "news"
  - name: "Industry Forum"
    base_url: "https://industry-forum.com"
    type: "forum"

keywords:
  primary:
    - "CompanyName"
    - "Company Name Ltd"
  secondary:
    - "battery factory"
    - "EV investment"

languages:
  - "en"
  - "hu"

schedule:
  interval_minutes: 30

storage:
  type: "local"
  path: "./data"
  format: "json"

retention:
  cleanup_cycle_days: 30

alerts:
  enabled: true
  method: "email"
