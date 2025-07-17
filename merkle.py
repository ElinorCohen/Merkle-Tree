import sys
import base64
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

class MerkleTree:
    def __init__(self):
        # Initialize an empty list of leaves
        self.leaves = []
        
    def add_leaf(self, data: str):
        # Hash the data using SHA-256
        hashed_data = hashlib.sha256(data.encode()).hexdigest()
    
        # Add a leaf to the tree
        self.leaves.append(hashed_data)

        
    def get_merkle_root(self) -> str:
        level = self.leaves
        if not level:
            return ""
        
        # Repeatedly hash pairs on each level until one hash is left
        while len(level) > 1:
            new_level = []
            i = 0

            # Hash pairs of nodes in the current level
            while i < len(level) - 1:
                combined = level[i] + level[i + 1]
                hashed = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(hashed)
                i += 2

            # If there's an odd number of nodes in the current level, move the last one up
            if i == len(level) - 1:
                new_level.append(level[i])

            level = new_level
            
        return level[0]
    
    
    def create_proof_of_inclusion_for_leaf(self, leaf_index: int) -> str:
        proof = []
        current_index = leaf_index
        current_level = self.leaves
        left_prefix = "0"
        right_prefix = "1"
        
        while len(current_level) > 1:
            next_level = []
            i = 0
            while i < len(current_level):
                # If there's a pair of nodes, hash them and add the result to the next level
                if i + 1 < len(current_level):
                    left_node = current_level[i]
                    right_node = current_level[i + 1]
                    parent_node = hashlib.sha256((left_node + right_node).encode()).hexdigest()
                    next_level.append(parent_node)

                    # The current index is the left node, add the right node to the proof (add 1)
                    if current_index == i:
                        proof.append(f"{right_prefix}{right_node}")
                        current_index = len(next_level) - 1

                    # The current index is the right node, add the left node to the proof (add 0)
                    elif current_index == i + 1:
                        proof.append(f"{left_prefix}{left_node}")
                        current_index = len(next_level) - 1

                    # Move to the next pair of nodes
                    i += 2
                else:
                    # If there's an odd number of nodes in the current level, move the last one up
                    lonely_node = current_level[i]
                    next_level.append(lonely_node)

                    # If the current index is the lonely node, update the current index to the index of the lonely node in the next level
                    if current_index == i:
                        current_index = len(next_level) - 1
                    i += 1

            current_level = next_level
            
        root = current_level[0]
        return f"{root} {' '.join(proof)}"
    

    def verify_proof_of_inclusion(self, leaf_data: str, proof: str) -> bool:
        try:
            # Hash the leaf data
            leaf_hash = hashlib.sha256(leaf_data.encode()).hexdigest()

            # Split the proof into the root and the proof steps
            root = proof.split()[0]
            proof_steps = proof.split()[1:]

            # Reconstruct the tree from the proof steps
            current_hash = leaf_hash
            for step in proof_steps:
                if step[0] == "0":
                    current_hash = hashlib.sha256((step[1:] + current_hash).encode()).hexdigest()
                elif step[0] == "1":
                    current_hash = hashlib.sha256((current_hash + step[1:]).encode()).hexdigest()

            return current_hash == root
        except:
            return False
        

    def generate_rsa_keys(self):
        # Generate the keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
            )
        public_key = private_key.public_key()

        # Convert the keys to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
            ).decode()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

        return private_pem, public_pem
    

    def sign_current_root(self, private_key: str) -> str:
        # Convert the private key string to a private key object
        private_key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=default_backend()
            )
        
        # Sign the current root
        signature = private_key.sign(
            self.get_merkle_root().encode(),
            padding.PKCS1v15(), # Deterministic padding
            hashes.SHA256()
            )
        
        # Convert the signature to a base64 string
        signature_base64 = base64.b64encode(signature).decode()
        return signature_base64
    

    def verify_signature(self, public_key: str, signature: str, root_to_verify : str) -> bool:
        try:
            # Convert the public key string to a public key object
            public_key = serialization.load_pem_public_key(
                public_key.encode(),
                backend=default_backend()
                )
            
            # Convert the signature from base64 to bytes
            signature_bytes = base64.b64decode(signature)

            # Verify the signature
            public_key.verify(
                signature_bytes, 
                root_to_verify.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
                )
            return True
        except:
            return False

if __name__ == "__main__":
    # Create a Merkle tree
    tree = MerkleTree()
    private_key = None
    public_key = None
    signature = None

    while True:
        try:
            command = sys.stdin.readline()
            if not command:
                break
            
            command = command.strip()
            parts = command.split()

            if command == "": # Do nothing
                continue
            
            if command[0] == "1": # Call add_leaf()
                data = parts[1]
                tree.add_leaf(data)
                
            elif command[0] == "2": # Call get_merkle_root()
                root = tree.get_merkle_root()
                print(root)

            elif command[0] == "3": # Call create_proof_of_inclusion()
                leaf_index = int(parts[1])
                proof = tree.create_proof_of_inclusion_for_leaf(leaf_index)
                print(proof)

            elif command[0] == "4": # Call verify_proof_of_inclusion()
                leaf_data = parts[1]
                proof = ' '.join(parts[2:])
                is_valid = tree.verify_proof_of_inclusion(leaf_data, proof)
                print(is_valid)

            elif command[0] == "5": # Call generate_rsa_keys()
                private_key, public_key = tree.generate_rsa_keys()
                print(private_key)
                print(public_key)

            elif command[0] == "6": # Call sign_current_root()
                # Read the private key from the input
                private_key_lines = []
                first_line = ' '.join(parts[1:])
                private_key_lines.append(first_line)
                while True:
                    line = input().strip()
                    private_key_lines.append(line)
                    if line == "-----END RSA PRIVATE KEY-----":
                        break

                private_key_text = '\n'.join(private_key_lines)

                signature = tree.sign_current_root(private_key_text)
                print(signature)

            elif command[0] == "7": # Call verify_signature()
                # Read the private key from the input
                public_key_lines = []
                first_line = ' '.join(parts[1:])
                public_key_lines.append(first_line)
                while True:
                    line = input().strip()
                    public_key_lines.append(line)
                    if line == "-----END PUBLIC KEY-----":
                        break

                public_key_text = '\n'.join(public_key_lines)
                
                # Read the signature and root from the input
                signature_lines = []
                while True:
                    line = input().strip()
                    if line == "":
                        continue

                    # If the line is 64 chars, it's likely the SHA-256 Merkle root, not base64 signature
                    if len(line) == 64:
                        # If the line is valid hex, it's the root hash (not a base64 signature)
                        try:
                            int(line, 16) # Try to parse the line as a hex number
                            root_to_verify = line
                            break
                        except:
                            signature_lines.append(line)
                    else:
                        signature_lines.append(line)

                signature_text = '\n'.join(signature_lines)

                is_valid = tree.verify_signature(public_key_text, signature_text, root_to_verify)
                print(is_valid)


        except:
            print("\n")
