# -*- coding: utf-8 -*-
import os
import re
import json
import base64
import requests
import socket
import concurrent.futures
from datetime import datetime

# ================= الإعدادات الشخصية والـ SEO =================
BRAND_NAME = "Haider Adel"
SEO_SUFFIX = " | Haider Adel Free V2Ray"
TELEGRAM_USER = "https://t.me/RXAXX"

# haider
SOURCES = [
    "https://shadowmere.xyz/api/b64sub/",
    "https://raw.githubusercontent.com/exhxx1/V2Nodes-Sub/main/sub.txt",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription4",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/main/sub.txt"
]

def decode_base64(data):
    try:
        data = re.sub(r'\s+', '', data)
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except:
        return ""

def check_and_rename_node(node, index):
    """دالة فحص السيرفر (Ping) وتعديل اسمه للتصدر بجوجل"""
    host = None
    port = None
    protocol = None
    renamed_node = node
    new_name = f"Node {index:03d}{SEO_SUFFIX}"

    try:
        # استخراج البروتوكول
        protocol = node.split("://")[0].lower()

        if protocol == "vmess":
            b64_str = node[8:]
            config = json.loads(decode_base64(b64_str))
            host = config.get("add") or config.get("host")
            port = config.get("port")
            config["ps"] = new_name
            renamed_node = f"vmess://{base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')}"
            
        elif protocol in ["vless", "trojan", "ss"]:
            match = re.search(r'@([^:/]+):(\d+)', node)
            if match:
                host = match.group(1)
                port = int(match.group(2))
            base_url = node.split("#")[0]
            renamed_node = f"{base_url}#{new_name}"
            
    except:
        return None # تجاهل السيرفر المعطوب برمجياً

    # فحص السيرفر (TCP Ping) - للتأكد انه شغال ومو ميت
    if host and port:
        try:
            socket.create_connection((host, int(port)), timeout=1.5)
        except:
            return None # السيرفر ميت، اتركه

    return (protocol, renamed_node)

