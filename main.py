import requests
import json
import os
import sys
import uuid
import time
import google.generativeai as genai
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax

# --- PENAMBAHAN: Import DeepSeek ---
try:
    from deepseek import DeepSeekAPI
except ImportError:
    console = Console()
    console.print("--> ⚠️  [yellow]DeepSeek library tidak ditemukan. Install dengan: pip install deepseek[/yellow]")
    DeepSeekAPI = None

console = Console()

# --- PENAMBAHAN: Konfigurasi Proxy ---
def load_proxy_config(filename="proxy.txt"):
    """Memuat konfigurasi proxy dari file proxy.txt"""
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            proxy_line = f.read().strip()
            if not proxy_line:
                return None
            
            # Format yang didukung:
            # 1. http://username:password@host:port
            # 2. http://host:port
            # 3. socks5://username:password@host:port
            # 4. socks5://host:port
            
            if proxy_line.startswith(('http://', 'https://', 'socks5://')):
                return {
                    'http': proxy_line,
                    'https': proxy_line
                }
            else:
                # Jika hanya host:port, tambahkan http://
                return {
                    'http': f'http://{proxy_line}',
                    'https': f'http://{proxy_line}'
                }
    except Exception as e:
        console.print(f"--> ⚠️  [yellow]Error membaca proxy.txt: {e}[/yellow]")
        return None

def get_proxy_choice():
    """Mendapatkan pilihan proxy dari user"""
    menu_text = Text("\n1. Tidak menggunakan proxy\n2. Gunakan proxy dari proxy.txt\n3. Masukkan proxy manual\n", justify="left")
    menu_panel = Panel(menu_text, title="[bold cyan]PILIH KONFIGURASI PROXY[/bold cyan]", border_style="magenta", padding=(1, 2))
    console.print(menu_panel)
    choice = Prompt.ask("[bold]Masukkan pilihan Anda[/bold]", choices=['1', '2', '3'], default='1')
    return choice

def get_manual_proxy():
    """Mendapatkan proxy dari input manual user"""
    console.print("\n[bold cyan]Format proxy yang didukung:[/bold cyan]")
    console.print("• http://username:password@host:port")
    console.print("• http://host:port")
    console.print("• socks5://username:password@host:port")
    console.print("• socks5://host:port")
    console.print("• host:port (akan otomatis ditambahkan http://)")
    
    proxy_input = Prompt.ask("\n[bold]Masukkan proxy[/bold] (kosongkan untuk tidak menggunakan)")
    if not proxy_input.strip():
        return None
    
    proxy_input = proxy_input.strip()
    if proxy_input.startswith(('http://', 'https://', 'socks5://')):
        return {
            'http': proxy_input,
            'https': proxy_input
        }
    else:
        return {
            'http': f'http://{proxy_input}',
            'https': f'http://{proxy_input}'
        }

