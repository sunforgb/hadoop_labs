import os
import requests
from urllib.parse import urljoin, urlparse
import argparse
import cmd
import sys
from lib import HDFSObject, LocalFSObject
import stat


class HDFSClient(cmd.Cmd):

    def __init__(self, base_url: str, base_port: str, user: str):
        cmd.Cmd.__init__(self)
        # save base_url as a root path
        self.base_url = f"http://{base_url}:{base_port}/webhdfs/v1/"
        # context path
        self.pwd = f"http://{base_url}:{base_port}/webhdfs/v1/"
        self.request_params = {"user.name": user}

    def __fix_dots(self, path: str, base: list=[]) -> list:
        for part in path.split("/"):
            if not part or part == ".":
                continue
            if base and part == "..":
                base.pop()
            else:
                base.append(part)
        return base


    def _fix_path(self, path: str):
        # absolute paths, just make it

        if path.startswith("/"):
            target_path = self.base_url
            path = path.strip("/")
            return urljoin(target_path, path)
        #
        path = "" if path is None else path.strip()
        # prepare mini-stack for dots
        spl = []
        tmp_1 = urlparse(self.base_url).path.split("/")
        tmp_2 = urlparse(self.pwd).path.split("/")
        for item in tmp_2:
            if item not in tmp_1:
                spl.append(item)
        spl = self.__fix_dots(path, spl)
        request_url = urljoin(self.base_url, "/".join(spl))
        return request_url
    
    def _fix_local_path(self, path: str):
        path = "" if path is None else path.strip()
        if not path.startswith("/"):
            path = f"{os.getcwd()}/{path}"
        spl = self.__fix_dots(path)
        return "/"+"/".join(spl)

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
        response = requests.put(self._fix_path(remote_path), params=request_param)
        if response.status_code == 200:
            print("directory was created!")
        else:
            return False

    def do_put(self, input_line: str) -> bool:
        """
        Usage: put <local file> <remote_dir>

        Upload local file into remote directory
        """
        local_path, remote_path = input_line.split()
        request_param = {"op": "CREATE", "overwrite": True}
        response = requests.put(
            self._fix_path(remote_path), params=request_param, allow_redirects=False
        )
        if response.status_code != 307:
            print("Error in create_file request, status_code: ", response.status_code)
            return False
        load_headers = {"content-type": "application/octet-stream"}
        with open(local_path, "rb") as file:
            content = file.read()
            response = requests.put(
                response.headers["location"],
                headers=load_headers,
                files={local_path: content},
            )
            if response.status_code == 201:
                print("File was created")
            else:
                print("Error in create_file request, status_code: ", response.status_code)
        

    def do_get(self, remote_path: str) -> bytes:
        """
        Usage: get <remote_file>

        Download remote file from HDFS and save in current local directory
        """
        request_param = {"op": "OPEN"}
        response = requests.get(
            self._fix_path(remote_path), params=request_param, allow_redirects=True
        )
        if response.status_code != 200:
            print("Error in get_file, status_code:", response.status_code)
            return False
        local_path = remote_path.split("/")[-1]
        with open(local_path, "wb") as f:
            f.write(response.content)

    def do_append(self, input_line: str):
        """
        Usage: append <local_file> <remote_file>

        Append local file to remote file
        """
        local_path, remote_path = input_line.split(" ")
        request_param = {"op": "APPEND"}
        response = requests.post(
            self._fix_path(remote_path), params=request_param, allow_redirects=False
        )
        if response.status_code != 307:
            print("Error in append_file request, status_code: ", response.status_code)
            return False
        load_headers = {"content-type": "application/octet-stream"}
        with open(local_path, "rb") as f:
            content = f.read()
        response = requests.post(
            response.headers["location"],
            headers=load_headers,
            files={local_path: content},
        )
        if response.status_code == 200:
            print("File was appended")
        else:
            print("Error in append_file request, status_code: ", response.status_code)
            return False

    def do_delete(self, remote_path: str):
        """
        Usage: delete <remote_file>

        Delete remote file
        """
        request_param = {"op": "DELETE"}
        response = requests.delete(self._fix_path(remote_path), params=request_param)
        if response.status_code == 200:
            print("Remote file was deleted")
        else:
            print("Error in delete_file request, status_code: ", response.status_code)
            return False
    def _complete_ls(self, objects: list[HDFSObject|LocalFSObject]):
        columns = ["mode", "repl", "owner", "group", "size", "name"]
        lengths = dict(zip(columns, [0] * len(columns)))
        build = {}
        align = {
            'repl': '>',
            'size': '>',
        }
        objs = []
        for item in objects:
            tmp = {}
            for name in columns:
                text = build.get(name, "{}").format(getattr(item, name))
                tmp[name] = text
                lengths[name] = max(lengths[name], len(text))
            objs.append(tmp)
            text = text = ' '.join('{%s:%s%s}' % (i, align.get(i, ''), lengths[i]) for i in columns)
        for item in objs:
            print(text.format(**item))

    def do_ls(self, remote_path: str = "."):
        """
        Usage: ls [remote_dir]

        List remote directory. If remote dir not provided, then list current dir.
        """
        objects = []
        request_param = {"op": "LISTSTATUS"}
        path = self._fix_path(remote_path)
        response = requests.get(path, params=request_param)
        if response.status_code == 200:
            for item in response.json()["FileStatuses"]["FileStatus"]:
                objects.append(HDFSObject(path, item))
            self._complete_ls(objects)
        elif response.status_code == 404:
            print("No such file or directory")
        else:
            print("Error in list_files, status_code: ", response.status_code)
            return False

    def do_cd(self, remote_path: str):
        """
        Usage: cd <remote_dir>

        Change current work directory in HDFS.
        """
        self.pwd = self._fix_path(remote_path)

    def do_lls(self, local_path: str):
        """
        Usage: lls [local_dir]

        List local directory. If local directory not provided, then list current dir
        """
        objects = []
        try:
            path = self._fix_local_path(local_path)
            info = os.stat(path)
            if stat.S_ISDIR(info.st_mode):
                objects = list(LocalFSObject(path, name) for name in os.listdir(path))
            elif stat.S_ISREG(info.st_mode):
                objects = [LocalFSObject(os.path.dirname(path), os.path.basename(path))]
            self._complete_ls(objects)
        except (KeyError, OSError) as e:
            print("Smth went wrong in local ls")
            print(e)

        
        

    def do_lcd(self, local_path: str):
        """
        Usage: lcd <local_dir>

        Change current local working directory.
        """
        os.chdir(local_path)

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
    parser.add_argument("-d", "--url", help="WebHDFS URL")
    parser.add_argument("-p", "--port", help="WebHDFS port")
    parser.add_argument("-u", "--user", help="WebHDFS username")
    args = parser.parse_args()
    try:
        print(args)
        main(args.url, args.port, args.user)
    except KeyboardInterrupt:
        print("Good Bye")
