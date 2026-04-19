🔷 Project Title

This is a complete End-to-End DevSecOps Pipeline that integrates SAST, DAST and container scanning using Dockerized tools of with Jenkins, Docker, SonarQube, Trivy & ZAP.
Security is enforced at multiple stages before deployment.
Pipeline fails automatically if vulnerabilities are found.

🔷 What this project does

This project demonstrates a complete DevSecOps pipeline:

Static Code Analysis using SonarQube
Container Vulnerability Scanning using Trivy
Dynamic Application Security Testing using OWASP ZAP
Automated CI/CD using Jenkins

🔷 Architecture Flow

GitHub → Jenkins → Docker Build → SonarQube → Trivy → Deploy → ZAP Scan

🔷 Tools Used

Tool	Purpose
Jenkins	CI/CD Automation
Docker	Containerization
SonarQube	Code Quality & SAST
Trivy	Image Vulnerability Scan
ZAP	DAST

🔷 How to Run

Start SonarQube container
Start Jenkins container
Configure credentials
Run pipeline

🔷 Key Features

Fails build on HIGH/CRITICAL vulnerabilities
Automated security testing
Container-based execution
Fully reproducible setup

I modularized the pipeline into reusable scripts to improve maintainability and portability.

Each security tool can be executed independently or via CI/CD.