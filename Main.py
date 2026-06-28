import time
import os
import random
import subprocess

# --- SETTINGS ---
RNAFOLD_PATH = os.path.expanduser("~/ViennaRNA/bin/RNAfold")
DNA_PARAMS = os.path.expanduser("~/ViennaRNA/share/ViennaRNA/dna_mathews2004.par")
OUTPUT_DIR = os.path.abspath("3d_input_files")
NUMBER_OF_SEQUENCES = 10
MIN_LENGTH = 30
MAX_LENGTH = 90
NUCLEOTIDES = ['A', 'T', 'G', 'C']

# --- Sequence generator ---
def generate_sequences(n, min_len, max_len):
    return [
        ''.join(random.choices(NUCLEOTIDES, k=random.randint(min_len, max_len)))
        for _ in range(n)
    ]

# --- Get structure from RNAfold ---
def get_structure(dna_seq):
    try:
        result = subprocess.run(
            [RNAFOLD_PATH, f"--paramFile={DNA_PARAMS}"],
            input=dna_seq,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split('\n')
        return lines[1].split()[0] if len(lines) > 1 else None
    except subprocess.CalledProcessError as e:
        print("RNAfold error:", e.stderr)
        return None

# --- Write sequence + structure to file for 3dRNA ---
def save_for_3drna(seq_id, rna_seq, dot_bracket, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"seq_{seq_id}.txt")
    with open(file_path, "w") as f:
        f.write(f"{rna_seq}\n{dot_bracket}\n")
    print(f"[{seq_id}] Saved input file for 3dRNA: {file_path}")

# --- Main ---
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sequences = generate_sequences(NUMBER_OF_SEQUENCES, MIN_LENGTH, MAX_LENGTH)

    for i, dna_seq in enumerate(sequences, start=1):
        print(f"\n[{i}] DNA: {dna_seq}")
        structure = get_structure(dna_seq)
        if not structure:
            print(f"[{i}] Structure not found")
            continue

        rna_seq = dna_seq.replace("T", "U")
        print(f"[{i}] RNA: {rna_seq}")
        print(f"[{i}] Structure: {structure}")

        save_for_3drna(i, rna_seq, structure, OUTPUT_DIR)