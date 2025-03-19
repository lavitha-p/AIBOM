
# Automated AI Bill of Materials (AIBOM) Generator

# Overview
This script automates the generation of an **AI Bill of Materials (AIBOM)**, a **Software Bill of Materials (SBOM)**, and a **Vulnerability Report** for an AI model. It helps ensure compliance, security, and transparency in AI model deployments by providing detailed component tracking and vulnerability scanning.

# Pre-requisites
Ensure the following dependencies are installed before using the script:
 **Python 3.7+**
 **Syft** (for generating SBOM)
 **Trivy** (for scanning vulnerabilities)
 **Cryptography** (for digital signing)
 **PrettyTable** (for formatted vulnerability output)

# Install required Python packages:
sh
pip install cryptography prettytable


# Install Syft and Trivy:
sh
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sudo sh -s -- -b /usr/local/bin
sudo apt install -y trivy  # Or follow official installation instructions


# Installation
Clone this repository and navigate into the directory:
sh
git clone https://github.com/your-repo/aibom-generator.git
cd aibom-generator


# Usage
Run the script inside the directory containing your AI model code:
sh
python generate_aibom.py --model_name "YourModel" --model_version "1.0"


Commands to Execute in PowerShell or Command Prompt
Run the following commands step by step:

1. Clone the repository:
powershell
git clone https://github.com/your-repo/aibom-generator.git
cd aibom-generator


2. Install Python dependencies:
powershell


3. Install Syft (Windows users may need WSL or alternative installation methods):
powershell
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b .


4. Install Trivy:
powershell
scoop install trivy  # If using Scoop (Windows)


5. Run the script:
powershell
python generate_aibom.py --model_name "YourModel" --model_version "1.0"


# Output Files
After execution, the script generates the following files in a `reports/` directory:
1. **`aibom.json`** - Contains AI model metadata, dataset details, dependencies, license, and training parameters.
2. **`sbom.json`** - Lists all software dependencies using **Syft**.
3. **`vulnerability_report.json`** - Contains vulnerabilities detected in dependencies using **Trivy**.
4. **Digital Signatures (`.sig` files, optional)** - If a private key is provided, signed versions of each report are generated.

# Example Output

 Running analysis for YourModel (Version: 1.0)
 AIBOM generated: reports/aibom.json
 SBOM generated: reports/sbom.json
 Vulnerability report generated: reports/vulnerability_report.json
 Digital signature created: reports/aibom.json.sig
 Digital signature created: reports/sbom.json.sig
 Digital signature created: reports/vulnerability_report.json.sig
 All tasks completed successfully!


# Notes
Ensure **Syft** and **Trivy** are installed before running the script.
The script assumes the AI model code directory contains **dataset.json** and necessary dependencies.
Use the **`--private_key`** option if digital signing of reports is required.

# License
This project is licensed under the **MIT License**.

# Limitations
 **Requires internet access** to fetch vulnerability databases.
 **Syft & Trivy compatibility** depends on system configurations.
 **No automatic dependency installation**—users must install required tools manually.
