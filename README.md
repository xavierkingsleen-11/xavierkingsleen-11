<div align="center">

# Xavier Kingsleen A.

### AWS Cloud Engineer • Cloud Support Engineer • Cloud Operations Engineer • SOC Analyst L1

Building practical experience across **AWS Cloud, Cloud Operations, Cloud Security, SOC, and Networking**.

<a href="https://xavier11sr-myportfolio.netlify.app">
  <img src="https://img.shields.io/badge/Portfolio-Visit%20Website-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio">
</a>
<a href="https://linkedin.com/in/xavierkingsleen01">
  <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>
<a href="https://github.com/xavierkingsleen-11">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>

<br>

<img src="https://komarev.com/ghpvc/?username=xavierkingsleen-11&style=flat-square&color=0A66C2" alt="Profile views">

</div>

---

## 👋 About Me

I'm **Xavier Kingsleen A.**, a BCA graduate focused on building practical skills in **AWS Cloud Engineering, Cloud Operations, Cloud Security, SOC Operations, and Networking**.

My approach is hands-on: I build, configure, troubleshoot, test, investigate, and document cloud and security environments rather than only listing technologies.

I'm currently targeting entry-level opportunities as an **AWS Cloud Engineer, Cloud Support Engineer, Cloud Operations Engineer, or SOC Analyst L1**, with a long-term direction toward **Cloud Security**.

> **Primary focus:** AWS Cloud  
> **Security strength:** SOC Operations • SIEM • Log Analysis • Threat Detection  
> **Supporting foundation:** Networking • Linux • Windows

---

## 🧰 Core Technology Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=aws,linux,windows,powershell,kali,git,github,html,css,vscode&perline=12" alt="Technology icons">

</div>

### ☁️ AWS Cloud & Infrastructure

`AWS` `IAM` `EC2` `S3` `VPC` `Security Groups` `Application Load Balancer` `Auto Scaling` `RDS` `Aurora` `CloudWatch` `Lambda` `EventBridge` `Systems Manager` `Route 53` `ACM`

### 🔐 Cloud Security

`AWS GuardDuty` `AWS CloudTrail` `IAM Access Control` `AWS KMS` `Least Privilege` `Threat Detection`

### 🛡️ SOC & Cybersecurity

`SOC Operations` `Security Monitoring` `Log Analysis` `SIEM` `Windows Event Logs` `MITRE ATT&CK` `Alert Investigation` `Insider Threat Detection` `Incident Response Fundamentals`

### 🔎 Security & Investigation Tools

`Splunk Cloud` `Wazuh` `Sysmon` `Windows Event Viewer` `PowerShell` `VirusTotal` `Thunderbird`

### 🌐 Networking & Systems

`TCP/IP` `IPv4/IPv6` `DNS` `DHCP` `ARP` `NAT` `VLAN` `Subnetting` `Routing` `Linux CLI` `Windows`

### 💻 Development & Supporting Technologies

`HTML` `CSS` `JavaScript` `React` `Node.js` `Express.js` `MongoDB` `Git` `GitHub`

---

# 🚀 Hands-on Projects

The projects below demonstrate practical work across **AWS infrastructure, serverless architecture, cloud operations, SIEM, incident response, insider-threat detection, secure access control, and phishing investigation**.

---

## 01 • Serverless Image Processing & Metadata System

A serverless AWS workflow for image ingestion, processing, and metadata handling.

**Built with:** `S3` `Lambda` `IAM` `DynamoDB` `CloudWatch` `Python` `Pillow`

**Highlights**
- Designed an event-driven image processing workflow.
- Used S3 for source image ingestion and processed output.
- Used Lambda for serverless image processing.
- Stored image metadata in DynamoDB.
- Applied IAM permissions for controlled access.
- Used CloudWatch for monitoring and troubleshooting.
- Resolved a DynamoDB key mismatch during testing by aligning the application field with the table partition key.

---

## 02 • Highly Available Website with Auto Scaling

A highly available web architecture designed across multiple Availability Zones.

**Built with:** `EC2` `VPC` `Security Groups` `ALB` `Auto Scaling` `CloudWatch`

**Highlights**
- Designed EC2 infrastructure across multiple Availability Zones.
- Configured VPC networking and Security Groups.
- Used an Application Load Balancer for traffic distribution.
- Configured Auto Scaling for capacity management.
- Used CloudWatch for application health monitoring.

---

## 03 • Security Monitoring & Log Analysis Lab

A SIEM-focused security monitoring project using Windows telemetry and Splunk Cloud.

**Built with:** `Splunk Cloud` `SPL` `Windows Event Logs` `PowerShell` `MITRE ATT&CK`

