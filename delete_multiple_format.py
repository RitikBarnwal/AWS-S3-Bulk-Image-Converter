import boto3
import concurrent.futures
from credentials import s3  # Import S3 client from credentials.py

BUCKET_NAME = "aws-restaurants"
SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".gif"]
MAX_WORKERS = 10  # Number of parallel threads


def delete_image(file_key):
    """Deletes an image from S3."""
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
        print(f"🗑️ Deleted: {file_key}")
    except Exception as e:
        print(f"❌ Error deleting {file_key}: {e}")


def delete_images():
    """Fetches and deletes all supported image formats from the S3 bucket."""
    print("🔍 Scanning for images to delete...")

    continuation_token = None
    total_deleted = 0

    while True:
        # Fetch 1000 objects at a time
        response = (
            s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=1000, ContinuationToken=continuation_token)
            if continuation_token
            else s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=1000)
        )

        if "Contents" not in response:
            print("✅ No more images left to delete!")
            break

        # Filter only supported image formats
        image_keys = [obj["Key"] for obj in response["Contents"] if any(obj["Key"].lower().endswith(ext) for ext in SUPPORTED_FORMATS)]

        if not image_keys:
            print("⚠ No matching images found in this batch.")
            continuation_token = response.get("NextContinuationToken")
            if not continuation_token:
                break
            continue

        # Delete images in parallel using multithreading
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(delete_image, image_keys)

        total_deleted += len(image_keys)
        print(f"🚀 Deleted {total_deleted} images so far...\n")

        # Check if more images exist
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break

    print("\n🎉 All selected images deleted successfully!")


if __name__ == "__main__":
    delete_images()
