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
BRAND_AR = "حيدر عادل"
SEO_SUFFIX = " | Haider Adel Free V2Ray"
TELEGRAM_USER = "https://t.me/RXAXX"
GOOGLE_VERIFICATION = "DEw0QfBJIZ8cq1yUyPN-tlFx7cQFFSRo6_CSTILXfzE"

# 18 مصدراً عالمياً تتحدث باستمرار
SOURCES = [
    "https://shadowmere.xyz/api/b64sub/",
    "https://raw.githubusercontent.com/exhxx1/V2Nodes-Sub/main/sub.txt",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription4",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/main/sub.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/base64/mix",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt",
    "https://raw.githubusercontent.com/ts-sf/fly/main/v2",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
    "https://raw.githubusercontent.com/NiREvil/vless/main/sub/SSTime",
    "https://raw.githubusercontent.com/alienvpn402/alienvpn402-subscribe-servers/main/index.html"
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

def parse_node_info(node):
    """استخراج البروتوكول والـ IP والبورت لمنع تكرار نفس السيرفر قبل الفحص"""
    try:
        protocol = node.split("://")[0].lower()
        if protocol == "vmess":
            b64_str = node[8:].split("#")[0]
            config = json.loads(decode_base64(b64_str))
            host = config.get("add") or config.get("host")
            port = int(config.get("port", 0))
            if host and port:
                return (protocol, host, port, config)
        elif protocol in ["vless", "trojan", "ss"]:
            base_url = node.split("#")[0]
            match = re.search(r'@([^:/?#]+):(\d+)', base_url)
            if match:
                return (protocol, match.group(1), int(match.group(2)), base_url)
    except:
        pass
    return None

def check_and_rename_node(parsed_item, index):
    """فحص السيرفر (TCP Ping) وإعادة تسميته باسم حيدر عادل"""
    protocol, host, port, payload = parsed_item
    new_name = f"Node {index:03d}{SEO_SUFFIX}"

    try:
        socket.create_connection((host, port), timeout=1.2)
    except:
        return None

    try:
        if protocol == "vmess":
            payload["ps"] = new_name
            encoded = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
            return (protocol, f"vmess://{encoded}")
        else:
            return (protocol, f"{payload}#{new_name}")
    except:
        return None

def generate_html_and_seo(categorized_nodes, total_count):
    """بناء المنصة التفاعلية + ملفات أرشفة جوجل (Sitemap & Robots)"""
    repo = os.environ.get('GITHUB_REPOSITORY', 'exhxx1/Free-V2Ray-Haider')
    user_name, repo_name = repo.split('/') if '/' in repo else ('exhxx1', 'Free-V2Ray-Haider')
    base_raw_url = f"https://raw.githubusercontent.com/{repo}/main"
    site_url = f"https://{user_name}.github.io/{repo_name}/"
    date_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    today_iso = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')

    nodes_for_js = {
        "vless": categorized_nodes["vless"],
        "vmess": categorized_nodes["vmess"],
        "trojan": categorized_nodes["trojan"],
        "ss": categorized_nodes["ss"]
    }

    html_template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="__GOOGLE_VERIFICATION__" />
    <title>__BRAND_AR__ | __BRAND_NAME__ - Free V2Ray, VLESS, VMess & Sing-box Servers</title>
    <meta name="description" content="الموقع الرسمي لـ __BRAND_AR__ (__BRAND_NAME__) لسيرفرات V2Ray و VLESS و VMess و Trojan و Sing-box المجانية والمفحوصة تلقائياً كل 4 ساعات. سرور رایگان V2Ray حیدر عادل. Бесплатные серверы V2Ray.">
    <meta name="keywords" content="حيدر عادل, موقع حيدر عادل, سيرفرات حيدر عادل, Haider Adel, Haider Adel Free V2Ray, free v2ray, vless free, vmess nodes, trojan proxy, shadowsocks free, iran vpn, russia bypass, sing-box config, v2rayng sub, حیدر عادل">
    <meta name="author" content="__BRAND_AR__ - __BRAND_NAME__">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="__SITE_URL__" />
    <meta property="og:type" content="website">
    <meta property="og:title" content="__BRAND_AR__ | __BRAND_NAME__ Network - Free V2Ray & Sing-box Nodes">
    <meta property="og:description" content="سيرفرات V2Ray و Sing-box مجانية، مفحوصة ومحدثة تلقائياً كل 4 ساعات بواسطة __BRAND_AR__ (__BRAND_NAME__).">
    <meta property="og:url" content="__SITE_URL__">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "__BRAND_AR__ | __BRAND_NAME__ Network",
      "alternateName": ["حيدر عادل", "Haider Adel", "Haider Adel Free V2Ray", "حیدر عادل"],
      "url": "__SITE_URL__",
      "author": {
        "@type": "Person",
        "name": "__BRAND_AR__ (Haider Adel)",
        "url": "__TELEGRAM_USER__"
      }
    }
    </script>
    <style>
        :root {
            --bg-main: #0b0f17;
            --bg-card: #151c28;
            --bg-card-hover: #1c2636;
            --accent: #00ff88;
            --accent-dim: rgba(0, 255, 136, 0.12);
            --tg-blue: #0088cc;
            --text-main: #f0f6fc;
            --text-muted: #8b949e;
            --border: #263142;
            --vless-color: #a371f7;
            --vmess-color: #58a6ff;
            --trojan-color: #f0883e;
            --ss-color: #3fb950;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            padding-bottom: 60px;
        }

        .top-bar {
            background: rgba(21, 28, 40, 0.9);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
            padding: 12px 20px;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .lang-switcher { display: flex; gap: 8px; flex-wrap: wrap; }
        .lang-btn {
            background: var(--bg-main);
            color: var(--text-muted);
            border: 1px solid var(--border);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: 0.2s;
        }
        .lang-btn:hover, .lang-btn.active {
            border-color: var(--accent);
            color: var(--accent);
            background: var(--accent-dim);
        }
        .tg-top-btn {
            background: var(--tg-blue);
            color: #fff;
            text-decoration: none;
            padding: 7px 16px;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: bold;
            transition: 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .tg-top-btn:hover { background: #006da3; box-shadow: 0 0 12px rgba(0,136,204,0.5); }

        .hero {
            text-align: center;
            padding: 45px 20px 30px;
            background: radial-gradient(circle at top, rgba(0, 255, 136, 0.12), transparent 60%);
        }
        .hero h1 {
            font-size: 2.5rem;
            color: var(--accent);
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            text-shadow: 0 0 20px rgba(0,255,136,0.25);
        }
        .hero p { color: var(--text-muted); font-size: 1.1rem; max-width: 650px; margin: 0 auto 25px; }

        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            max-width: 850px;
            margin: 0 auto;
        }
        .stat-item {
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 15px 28px;
            border-radius: 12px;
            min-width: 180px;
        }
        .stat-value { font-size: 2rem; font-weight: 800; color: var(--accent); }
        .stat-label { font-size: 0.85rem; color: var(--text-muted); }

        .container { max-width: 1150px; margin: 0 auto; padding: 20px; }

        .section-title {
            font-size: 1.4rem;
            margin: 35px 0 18px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: var(--text-main);
        }

        .sub-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 15px;
        }
        .sub-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            transition: 0.25s;
        }
        .sub-card:hover { border-color: var(--accent); transform: translateY(-3px); }
        .sub-card h3 { font-size: 1.1rem; margin-bottom: 6px; color: var(--accent); }
        .sub-count { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px; }
        .copy-sub-btn {
            width: 100%;
            background: var(--accent);
            color: #0b0f17;
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
            font-size: 0.9rem;
        }
        .copy-sub-btn:hover { opacity: 0.9; box-shadow: 0 0 12px rgba(0,255,136,0.4); }

        .tabs-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
        .tab-btn {
            background: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border);
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.95rem;
            transition: 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .tab-btn span.badge {
            background: var(--bg-main);
            color: var(--accent);
            padding: 2px 8px;
            border-radius: 20px;
            font-size: 0.8rem;
        }
        .tab-btn.active, .tab-btn:hover {
            background: var(--accent);
            color: #0b0f17;
            border-color: var(--accent);
        }
        .tab-btn.active span.badge, .tab-btn:hover span.badge {
            background: #0b0f17;
            color: var(--accent);
        }

        .nodes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
            gap: 16px;
        }
        .node-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: 0.2s;
        }
        .node-card:hover { background: var(--bg-card-hover); border-color: #3b4c66; }
        .node-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .node-title { font-weight: 700; font-size: 0.95rem; color: var(--text-main); display: flex; align-items: center; gap: 6px; }
        .online-dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; display: inline-block; box-shadow: 0 0 8px var(--accent); }
        .proto-badge { font-size: 0.75rem; font-weight: 800; padding: 3px 9px; border-radius: 5px; text-transform: uppercase; color: #fff; }
        .proto-vless { background: var(--vless-color); }
        .proto-vmess { background: var(--vmess-color); }
        .proto-trojan { background: var(--trojan-color); }
        .proto-ss { background: var(--ss-color); }

        .node-code {
            background: var(--bg-main);
            border: 1px solid var(--border);
            color: var(--text-muted);
            font-family: monospace;
            font-size: 0.8rem;
            padding: 10px;
            border-radius: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-bottom: 12px;
            direction: ltr;
            text-align: left;
        }
        .copy-node-btn {
            background: transparent;
            color: var(--accent);
            border: 1px solid var(--accent);
            padding: 9px;
            border-radius: 7px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
            width: 100%;
        }
        .copy-node-btn:hover { background: var(--accent); color: #0b0f17; }

        .load-more-wrap { text-align: center; margin-top: 28px; }
        .load-more-btn {
            background: var(--bg-card);
            color: var(--accent);
            border: 1px solid var(--accent);
            padding: 12px 35px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        .load-more-btn:hover { background: var(--accent); color: #0b0f17; }

        #toast {
            position: fixed;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: var(--accent);
            color: #0b0f17;
            padding: 12px 28px;
            border-radius: 30px;
            font-weight: 800;
            box-shadow: 0 5px 20px rgba(0,255,136,0.4);
            transition: 0.3s ease;
            z-index: 999;
        }
        #toast.show { transform: translateX(-50%) translateY(0); }

        footer { text-align: center; margin-top: 50px; color: var(--text-muted); font-size: 0.9rem; }
    </style>
</head>
<body>

    <div class="top-bar">
        <div class="lang-switcher">
            <button class="lang-btn active" onclick="setLanguage('ar')" id="btn-ar">🇮🇶 العربية</button>
            <button class="lang-btn" onclick="setLanguage('en')" id="btn-en">🇬🇧 English</button>
            <button class="lang-btn" onclick="setLanguage('fa')" id="btn-fa">🇮🇷 فارسی</button>
            <button class="lang-btn" onclick="setLanguage('ru')" id="btn-ru">🇷🇺 Русский</button>
        </div>
        <a href="__TELEGRAM_USER__" target="_blank" class="tg-top-btn">
            <span>✈️</span> <span data-i18n="contact_tg">تواصل معي @RXAXX</span>
        </a>
    </div>

    <div class="hero">
        <h1>__BRAND_NAME__ | __BRAND_AR__</h1>
        <p data-i18n="hero_sub">سيرفرات V2Ray و Sing-box مجانية، مفحوصة بالبينج ومحدثة تلقائياً كل 4 ساعات</p>

        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">__TOTAL_COUNT__</div>
                <div class="stat-label" data-i18n="stat_alive">سيرفر شغال ومفحوص</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">4 Hours</div>
                <div class="stat-label" data-i18n="stat_cycle">دورة التحديث التلقائي</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" style="font-size: 1.1rem; margin-top: 10px;">__DATE_NOW__</div>
                <div class="stat-label" data-i18n="stat_updated">آخر فحص وتحديث</div>
            </div>
        </div>
    </div>

    <div class="container">
        <h2 class="section-title">
            <span data-i18n="sub_section_title">📦 روابط الاشتراك الشاملة (تضاف داخل التطبيق مباشرة)</span>
        </h2>
        <div class="sub-grid" id="sub-grid-container"></div>

        <h2 class="section-title">
            <span data-i18n="nodes_section_title">⚡ تصفح السيرفرات المباشر (انسخ أي سيرفر بضغطة زر)</span>
        </h2>

        <div class="tabs-bar" id="tabs-container"></div>
        <div class="nodes-grid" id="nodes-container"></div>

        <div class="load-more-wrap">
            <button class="load-more-btn" id="load-more-btn" onclick="loadMoreNodes()" data-i18n="load_more">عرض المزيد من السيرفرات</button>
        </div>
    </div>

    <footer>
        <p>Powered by <b>__BRAND_AR__ (__BRAND_NAME__)</b> | <a href="__TELEGRAM_USER__" style="color: var(--accent); text-decoration: none;">@RXAXX</a></p>
    </footer>

    <div id="toast">Copied!</div>

    <script>
        const BASE_RAW_URL = "__BASE_RAW_URL__";
        const RAW_NODES = __NODES_JSON__;
        
        const ALL_LIST = [];
        ['vless', 'vmess', 'trojan', 'ss'].forEach(proto => {
            (RAW_NODES[proto] || []).forEach((cfg, idx) => {
                ALL_LIST.push({ proto: proto, config: cfg, id: idx + 1 });
            });
        });

        const I18N = {
            en: {
                dir: "ltr",
                contact_tg: "Contact @RXAXX",
                hero_sub: "Tested, Classified & High-Speed Free V2Ray / Sing-box Servers Updated Automatically",
                stat_alive: "Online Tested Servers",
                stat_cycle: "Auto-Update Cycle",
                stat_updated: "Last Checked (UTC)",
                sub_section_title: "📦 Subscription Links (Import All at Once)",
                nodes_section_title: "⚡ Direct Server Explorer (Copy Individual Servers)",
                copy_sub: "📋 Copy Subscription",
                copy_node: "📋 Copy Config",
                copied_msg: "✅ Copied to Clipboard!",
                load_more: "Show More Servers",
                server_unit: "Servers",
                tab_all: "All Nodes"
            },
            ar: {
                dir: "rtl",
                contact_tg: "تواصل معي @RXAXX",
                hero_sub: "سيرفرات V2Ray و Sing-box مجانية، مفحوصة بالبينج ومحدثة تلقائياً كل 4 ساعات",
                stat_alive: "سيرفر شغال ومفحوص",
                stat_cycle: "دورة التحديث التلقائي",
                stat_updated: "آخر فحص وتحديث",
                sub_section_title: "📦 روابط الاشتراك الشاملة (تضاف داخل التطبيق مباشرة)",
                nodes_section_title: "⚡ تصفح السيرفرات المباشر (انسخ أي سيرفر بضغطة زر)",
                copy_sub: "📋 نسخ رابط الاشتراك",
                copy_node: "📋 نسخ هذا السيرفر",
                copied_msg: "✅ تم النسخ بنجاح!",
                load_more: "عرض المزيد من السيرفرات",
                server_unit: "سيرفر",
                tab_all: "الكل (Mix)"
            },
            fa: {
                dir: "rtl",
                contact_tg: "تلگرام @RXAXX",
                hero_sub: "سرورهای رایگان، تست شده و پرسرعت V2Ray و Sing-box با بروزرسانی خودکار",
                stat_alive: "سرورهای فعال و تست شده",
                stat_cycle: "بروزرسانی خودکار",
                stat_updated: "آخرین بررسی",
                sub_section_title: "📦 لینک‌های اشتراک (مناسب V2RayNG و Sing-box)",
                nodes_section_title: "⚡ لیست مستقیم سرورها (کپی تکی کانفیگ‌ها)",
                copy_sub: "📋 کپی لینک اشتراک",
                copy_node: "📋 کپی کانفیگ",
                copied_msg: "✅ با موفقیت کپی شد!",
                load_more: "نمایش سرورهای بیشتر",
                server_unit: "سرور",
                tab_all: "همه سرورها"
            },
            ru: {
                dir: "ltr",
                contact_tg: "Telegram @RXAXX",
                hero_sub: "Бесплатные проверенные серверы V2Ray и Sing-box с автоматическим обновлением",
                stat_alive: "Активных серверов",
                stat_cycle: "Интервал обновления",
                stat_updated: "Последняя проверка",
                sub_section_title: "📦 Ссылки на подписку (Для V2RayNG / Sing-box)",
                nodes_section_title: "⚡ Список серверов (Копировать по одному)",
                copy_sub: "📋 Скопировать подписку",
                copy_node: "📋 Скопировать конфиг",
                copied_msg: "✅ Скопировано в буфер!",
                load_more: "Показать еще",
                server_unit: "серв.",
                tab_all: "Все серверы"
            }
        };

        let currentLang = 'ar';
        let currentTab = 'all';
        let visibleCount = 24;

        function copyText(text) {
            navigator.clipboard.writeText(text).then(() => {
                const toast = document.getElementById('toast');
                toast.textContent = I18N[currentLang].copied_msg;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2200);
            });
        }

        function renderSubscriptions() {
            const subs = [
                { id: 'all', title: '🌟 ALL MIX', count: ALL_LIST.length, file: 'all.txt' },
                { id: 'vless', title: '🚀 VLESS', count: (RAW_NODES.vless || []).length, file: 'vless.txt' },
                { id: 'vmess', title: '⚡ VMESS', count: (RAW_NODES.vmess || []).length, file: 'vmess.txt' },
                { id: 'trojan', title: '🐎 TROJAN', count: (RAW_NODES.trojan || []).length, file: 'trojan.txt' },
                { id: 'ss', title: '🛡️ SHADOWSOCKS', count: (RAW_NODES.ss || []).length, file: 'ss.txt' }
            ];
            const container = document.getElementById('sub-grid-container');
            container.innerHTML = subs.map(s => `
                <div class="sub-card">
                    <h3>${s.title}</h3>
                    <div class="sub-count">${s.count} ${I18N[currentLang].server_unit}</div>
                    <button class="copy-sub-btn" onclick="copyText('${BASE_RAW_URL}/${s.file}')">
                        ${I18N[currentLang].copy_sub}
                    </button>
                </div>
            `).join('');
        }

        function renderTabs() {
            const tabs = [
                { key: 'all', label: I18N[currentLang].tab_all, count: ALL_LIST.length },
                { key: 'vless', label: 'VLESS', count: (RAW_NODES.vless || []).length },
                { key: 'vmess', label: 'VMESS', count: (RAW_NODES.vmess || []).length },
                { key: 'trojan', label: 'TROJAN', count: (RAW_NODES.trojan || []).length },
                { key: 'ss', label: 'SHADOWSOCKS', count: (RAW_NODES.ss || []).length }
            ];
            const container = document.getElementById('tabs-container');
            container.innerHTML = tabs.map(t => `
                <button class="tab-btn ${currentTab === t.key ? 'active' : ''}" onclick="switchTab('${t.key}')">
                    <span>${t.label}</span>
                    <span class="badge">${t.count}</span>
                </button>
            `).join('');
        }

        function getFilteredList() {
            if (currentTab === 'all') return ALL_LIST;
            return (RAW_NODES[currentTab] || []).map((cfg, idx) => ({
                proto: currentTab,
                config: cfg,
                id: idx + 1
            }));
        }

        function renderNodes() {
            const list = getFilteredList();
            const slice = list.slice(0, visibleCount);
            const container = document.getElementById('nodes-container');

            container.innerHTML = slice.map((item, idx) => {
                const safeCfg = item.config.replace(/\\\\/g, "\\\\\\\\").replace(/'/g, "\\\\'");
                return `
                <div class="node-card">
                    <div>
                        <div class="node-header">
                            <div class="node-title">
                                <span class="online-dot"></span>
                                <span>Haider Adel #${String(idx + 1).padStart(3, '0')}</span>
                            </div>
                            <span class="proto-badge proto-${item.proto}">${item.proto}</span>
                        </div>
                        <div class="node-code">${item.config.substring(0, 65)}...</div>
                    </div>
                    <button class="copy-node-btn" onclick="copyText('${safeCfg}')">
                        ${I18N[currentLang].copy_node}
                    </button>
                </div>
                `;
            }).join('');

            const loadBtn = document.getElementById('load-more-btn');
            loadBtn.style.display = visibleCount >= list.length ? 'none' : 'inline-block';
        }

        function switchTab(tabKey) {
            currentTab = tabKey;
            visibleCount = 24;
            renderTabs();
            renderNodes();
        }

        function loadMoreNodes() {
            visibleCount += 24;
            renderNodes();
        }

        function setLanguage(lang) {
            currentLang = lang;
            document.documentElement.lang = lang;
            document.documentElement.dir = I18N[lang].dir;

            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-' + lang).classList.add('active');

            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (I18N[lang][key]) el.textContent = I18N[lang][key];
            });

            renderSubscriptions();
            renderTabs();
            renderNodes();
        }

        setLanguage('ar');
    </script>
</body>
</html>"""

    final_html = (
        html_template
        .replace("__GOOGLE_VERIFICATION__", GOOGLE_VERIFICATION)
        .replace("__BRAND_NAME__", BRAND_NAME)
        .replace("__BRAND_AR__", BRAND_AR)
        .replace("__SITE_URL__", site_url)
        .replace("__TOTAL_COUNT__", str(total_count))
        .replace("__DATE_NOW__", date_now)
        .replace("__BASE_RAW_URL__", base_raw_url)
        .replace("__TELEGRAM_USER__", TELEGRAM_USER)
        .replace("__NODES_JSON__", json.dumps(nodes_for_js))
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    # توليد خريطة الموقع Sitemap لجوجل
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    # توليد ملف Robots لجوجل
    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {site_url}sitemap.xml\n"
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_txt)

def main():
    print(f"🚀 Starting {BRAND_NAME} Mega Spider & Checker (18 Sources)...")
    raw_nodes = []
    
    for url in SOURCES:
        try:
            resp = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                text = resp.text.strip()
                if "://" not in text[:80]:
                    decoded = decode_base64(text)
                    if "://" in decoded:
                        text = decoded
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', text)
                raw_nodes.extend(links)
                print(f"✅ Fetched {len(links)} nodes from {url}")
        except Exception as e:
            print(f"⚠️ Skipped {url}: {e}")

    unique_endpoints = {}
    for node in raw_nodes:
        info = parse_node_info(node)
        if info:
            protocol, host, port, payload = info
            key = f"{protocol}:{host}:{port}"
            if key not in unique_endpoints:
                unique_endpoints[key] = info

    items_to_test = list(unique_endpoints.values())[:2500]
    print(f"\n🔍 Extracted {len(items_to_test)} unique IP:Port servers. Running fast TCP Ping...")

    categorized = {'vless': [], 'vmess': [], 'trojan': [], 'ss': [], 'all': []}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
        futures = {executor.submit(check_and_rename_node, item, i+1): item for i, item in enumerate(items_to_test)}
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

    for cat, nodes in categorized.items():
        if nodes:
            b64_content = base64.b64encode("\n".join(nodes).encode('utf-8')).decode('utf-8')
            with open(f"{cat}.txt", "w", encoding="utf-8") as f:
                f.write(b64_content)
            print(f"💾 Saved {cat}.txt ({len(nodes)} nodes)")

    generate_html_and_seo(categorized, total_alive)
    print("🌍 Generated index.html, sitemap.xml, and robots.txt!")

if __name__ == "__main__":
    main()
