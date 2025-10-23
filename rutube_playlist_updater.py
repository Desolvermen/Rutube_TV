import requests
import os
import base64
import time
from datetime import datetime

# Укажите список URL API и названий каналов
api_data = [
    ("https://rutube.ru/api/play/options/c58f502c7bb34a8fcdd976b221fca292/", "Первый канал HD"),
    ("https://rutube.ru/api/play/options/c37cd74192c6bc3d6cd6077c0c4fd686/", "НТВ HD"),
    ("https://rutube.ru/api/play/options/546602986e6a424d74d594876ddb3f04/", "ТНТ HD"),
    ("https://rutube.ru/api/play/options/c801a7087e29a097192d74c270fbc6c1/", "ТНТ-4 HD"),
    ("https://rutube.ru/api/play/options/7bf12d9c050f9a7ef3728db5730432ae/", "ТВ-3 HD"),
    ("https://rutube.ru/api/play/options/9f87a9a0cecbe773be6fddcbd93585ac/", "Пятница! HD"),
    ("https://rutube.ru/api/play/options/310744c10a5809da38aa445c952976da/", "Суббота! HD"),
    ("https://rutube.ru/api/play/options/9ae8e8a6dc58bdad66190475f9872ecd/", "Rutube TV HD"),
    ("https://rutube.ru/api/play/options/c9b87c0b00cfff9b37f95b9c8e4eed42/", "Соловьёв Live HD"),
    ("https://rutube.ru/api/play/options/11bbbec75a2ceb8cf446ad16813c6eec/", "Матч! ТВ HD"),
    ("https://rutube.ru/api/play/options/df6fe73494a26f74da51573fd97b9baa/", "Муз-ТВ HD"),
    ("https://rutube.ru/api/play/options/5c9327074e25ca86f3111d4085cbbb65/", "Ю-ТВ HD"),
    ("https://rutube.ru/api/play/options/faa934385b83f9e8a92f5484defae5fa/", "ОТР HD"),
    ("https://rutube.ru/api/play/options/5ab908fccfac5bb43ef2b1e4182256b0/", "Звезда HD"),
    ("https://rutube.ru/api/play/options/afef67d151b5a607dee1ef0aa299a52c/", "Мир HD"),
    ("https://rutube.ru/api/play/options/43269ba8fb179e298b1e497f557e8d2d/", "Мир 24 HD"),
    ("https://rutube.ru/api/play/options/88f6485ee28d56daf13302ac6fe3d931/", "РБК HD"),
    ("https://rutube.ru/api/play/options/1f550a23c44ec7f287324b0b3e4f5a29/", "ОСН HD"),
    ("https://rutube.ru/api/play/options/07beff61e617797db550cc3a5f6ad92b/", "Телеканал 360° HD"),
    ("https://rutube.ru/api/play/options/d14fcf59cb7d07a26c48ebc8c6565f44/", "360° Новости HD"),
    ("https://rutube.ru/api/play/options/f6a6d5c955180d0d0f80c66d0b6150d3/", "Вместе-РФ HD"),
    ("https://rutube.ru/api/play/options/91815da4edb167b5bd617bae490e57da/", "Царьград HD"),
    ("https://rutube.ru/api/play/options/80b308e455f2aceb498e5dccd58ca050/", "Союз HD"),
    ("https://rutube.ru/api/play/options/392b4686b770bae2da6bf5ac4574add5/", "2х2 HD"),
    ("https://rutube.ru/api/play/options/2f052691c75d72b3ed7f3c33ea956a41/", "Смайл ТВ HD"),
    ("https://rutube.ru/api/play/options/2b06a5c4c688fdc05014acb4cba83de0/", "Moonbug Kids TV HD (eng)"),
    ("https://rutube.ru/api/play/options/0e9e44725d5d5ab7ee92c10b40215419/", "Mr.Bean Cartoon HD (eng)"),
    ("https://rutube.ru/api/play/options/1da5d92af8c55b16241f1eb12a27f00c/", "Охотник и рыболов Int HD"),
    ("https://rutube.ru/api/play/options/406973c72e9d0449feef05ef7811ad01/", "Загородный Int HD"),
    ("https://rutube.ru/api/play/options/5a294ae1ed12c44c7053301fb5fa9ba0/", "ТНТ Music HD"),
    ("https://rutube.ru/api/play/options/b1eb8e90d7e636677b3eb73b4fcbb717/", "RU.TV HD"),
    ("https://rutube.ru/api/play/options/f712ae5ff3db23ec09b3674133d44daa/", "VIVA Russia HD"),
    ("https://rutube.ru/api/play/options/965a025e4ebbaf0957415f80c6de8534/", "Музыка Мода ТВ HD"),
    ("https://rutube.ru/api/play/options/bc1b811349f526188c839d377913e16a/", "Kronehit TV HD"),
    ("https://rutube.ru/api/play/options/ee6a3d5ba98066c2aaace3c428a3170c/", "World Fashion Channel HD"),
    ("https://rutube.ru/api/play/options/47fdffd6ab82bbab0a19039d7018839f/", "Deluxe Dance HD"),
    ("https://rutube.ru/api/play/options/047ba54d846ee185b4209a797a2ae138/", "NOW:Rock HD"),
    ("https://rutube.ru/api/play/options/09e51eefa939595a4ac67182c6fb3e4e/", "Кино и Жизнь HD"),
    ("https://rutube.ru/api/play/options/3b7d1499da9396462bfd17282d758d30/", "Кинолаффка HD"),
    ("https://rutube.ru/api/play/options/4965b7b928c4a143d708ab424be01d37/", "Киножелезо HD"),
    ("https://rutube.ru/api/play/options/dcc02ed1ff97923541c6d4c030c54c65/", "Comedy Hub HD"),
    ("https://rutube.ru/api/play/options/99d4597cea881a27cf7dd6e65a74dade/", "Плюс Минус 16 HD")
]

