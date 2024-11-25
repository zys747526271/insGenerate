import re
from datetime import datetime
import yt_dlp
import os
import csv
import time
import random
import shutil
import json
from fake_useragent import UserAgent
import browser_cookie3

def get_random_delay():
    """生成随机延迟时间"""
    # 生成2-5秒的随机延迟
    return random.uniform(2, 5)

def get_random_user_agent():
    """获取随机User-Agent"""
    try:
        ua = UserAgent()
        return ua.random
    except:
        # 如果fake_useragent失败，使用预定义的User-Agent列表
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        ]
        return random.choice(user_agents)

def get_instagram_cookies():
    """获取浏览器中的Instagram cookies"""
    try:
        # 尝试从多个浏览器获取cookies
        browsers = [
            ('chrome', browser_cookie3.chrome),
            ('edge', browser_cookie3.edge),
            ('firefox', browser_cookie3.firefox),
        ]
        
        for browser_name, browser_func in browsers:
            try:
                cookies = browser_func(domain_name='.instagram.com')
                print(f"成功从 {browser_name} 获取cookies")
                return cookies
            except:
                continue
                
        print("无法从浏览器获取cookies，请确保已在浏览器中登录Instagram")
        return None
    except Exception as e:
        print(f"获取cookies时出错: {str(e)}")
        return None

def extract_instagram_links(file_path: str) -> list:
    """从文件或文本中提取Instagram链接"""
    try:
        # 如果是文件路径，读取文件内容
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        else:
            # 如果不是文件，直接使用输入的文本
            content = file_path
        
        # 匹配 Instagram 链接的正则表达式，包括查询参数
        pattern = r'https?://(?:www\.)?instagram\.com/reel/[^/\s]+/?\?[^\s"\')]+|https?://(?:www\.)?instagram\.com/p/[^/\s]+/?\?[^\s"\')]+|https?://(?:www\.)?instagram\.com/reels/[^/\s]+/?\?[^\s"\')]+|https?://(?:www\.)?instagram\.com/stories/[^/\s]+/?\?[^\s"\')]+|https?://(?:www\.)?instagram\.com/tv/[^/\s]+/?\?[^\s"\')]+|https?://(?:www\.)?instagram\.com/[^/\s]+/[^/\s]+/?\?[^\s"\')]+|https?://(?:www\.)?instagram\.com/[^/\s]+/?\?[^\s"\')]+|https?://(?:www\.)?instagram\.com/[^/\s]+/[^/\s]+/?'
        links = re.findall(pattern, content)
        
        if links:
            print(f"找到 {len(links)} 个链接:")
            for link in links:
                print(f"- {link}")
        
        return links
    except Exception as e:
        print(f"提取链接时出错: {str(e)}")
        return []

def download_videos(links, output_path='downloads'):
    """下载视频"""
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 下载配置
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'quiet': False,
        'no_warnings': False,
        'cookiefile': 'cookies.txt',  # 使用cookies文件
        'http_headers': {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/',
            'DNT': '1'
        }
    }

    for i, link in enumerate(links, 1):
        try:
            print(f"\n[{i}/{len(links)}] 正在下载: {link}")
            
            # 每次下载前更新User-Agent
            ydl_opts['http_headers']['User-Agent'] = get_random_user_agent()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            
            # 模拟真实用户行为的随机延迟
            delay = get_random_delay()
            print(f"等待 {delay:.1f} 秒后继续...")
            time.sleep(delay)
            
        except Exception as e:
            print(f"下载失败: {str(e)}")
            # 发生错误时增加额外延迟
            time.sleep(random.uniform(5, 8))
            continue

if __name__ == "__main__":
    # 指定包含链接的文本文件路径
    links_file = "11-25.txt"  # 你可以修改为实际的文件路径
    
    # 使用txt文件名（不包括扩展名）作为输出目录
    output_folder = os.path.splitext(os.path.basename(links_file))[0]

    print("开始提取链接...")
    links = extract_instagram_links(links_file)
    
    if not links:
        print("未找到任何 Instagram 链接")
        exit()
    
    # 随机打乱链接顺序
    random.shuffle(links)
    
    print(f"找到 {len(links)} 个链接")
    print(f"视频将保存到 {output_folder} 目录")
    print("开始下载视频...")
    download_videos(links, output_folder)