def generate_html(categorized_nodes, total_count):
    """برمجة صفحة الويب بـ 4 لغات مع تصنيف الروابط"""
    repo = os.environ.get('GITHUB_REPOSITORY', 'USER/REPO')
    base_raw_url = f"https://raw.githubusercontent.com/{repo}/main"
    date_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free V2Ray & Sing-box Nodes | {BRAND_NAME}</title>
    <meta name="description" content="Free V2Ray, Vless, Vmess, Trojan nodes updated hourly. سرور رایگان v2ray. Бесплатные серверы V2Ray.">
    <meta name="keywords" content="free v2ray, vless free, vmess free, trojan, iran vpn, anti-filter, {BRAND_NAME}">
    <style>
        body {{ background-color: #121212; color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; text-align: center; }}
        .header {{ background-color: #1a1a1a; padding: 25px; border-bottom: 2px solid #00ff88; }}
        .header h1 {{ margin: 0; color: #00ff88; font-size: 2.2em; }}
        .header p {{ color: #ccc; font-size: 1.1em; }}
        .container {{ max-width: 900px; margin: 30px auto; padding: 20px; }}
        .stats {{ background-color: #1e1e1e; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 30px; }}
        .stats h2 {{ color: #00ff88; font-size: 3em; margin: 10px 0; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: #1e1e1e; padding: 20px; border-radius: 10px; border: 1px solid #333; }}
        .card h3 {{ color: #00ff88; margin-top: 0; text-transform: uppercase; }}
        input.link-box {{ width: 90%; padding: 12px; background: #2a2a2a; border: 1px solid #444; color: #00ff88; font-size: 0.9em; border-radius: 5px; text-align: center; margin-bottom: 10px; cursor: pointer; }}
        .btn {{ display: inline-block; background-color: #0088cc; color: #fff; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; transition: 0.3s; margin-top: 20px; }}
        .btn:hover {{ background-color: #006699; box-shadow: 0 0 15px #0088cc; }}
        .langs {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 40px; text-align: left; }}
        .lang-box {{ background: #1a1a1a; padding: 15px; border-radius: 8px; border-left: 3px solid #00ff88; }}
        .lang-box h4 {{ color: #00ff88; margin-top: 0; }}
        .lang-box p {{ font-size: 0.9em; color: #bbb; line-height: 1.5; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{BRAND_NAME} Network</h1>
        <p>Tested, Classified & 100% Free V2Ray Nodes</p>
    </div>
    <div class="container">
        <div class="stats">
            <p>Tested Alive Servers</p>
            <h2>{total_count}</h2>
            <p>Last Checked: {date_now}</p>
        </div>

        <div class="grid">
            <div class="card">
                <h3>🌟 All Nodes (Mix)</h3>
                <p>Count: {total_count}</p>
                <input class="link-box" type="text" value="{base_raw_url}/all.txt" readonly onclick="this.select();">
            </div>
            <div class="card">
                <h3>🚀 VLESS</h3>
                <p>Count: {len(categorized_nodes['vless'])}</p>
                <input class="link-box" type="text" value="{base_raw_url}/vless.txt" readonly onclick="this.select();">
            </div>
            <div class="card">
                <h3>⚡ VMESS</h3>
                <p>Count: {len(categorized_nodes['vmess'])}</p>
                <input class="link-box" type="text" value="{base_raw_url}/vmess.txt" readonly onclick="this.select();">
            </div>
            <div class="card">
                <h3>🐎 TROJAN</h3>
                <p>Count: {len(categorized_nodes['trojan'])}</p>
                <input class="link-box" type="text" value="{base_raw_url}/trojan.txt" readonly onclick="this.select();">
            </div>
        </div>

        <a href="{TELEGRAM_USER}" target="_blank" class="btn">💬 Contact @RXAXX on Telegram</a>

        <div class="langs">
            <div class="lang-box">
                <h4>🇬🇧 English</h4>
                <p>All servers are Ping-tested before publishing. Copy the link of your preferred protocol and import it into V2RayNG, Sing-box, or Clash.</p>
            </div>
            <div class="lang-box">
                <h4>🇮🇷 فارسی (Persian)</h4>
                <p>تمامی سرورها قبل از انتشار پینگ و تست می‌شوند. لینک پروتکل دلخواه خود را کپی کرده و در V2RayNG یا Sing-box وارد کنید.</p>
            </div>
            <div class="lang-box">
                <h4>🇷🇺 Русский (Russian)</h4>
                <p>Все серверы проверены на работоспособность. Скопируйте ссылку нужного протокола и вставьте в V2RayNG/Sing-box.</p>
            </div>
            <div class="lang-box">
                <h4>🇮🇶 العربية (Arabic)</h4>
                <p>يتم فحص جميع السيرفرات وطرد العاطلة تلقائياً. انسخ رابط البروتوكول الذي يناسبك وضعه في تطبيق التخطي الخاص بك.</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    print(f"🚀 Starting {BRAND_NAME} Spider & Checker...")
    raw_nodes = []
    
    # 1. سحب البيانات
    for url in SOURCES:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                text = resp.text
                if "://" not in text[:50]:
                    text = decode_base64(text)
                links = re.findall(r'(vless://\S+|vmess://\S+|trojan://\S+|ss://\S+)', text)
                raw_nodes.extend(links)
                print(f"✅ Fetched {len(links)} nodes from {url}")
        except:
            pass

    unique_nodes = list(set(raw_nodes))
    print(f"\n🔍 Found {len(unique_nodes)} unique nodes. Starting Ping test...")

    categorized = {'vless': [], 'vmess': [], 'trojan': [], 'ss': [], 'all': []}
    
    # 2. فحص السيرفرات بسرعة عالية (50 اتصال بنفس الوقت)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_and_rename_node, node, i+1): node for i, node in enumerate(unique_nodes)}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                protocol, renamed_node = result
                if protocol in categorized:
                    categorized[protocol].append(renamed_node)
                categorized['all'].append(renamed_node)

    total_alive = len(categorized['all'])
    if total_alive == 0:
        print("❌ No alive nodes found after testing!")
        return
        
    print(f"\n✅ Testing Complete! {total_alive} servers are alive & working.")

    # 3. تشفير وحفظ الملفات مفصولة حسب البروتوكول
    for cat, nodes in categorized.items():
        if nodes:
            b64_content = base64.b64encode("\n".join(nodes).encode('utf-8')).decode('utf-8')
            with open(f"{cat}.txt", "w", encoding="utf-8") as f:
                f.write(b64_content)
            print(f"💾 Saved {cat}.txt ({len(nodes)} nodes)")

    # 4. بناء الموقع
    generate_html(categorized, total_alive)
    print("🌍 Generated index.html")

if __name__ == "__main__":
    main()
