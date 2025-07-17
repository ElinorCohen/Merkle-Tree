# 🌳 Merkle Tree CLI Tool with Proofs & RSA Signatures

## 📌 Overview

This project implements a Merkle Tree structure in Python, including:

- Leaf addition with SHA-256 hashing
- Merkle root calculation
- Proof of inclusion generation and verification
- RSA-based signing and signature verification
- A command-line interface for interactive use

---

## 🧠 Features

- ✅ Add leaves to a Merkle tree
- 🧮 Calculate the Merkle root
- 🔎 Generate proof of inclusion for any leaf
- 🔐 Generate RSA key pair (PEM format)
- ✍️ Sign Merkle root with private key
- 🕵️ Verify signature using public key

---

## 🧾 Command Reference

Each command must be entered in a separate line:

| Command | Description | Example Input | Expected Output |
|---------|-------------|----------------|------------------|
| `1 <data>` | Add a leaf with the given value | `1 apple` | *(no output)* |
| `2` | Print the current Merkle root | `2` | e.g., `9b74c9897bac770ffc029102a200c5de` |
| `3 <index>` | Generate a proof of inclusion for the leaf at index `<index>` | `3 0` | Root + sibling path for proof |
| `4 <data> <proof>` | Verify a proof of inclusion for `<data>` using proof string | `4 apple <proof>` | `True` or `False` |
| `5` | Generate RSA key pair (PEM format) | `5` | Printed private & public keys |
| `6 <private_key>` | Sign the Merkle root using private key | `6 -----BEGIN RSA PRIVATE KEY----- ...` | Base64-encoded signature |
| `7 <public_key>` | Verify a signature and Merkle root using public key | `7 -----BEGIN PUBLIC KEY----- ...` | `True` or `False` |

---

## ▶️ How to Run the Script

### 🔧 Prerequisites

1. Make sure Python 3.x is installed on your machine.
2. Install the required library using pip:

```bash
pip install cryptography
