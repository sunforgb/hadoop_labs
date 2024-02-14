import os
import requests
from urllib.parse import urljoin
import argparse
import cmd
import sys

usage = """
    This is future help message
"""
hadoop_url = "http://192.168.122.8:50070/webhdfs/v1/"


class HDFSClient(cmd.Cmd):

    def __init__(self, base_url: str, base_port: str, user: str):
        cmd.Cmd.__init__(self)
        self.url = f"http://{base_url}:{base_port}/webhdfs/v1/"
        self.request_params = {"user.name": user}

    def do_exit(self, _):
        """
        Usage: exit

        Exits client.
        """
        print("Good Bye")
        sys.exit(0)

    def do_EOF(self, _):
        print()
        return True

    def do_mkdir(self, remote_path: str) -> bool:
        """
        Usage: mkdir <remote_dir>

         Creates remote directory
        """
        request_param = {"op": "MKDIRS"}
        response = requests.put(urljoin(self.url, remote_path), params=request_param)
        if response.status_code == 200:
            return response.json()["boolean"]
        else:
            return False

    def do_put(self, data: str, path: str) -> bool:
        """
        Usage: put <local file> <remote_dir>

        Upload local file into remote directory
        """
        request_param = {"op": "CREATE", "overwrite": True}
        response = requests.put(
            urljoin(self.url, path), params=request_param, allow_redirects=False
        )
        # TODO check for redirect status code
        load_headers = {"content-type": "application/octet-stream"}
        with open(data, "rb") as file:
            content = file.read()
            response = requests.put(
                response.headers["location"],
                headers=load_headers,
                files={data: content},
            )
        print(response.status_code)
        # TODO check for 201 status_code

    def do_get(self, path: str) -> bytes:
        """
        Usage: get <remote_file>

        Download remote file from HDFS and save in current local directory
        """
        request_param = {"op": "OPEN"}
        response = requests.get(
            urljoin(self.url, path), params=request_param, allow_redirects=True
        )
        return response.content

    def do_append(self, file_path: str, path: str):
        """
        Usage: append <local_file> <remote_file>

        Append local file to remote file
        """
        request_param = {"op": "APPEND"}
        response = requests.post(
            urljoin(self.url, path), params=request_param, allow_redirects=False
        )
        load_headers = {"content-type": "application/octet-stream"}
        with open(file_path, "rb") as f:
            content = f.read()
        response = requests.post(
            response.headers["location"],
            headers=load_headers,
            files={file_path: content},
        )
        print(response.status_code)

    def do_delete(self, path: str):
        """
        Usage: delete <remote_file>

        Delete remote file
        """
        request_param = {"op": "DELETE"}
        response = requests.delete(urljoin(self.url, path), params=request_param)
        if response.status_code == 200:
            return response.json()["boolean"]
        else:
            return False

    # TODO check for statuses and pretty print
    def do_ls(self, path: str = "."):
        """
        Usage: ls [remote_dir]

        List remote directory. If remote dir not provided, then list current dir.
        """
        request_param = {"op": "LISTSTATUS"}
        response = requests.get(urljoin(self.url, path), params=request_param)
        for item in response.json()["FileStatuses"]["FileStatus"]:
            print(item["pathSuffix"])

    def do_cd(self):
        """
        Usage: cd <remote_dir>

        Change current work directory in HDFS.
        """
        pass

    def do_lls(self):
        """
        Usage: lls [local_dir]

        List local directory. If local directory not provided, then list current dir
        """
        pass

    def do_lcd(self):
        """
        Usage: lcd <local_dir>

        Change current local working directory.
        """
        pass

    def do_doc(self, line):
        help_message = """
            Available commands:
    * mkdir <remote_dir>
    * put <local_file> <remote_dir>
    * get <remote_file>
    * append <local_file> <remote_file>
    * delete <remote_file>
    * ls [remote_dir]
    * cd <remote_dir>
    * lls [local_dir]
    * lcd <local_dir>

    For more information type help <command>
        """
        print(help_message.strip())


def main(url: str, port: str, user: str):
    print(f"Welcome to Hadoop HDFS Client {user}")
    print("Current HDFS directory: /")
    print(f"Current local directory: {os.getcwd()}")
    client = HDFSClient(url, port, user)
    client.cmdloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="webhdfs client shell",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-u", "--url", help="WebHDFS URL")
    parser.add_argument("-p", "--port", help="WebHDFS port")
    parser.add_argument("-U", "--user", help="WebHDFS username")
    args = parser.parse_args()
    try:
        main(args.url, args.port, args.user)
    except KeyboardInterrupt:
        print("Good Bye")
