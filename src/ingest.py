import os
from minio import Minio
from minio.error import S3Error

# Configuration
MINIO_ENDPOINT = "localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "raw"
# Path relative to where the script is executed (project root)
LOCAL_DATASET_PATH = os.path.join("datasets", "ml-latest-small")

def upload_to_minio():
    client = Minio(
        MINIO_ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False
    )

    # Ensure bucket exists
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
    
    files_to_upload = ["ratings.csv", "movies.csv"]
    
    for filename in files_to_upload:
        file_path = os.path.join(LOCAL_DATASET_PATH, filename)
        if os.path.exists(file_path):
            print(f"Uploading {filename} from {file_path} to MinIO...")
            client.fput_object(
                BUCKET_NAME,
                filename,
                file_path,
            )
        else:
            print(f"File {filename} not found at {file_path}!")

    print("Upload complete.")

if __name__ == "__main__":
    try:
        upload_to_minio()
    except Exception as e:
        print(f"Error: {e}")
