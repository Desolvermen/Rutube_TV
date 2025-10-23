import base64
import requests
import os
from update_playlist import create_playlist

class GitHubUploader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
        
    def get_headers(self):
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_file_sha(self, file_path):
        """Получает SHA существующего файла"""
        try:
            url = f"{self.base_url}/{file_path}"
            response = requests.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return response.json()["sha"]
            return None
        except:
            return None
    
    def upload_file(self, file_path, content, commit_message):
        """Загружает или обновляет файл в репозитории"""
        try:
            # Кодируем содержимое в base64
            content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            url = f"{self.base_url}/{file_path}"
            data = {
                "message": commit_message,
                "content": content_b64,
                "branch": "main"
            }
            
            # Проверяем, существует ли файл
            sha = self.get_file_sha(file_path)
            if sha:
                data["sha"] = sha
            
            response = requests.put(url, headers=self.get_headers(), json=data)
            
            if response.status_code in [200, 201]:
                print(f"Файл {file_path} успешно загружен в GitHub")
                return True
            else:
                print(f"Ошибка загрузки: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Ошибка при загрузке в GitHub: {e}")
            return False

def update_playlist_on_github():
    """Основная функция для обновления плейлиста на GitHub"""
    
    # Получаем токен из переменных окружения
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Ошибка: GITHUB_TOKEN не установлен")
        return False
    
    # Настройки репозитория
    repo_owner = "Desolvermen"  # Замените на ваш username
    repo_name = "Rutube_TV"  # Замените на название репозитория
    
    # Создаем плейлист
    playlist_content, success_count, fail_count = create_playlist()
    if not playlist_content:
        return False
    
    # Загружаем в GitHub
    uploader = GitHubUploader(github_token, repo_owner, repo_name)
    
    commit_message = f"Auto-update playlist: {success_count} channels, {fail_count} failed"
    
    return uploader.upload_file("playlists/Rutube_TV.m3u8", playlist_content, commit_message)

if __name__ == "__main__":
    update_playlist_on_github()