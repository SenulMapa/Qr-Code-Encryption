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

def reconstruct_file(scanned_chunks, output_path="reconstructed.jpg"):
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
            try:
                bytes.fromhex(hex_data)  # test if it's valid
                valid_chunks.append(hex_data)
            except ValueError as e:
                print(f"❌ Invalid hex in chunk {i} (prefix={chunk[0]}):", e)

        rejoined_hex = ''.join(valid_chunks)
        with open(output_path, "wb") as f:
            f.write(bytes.fromhex(rejoined_hex))

        print(f"✅ File reconstructed and saved as: {output_path}")

    except Exception as e:
        print("❌ General error during reconstruction:", e)


# --- USAGE ---
folder_with_qrs = str(input("Enter path to folder with qr codes: "))  # Folder containing QR images
scanned = scan_qr_codes(folder_with_qrs)
reconstruct_file(scanned, output_path="reconstructed.jpg")
