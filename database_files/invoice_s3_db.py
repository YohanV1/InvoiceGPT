import boto3
from botocore.exceptions import ClientError
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3')

BUCKET_NAME = 'invoicegpt'

def upload_to_s3(file_object, filename, user_email):
    try:
        s3_path = f"invoices/{user_email}/{filename}"

        s3_client.upload_fileobj(file_object, BUCKET_NAME, s3_path)

        return s3_path
    except ClientError as e:
        st.error(f"Error uploading file to S3: {e}")
        return None
