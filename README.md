****Steps to initiate and try out imageInterpretor.****
Step 1: Activate virtual environment, open linux kernal and perform the following actions given below.
```bash
- sudo apt-get update
- sudo apt-get install ffmpeg
```

Install tesseract-ocr and replace existing tessdata folder with the given tessdata folder from repo.

```bash
- sudo apt-get install python3.11-venv python3.11-dev
- python3.11 -m venv .venv
- . .venv/bin/activate
```

Step 2: Install python requirements, open terminal and perform the following action given below.
```bash
- pip install -r requirements.txt
```

Step 3:
use the imageInterpretor.py script and insert the required path to translate to english.
```bash
img_inter = imageInterpretor
image_path = ""
value = img_inter.translate()
print(value)
```

#Note: Currently only languages like tamil, hindi, gujarati and other fe configured languages can be translated. This can extended by adding all the languages available in the tessdata folder.