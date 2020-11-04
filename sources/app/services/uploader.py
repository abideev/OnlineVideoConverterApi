import shutil
import boto3
import os
from botocore.exceptions import NoCredentialsError


def uploader_file(filename,title):
    # abs_path_ytdl = os.path.dirname(os.path.abspath(__file__))
    # path_download = os.path.join(abs_path_ytdl, "..", "data")
    # src = rf'{path_download}/{filename}'
    # outdir = rf'/download/{filename}'
    # shutil.move(src, outdir)
    # dst_url = (filename)
    ##
    abs_path_ytdl = os.path.dirname(os.path.abspath(__file__))
    path_download = os.path.join(abs_path_ytdl, "..", "data")
    dst_url=rf'{path_download}/{filename}'
    return (dst_url,title)

##TODO
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv("ACCESS_KEY"),
                      aws_secret_access_key=os.getenv("SECRET_KEY"))

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


#uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')
