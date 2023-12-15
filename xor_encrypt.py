import hashlib
import base64
from typing import Optional, Tuple

STR_ENCODING = "utf-8"

def encrypt(content: str, key: str) -> Tuple[str, str]:
    key_bytes = key.encode(encoding = STR_ENCODING)
    content_bytes = content.encode(encoding = STR_ENCODING)
    result = b""
    for i in range(len(content_bytes)):
        result += bytes([content_bytes[i] ^ key_bytes[i % len(key_bytes)]])
    result_str = base64.b64encode(result).decode(encoding = STR_ENCODING)
    md5 = hashlib.md5()
    md5.update(content_bytes)
    result_md5 = md5.hexdigest()
    return (result_str, result_md5)

def decrypt(content: str, key: str, md5_str: str) -> Optional[str]:
    content_bytes = None
    try:
        content_bytes = base64.b64decode(content)
    except:
        pass
    if content_bytes == None:
        return None
    key_bytes = key.encode(encoding = STR_ENCODING)
    result = b""
    for i in range(len(content_bytes)):
        result += bytes([content_bytes[i] ^ key_bytes[i % len(key_bytes)]])
    md5 = hashlib.md5()
    md5.update(result)
    if md5.hexdigest() != md5_str:
        return None
    return result.decode(encoding = STR_ENCODING)
    