**Highlights**
- Centralized Windows Security telemetry including **4624, 4625 and 4688** events.
- Built SPL detections for authentication, process, and PowerShell activity.
- Investigated encoded PowerShell and sensitive file-access alerts.
- Correlated findings into SOC-style assessments.
- Built security dashboards and Splunk email alerting.

---

## 04 • Cloud Monitoring & Automated Incident Response

An automated AWS remediation pipeline for detecting and recovering an HTTPD service failure.

### Architecture

`EC2 → CloudWatch → EventBridge → Lambda → Systems Manager → HTTPD Recovery`

**Built with:** `EC2` `CloudWatch` `EventBridge` `Lambda` `Systems Manager`

**Highlights**
- Monitored the HTTPD process on an EC2 Linux instance.
- Triggered CloudWatch alarms when the service entered an abnormal state.
- Routed the state change through EventBridge.
- Used Lambda to invoke Systems Manager Run Command.
- Restarted HTTPD automatically.
- Verified the complete end-to-end recovery workflow.

---

## 05 • AWS Three-Tier Architecture

A production-style architecture separating web, application, and database layers.

### Architecture

`Users → Route 53 → ACM/TLS → ALB → Web Tier → ALB → App Tier → RDS MySQL`

**Built with:** `VPC` `Route 53` `ACM` `ALB` `Auto Scaling` `RDS MySQL`

**Highlights**
- Designed separate web, application, and database tiers.
- Used a multi-AZ VPC.
- Configured Route 53 and ACM for DNS and TLS.
- Used frontend and backend Application Load Balancers.
- Configured Auto Scaling Groups.
- Isolated RDS MySQL in private subnets.

---

## 06 • AWS WordPress CMS Deployment

A WordPress CMS deployment using EC2, RDS MySQL, IAM, and S3.

**Built with:** `EC2` `RDS MySQL` `S3` `IAM` `WordPress` `Amazon Linux 2023`

**Highlights**
- Deployed WordPress on Amazon EC2 using Amazon Linux 2023.
- Used Amazon RDS MySQL for application data.
- Attached an IAM role to EC2 for S3 permissions.
- Integrated WP Offload Media for S3-based media storage.
- Verified the WordPress → S3 media workflow.

---

## 07 • Insider Threat Detection Project

A Splunk Cloud security monitoring project focused on detecting suspicious insider activity.

**Built with:** `Splunk Cloud` `Sysmon` `PowerShell` `Risk Scoring`

**Highlights**
- Built a **seven-detection insider-threat framework**.
- Covered USB usage, logins, PowerShell, sensitive file access, compression, and outbound connections.
- Designed a risk-scoring engine combining detection severity and weights.
- Normalized risk into **LOW → CRITICAL** thresholds.
- Built an **INSIDER-THREAT-2** dashboard with risk score, severity breakdown, and recent alerts.

---

## 08 • AWS Secure File-Sharing & Access Control

A serverless file-access control system focused on authorization, encryption, auditing, and alerting.

**Built with:** `API Gateway` `Lambda` `DynamoDB` `S3` `KMS` `CloudTrail` `EventBridge` `SNS`

**Highlights**
- Built prefix-based authorization using API Gateway, Lambda, and DynamoDB.
- Applied least-privilege IAM permissions.
- Encrypted application files and audit logs with customer-managed KMS keys.
- Configured CloudTrail for API auditing.
- Used EventBridge and SNS for security alerting.
- Tested both authorized and unauthorized access paths.

---

## 09 • Phishing Email Investigation

A SOC-style phishing investigation workflow using email header analysis, IOC validation, and SIEM correlation.

**Built with:** `Thunderbird` `SPF/DKIM/DMARC` `VirusTotal` `Splunk Cloud` `SPL`

**Highlights**
- Investigated a simulated phishing email.
- Analyzed email headers for SPF, DKIM, and DMARC failures.
- Investigated From/Reply-To mismatches.
- Extracted and validated IOCs including domains, URLs, and IP addresses.
- Used VirusTotal for reputation checks.
- Ingested email telemetry into Splunk Cloud.
- Built SPL correlation searches.
- Documented the investigation as a SOC response workflow.

---

# 🎓 Academic Project

## Digital Hostel Issue, Leave & Management System

A **MERN-stack full-stack application** designed to digitize hostel operations through separate Student and Admin portals.

### Key Features

- JWT-based authentication
- Role-based access control
- Student registration with admin approval
- Complaint management with image evidence
- Leave request and approval workflow
- Gate-pass management
- GPS-based movement/attendance validation
- Hostel fee management with Razorpay
- Room allocation
- Hostel announcements
- Mess menu
- Emergency contact information
- Real-time notifications

