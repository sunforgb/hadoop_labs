import os
import requests
from urllib.parse import urljoin

usage = """
    This is future help message
"""
hadoop_url = "http://192.168.122.8:50070/webhdfs/v1/"


def create_hdfs_dir(path: str) -> bool:
    request_param = {
        "op": "MKDIRS"
    }
    response = requests.put(urljoin(hadoop_url, path),
                            params=request_param)
    if response.status_code == 200:
        return response.json()["boolean"]
    else:
        return False

def load_hdfs_file(data: str, path: str) -> bool:
    request_param = {
        "op": "CREATE",
        "overwrite": True
    }
    response = requests.put(urljoin(hadoop_url, path),
                            params=request_param,
                            allow_redirects=False)
    #TODO check for redirect status code
    load_headers = {
        "content-type": "application/octet-stream"
    }
    with open(data, 'rb') as file:
        content = file.read()
        response = requests.put(response.headers['location'],
                            headers=load_headers,
                            files={data: content})
    print(response.status_code)
    #TODO check for 201 status_code
    


def download_hdfs_file(path: str) -> bytes:
    request_param = {
        "op": "OPEN"
    }
    response = requests.get(urljoin(hadoop_url, path),
                            params=request_param,
                            allow_redirects=True)
    return response.content

def append_hdfs_file(file_path: str, path: str):
    request_param = {
        "op": "APPEND"
    }
    response = requests.post(urljoin(hadoop_url, path),
                             params=request_param,
                             allow_redirects=False)
    load_headers = {
        "content-type": "application/octet-stream"
    }
    with open(file_path, "rb") as f:
        content = f.read()
    response = requests.post(response.headers['location'],
                             headers=load_headers,
                             files={file_path: content})
    print(response.status_code)

def delete_hdfs_file(path: str):
    request_param = {
        "op": "DELETE"
    }
    response = requests.delete(urljoin(hadoop_url, path),
                               params=request_param)
    if response.status_code == 200:
        return response.json()["boolean"]
    else:
        return False

#TODO check for statuses and pretty print
def list_hdfs_dirs(path: str):
    request_param = {
        "op": "LISTSTATUS"
    }
    response = requests.get(urljoin(hadoop_url, path),
                            params=request_param)
    for item in response.json()["FileStatuses"]["FileStatus"]:
        print(item['pathSuffix'])

def cd_hdfs_dir():
    pass

def list_local_dirs():
    pass

def cd_local_dir():
    pass

def main():
    print("Welcome to Hadoop HDFS Client")
    while True:
        user_input = str(input(f"{os.environ['LOGNAME']}>>>"))
        if user_input == "exit":
            print("Good Bye")
            break
        if user_input == "help":
            print(usage)
        user_input = user_input.split(" ")
        if user_input[0] == "mkdir":
            result = create_hdfs_dir(user_input[1])
            if result:
                print("Directory was created!")
            else:
                print("Error apeared")
        if user_input[0] == "load":
            result = load_hdfs_file(user_input[1], user_input[2])
        if user_input[0] == "download":
            result = download_hdfs_file(user_input[1])
            with open(user_input[2], "wb") as f:
                f.write(result)
        if user_input[0] == "append":
            result = append_hdfs_file(user_input[1], user_input[2])
        if user_input[0] == "delete":
            result = delete_hdfs_file(user_input[1])
            print(result)
        if user_input[0] == "list":
            result = list_hdfs_dirs(user_input[1])
            
            
        


if __name__ == "__main__":
    main()