# Network Security:  ECC Implementation

## Overview
This repository contains one assignments:
1. **ECC Implementation** – Elliptic Curve Cryptography with ECDH, AES, and digital signatures

---

## Author Information

| No. | Name | UGR ID |
|-----|------|--------|
| 1 | Rabuma Milisha | UGR/7371/14 |
| 2 | Robsan Chimdi | UGR/4515/15 |
| 3 | Robera Shimelis | UGR/1994/12 |
| 4 | Merera Edosa | UGR/9521/15 |

| | |
|---|---|
| **Submitted to** | Mr. Samuel Getachew |
| **Course** | Computer Security |
| **Date** | April 20, 2026 |

---

## Files

| File | Description |
|------|-------------|
| `TCP_Hijacking.docx` | Complete attack analysis report |
| `ecc.py` | Core ECC functions (keygen, ECDH, AES-GCM) |
| `demo.py` | Basic ECDH + encryption demo |
| `secure_ecc.py` | Authenticated ECC with ECDSA signatures |
| `attack_demo.py` | Man-in-the-Middle attack simulation |
| `performance_test.py` | Speed benchmarks |
| `run_all.py` | Run all demos sequentially |

---

## Quick Start

### Install dependencies
pip install cryptography

### Run all demos
python run_all.py

### Run individual scripts
python demo.py            
python secure_ecc.py      
python attack_demo.py      
python performance_test.py

---

## ECC Features

| Feature | Algorithm |
|---------|-----------|
| Key Exchange | ECDH (SECP256R1) |
| Digital Signatures | ECDSA + SHA-256 |
| Encryption | AES-256-GCM |
| Key Derivation | HKDF-SHA256 |

### ECC vs RSA Key Size Comparison

| Security Level | RSA Key Size | ECC Key Size |
|----------------|--------------|--------------|
| 128 bits | 3072 bits | 256 bits |
| 192 bits | 7680 bits | 384 bits |
| 256 bits | 15360 bits | 512 bits |

---

## Requirements

- Python 3.8+
- cryptography >= 41.0.0

---

## Submission Date

April 20, 2026