# --- PENAMBAHAN: Multiple Accounts/Cookies Support ---
def load_multiple_cookies_from_file(filename="cookies.txt"):
    """Memuat multiple cookies dari file cookies.txt dengan dukungan proxy, user_id, dan device profile per account"""
    accounts_list = []
    
    if not os.path.exists(filename):
        console.print(f"--> ❌ [bold red]Error: File '{filename}' tidak ditemukan.[/bold red]")
        return accounts_list
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            current_cookies = {}
            current_proxy = None
            current_user_id = "37cf0952-9403-4d29-bf7a-1d1c08368a4a"  # Default user_id
            current_device_profile = None  # Default device profile
            
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip baris kosong dan komentar
                if not line or line.startswith('#'):
                    continue
                
                # Jika baris dimulai dengan "---", itu adalah pemisah antar account
                if line.startswith('---'):
                    if current_cookies:
                        # Jika device profile tidak diatur, gunakan random
                        if current_device_profile is None:
                            current_device_profile = get_random_device_profile()
                        
                        accounts_list.append({
                            'cookies': current_cookies.copy(),
                            'proxy': current_proxy,
                            'user_id': current_user_id,
                            'device_profile': current_device_profile
                        })
                        current_cookies = {}
                        current_proxy = None
                        current_user_id = "37cf0952-9403-4d29-bf7a-1d1c08368a4a"  # Reset ke default
                        current_device_profile = None  # Reset device profile
                    continue
                
                # Parse proxy jika baris dimulai dengan "PROXY:"
                if line.startswith('PROXY:'):
                    proxy_line = line[6:].strip()
                    if proxy_line:
                        if proxy_line.startswith(('http://', 'https://', 'socks5://')):
                            current_proxy = {
                                'http': proxy_line,
                                'https': proxy_line
                            }
                        else:
                            current_proxy = {
                                'http': f'http://{proxy_line}',
                                'https': f'http://{proxy_line}'
                            }
                    continue
                
                # Parse user_id jika baris dimulai dengan "USER_ID:"
                if line.startswith('USER_ID:'):
                    user_id_line = line[8:].strip()
                    if user_id_line:
                        current_user_id = user_id_line
                    continue
                
                # Parse device profile jika baris dimulai dengan "DEVICE_PROFILE:"
                if line.startswith('DEVICE_PROFILE:'):
                    device_profile_name = line[15:].strip()
                    if device_profile_name:
                        profile = get_device_profile_by_name(device_profile_name)
                        if profile:
                            current_device_profile = profile
                            console.print(f"   [dim]Device profile untuk account: {profile['name']}[/dim]")
                        else:
                            console.print(f"   [yellow]⚠️  Device profile '{device_profile_name}' tidak ditemukan. Menggunakan random.[/yellow]")
                    continue
                
                # Parse cookie name=value
                try:
                    if '=' in line:
                        name, value = line.split('=', 1)
                        current_cookies[name.strip()] = value.strip()
                    else:
                        console.print(f"--> ⚠️  [yellow]Peringatan: Format tidak valid di baris {line_num}: {line}[/yellow]")
                except ValueError:
                    console.print(f"--> ⚠️  [yellow]Peringatan: Format tidak valid di baris {line_num}: {line}[/yellow]")
            
            # Tambahkan account terakhir jika ada
            if current_cookies:
                # Jika device profile tidak diatur, gunakan random
                if current_device_profile is None:
                    current_device_profile = get_random_device_profile()
                
                accounts_list.append({
                    'cookies': current_cookies,
                    'proxy': current_proxy,
                    'user_id': current_user_id,
                    'device_profile': current_device_profile
                })
        
        console.print(f"✅ [green]Berhasil memuat {len(accounts_list)} account dari {filename}[/green]")
        return accounts_list
        
    except Exception as e:
        console.print(f"--> ❌ [bold red]Error membaca {filename}: {e}[/bold red]")
        return accounts_list

def load_single_cookie_from_file(filename="cookie.txt"):
    """Memuat single cookie dari file cookie.txt (backward compatibility)"""
    cookies = {}
    if not os.path.exists(filename):
        console.print(f"--> ❌ [bold red]Error: File '{filename}' tidak ditemukan.[/bold red]")
        return cookies
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            try: 
                name, value = line.split('=', 1)
                cookies[name] = value
            except ValueError: 
                console.print(f"--> ⚠️  [yellow]Peringatan: Melewatkan baris di {filename}:[/yellow] {line}")
    return cookies

def get_cookie_choice():
    """Mendapatkan pilihan cookie dari user"""
    menu_text = Text("\n1. Gunakan single cookie (cookie.txt)\n2. Gunakan multiple cookies (cookies.txt)\n", justify="left")
    menu_panel = Panel(menu_text, title="[bold cyan]PILIH KONFIGURASI COOKIE[/bold cyan]", border_style="magenta", padding=(1, 2))
    console.print(menu_panel)
    choice = Prompt.ask("[bold]Masukkan pilihan Anda[/bold]", choices=['1', '2'], default='1')
    return choice

def get_proxy_mode():
    """Mendapatkan mode proxy dari user"""
    menu_text = Text("\n1. Tidak menggunakan proxy\n2. Gunakan 1 proxy untuk semua account\n3. Gunakan proxy individual per account (dari cookies.txt)\n4. Masukkan proxy manual untuk semua account\n", justify="left")
    menu_panel = Panel(menu_text, title="[bold cyan]PILIH MODE PROXY[/bold cyan]", border_style="magenta", padding=(1, 2))
    console.print(menu_panel)
    choice = Prompt.ask("[bold]Masukkan pilihan Anda[/bold]", choices=['1', '2', '3', '4'], default='1')
    return choice

