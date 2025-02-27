def delete_png_files():
    """Delete all PNG files from S3 bucket."""
    print("\n🗑 Deleting all PNG images from the bucket...\n")

    continuation_token = None
    while True:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, ContinuationToken=continuation_token) if continuation_token else s3.list_objects_v2(Bucket=BUCKET_NAME)

        if 'Contents' not in response:
            print("❌ No PNG files found!")
            break

        png_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith(".png")]

        if not png_files:
            print("✅ No more PNG files left to delete.")
            break

        # Batch delete files (S3 allows batch delete of 1000 objects max)
        delete_objects = {'Objects': [{'Key': file_key} for file_key in png_files]}
        s3.delete_objects(Bucket=BUCKET_NAME, Delete=delete_objects)

        print(f"🗑 Deleted {len(png_files)} PNG files.")

        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break

    print("\n🎉 PNG cleanup completed!")

if __name__ == "__main__":
    delete_png_files()
