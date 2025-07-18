import os
from PIL import Image
from pyzbar.pyzbar import decode

def scan_qr_codes(folder_path):
    scanned_chunks = []

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(image_path)
                decoded_objs = decode(img)

                if decoded_objs:
                    data = decoded_objs[0].data.decode("utf-8")
                    print(f"✅ Decoded {filename}: starts with '{data[:10]}'")
                    scanned_chunks.append(data)
                else:
                    print(f"❌ Failed to decode: {filename}")
            except Exception as e:
                print(f"⚠️ Error opening {filename}: {e}")

    return scanned_chunks

def simple_decrypt(encrypted_hex, key):
    seed_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    if not seed_bytes:
        seed_bytes = b'\x00'

    raw_bytes = bytes.fromhex(encrypted_hex)
    repeated_key = (seed_bytes * ((len(raw_bytes) // len(seed_bytes)) + 1))[:len(raw_bytes)]

    decrypted_bytes = bytes([b ^ k for b, k in zip(raw_bytes, repeated_key)])
    return decrypted_bytes.hex()


    decrypted = ''
    for h_char, b_char in zip(encrypted_hex, binary_extended):
        xor_result = int(h_char, 16) ^ int(b_char)
        decrypted += hex(xor_result)[2:]

    return decrypted

def reconstruct_file(scanned_chunks, encrypted=False, key=None, output_path="reconstructed.jpg"):
    if not scanned_chunks:
        print("🚫 No valid QR codes were decoded.")
        return

    try:
        # Sort by prefix
        ordered_chunks = sorted(scanned_chunks, key=lambda x: int(x[0], 16))

        # Remove prefixes and validate hex
        valid_chunks = []
        for i, chunk in enumerate(ordered_chunks):
            hex_data = chunk[1:]

            if encrypted:
                hex_data = simple_decrypt(hex_data, key)

            try:
                bytes.fromhex(hex_data)
                valid_chunks.append(hex_data)
            except ValueError as e:
                print(f"❌ Invalid hex in chunk {i} (prefix={chunk[0]}):", e)

        rejoined_hex = ''.join(valid_chunks)
        with open(output_path, "wb") as f:
            f.write(bytes.fromhex(rejoined_hex))

        print(f"✅ File reconstructed and saved as: {output_path}")

    except Exception as e:
        print("❌ General error during reconstruction:", e)

# === MENU ===
print("=== QR Reconstructor ===")
print("1. Reconstruct plain QR codes")
print("2. Reconstruct encrypted QR codes")

menu_choice = input("Enter menu number: ")

folder_with_qrs = input("Enter path to folder with QR codes: ")
scanned = scan_qr_codes(folder_with_qrs)

if menu_choice == "1":
    reconstruct_file(scanned, encrypted=False)

elif menu_choice == "2":
    try:
        user_key = int(input("Enter decryption key: "))
        reconstruct_file(scanned, encrypted=True, key=user_key)
    except ValueError:
        print("❌ Invalid key. Must be a number.")
else:
    print("❌ Invalid option.")
