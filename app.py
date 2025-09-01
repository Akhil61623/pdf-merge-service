import time
from tqdm import tqdm

# Dummy function to simulate file compression
def compress_file(input_file, target_size_mb):
    print(f"\nCompressing {input_file} to ~{target_size_mb} MB...\n")
    for _ in tqdm(range(100), desc="Compressing", ncols=100):
        time.sleep(0.03)  # simulate processing
    print(f"✅ File compressed successfully to {target_size_mb} MB\n")

# Dummy function to simulate file splitting
def split_file(input_file, part_size_mb):
    print(f"\nSplitting {input_file} into parts of {part_size_mb} MB...\n")
    for _ in tqdm(range(100), desc="Splitting", ncols=100):
        time.sleep(0.02)  # simulate processing
    print(f"✅ File split into chunks of {part_size_mb} MB each\n")

# Main program
if __name__ == "__main__":
    print("==== File Compressor & Splitter ====")
    file_name = input("Enter your file name (e.g., example.pdf): ")

    # Compression target
    target_size = int(input("Enter target size in MB (e.g., 70): "))
    compress_file(file_name, target_size)

    # Splitting size
    part_size = int(input("Enter part size in MB for splitting (e.g., 20): "))
    split_file(file_name, part_size)

    print("🎉 All operations completed successfully!")