# --- PENAMBAHAN KEMBALI: Daftar Profil Device ---
DEVICE_PROFILES = [
    {
        "name": "Windows Chrome",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="125", "Not.A/Brand";v="24", "Chromium";v="125"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    },
    {
        "name": "macOS Chrome",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="125", "Not.A/Brand";v="24", "Chromium";v="125"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    },
    {
        "name": "Android Chrome",
        "user-agent": "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
    },
    {
        "name": "Windows Firefox",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    },
    {
        "name": "macOS Safari",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    },
    {
        "name": "iOS Safari",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"iOS"',
    },
    {
        "name": "Linux Firefox",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
    },
    {
        "name": "Windows Edge",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "sec-ch-ua": '"Microsoft Edge";v="125", "Not.A/Brand";v="24", "Chromium";v="125"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    },
]

def get_device_profile_by_name(profile_name):
    """Mendapatkan device profile berdasarkan nama."""
    for profile in DEVICE_PROFILES:
        if profile["name"].lower() == profile_name.lower():
            return profile
    return None

def get_random_device_profile():
    """Memilih satu profil device secara acak dari daftar."""
    return random.choice(DEVICE_PROFILES)

def get_device_profile_choice():
    """Mendapatkan pilihan device profile dari user."""
    menu_text = Text("\n1. Random device profile per loop\n2. Assign device profile per account (dari cookies.txt)\n", justify="left")
    menu_panel = Panel(menu_text, title="[bold cyan]PILIH MODE DEVICE PROFILE[/bold cyan]", border_style="magenta", padding=(1, 2))
    console.print(menu_panel)
    choice = Prompt.ask("[bold]Masukkan pilihan Anda[/bold]", choices=['1', '2'], default='1')
    return choice

def show_available_device_profiles():
    """Menampilkan daftar device profile yang tersedia."""
    console.print("\n[bold cyan]Device Profile yang Tersedia:[/bold cyan]")
    for i, profile in enumerate(DEVICE_PROFILES, 1):
        console.print(f"{i}. {profile['name']} - {profile['user-agent'][:50]}...")
    console.print()

# --- Fungsi-fungsi pembantu lainnya ---

def get_user_choice():
    menu_text = Text("\n1. Acak pesan per baris dari `pesan.txt`\n2. Hasilkan pesan baru dengan Gemini AI\n3. Hasilkan pesan baru dengan DeepSeek\n", justify="left")
    menu_panel = Panel(menu_text, title="[bold cyan]PILIH SUMBER PESAN[/bold cyan]", border_style="magenta", padding=(1, 2))
    console.print(menu_panel)
    choice = Prompt.ask("[bold]Masukkan pilihan Anda[/bold]", choices=['1', '2', '3'], default='2')
    return choice

def load_api_key(filename="apikey.txt"):
    if not os.path.exists(filename): return None
    with open(filename, 'r', encoding='utf-8') as f: return f.read().strip()

def load_deepseek_api_key(filename="deepseek_apikey.txt"):
    """Memuat API key DeepSeek dari file deepseek_apikey.txt"""
    if not os.path.exists(filename): return None
    with open(filename, 'r', encoding='utf-8') as f: return f.read().strip()

def generate_message_with_ai(api_key, ai_provider="gemini"):
    """Menghasilkan pesan menggunakan AI provider yang dipilih"""
    if ai_provider == "gemini":
        return generate_message_with_gemini(api_key)
    elif ai_provider == "deepseek":
        return generate_message_with_deepseek(api_key)
    else:
        console.print(f"--> ❌ [bold red]AI provider '{ai_provider}' tidak didukung.[/bold red]")
        return "Make any question from the discussion on crypto."

def generate_message_with_gemini(api_key):
    console.print("--> 🤖 Menghasilkan pesan baru dengan Gemini AI...", style="cyan")
    if not api_key:
        console.print("--> ⚠️  [yellow]Peringatan: `apikey.txt` tidak ditemukan. Menggunakan pesan fallback.[/yellow]")
        return "Tolong jelaskan apa itu black hole."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Menambahkan randomization untuk menghindari cache
        import random
        import time
        
        # Random seed berdasarkan waktu
        random.seed(time.time())
        
        # Topik yang bisa dipilih secara random
        topics = ["politik", "crypto", "teknologi", "sains", "ekonomi", "sosial", "lingkungan", "pendidikan", "kesehatan", "keamanan"]
        selected_topic = random.choice(topics)
        
        # Kata kunci random untuk variasi
        keywords = ["dampak", "tantangan", "risiko", "solusi", "strategi", "perubahan", "inovasi", "krisis", "peluang", "ancaman"]
        selected_keyword = random.choice(keywords)
        
        # Panjang random untuk variasi
        min_length = random.randint(50, 80)
        max_length = random.randint(250, 350)
        
        # Timestamp untuk menghindari cache
        timestamp = int(time.time())
        
        prompt = f"""Buatkan 1 pertanyaan atau perintah dalam bahasa Indonesia dengan panjang {min_length}-{max_length} huruf. 
Fokus pada topik: {selected_topic}. 
Gunakan kata kunci: {selected_keyword}.
Pertanyaan harus sulit dijawab dan memerlukan analisis mendalam.
Berikan hasilnya langsung berupa pertanyaan/perintah saja, tanpa penjelasan tambahan.
Timestamp: {timestamp}"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "quota" in error_message.lower():
            console.print("--> ⚠️  [yellow]Rate limit Gemini API terdeteksi. Menunggu 1 menit...[/yellow]")
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%")) as progress:
                task = progress.add_task("[yellow]Menunggu rate limit...", total=60)
                for _ in range(60):
                    time.sleep(1)
                    progress.update(task, advance=1)
            console.print("--> 🔄 [green]Mencoba lagi setelah jeda...[/green]")
            try:
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as retry_error:
                console.print(f"--> ❌ [bold red]Error setelah retry:[/bold red] {retry_error}")
                console.print("--> Menggunakan pesan fallback.", style="yellow")
                return "Make any question from the discussion on crypto."
        else:
            console.print(f"--> ❌ [bold red]Error saat menghubungi Gemini AI:[/bold red] {e}")
            console.print("--> Menggunakan pesan fallback.", style="yellow")
            # Mempertahankan fallback baru Anda
            return "Make any question from the discussion on crypto."

def generate_message_with_deepseek(api_key):
    """Menghasilkan pesan menggunakan DeepSeek AI"""
    console.print("--> 🧠 Menghasilkan pesan baru dengan DeepSeek AI...", style="cyan")
    if not api_key:
        console.print("--> ⚠️  [yellow]Peringatan: `deepseek_apikey.txt` tidak ditemukan. Menggunakan pesan fallback.[/yellow]")
        return "Tolong jelaskan apa itu black hole."
    
    if DeepSeekAPI is None:
        console.print("--> ❌ [bold red]DeepSeek library tidak tersedia. Install dengan: pip install deepseek[/bold red]")
        return "Make any question from the discussion on crypto."
    
    try:
        client = DeepSeekAPI(api_key=api_key)
        
        # Menambahkan randomization untuk menghindari cache
        import random
        import time
        
        # Random seed berdasarkan waktu
        random.seed(time.time())
        
        # Topik yang bisa dipilih secara random
        topics = ["politik", "crypto", "teknologi", "sains", "ekonomi", "sosial", "lingkungan", "pendidikan", "kesehatan", "keamanan"]
        selected_topic = random.choice(topics)
        
        # Kata kunci random untuk variasi
        keywords = ["dampak", "tantangan", "risiko", "solusi", "strategi", "perubahan", "inovasi", "krisis", "peluang", "ancaman"]
        selected_keyword = random.choice(keywords)
        
        # Panjang random untuk variasi
        min_length = random.randint(50, 80)
        max_length = random.randint(250, 350)
        
        # Timestamp untuk menghindari cache
        timestamp = int(time.time())
        
        prompt = f"""Buatkan 1 pertanyaan atau perintah dalam bahasa Indonesia dengan panjang {min_length}-{max_length} huruf. 
Fokus pada topik: {selected_topic}. 
Gunakan kata kunci: {selected_keyword}.
Pertanyaan harus sulit dijawab dan memerlukan analisis mendalam.
Berikan hasilnya langsung berupa pertanyaan/perintah saja, tanpa penjelasan tambahan.
Timestamp: {timestamp}"""
        
        response = client.chat_completion(
            prompt=prompt,
            model="deepseek-chat",
            stream=False
        )
        
        # DeepSeek API mengembalikan string langsung, bukan object dengan choices
        return response.strip()
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and ("rate" in error_message.lower() or "quota" in error_message.lower()):
            console.print("--> ⚠️  [yellow]Rate limit DeepSeek API terdeteksi. Menunggu 1 menit...[/yellow]")
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%")) as progress:
                task = progress.add_task("[yellow]Menunggu rate limit...", total=60)
                for _ in range(60):
                    time.sleep(1)
                    progress.update(task, advance=1)
            console.print("--> 🔄 [green]Mencoba lagi setelah jeda...[/green]")
            try:
                # Menambahkan randomization untuk retry juga
                random.seed(time.time() + 1)  # Seed berbeda untuk retry
                selected_topic = random.choice(topics)
                selected_keyword = random.choice(keywords)
                min_length = random.randint(50, 80)
                max_length = random.randint(250, 350)
                timestamp = int(time.time())
                
                retry_prompt = f"""Buatkan 1 pertanyaan atau perintah dalam bahasa Indonesia dengan panjang {min_length}-{max_length} huruf. 
Fokus pada topik: {selected_topic}. 
Gunakan kata kunci: {selected_keyword}.
Pertanyaan harus sulit dijawab dan memerlukan analisis mendalam.
Berikan hasilnya langsung berupa pertanyaan/perintah saja, tanpa penjelasan tambahan.
Timestamp: {timestamp}"""
                
                response = client.chat_completion(
                    prompt=retry_prompt,
                    model="deepseek-chat",
                    stream=False
                )
                return response.strip()
            except Exception as retry_error:
                console.print(f"--> ❌ [bold red]Error setelah retry:[/bold red] {retry_error}")
                console.print("--> Menggunakan pesan fallback.", style="yellow")
                return "Make any question from the discussion on crypto."
        else:
            console.print(f"--> ❌ [bold red]Error saat menghubungi DeepSeek AI:[/bold red] {e}")
            console.print("--> Menggunakan pesan fallback.", style="yellow")
            return "Make any question from the discussion on crypto."

# --- PERUBAHAN: Fungsi utama sekarang menerima profil device, proxy, cookies, dan user_id ---
def run_single_bot_process(message_to_send: str, device_profile: dict, proxy_config: dict = None, cookies: dict = None, account_id: int = 1, user_id: str = "37cf0952-9403-4d29-bf7a-1d1c08368a4a"):
    """Menjalankan satu siklus lengkap proses bot dengan pesan, profil device, proxy, cookies, dan user_id yang sudah ditentukan."""
    console.print(f"▶️  [bold]Pesan yang akan dikirim:[/bold] [italic]'{message_to_send[:80]}...'[/italic]")
    
    # --- PERUBAHAN: Menggabungkan header dasar dengan profil device yang dipilih ---
    base_headers = {
        'accept': '*/*', 'accept-language': 'en-US,en;q=0.9,id;q=0.8', 'origin': 'https://yupp.ai', 'priority': 'u=1, i',
        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
        **device_profile # Ini akan menambahkan user-agent, sec-ch-ua, dll.
    }
    
    session = requests.Session()
    session.headers.update(base_headers)
    
    # --- PENAMBAHAN: Gunakan cookies yang diberikan ---
    if cookies:
        session.cookies.update(cookies)
        console.print(f"🍪 [dim]Menggunakan Account #{account_id}[/dim]")
    else:
        console.print("❌ [bold red]Error: Tidak ada cookies yang diberikan![/bold red]")
        return
    
    # --- PENAMBAHAN: Konfigurasi proxy ---
    if proxy_config:
        session.proxies.update(proxy_config)
        proxy_display = proxy_config.get('http', 'N/A')
        if len(proxy_display) > 50:
            proxy_display = proxy_display[:47] + "..."
        console.print(f"🌐 [dim]Menggunakan proxy:[/] [italic dim]{proxy_display}[/italic dim]")
    
    chat_id = str(uuid.uuid4())
    turn_id = str(uuid.uuid4())
    
    console.print(Panel(f"[bold]Chat ID:[/] [green]{chat_id}[/]\n[bold]Turn ID:[/] [green]{turn_id}[/]\n[bold]Account:[/] [blue]#{account_id}[/blue]\n[bold]User ID:[/] [cyan]{user_id[:8]}...[/cyan]", title="Sesi Baru Dimulai", style="green"))

    console.print("\n[bold]1-3.[/bold] ⚙️  [cyan]Menjalankan Inisiasi & Mengirim Pesan...[/cyan]")
    
    try:
        session.post('https://yupp.ai/api/authentication/session', json={"userId": user_id})
        session.post('https://yupp.ai/api/trpc/logging.logEvent?batch=1', json={"0":{"json":{"event":"start_chat","params":{"Chat_ID":chat_id,"Turn_ID":turn_id}}}})
    except requests.exceptions.ProxyError:
        console.print("   [bold red]❌ Error proxy: Tidak dapat terhubung melalui proxy yang diberikan.[/bold red]")
        return
    except requests.exceptions.RequestException as e:
        console.print(f"   [bold red]❌ Error koneksi: {e}[/bold red]")
        return
    
    extracted_reward_id = None
    chat_stream_headers = {**session.headers, 'content-type': 'text/plain;charset=UTF-8', 'next-action': '7f48888536e2f0c0163640837db291777c39cc40c3'}
    data_list = [chat_id, turn_id, message_to_send, "$undefined", "$undefined", [], "$undefined", [], "none", False]
    chat_stream_data = json.dumps(data_list)
    
    try:
        response_stream = session.post(f'https://yupp.ai/chat/{chat_id}?stream=true', headers=chat_stream_headers, data=chat_stream_data.encode('utf-8'), stream=True)
    except requests.exceptions.ProxyError:
        console.print("   [bold red]❌ Error proxy: Tidak dapat terhubung ke streaming melalui proxy.[/bold red]")
        return
    except requests.exceptions.RequestException as e:
        console.print(f"   [bold red]❌ Error koneksi streaming: {e}[/bold red]")
        return
    
    if response_stream.status_code == 200:
        console.print("   [green]📡 Koneksi streaming berhasil. Mendengarkan respons...[/green]")
        try:
            for line in response_stream.iter_lines():
                if line and line.decode('utf-8').startswith('a:'):
                    json_string = line.decode('utf-8')[2:]
                    try:
                        data = json.loads(json_string)
                        if 'unclaimedRewardInfo' in data and data['unclaimedRewardInfo'] and 'rewardId' in data['unclaimedRewardInfo']:
                            extracted_reward_id = data['unclaimedRewardInfo']['rewardId']
                            console.print(f"   [bold green]✅ Reward ID DITEMUKAN:[/bold green] [yellow]{extracted_reward_id}[/yellow]")
                            break 
                    except json.JSONDecodeError: pass
        except requests.exceptions.ChunkedEncodingError as e:
            console.print(f"[bold red]❌ Streaming error: {e}[/bold red]")
            return
    
    if not extracted_reward_id:
        console.print("\n--> ❌ [bold red]Peringatan: Streaming selesai tetapi tidak ada Reward ID yang ditemukan.[/bold red]")
        return
    
    console.print("[bold]4.[/bold]   ✍️  [cyan]Mengirim Log Event Umpan Balik...[/cyan]")
    try:
        session.post('https://yupp.ai/api/trpc/logging.logEvent,logging.logEvent,logging.logEvent?batch=1', json={"0":{"json":{"event":"prefer_this"}},"1":{"json":{"event":"showed_unclaimed_scratch_card","insertId":turn_id}},"2":{"json":{"event":"pref_to_mof_visible"}}})
    except requests.exceptions.RequestException as e:
        console.print(f"   [yellow]⚠️  Warning: Gagal mengirim log event: {e}[/yellow]")
    
    # Mempertahankan jeda 5 detik Anda
    time.sleep(5)
    
    console.print(f"[bold]5.[/bold]   🎁 [cyan]Mengklaim Hadiah dengan ID:[/] [yellow]{extracted_reward_id}[/yellow]...")
    try:
        response5 = session.post('https://yupp.ai/api/trpc/reward.claim?batch=1', json={"0":{"json":{"rewardId": extracted_reward_id}}})
    except requests.exceptions.ProxyError:
        console.print("   [bold red]❌ Error proxy: Tidak dapat mengklaim reward melalui proxy.[/bold red]")
        return
    except requests.exceptions.RequestException as e:
        console.print(f"   [bold red]❌ Error koneksi klaim: {e}[/bold red]")
        return
    
    if response5.status_code == 200:
        try:
            claim_response = response5.json()
            if 'error' not in claim_response[0]:
                console.print("   [bold green]✅ PROSES KLAIM BERHASIL![/bold green]")
                json_syntax = Syntax(json.dumps(claim_response, indent=2), "json", theme="monokai", line_numbers=True)
                console.print(Panel(json_syntax, title=f"Respons Klaim - Account #{account_id}", border_style="green"))
            else:
                console.print("   [bold red]❌ PROSES KLAIM GAGAL (dari server)![/bold red]")
                json_syntax = Syntax(json.dumps(claim_response, indent=2), "json", theme="monokai", line_numbers=True)
                console.print(Panel(json_syntax, title=f"Respons Error - Account #{account_id}", border_style="red"))
        except requests.exceptions.JSONDecodeError:
            console.print(f"--> ❌ [bold red]Klaim Gagal, respons bukan JSON:[/bold red] {response5.text}")
    else:
        console.print(f"--> ❌ [bold red]PROSES KLAIM GAGAL! Status HTTP:[/bold red] {response5.status_code}")


# --- BAGIAN UTAMA UNTUK EKSEKUSI ---
if __name__ == "__main__":
    console.print(Panel("[bold magenta]🚀 Yupp.ai Auto-Bot v4.3 (Device Spoofing + Multi-Proxy + Multi-Account) 🚀[/bold magenta]", subtitle="by Gemini"))
    
    # --- PENAMBAHAN: Konfigurasi proxy dengan mode yang lebih fleksibel ---
    proxy_mode = get_proxy_mode()
    global_proxy_config = None
    
    if proxy_mode == '2':
        # 1 proxy untuk semua account
        global_proxy_config = load_proxy_config()
        if global_proxy_config:
            console.print(f"✅ [green]Proxy global berhasil dimuat dari proxy.txt[/green]")
        else:
            console.print("--> ⚠️  [yellow]proxy.txt tidak ditemukan atau kosong. Lanjut tanpa proxy.[/yellow]")
    elif proxy_mode == '4':
        # Proxy manual untuk semua account
        global_proxy_config = get_manual_proxy()
        if global_proxy_config:
            console.print(f"✅ [green]Proxy manual berhasil dikonfigurasi untuk semua account[/green]")
        else:
            console.print("--> [dim]Tidak menggunakan proxy.[/dim]")
    elif proxy_mode == '1':
        console.print("--> [dim]Tidak menggunakan proxy.[/dim]")
    elif proxy_mode == '3':
        console.print("--> [dim]Proxy akan diambil dari cookies.txt per account.[/dim]")
    
    # --- PENAMBAHAN: Konfigurasi cookies ---
    cookie_choice = get_cookie_choice()
    accounts_list = []
    
    if cookie_choice == '1':
        # Single cookie
        single_cookie = load_single_cookie_from_file()
        if single_cookie:
            accounts_list = [{
                'cookies': single_cookie,
                'proxy': global_proxy_config,
                'user_id': "37cf0952-9403-4d29-bf7a-1d1c08368a4a"  # Default user_id untuk single cookie
            }]
            console.print(f"✅ [green]Single cookie berhasil dimuat dari cookie.txt[/green]")
        else:
            console.print("--> ❌ [bold red]cookie.txt tidak ditemukan atau kosong. Menghentikan skrip.[/bold red]")
            sys.exit(1)
    elif cookie_choice == '2':
        # Multiple cookies
        accounts_list = load_multiple_cookies_from_file()
        if not accounts_list:
            console.print("--> ❌ [bold red]cookies.txt tidak ditemukan atau kosong. Menghentikan skrip.[/bold red]")
            sys.exit(1)
        
        # Jika mode proxy global, override proxy individual
        if proxy_mode in ['2', '4'] and global_proxy_config:
            for account in accounts_list:
                account['proxy'] = global_proxy_config
    
    loop_count = IntPrompt.ask("[bold]Masukkan jumlah looping yang diinginkan[/bold]", default=1)
    choice = get_user_choice()
    
    pesan_list = []
    api_key_gemini = ""
    api_key_deepseek = ""
    ai_provider = ""

    if choice == '1':
        try:
            with open('pesan.txt', 'r', encoding='utf-8') as f:
                pesan_list = [line.strip() for line in f.readlines() if line.strip()]
            if not pesan_list:
                console.print("--> ❌ [bold red]`pesan.txt` ada tapi kosong! Menghentikan skrip.[/bold red]")
                sys.exit(1)
            console.print(f"\n✅ [green]Pilihan: Menggunakan `pesan.txt`. Ditemukan {len(pesan_list)} pesan untuk diacak.[/green]")
        except FileNotFoundError:
            console.print("--> ❌ [bold red]`pesan.txt` tidak ditemukan! Menghentikan skrip.[/bold red]")
            sys.exit(1)
    elif choice == '2':
        api_key_gemini = load_api_key()
        if not api_key_gemini:
            console.print("--> ❌ [bold red]`apikey.txt` tidak ditemukan atau kosong! Menghentikan skrip.[/bold red]")
            sys.exit(1)
        ai_provider = "gemini"
        console.print("\n✅ [green]Pilihan: Menggunakan Gemini AI untuk menghasilkan pesan di setiap loop.[/green]")
    elif choice == '3':
        api_key_deepseek = load_deepseek_api_key()
        if not api_key_deepseek:
            console.print("--> ❌ [bold red]`deepseek_apikey.txt` tidak ditemukan atau kosong! Menghentikan skrip.[/bold red]")
            sys.exit(1)
        ai_provider = "deepseek"
        console.print("\n✅ [green]Pilihan: Menggunakan DeepSeek AI untuk menghasilkan pesan di setiap loop.[/green]")

    console.print("\n[bold]--- Pengaturan Selesai. Memulai Looping. ---[/bold]")
    time.sleep(2)

    for i in range(loop_count):
        console.print(Panel(f"LOOP KE-{i + 1} DARI {loop_count}", style="bold blue", padding=1))
        
        # --- PENAMBAHAN: Rotasi account untuk setiap loop ---
        for account_idx, account_data in enumerate(accounts_list, 1):
            console.print(Panel(f"ACCOUNT #{account_idx} DARI {len(accounts_list)}", style="bold yellow", padding=1))
            
            # --- PERUBAHAN: Generate message untuk setiap account ---
            message_for_this_account = ""
            if choice == '1':
                message_for_this_account = random.choice(pesan_list)
            elif choice == '2':
                message_for_this_account = generate_message_with_ai(api_key_gemini, "gemini")
            elif choice == '3':
                message_for_this_account = generate_message_with_ai(api_key_deepseek, "deepseek")
            
            # --- PERUBAHAN: Menggunakan device profile yang sudah diassign ke account ---
            device_profile = account_data.get('device_profile', get_random_device_profile())
            console.print(f"🖥️  [dim]Menggunakan profil device:[/] [italic dim]{device_profile['name']} - {device_profile['user-agent'][:50]}...[/italic dim]")
            
            # --- PERUBAHAN: Mengirim profil device, proxy, dan cookies ke fungsi ---
            run_single_bot_process(
                message_for_this_account, 
                device_profile, 
                account_data['proxy'], 
                account_data['cookies'], 
                account_idx,
                account_data['user_id']
            )
            
            # Jeda antar account (kecuali account terakhir)
            if account_idx < len(accounts_list):
                console.print("\n[dim]Jeda 10 detik sebelum account berikutnya...[/dim]")
                time.sleep(10)
        
        if i < loop_count - 1:
            console.print()
            # Mempertahankan jeda 60 detik Anda
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%")) as progress:
                task = progress.add_task("[yellow]Jeda...", total=60)
                for _ in range(60):
                    time.sleep(1)
                    progress.update(task, advance=1)

    console.print(Panel("🎉 [bold green]Semua proses looping telah selesai.[/bold green] ", style="green"))