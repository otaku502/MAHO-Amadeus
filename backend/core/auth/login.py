import hashlib
import secrets
import json
import base64
import logging
from pathlib import Path
import sys

# 添加项目根路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from core.util.storage import get_database_connection


class AuthManager:
    """
    用户认证管理器，负责用户注册、登录、token生成和验证
    """
    
    def __init__(self, db_name: str = "data/db/users.db"):
        self.db_name = db_name
        self._init_database()
    
    def _init_database(self):
        """初始化用户数据库表"""
        conn = get_database_connection(self.db_name)
        cursor = conn.cursor()
        # 检查表是否已存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone() is None:
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logging.info(f"用户数据库已初始化: {self.db_name}")
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """对密码进行哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str) -> bool:
        """
        注册新用户
        
        参数:
            username: 用户名
            password: 密码（明文）
        
        返回:
            bool: 注册成功返回True，用户名已存在返回False
        """
        try:
            conn = get_database_connection(self.db_name)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            conn.close()
            logging.info(f"用户 {username} 注册成功")
            return True
        except Exception as e:
            logging.error(f"注册用户失败: {e}")
            return False
    
    def verify_user(self, username: str, password: str) -> bool:
        """
        验证用户名和密码
        
        参数:
            username: 用户名
            password: 密码（明文）
        
        返回:
            bool: 验证成功返回True，否则返回False
        """
        try:
            conn = get_database_connection(self.db_name)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            logging.error(f"验证用户失败: {e}")
            return False
    
    def pack_token(self, username: str) -> str:
        """
        将用户信息打包成token
        
        参数:
            username: 用户名
        
        返回:
            str: Base64编码的token字符串
        """
        # 生成随机salt增强安全性
        salt = secrets.token_hex(16)
        user_info = {
            "username": username,
            "salt": salt
        }
        json_str = json.dumps(user_info)
        token = base64.urlsafe_b64encode(json_str.encode()).decode()
        return token
    
    def verify_token(self, token: str) -> dict:
        """
        验证token并返回用户信息
        
        参数:
            token: Base64编码的token字符串
        
        返回:
            dict: 验证成功返回用户信息字典，失败返回None
        """
        try:
            json_str = base64.urlsafe_b64decode(token.encode()).decode()
            user_info = json.loads(json_str)
            
            # 验证用户是否存在
            username = user_info.get("username")
            if username and self._user_exists(username):
                return user_info
            return None # pyright: ignore[reportReturnType]
        except Exception as e:
            logging.error(f"验证token失败: {e}")
            return None # pyright: ignore[reportReturnType]
    
    def _user_exists(self, username: str) -> bool:
        """检查用户是否存在"""
        try:
            conn = get_database_connection(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            logging.error(f"检查用户是否存在失败: {e}")
            return False
    
    def list_users(self) -> list:
        """列出所有用户"""
        try:
            conn = get_database_connection(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT username, created_at FROM users")
            users = cursor.fetchall()
            conn.close()
            return users
        except Exception as e:
            logging.error(f"列出用户失败: {e}")
            return []


# 命令行工具：用于管理用户
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    auth = AuthManager()
    
    print("=== MAHO 用户管理工具 ===")
    print("1. 注册新用户")
    print("2. 验证用户")
    print("3. 生成token")
    print("4. 验证token")
    print("5. 列出所有用户")
    
    choice = input("请选择操作 (1-5): ")
    
    if choice == "1":
        username = input("用户名: ")
        password = input("密码: ")
        if auth.register_user(username, password):
            print("✓ 注册成功")
        else:
            print("✗ 注册失败（用户名可能已存在）")
    
    elif choice == "2":
        username = input("用户名: ")
        password = input("密码: ")
        if auth.verify_user(username, password):
            print("✓ 验证成功")
        else:
            print("✗ 验证失败")
    
    elif choice == "3":
        username = input("用户名: ")
        token = auth.pack_token(username)
        print(f"Token: {token}")
    
    elif choice == "4":
        token = input("Token: ")
        user_info = auth.verify_token(token)
        if user_info:
            print(f"✓ Token有效，用户: {user_info['username']}")
        else:
            print("✗ Token无效")
    
    elif choice == "5":
        users = auth.list_users()
        print(f"\n共 {len(users)} 个用户:")
        for username, created_at in users:
            print(f"  - {username} (创建于 {created_at})")
