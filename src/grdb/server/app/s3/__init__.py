import boto3
from botocore.exceptions import ClientError
import logging
from ..config import Config
from datetime import datetime


def upload_file(file, object_name):
    """

    Args:
        file: File-like object to upload
        object_name: Object name in the bucket (Full path)

    Returns: True only if upload succeeded.

    """
    s3_client = boto3.client('s3',
                             aws_access_key_id=Config.AWS_S3_ACCESS_KEY_ID,
                             aws_secret_access_key=Config.AWS_S3_SECRET_ACCESS_KEY,
                             region_name=Config.AWS_S3_REGION_NAME)
    try:
        s3_client.upload_fileobj(file,
                                 Config.AWS_S3_BUCKET_NAME,
                                 object_name,
                                 ExtraArgs={
                                     'ContentType': file.content_type
                                 })
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_presigned_url(object_name, expiration=3600):
    s3_client = boto3.client('s3',
                             aws_access_key_id=Config.AWS_S3_ACCESS_KEY_ID,
                             aws_secret_access_key=Config.AWS_S3_SECRET_ACCESS_KEY,
                             region_name=Config.AWS_S3_REGION_NAME)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': Config.AWS_S3_BUCKET_NAME,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def generate_object_name(filename: str, i: int):
    object_name = None
    timestamp = datetime.now().timestamp()

    if is_sem_file(filename):
        object_name = f'sem/{timestamp}_{str(i)}_{filename}'
    elif is_raman_file(filename):
        object_name = f'raman/{timestamp}_{str(i)}_{filename}'
    return object_name


def is_sem_file(filename):
    return len(filename) >= 3 and filename[:3] == 'sem'


def is_raman_file(filename):
    return len(filename) >= 5 and filename[:3] == 'raman'
