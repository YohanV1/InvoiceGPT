import boto3
from botocore.exceptions import ClientError
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3')

BUCKET_NAME = 'invoicegpt-bucket'

def upload_to_s3(file_object, filename, user_email):
    try:
        s3_path = f"invoices/{user_email}/{filename}"

        s3_client.upload_fileobj(file_object, BUCKET_NAME, s3_path)

        return s3_path
    except ClientError as e:
        st.error(f"Error uploading file to S3: {e}")
        return None


def remove_user_files_from_s3(user_email):
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=f"invoices/{user_email}/"
        )
        if 'Contents' not in response:
            return
        objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

        s3_client.delete_objects(
            Bucket=BUCKET_NAME,
            Delete={'Objects': objects_to_delete}
        )

    except ClientError as e:
        st.error(f"Error deleting files from S3: {e}")