def get_stream_url_advanced(api_url, channel_name):
    """Продвинутый метод получения URL потока"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
        'Origin': 'https://rutube.ru',
        'Referer': 'https://rutube.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    try:
        print(f"🔍 Получение потока для: {channel_name}")
        
        # Метод 1: Прямой запрос к API
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"  ❌ HTTP {response.status_code} для {channel_name}")
            return None
            
        data = response.json()
        
        # Поиск в разных структурах ответа
        stream_url = None
        
        # Метод 2: Поиск в live_streams -> hls
        if not stream_url:
            hls_streams = data.get('live_streams', {}).get('hls', [])
            for stream in hls_streams:
                url = stream.get('url')
                if url and 'm3u8' in url:
                    stream_url = url
                    print(f"  ✅ Найден через live_streams.hls")
                    break
        
        # Метод 3: Поиск в video_meta
        if not stream_url:
            video_meta = data.get('video_meta', {})
            url = video_meta.get('url')
            if url and 'm3u8' in url:
                stream_url = url
                print(f"  ✅ Найден через video_meta")
        
        # Метод 4: Поиск в других возможных полях
        if not stream_url:
            # Пробуем разные пути в JSON
            possible_paths = [
                ['video', 'url'],
                ['streams', 0, 'url'],
                ['hls_url'],
                ['m3u8_url'],
                ['playlist', 'url']
            ]
            
            for path in possible_paths:
                try:
                    current = data
                    for key in path:
                        if isinstance(key, int) and isinstance(current, list) and len(current) > key:
                            current = current[key]
                        elif isinstance(current, dict) and key in current:
                            current = current[key]
                        else:
                            break
                    else:
                        if current and 'm3u8' in str(current):
                            stream_url = current
                            print(f"  ✅ Найден через путь {path}")
                            break
                except:
                    continue
        
        # Метод 5: Если есть ID, пробуем альтернативный API
        if not stream_url and '/' in api_url:
            try:
                video_id = api_url.split('/')[-2] if api_url.endswith('/') else api_url.split('/')[-1]
                alt_url = f"https://rutube.ru/api/playlist/options/{video_id}/"
                alt_response = requests.get(alt_url, headers=headers, timeout=5)
                if alt_response.status_code == 200:
                    alt_data = alt_response.json()
                    # Поиск в альтернативном ответе
                    for item in alt_data.get('results', []):
                        for stream in item.get('live_streams', {}).get('hls', []):
                            url = stream.get('url')
                            if url and 'm3u8' in url:
                                stream_url = url
                                print(f"  ✅ Найден через альтернативный API")
                                break
                        if stream_url:
                            break
            except:
                pass
        
        if stream_url:
            # Очистка URL от лишних параметров если нужно
            if '?' in stream_url:
                base_url = stream_url.split('?')[0]
                if base_url.endswith('.m3u8'):
                    stream_url = base_url
            
            print(f"  📺 URL: {stream_url[:80]}..." if len(stream_url) > 80 else f"  📺 URL: {stream_url}")
            return stream_url
        else:
            print(f"  ❌ Поток не найден в ответе API")
            # Выводим отладочную информацию
            print(f"  🔍 Ключи в ответе: {list(data.keys()) if isinstance(data, dict) else 'Не dict'}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"  ⏰ Таймаут при запросе")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Ошибка сети: {e}")
        return None
    except Exception as e:
        print(f"  💥 Неожиданная ошибка: {e}")
        return None

def create_playlist():
    """Создает плейлист и возвращает его содержимое"""
    try:
        playlist_content = ["#EXTM3U"]
        playlist_content.append(f"#EXTM3U url-tvg=\"https://i.mjh.nz/ru/tvg.xml\"")
        playlist_content.append(f"#PLAYLIST: Rutube TV Channels")
        playlist_content.append(f"#Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        playlist_content.append("")
        
        successful_channels = 0
        failed_channels = []

        print("🎬 Начинаем сбор плейлиста...")
        print("=" * 50)

        # Обработка каждого URL API с задержкой
        for i, (api_url, channel_name) in enumerate(api_data):
            print(f"\n📡 Канал {i+1}/{len(api_data)}: {channel_name}")
            
            stream_url = get_stream_url_advanced(api_url, channel_name)
            
            if stream_url:
                # Добавляем канал в плейлист
                playlist_content.append(f"#EXTINF:-1 tvg-id=\"{channel_name}\" tvg-name=\"{channel_name}\" group-title=\"Rutube\",{channel_name}")
                playlist_content.append(stream_url)
                successful_channels += 1
                print(f"  ✅ Добавлен в плейлист")
            else:
                failed_channels.append(channel_name)
                print(f"  ❌ Не добавлен")
            
            # Задержка между запросами
            if i < len(api_data) - 1:
                time.sleep(0.5)

        print("\n" + "=" * 50)
        print(f"📊 ИТОГ: Успешно {successful_channels}/{len(api_data)}")
        
        # Добавляем информацию о статусе в конец плейлиста
        playlist_content.append("")
        playlist_content.append("# Статистика:")
        playlist_content.append(f"# Всего каналов: {len(api_data)}")
        playlist_content.append(f"# Успешно: {successful_channels}")
        playlist_content.append(f"# Не найдено: {len(failed_channels)}")
        
        if failed_channels:
            playlist_content.append("# Не удалось получить:")
            for failed in failed_channels:
                playlist_content.append(f"# - {failed}")
        
        return "\n".join(playlist_content), successful_channels, len(failed_channels)
        
    except Exception as e:
        print(f"💥 Критическая ошибка при создании плейлиста: {e}")
        return None, 0, len(api_data)

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
                print(f"✅ Файл {file_path} успешно загружен в GitHub")
                return True
            else:
                print(f"❌ Ошибка загрузки: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при загрузке в GitHub: {e}")
            return False

def update_playlist_on_github():
    """Основная функция для обновления плейлиста на GitHub"""
    
    # Получаем токен из переменных окружения
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ Ошибка: GITHUB_TOKEN не установлен")
        return False
    
    # Настройки репозитория
    repo_owner = "Desolvermen"  # Замените на ваш username
    repo_name = "Rutube_TV"   # Замените на название репозитория
    
    # Создаем плейлист
    print("🔄 Создание плейлиста...")
    playlist_content, success_count, fail_count = create_playlist()
    
    if not playlist_content:
        print("❌ Не удалось создать плейлист")
        return False
    
    # Загружаем в GitHub
    print("🔄 Загрузка в GitHub...")
    uploader = GitHubUploader(github_token, repo_owner, repo_name)
    
    commit_message = f"Auto-update: {success_count} channels, {fail_count} failed - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    success = uploader.upload_file("Rutube_TV.m3u8", playlist_content, commit_message)
    
    if success:
        print(f"🎉 Плейлист успешно обновлен! {success_count} каналов")
    else:
        print("💥 Ошибка при загрузке плейлиста")
        
    return success

def create_local_playlist():
    """Создает плейлист локально (для тестирования)"""
    playlist_content, success_count, fail_count = create_playlist()
    
    if playlist_content:
        try:
            with open('Rutube_TV.m3u8', 'w', encoding='utf-8') as f:
                f.write(playlist_content)
            print(f"✅ Локальный плейлист создан: {success_count} успешно, {fail_count} с ошибками")
            print("📁 Файл: Rutube_TV.m3u8")
            return True
        except Exception as e:
            print(f"❌ Ошибка при сохранении файла: {e}")
            return False
    return False

if __name__ == "__main__":
    print("🚀 Запуск Rutube Playlist Updater")
    print("=" * 40)
    
    # Если запускается в GitHub Actions, используем GitHub загрузку
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print("🌐 Режим: GitHub Actions")
        success = update_playlist_on_github()
        exit(0 if success else 1)
    else:
        # Локальный запуск
        print("💻 Режим: Локальный")
        success = create_local_playlist()
        if success:
            print("✅ Скрипт завершен успешно")
        else:
            print("❌ Скрипт завершен с ошибками")
