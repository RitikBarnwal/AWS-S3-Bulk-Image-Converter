# AWS S3 Image Converter

A Python script to convert images in an AWS S3 bucket to WebP format using multithreading for faster processing. This script supports `.png`, `.jpg`, `.jpeg`, and `.gif` formats.

---

## 🚀 Features
- Converts images from `.png`, `.jpg`, `.jpeg`, and `.gif` to `.webp`
- Uses **multithreading** for faster processing
- Skips images that have already been converted
- Optimized to process large numbers of images efficiently

---

## 🛠 Setup & Installation

### 1️⃣ Install Python & Pip
Make sure you have **Python 3** and **pip** installed on your system.

```sh
sudo apt update && sudo apt install python3 python3-pip -y  # Ubuntu/Debian
```

For Windows, download Python from [python.org](https://www.python.org/downloads/) and install it.

---

### 2️⃣ Clone the Repository

```sh
git clone https://github.com/your-repo/aws-s3-image-converter.git
cd aws-s3-image-converter
```

---

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

---

### 4️⃣ Setup AWS Credentials

Open `credentials.py` file and configure it with your AWS S3 credentials:

```python
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='YOUR_REGION'
)
```

Replace `YOUR_ACCESS_KEY`, `YOUR_SECRET_KEY`, and `YOUR_REGION` with your actual AWS credentials.

---

## ▶️ Running the Script

Run the image conversion script:

```sh
python convert_images.py
```

This will scan all images in your AWS S3 bucket and convert them to WebP format.

---

## 🗑 Deleting PNG Files

To delete all `.png` files after conversion, run:

```sh
python delete_png.py
```

---

## 🔄 Custom Image Format Conversion

By default, this script converts images to `.webp`. However, you can modify the script to convert images to any other format (e.g., `.png`, `.jpeg`, `.jpg`, etc.). Simply update this line in `convert_images.py`:

```python
new_file_key = file_key.rsplit(".", 1)[0] + ".webp"
```

Replace `.webp` with your desired format, such as `.jpg` or `.png`. For example:

```python
new_file_key = file_key.rsplit(".", 1)[0] + ".jpg"
```

This allows the script to convert images into `.jpg` instead of `.webp`.

---

## 👨‍💻 Author & Services

This script is developed by **Ritik Barnwal**. If you need professional server management, AWS S3 automation, or custom scripts, feel free to contact us at:

🌐 **Website:** [myserverhelper.com](https://myserverhelper.com)

📩 **Hire us for your server & automation needs!**

