import os
import json
import subprocess
import argparse
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from prettytable import PrettyTable

def get_model_name_from_directory():
    return os.path.basename(os.getcwd())

def ensure_reports_directory(model_path):
    reports_folder = os.path.join(model_path, "reports")
    os.makedirs(reports_folder, exist_ok=True)
    return reports_folder

def generate_model_info():
    model_info = {
        "model_name": "Generic AI Model",
        "type": "Transformer-based Language Model",
        "model_version": "1.0",
        "developer_name": "YourOrganization",
        "license_information": "MIT",
        "model_architecture": {
            "ml_model": "Transformer-based autoregressive model",
            "algorithm": "Self-Attention Mechanism (Transformer)"
        },
        "model_parameters": {
            "number_of_layers": "Variable",
            "number_of_attention_heads": "Variable",
            "hidden_layer_size": "Variable",
            "context_length": "Variable"
        },
        "input": {
            "type": "Plain text",
            "encoding": "UTF-8",
            "example": "Once upon a time..."
        },
        "output": {
            "type": "Plain text",
            "encoding": "UTF-8",
            "example": "Once upon a time, there was a kingdom ruled by a wise king..."
        },
        "usage_scenarios": [
            "Text generation",
            "Chatbots and virtual assistants",
            "Code completion",
            "Content summarization"
        ],
        "limitations": [
            "Can generate biased or inaccurate content",
            "No real-world knowledge beyond training data",
            "Prone to generating misleading or nonsensical text"
        ]
    }
    with open("modelinfo.json", "w") as f:
        json.dump(model_info, f, indent=4)
    print(" modelinfo.json generated.")

def generate_dataset_info():
    dataset_info = {
        "dataset_name": "WebText",
        "description": "A dataset of high-quality web pages collected from outbound Reddit links, used for training large-scale language models.",
        "source": "Collected by OpenAI (not publicly released)",
        "format": ["Text"],
        "training_method": "Unsupervised learning with next-word prediction",
        "applicable_models": [
            "Transformer-based Language Models",
            "Chatbots",
            "Summarization Models",
            "Text Classification",
            "Question-Answering Systems"
        ],
        "limitations": [
            "Not suitable for computer vision or audio-based AI models",
            "Biases present in internet content may be reflected in model outputs"
        ],
        "data_samples": [
            {"text": "The future of artificial intelligence is unfolding rapidly with new advancements."},
            {"text": "Climate change policies are crucial to ensuring a sustainable future."},
            {"text": "Deep learning models, such as transformers, have revolutionized natural language processing."},
            {"text": "The history of space exploration is filled with remarkable achievements and discoveries."},
            {"text": "Advancements in quantum computing may reshape industries in the next decade."}
        ]
    }
    with open("dataset.json", "w") as f:
        json.dump(dataset_info, f, indent=4)
    print("dataset.json generated.")

def generate_aibom(model_name, model_version, reports_folder):
    aibom_data = {
        "model_name": model_name,
        "model_version": model_version,
        "dataset": "dataset.json",
        "license": "MIT",
        "developer": "YourOrganization",
        "training_parameters": {"learning_rate": 0.001, "batch_size": 32},
        "hardware_requirements": "GPU (NVIDIA Tesla T4)",
        "software_components": [
            {"name": "TensorFlow", "version": "2.9.1"},
            {"name": "PyTorch", "version": "1.13.0"}
        ],
        "api_specifications": "REST API"
    }
    
    aibom_path = os.path.join(reports_folder, "aibom.json")
    with open(aibom_path, "w") as f:
        json.dump(aibom_data, f, indent=4)
    
    print(f" AIBOM generated: {aibom_path}")
    return aibom_path

def generate_sbom(reports_folder):
    try:
        sbom_path = os.path.join(reports_folder, "sbom.json")
        subprocess.run(["syft", "-o", "json", f"--file={sbom_path}", "."], check=True)
        print(f"SBOM generated: {sbom_path}")
        return sbom_path
    except subprocess.CalledProcessError:
        print("Failed to generate SBOM. Ensure Syft is installed and try again.")
        return None

def scan_vulnerabilities(reports_folder):
    vulnerability_path = os.path.join(reports_folder, "vulnerability_report.json")
    
    try:
        subprocess.run(["trivy", "fs", ".", "--include-dev-deps", "-f", "json", f"--output={vulnerability_path}"], check=True)
        print(f"Vulnerability report generated: {vulnerability_path}")
        
        with open(vulnerability_path, "r") as f:
            data = json.load(f)

        vulnerabilities = []
        for result in data.get("Results", []):
            for vuln in result.get("Vulnerabilities", []):
                vulnerabilities.append([
                    vuln.get("ID", "N/A"),
                    vuln.get("PkgName", "N/A"),
                    vuln.get("InstalledVersion", "N/A"),
                    vuln.get("Severity", "N/A"),
                    vuln.get("FixedVersion", "N/A")
                ])

        if vulnerabilities:
            table = PrettyTable(["Vulnerability ID", "Package", "Installed Version", "Severity", "Fixed Version"])
            table.align = "l"
            for vuln in vulnerabilities:
                table.add_row(vuln)
            print("\nVulnerability Scan Results:\n")
            print(table)
        else:
            print("\n No vulnerabilities found.")
        
        return vulnerability_path
    except subprocess.CalledProcessError:
        print(" Failed to scan for vulnerabilities. Ensure Trivy is installed and try again.")
        return None
    except json.JSONDecodeError:
        print(" Error parsing vulnerability report JSON.")
        return None

def sign_file(file_path, private_key_path):
    if not private_key_path:
        print(" Skipping digital signature (no private key provided).")
        return
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
        file_hash = hashlib.sha256(file_data).digest()
        
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None
            )
        
        signature = private_key.sign(
            file_hash,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        
        signature_path = file_path + ".sig"
        with open(signature_path, "wb") as sig_file:
            sig_file.write(signature)
        print(f" Digital signature created: {signature_path}")
    except Exception as e:
        print(f" Error signing file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate AIBOM, SBOM, scan vulnerabilities, and sign reports.")
    parser.add_argument("--model_name", type=str, help="Specify the model name. Auto-detected if not provided.")
    parser.add_argument("--model_version", type=str, default="1.0", help="Specify the model version.")
    parser.add_argument("--private_key", type=str, help="Path to the private key for signing (optional).", default=None)
    
    args = parser.parse_args()
    
    model_name = args.model_name if args.model_name else get_model_name_from_directory()
    model_version = args.model_version
    private_key_path = args.private_key

    model_path = os.getcwd()
    reports_folder = ensure_reports_directory(model_path)

    #  Auto-generate metadata
    generate_model_info()
    generate_dataset_info()
    
    print(f" Running analysis for {model_name} (Version: {model_version})")
    
    aibom_path = generate_aibom(model_name, model_version, reports_folder)
    sbom_path = generate_sbom(reports_folder)
    vulnerability_path = scan_vulnerabilities(reports_folder)
    
    for file in [aibom_path, sbom_path, vulnerability_path]:
        if file:
            sign_file(file, private_key_path)
    
    print("\n All tasks completed successfully!")

if __name__ == "__main__":
    main()
