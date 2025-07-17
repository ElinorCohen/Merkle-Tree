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
| `2` | Print the current Merkle root | `2` | e.g., `3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b` |
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
```

---

### 🧪 Option 1: Run from a File

1. Create a new file in the project directory, for example: `commands.txt`
2. Add the following content to the file:
   ```bash
   1 apple
   1 banana
   2
   3 1
   ```
3. Run the program by entering the following command in your terminal:
   ```bash
   python3 merkle.py < commands.txt
   ```
4. The expected output might look like:
   ```bash
   004e48bbd922653f4cb0b656f13dbaaf72974acea5d6d836ba240ddcc780a994
   004e48bbd922653f4cb0b656f13dbaaf72974acea5d6d836ba240ddcc780a994 03a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
   ```

---

### 💬 Option 2: Run Interactively

1. Open a terminal and run:
   ```bash
   python3 merkle.py
   ```
2. Then enter commands manually, after entering, press Enter, and if there is an output, it will be printed.
3. To exit the program: press `Ctrl + Z` (Depending on your OS)

---

## 🙋 Author

Developed as an independent academic project.
