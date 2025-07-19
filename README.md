# Qr-Code-Encryption
This is a simple tool made using python to convert images to qr codes , A fun little twist on encryption 

## How it works ⚡
When you upload an image to the encoder it grabs the hex data from the images, and since qr codes are just another form of media storage, the program will write the hex data into qr codes. BUT since qr codes can only hold so much informtation the program would break the information down into chunks, These chunks have 4 hex values seperated to store the chunk number which helps with smoother regeneration.

The encryption is optional and very simple, it was built with the help of Open Ai's ChatGPT. Essentially it messes up the hex data so unless you use the correct (seed/password) the image would be corrupted. A use case would be leaving 3-4 qr codes on your computer and carrying 2-3 of them on a seperate pendrive. This way the images could only be reconstructed using the pen drive and the computer in unison.
- 🔥 **Note**: Lose even one QR code, and you lose the image. Whether that’s a _security feature_ or a _problem_ is up to you.




  ## 🛠️ Built With
- **Python 3.13** – core programming language (Python 3.6+ is compatible)
- [`qrcode`](https://pypi.org/project/qrcode/) – for generating QR codes
- [`Pillow`](https://pypi.org/project/Pillow/) – for image processing
- [`pyzbar`](https://pypi.org/project/pyzbar/) – for decoding QR codes from images

---

### 🔧 Prerequisites
Make sure you have the following installed:

- **Python 3.13**
- `pip` – Python package manager
- Required Python libraries:
  - `qrcode`
  - `Pillow`
  - `pyzbar`

You can install all dependencies with:


```bash
pip install qrcode
pip install pillow
pip install pyzbar
```


### ⚠ Note
_**SOME OF THE COMMENTS AND ERROR HANDLING HAS HUMOUR SO A MORE PROFESIONAL VERSION IS IN THE WORKS AND WILL BE RELEASED CUREENTLY THE CODE IS QUITE MESSY AND THERE ARE TWO OF EACH ENCODERS AND DECODERS , IN A FUTURE UPDATE I PLAN ON CLEANING THAT UP AND MAKING SURE THE ONLY USEFUL PYTHON SCRIPTS ARE THERE.**_

