import qrcode
menuNum = 0
def OpenFile():
    ImageFile = ""
    ImageFile = str(input("Enter path to file: "))
    with open(ImageFile, "rb") as fo:
        hex_data = fo.read().hex()

        # Make sure chunk_size is a multiple of 2 (each byte = 2 hex chars)
        chunk_size = 1000 * 2  # 1000 bytes = 2000 hex characters

        chunks = []
        order = 0
        for i in range(0, len(hex_data), chunk_size):
            chunk_data = hex_data[i:i + chunk_size]
            prefix = hex(order)[2:]  # convert order to hex string
            chunks.append(prefix + chunk_data)
            order += 1

        return hex_data, chunks
def xor_encrypt(hex_data, seed):
    # Convert seed to a repeated byte pattern
    seed_bytes = seed.to_bytes((seed.bit_length() + 7) // 8, 'big')
    if not seed_bytes:
        seed_bytes = b'\x00'
    
    # Convert hex string back to actual bytes
    raw_bytes = bytes.fromhex(hex_data)
    
    # Extend key to match data length
    repeated_key = (seed_bytes * (len(raw_bytes) // len(seed_bytes) + 1))[:len(raw_bytes)]
    
    # XOR
    encrypted_bytes = bytes([b ^ k for b, k in zip(raw_bytes, repeated_key)])
    
    # Return encrypted hex string
    return encrypted_bytes.hex()


#def makingChunks(hex_data,chunks):
    # for idx, chunk in enumerate(chunks):
    #     qr = qrcode.make(chunk)
    #     qr.save(f"qr{idx + 1}.png")
    #     print("original hex data: ")
    #     print(hex_data)

def makingChunks(hex_data, chunks):
    for idx, chunk in enumerate(chunks):
        qr = qrcode.QRCode(
            version=None,  # Automatically find best version ≤ 40
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # M = ~15% correction
            box_size=10,
            border=4,
        )
        qr.add_data(chunk)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"qr{idx + 1}.png")

def simpleEncrypt(hex_data):
    userseed = int(input("Enter preferred key : "))
    binary_seed = bin(userseed)[2:]  
    # Repeat the seed to match length of hex_data
    binary_extended = (binary_seed * ((len(hex_data) // len(binary_seed)) + 1))[:len(hex_data)]
    # XOR for simple encryption
    encrypted = ''
    for h_char, b_char in zip(hex_data, binary_extended):
        encrypted += hex(int(h_char, 16) ^ int(b_char))[-1]
    return encrypted

print("Menu")
print("1. Just Convert ")
print("2. With Encryption")
menuNum = int(input("Enter menu number: "))
if menuNum == 1:
    hex_data, chunks = OpenFile()
    makingChunks(hex_data, chunks)

elif menuNum == 2:
    hex_data, _ = OpenFile()
    userseed = int(input("Enter preferred key : "))
    encrypted_data =xor_encrypt(hex_data,userseed)

    # Chunk encrypted data
    chunk_size = 1000 * 2
    encrypted_chunks = []
    order = 0
    for i in range(0, len(encrypted_data), chunk_size):
        chunk_data = encrypted_data[i:i + chunk_size]
        prefix = hex(order)[2:]
        encrypted_chunks.append(prefix + chunk_data)
        order += 1

    makingChunks(encrypted_data, encrypted_chunks)

else:
    print("Invalid menu number.")

