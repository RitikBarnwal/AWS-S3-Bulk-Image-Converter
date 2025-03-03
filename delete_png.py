import boto3
from credentials import s3  # Import S3 client from credentials.py

BUCKET_NAME = "aws-restaurants"


def delete_png_files():
    print("🔍 Scanning for PNG files in the S3 bucket...")
    
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
            print("✅ No PNG files found or all have been deleted!")
            break
        
        # Filter PNG files
        png_files = [obj["Key"] for obj in response["Contents"] if obj["Key"].lower().endswith(".png")]
        
        if not png_files:
            continuation_token = response.get("NextContinuationToken")
            if not continuation_token:
                break
            continue
        
        # Delete PNG files in batches
        delete_objects = {"Objects": [{"Key": key} for key in png_files]}
        s3.delete_objects(Bucket=BUCKET_NAME, Delete=delete_objects)
        total_deleted += len(png_files)
        
        print(f"🗑 Deleted {len(png_files)} PNG files... (Total: {total_deleted})")
        
        # Check if more images exist
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    
    print("🎉 All PNG files deleted successfully!")


if __name__ == "__main__":
    delete_png_files()
