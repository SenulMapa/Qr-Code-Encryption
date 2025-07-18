import qrcode

def OpenFile():
    ImageFile = input("Enter path to file: ")
    with open(ImageFile, "rb") as fo:
        hex_data = fo.read().hex()

    # Make sure chunk_size is a multiple of 2 (each byte = 2 hex chars)
    chunk_size = 1000 * 2  # 1000 bytes = 2000 hex characters

    chunks = []
    order = 0
    for i in range(0, len(hex_data), chunk_size):
        chunk_data = hex_data[i:i + chunk_size]
        prefix = hex(order)[2:].zfill(2)  # zero pad to ensure consistent sorting
        chunks.append(prefix + chunk_data)
        order += 1

    return hex_data, chunks

def makingChunks(hex_data, chunks, prefix="qr"):
    for idx, chunk in enumerate(chunks):
        qr = qrcode.QRCode(
            version=None,  # Automatically find best version ≤ 40
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(chunk)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{prefix}{idx + 1}.png")

def simpleEncrypt(hex_data):
    userseed = int(input("Enter preferred key : "))
    binary_seed = bin(userseed)[2:]  
    binary_extended = (binary_seed * ((len(hex_data) // len(binary_seed)) + 1))[:len(hex_data)]

    encrypted = ''
    for h_char, b_char in zip(hex_data, binary_extended):
        xor_result = int(h_char, 16) ^ int(b_char)
        encrypted += hex(xor_result)[2:]

    return encrypted

# === MENU ===
print("=== MENU ===")
print("1. Convert file to QR (no encryption)")
print("2. Convert file to QR with simple encryption")

menuNum = int(input("Enter menu number: "))

if menuNum == 1:
    hex_data, chunks = OpenFile()
    makingChunks(hex_data, chunks, prefix="qr_plain_")

elif menuNum == 2:
    hex_data, _ = OpenFile()
    encrypted_data = simpleEncrypt(hex_data)

    # Chunk the encrypted data manually:
    chunk_size = 1000 * 2
    encrypted_chunks = []
    order = 0
    for i in range(0, len(encrypted_data), chunk_size):
        chunk_data = encrypted_data[i:i + chunk_size]
        prefix = hex(order)[2:].zfill(2)
        encrypted_chunks.append(prefix + chunk_data)
        order += 1

    makingChunks(encrypted_data, encrypted_chunks, prefix="qr_encrypted_")

else:
    print("❌ Invalid menu number.")

