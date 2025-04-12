# dotenv 테스트를 위한 코드
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('PORTAL_ID'))
print(os.getenv('PORTAL_PASSWORD'))
