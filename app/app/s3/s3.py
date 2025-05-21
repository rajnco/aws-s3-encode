import os
import io

import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import S3UploadFailedError


class S3Bucket:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3bucket_resource = boto3.resource("s3")
        self.s3bucket = self.s3bucket_resource.Bucket(self.bucket_name)        

    def create(self)-> bool:
        try:
            self.s3bucket.create(CreateBucketConfiguration={
                "LocationConstraint": self.s3bucket_resource.meta.client.meta.region_name
            })
            return True
        except ClientError as err:
            print(f"Tried and failed to create demo bucket {self.bucket_name}.")
            print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")
            print(f"\nCan't continue the demo without a bucket!")
            return False                
        

    def list(self):
        return self.s3bucket.objects.all()

    def get(self, file_name: str, file_path: str) -> bool:
        self.s3bucket.key = file_name
        obj = self.s3bucket.Object(file_name)    
        # data = io.BytesIO()
        try:
            with open(file_path, 'wb') as file:
                file.write(obj.get()["Body"].read())
            return True
        except ClientError as err:
            print(f"Couldn't download {obj.key}.")
            print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")        
            return False

    def put(self, file_name: str) -> bool:
        obj = self.s3bucket.Object(os.path.basename(file_name))    
        try:
            obj.upload_file(file_name)
            # print(f"Uploaded file {file_name} into bucket {self.bucket_name} with key {obj.key}.")
            return True
        except S3UploadFailedError as err:
            print(f"Couldn't upload file {file_name} to {self.bucket_name}.")
            print(f"\t{err}")
            return False


    def delete_all(self) -> bool:
        try:
            self.s3bucket.objects.delete()
            self.s3bucket.delete()
            #print(f"Emptied and deleted bucket {self.bucket_name}.\n")
            return True
        except ClientError as err:
            print(f"Couldn't empty and delete bucket {self.bucket_name}.")
            print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")
            return False

def main():
    """ main method """
    bucket_name = "csvin-1"
    input_dir = "app/in/"
    output_dir = "app/out/"

    ### S3 bucket creation
    s3bucket = S3Bucket(bucket_name)  
    status = s3bucket.create()
    if not status:
        print("failed to create S3 bucket : {}".format(bucket_name))
        # os.exit()
        # sys.exit()

    ### uploading files to s3 bucket
    files = os.listdir(input_dir)
    current_directory = os.getcwd()
    file_name = ""
    for file_name in files:
        file_path = os.path.join(current_directory, input_dir, file_name)
        file_status = s3bucket.put(file_path)
        if not file_status:
            print(f"failed to uploaded file {file_name} into {bucket_name}")


    ### download file from s3 bucket  
    file_path = os.path.join(current_directory, output_dir, file_name)
    print(file_path)
    file_status = s3bucket.get(file_name, file_path)
    print(file_status)

    ### list all objects on the s3 bucket 
    s3objects = s3bucket.list()
    for o in s3objects:
        print(f"object name {o.bucket_name} : file name {o.key}")

    ### delete all objects and bucket in s3
    # s3bucket.delete_all()



if __name__ == "__main__":
    main()