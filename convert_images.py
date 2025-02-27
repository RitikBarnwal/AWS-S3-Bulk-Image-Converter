import os
import boto3
import concurrent.futures
from credentials import s3  # Import S3 client from credentials.py
from PIL import Image
from io import BytesIO

BUCKET_NAME = "aws-restaurants"
SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".gif"]
MAX_WORKERS = 10  # Number of parallel threads

def print_info():
    print("Code written by Ritik Barnwal")
    print("Visit myserverhelper.com if you need server management services.\n")
    print("🔍 Scanning all images in the bucket...\n")

def process_image(file_key):
    """Converts an image to WebP and uploads it."""
    try:
        new_file_key = file_key.rsplit(".", 1)[0] + ".webp"

        # Skip if WebP file already exists
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=new_file_key)
            print(f"⚠ Skipping (already exists): {new_file_key}")
            return
        except:
            pass  # WebP file does not exist, proceed with conversion

        print(f"📂 Processing: {file_key}")

        # Download the original image
        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
        image = Image.open(BytesIO(file_obj["Body"].read()))

        # Convert to WebP (Streaming upload)
        webp_buffer = BytesIO()
        image.save(webp_buffer, "WEBP", quality=80)
        webp_buffer.seek(0)

        # Upload the WebP image
        s3.put_object(
            Bucket=BUCKET_NAME, Key=new_file_key, Body=webp_buffer, ContentType="image/webp"
        )
        print(f"✅ Converted and uploaded: {new_file_key}")

    except Exception as e:
        print(f"❌ Error processing {file_key}: {e}")

def convert_images():
    print_info()
    
    continuation_token = None
    total_processed = 0

    while True:
        # Fetch 1000 images at a time (S3 limit)
        response = (
            s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=1000, ContinuationToken=continuation_token)
            if continuation_token
            else s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=1000)
        )

        if "Contents" not in response:
            print("✅ No more images left to process!")
            break

        # Get all relevant image keys
        image_keys = [obj["Key"] for obj in response["Contents"] if any(obj["Key"].lower().endswith(ext) for ext in SUPPORTED_FORMATS)]

        if not image_keys:
            print("⚠ No valid images found in this batch!")
            continuation_token = response.get("NextContinuationToken")
            if not continuation_token:
                break
            continue

        # Process images in parallel (multithreading)
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(process_image, image_keys)

        total_processed += len(image_keys)
        print(f"🚀 Processed {total_processed} images so far...\n")

        # Check if more images exist
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break

    print("\n🎉 All images converted successfully!")

if __name__ == "__main__":
    convert_images()
