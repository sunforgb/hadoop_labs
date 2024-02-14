import os
import stat

#Just filemode table from stat
_permissions = (
    ((stat.S_IFREG,              "-"),
     (stat.S_IFDIR,              "d")),

    ((stat.S_IRUSR,              "r"),),
    ((stat.S_IWUSR,              "w"),),
    ((stat.S_IXUSR,              "x"),),

    ((stat.S_IRGRP,              "r"),),
    ((stat.S_IWGRP,              "w"),),
    ((stat.S_IXGRP,              "x"),),

    ((stat.S_IROTH,              "r"),),
    ((stat.S_IWOTH,              "w"),),
    ((stat.S_IXOTH,              "x"),)
)


def perm_to_mode(perm: str):
    mode = []
    for t in _permissions:
        for b, c in t:
            if perm & b == b:
                mode.append(c)
                break
            else:
                mode.append("-")
    return ''.join(mode)

def fix_encoding(bits: str|bytes):
    return str(bits, "utf-8") if isinstance(bits, bytes) else bits

class HDFSObject():
    def __init__(self, path:str, bits):
        self.path = path.rstrip("/")
        self.bits = bits

        if not self.bits["pathSuffix"]:
            self.bits["pathSuffix"] = os.path.basename(self.path)
            self.path = os.path.dirname(fix_encoding(self.path)).rstrip("/")
        
        self.info = {
            "perm": int(self.bits["permission"], 8) | (stat.S_IFDIR if self.is_dir() else stat.S_IFREG)
        }
        self.info["mode"] = perm_to_mode(self.info["perm"])
    
    def __str__(self):
        return self.full_name
    
    def is_dir(self):
        return self.type == "DIRECTORY"
    
    def is_file(self):
        return self.type == "FILE"
    
    @property
    def owner(self):
        return fix_encoding(self.bits["owner"])
    
    @property
    def group(self):
        return fix_encoding(self.bits["group"])
    
    @property
    def name(self):
        return fix_encoding(self.bits['pathSuffix'])
    @property
    def full_name(self):
        return f"{self.path}/{self.name}"
    @property
    def size(self):
        return self.bits["length"]
    @property
    def repl(self):
        return self.bits["replication"]
    @property
    def type(self):
        return fix_encoding(self.bits["type"])
    @property
    def mode(self):
        return self.info["mode"]
    @property
    def perm(self):
        return self.info["perm"]
    
class LocalFSObject():
    def __init__(self, path, name):
        self.path = path.rstrip("/")
        self.bits = os.stat(f"{self.path}/{name}")
        self.info = {
            "name": name,
            "type": "DIRECTORY" if stat.S_ISDIR(self.bits.st_mode) else "FILE",
            "mode": perm_to_mode(self.bits.st_mode)
        }
        self.info["owner"] = str(self.bits.st_uid)
        self.info['group'] = str(self.bits.st_gid)

    def __str__(self):
        return self.full_name
    
    def is_dir(self):
        return self.type == "DIRECTORY"
    
    @property
    def owner(self):
        return self.info["owner"]
    @property
    def group(self):
        return self.info["group"]
    @property
    def name(self):
        return self.info["name"]
    @property
    def full_name(self):
        return f"{self.path}/{self.name}"
    @property
    def size(self):
        return self.bits.st_size
    @property
    def repl(self):
        return self.bits.st_nlink
    @property
    def type(self):
        return self.info["type"]
    @property
    def mode(self):
        return self.info["mode"]
    @property
    def perm(self):
        return self.bits.st_mode
    