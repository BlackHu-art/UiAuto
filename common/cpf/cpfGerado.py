#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :    16:43
"""
import os
import random
import string
from datetime import datetime

import requests
import re
from common.logger.logTool import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class CPFGenerator:
    def __init__(self, max_threads=5):
        self.url = "https://www.4devs.com.br/ferramentas_online.php"
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,pt-BR;q=0.8,pt;q=0.7,en-US;q=0.6,en;q=0.5",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.4devs.com.br",
            "referer": "https://www.4devs.com.br/gerador_de_cpf",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        self.payload = {
            "acao": "gerar_cpf",
            "pontuacao": "S",
            "cpf_estado": ""
        }
        self.max_threads = max_threads
        self.lock = threading.Lock()  # 文件写入锁

    def generate_cpfs(self, number=1):
        """Generate multiple CPF numbers concurrently and save each to file as it is generated."""
        filename = f"cpf_results_{datetime.now().strftime('%Y%m%d')}.txt"
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self._request_and_save_cpf, filename) for _ in range(number)]
            for future in as_completed(futures):
                result = future.result()  # 获取线程执行结果（可以选择性处理）

    def _request_and_save_cpf(self, filename):
        """Generate a single CPF and save it to the file."""
        cpf = self.generate_single_cpf()
        self.save_line_to_file(cpf, filename)

    def generate_single_cpf(self, index=None):
        """Generate and return a single CPF number if successful, or None if failed."""
        try:
            response = requests.post(self.url, headers=self.headers, data=self.payload)
            if response.status_code == 200:
                # cpf = re.sub(r"\D", "", response.text)  # Remove all non-digit characters
                cpf = response.text
                logger.info(f"Generated CPF {index}: {cpf}" if index else f"Generated CPF: {cpf}")
                return cpf
            else:
                logger.error(f"Error {response.status_code} - Failed to generate CPF {index}")
                return None
        except requests.RequestException as e:
            logger.error(f"Request failed for CPF {index}: {e}")
            return None

    def save_line_to_file(self, data, filename):
        """Thread-safe method to save a single line of data to the specified file."""
        with self.lock:
            try:
                with open(filename, "a") as file:
                    file.write(data + "\n")
                logger.info(f"Data saved to {filename}: {data}")
            except IOError as e:
                logger.error(f"File write error: {e}")

    def generate_random_email(self):
        """Generate a random email with a username of 10 random characters."""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{username}@ipwangxin.cn"

    def generate_document(self, num_entries):
        """Generate a document with specified number of valid entries, using a unique filename."""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"generated_{timestamp}.txt"
        entries = []

        try:
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = {executor.submit(self.generate_single_cpf, i + 1): i + 1 for i in range(num_entries)}
                for future in as_completed(futures):
                    index = futures[future]
                    cpf = future.result()
                    if cpf:  # Only proceed if CPF is valid (not None)
                        email = self.generate_random_email()
                        entry = f"TESTEDOOZY;{cpf};{email};Nome;Sobrenome"
                        entries.append(entry)
                    else:
                        logger.warning(f"Skipped entry {index} due to invalid CPF")

            # 线程任务全部完成后，以写模式创建新文件
            with open(filename, "w") as file:  # 使用 "w" 模式创建新文件
                for entry in entries:
                    file.write(entry + "\n")
            logger.info(f"Generated document saved to {filename} at: {os.path.abspath(filename)}")

        except Exception as e:
            logger.error(f"Error during document generation: {e}")
        finally:
            logger.info("All CPF generation tasks completed.")


# 使用示例
if __name__ == "__main__":
    cpf_generator = CPFGenerator(max_threads=20)
    cpf_generator.generate_document(num_entries=10000)



# # 使用示例
# if __name__ == "__main__":
#     cpf_generator = CPFGenerator(max_threads=5)
#
#     # 获取单个 CPF
#     single_cpf = cpf_generator.generate_single_cpf()
#     print(f"Generated single CPF: {single_cpf}")
#
#     # 批量获取多个 CPF 并保存到文件
#     cpf_generator.generate_cpfs(number=10)