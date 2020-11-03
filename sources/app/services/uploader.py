import shutil
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def uploader_file(filename):
    src = rf'C:\Users\ph03n1x\Documents\Downloads\{filename}'
    outdir = rf'C:\Users\ph03n1x\Documents\123\{filename}'
    shutil.move(src, outdir)
    dst_url = (filename)
    return dst_url


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')