**Stack:** `React` `Vite` `Node.js` `Express.js` `MongoDB` `Mongoose` `Tailwind CSS` `JWT` `Razorpay`

---

# 🏆 Certifications & Professional Development

> Certificate links below are **repository-relative links**. Upload the corresponding original PDF files into a `certificates/` folder in the profile repository using the filenames shown below. No fake external certificate URLs are used.

| Certification / Program | Issuer | Certificate |
|---|---|---|
| Python for Data Science | NPTEL / IIT Madras | [View Certificate](./certificates/Python-for-Data-Science-NPTEL.pdf) |
| AWS Solutions Architecture Job Simulation | Forage | [View Certificate](./certificates/AWS-Solutions-Architecture-Forage.pdf) |
| Data Science Job Simulation | Forage | [View Certificate](./certificates/Data-Science-Forage.pdf) |
| Entrepreneurship & Innovation: Web Development Job Simulation | Forage | [View Certificate](./certificates/Web-Development-Forage.pdf) |
| 30 Days MasterClass in Full Stack Development | NoviTech R&D Private Limited | [View Certificate](./certificates/Full-Stack-Development-NoviTech.pdf) |
| Introduction to HTML | SoloLearn | [View Certificate](./certificates/Introduction-to-HTML-SoloLearn.pdf) |
| Building SAP e-Commerce Website — INFO TECHIES 2K25 Workshop | Sadakathullah Appa College | [View Certificate](./certificates/SAP-eCommerce-Workshop-Sadakathullah-Appa-College.pdf) |

---

# 🎓 Education

### Bachelor of Computer Applications — BCA
**Sadakathullah Appa College, Tirunelveli**  
`2023 – 2026`

### Higher Secondary Education — 12th
**TNDTA RMP Pulamadan Chettiar National Higher Secondary School, Sathankulam**  
`2022 – 2023`

> GPA/CGPA is intentionally not displayed because no verified GPA figure is being used in this profile.

---

# 📊 GitHub Activity

<div align="center">

[![Xavier's GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=xavierkingsleen-11&theme=github-compact)](https://github.com/xavierkingsleen-11)

</div>

---

# 📈 GitHub Analytics

<div align="center">

<img height="170" src="https://github-readme-stats.vercel.app/api?username=xavierkingsleen-11&show_icons=true&hide_border=true&include_all_commits=true&count_private=true&rank_icon=github" alt="GitHub Stats">

<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=xavierkingsleen-11&layout=compact&hide_border=true&langs_count=8" alt="Top Languages">

</div>

---

# 🏅 GitHub Achievements

<div align="center">

<img src="https://github-profile-trophy.vercel.app/?username=xavierkingsleen-11&theme=flat&no-frame=true&no-bg=true&margin-w=8&row=1" alt="GitHub Profile Trophies">

</div>

---

# 🔥 Contribution Streak

<div align="center">

<img src="https://streak-stats.demolab.com?user=xavierkingsleen-11&hide_border=true" alt="GitHub Contribution Streak">

</div>

---

# 🎯 Career Direction

```text
Networking
     ↓
Linux & Windows
     ↓
Cybersecurity Fundamentals
     ↓
SOC Operations & SIEM
     ↓
AWS Cloud Engineering
     ↓
Cloud Security
```

### Target Roles

`AWS Cloud Engineer` • `Cloud Support Engineer` • `Cloud Operations Engineer` • `SOC Analyst L1`

My long-term direction is to combine **AWS cloud infrastructure + security operations** and grow toward **Cloud Security**.

---

# 🧪 Current Learning & Practice

- AWS infrastructure and architecture
- IAM and least-privilege access
- EC2, VPC, S3 and cloud networking
- CloudWatch monitoring
- AWS security services
- Linux administration and CLI
- Windows Event Logs
- PowerShell for SOC investigation
- Splunk and SIEM investigation
- Wazuh
- Sysmon
- MITRE ATT&CK
- Incident response fundamentals
- Threat detection and log analysis
- Networking fundamentals and troubleshooting

---

# 📫 Connect With Me

<div align="center">

<a href="https://xavier11sr-myportfolio.netlify.app">
  <img src="https://img.shields.io/badge/🌐%20Portfolio-Visit-0A66C2?style=for-the-badge" alt="Portfolio">
</a>

<a href="https://linkedin.com/in/xavierkingsleen01">
  <img src="https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>

<a href="https://github.com/xavierkingsleen-11">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>

<a href="mailto:xavierkingsleen@gmail.com">
  <img src="https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
</a>

</div>

---

<div align="center">

### Building. Troubleshooting. Investigating. Documenting.

**Open to entry-level AWS Cloud, Cloud Operations, Cloud Support and SOC opportunities.**

</div>
