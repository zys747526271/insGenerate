import os
import tempfile
import json
from typing import Optional, List
import gradio as gr
from video_downloader import download_videos, extract_instagram_links
from video_merger import merge_videos

def download_only(links: str, output_folder: str) -> str:
    """仅下载视频"""
    try:
        # 确保输出文件夹存在
        os.makedirs(output_folder, exist_ok=True)
        
        # 直接从文本中提取链接
        links_list = extract_instagram_links(links)
        if not links_list:
            return """未找到有效的Instagram链接，请确保链接格式正确。
                支持的格式：
                - https://www.instagram.com/reel/xxx
                - https://www.instagram.com/p/xxx
                - https://www.instagram.com/reels/xxx
                - https://www.instagram.com/stories/xxx
                - https://www.instagram.com/tv/xxx"""
        
        print(f"找到 {len(links_list)} 个有效链接：")
        for link in links_list:
            print(f"- {link}")
        
        # 下载视频
        download_videos(links_list, output_folder)
        
        return f"下载完成！视频已保存到: {output_folder}"
    except Exception as e:
        return f"下载过程中出错: {str(e)}"

def merge_only(input_folder: str, output_path: str, title: str, author: str) -> str:
    """仅合并视频"""
    try:
        merge_videos(input_folder, output_path, title, author)
        return f"合并完成！视频已保存到: {output_path}"
    except Exception as e:
        return f"合并过程中出错: {str(e)}"

def download_and_merge(links: str, output_folder: str, output_path: str, title: str, author: str) -> str:
    """下载并合并视频"""
    try:
        # 先下载
        download_result = download_only(links, output_folder)
        if "错误" in download_result:
            return download_result
        
        # 再合并
        merge_result = merge_only(output_folder, output_path, title, author)
        return merge_result
    except Exception as e:
        return f"处理过程中出错: {str(e)}"

def create_ui():
    """创建用户界面"""
    sortable_js = r"""
// Sortable.js v1.15.0 minimal version for our needs
!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define(e):(t=t||self).Sortable=e()}(this,function(){"use strict";function t(t){return(t=t.slice(5)).charAt(0).toLowerCase()+t.slice(1)}var e=/[^.]*(?=\..*)\.|.*/,n=/\..*/,o=/::\d+$/,i={};let r=1;var a={mousedown:"touchstart",mousemove:"touchmove",mouseup:"touchend"},l={touchstart:"mousedown",touchmove:"mousemove",touchend:"mouseup"};function s(t,e){t.lastSort={},t.options=Object.assign({},e),t.options.animation=250}return function(){function t(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function e(t,e,n){return e&&i(t.prototype,e),n&&i(t,n),t}function i(t,e){for(var n=0;n<e.length;n++){var o=e[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}var n=function(){function n(e,o){t(this,n),void 0!==o&&s(this,o),this.el=e,this._initializeEventListeners()}return e(n,[{key:"destroy",value:function(){this._removeEventListeners()}},{key:"_initializeEventListeners",value:function(){var t=this;this.el.addEventListener("mousedown",function(e){t._onStart(e)})}},{key:"_removeEventListeners",value:function(){this.el.removeEventListener("mousedown",this._onStart)}},{key:"_onStart",value:function(t){var e=this,n=t.target;if(n.classList.contains("video-item")){var o=t.clientY,i=n.offsetTop;document.addEventListener("mousemove",r),document.addEventListener("mouseup",a),this.el.classList.add("sorting");var r=function(t){var r=t.clientY-o,a=e.el.children,l=Array.from(a).indexOf(n),s=Array.from(a);n.style.position="absolute",n.style.top=i+r+"px",n.style.width=n.offsetWidth+"px",n.style.zIndex="1000",Array.from(a).forEach(function(t,e){if(t!==n){var o=t.offsetTop+t.offsetHeight/2;if(t.offsetTop<i+r&&t.offsetTop+t.offsetHeight>i+r){var a=s.indexOf(t);s.splice(l,1),s.splice(a,0,n),e<l?t.style.transform="translateY(".concat(n.offsetHeight,"px)"):t.style.transform="translateY(-".concat(n.offsetHeight,"px)")}}})},a=function t(){document.removeEventListener("mousemove",r),document.removeEventListener("mouseup",t),n.style.position="",n.style.top="",n.style.width="",n.style.zIndex="",Array.from(e.el.children).forEach(function(t){t.style.transform=""}),e.el.classList.remove("sorting");var o=Array.from(e.el.children).map(function(t){return t.dataset.file});document.querySelector("#video-list-state").value=JSON.stringify(o),document.querySelector("#video-list-state").dispatchEvent(new Event("change",{bubbles:!0}))}}}}]),n}();return n}());
    """
    
    # 首先创建HTML内容
    html_content = f"""
<script>
{sortable_js}
</script>
<script>
    function initSortable() {{
        const list = document.querySelector('.sortable-list');
        if (list && !list.dataset.sortableInitialized) {{
            new Sortable(list, {{
                animation: 150,
                onEnd: function() {{
                    const items = Array.from(list.children).map(item => item.dataset.file);
                    const stateEl = document.querySelector('#video-list-state');
                    if (stateEl) {{
                        stateEl.value = JSON.stringify(items);
                        stateEl.dispatchEvent(new Event('change', {{bubbles: true}}));
                    }}
                }}
            }});
            list.dataset.sortableInitialized = 'true';
        }}
    }}

    // 监听DOM变化
    const observer = new MutationObserver((mutations) => {{
        mutations.forEach((mutation) => {{
            if (mutation.type === 'childList') {{
                initSortable();
            }}
        }});
    }});

    // 定期检查并初始化
    const interval = setInterval(() => {{
        const videoList = document.querySelector('#video-list');
        if (videoList) {{
            observer.observe(videoList, {{ childList: true, subtree: true }});
            initSortable();
            clearInterval(interval);
        }}
    }}, 100);
</script>
"""
    
    with gr.Blocks(title="Instagram视频批量下载器", css="""
        #video-list {
            border: 1px solid #ddd;
            padding: 10px;
            min-height: 100px;
            border-radius: 4px;
            position: relative;
        }
        .video-item {
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: move;
            transition: transform 0.2s;
            user-select: none;
        }
        .video-item:hover {
            background: #e9e9e9;
            transform: translateX(5px);
        }
        .sorting .video-item {
            transition: transform 0.2s;
        }
        .video-item.dragging {
            opacity: 0.5;
            background: #c8ebfb;
        }
    """) as app:
        gr.Markdown("# 📱 Instagram视频批量下载器")
        
        # 然后使用gr.HTML组件
        gr.HTML(html_content)
        
        with gr.Tabs():
            # 下载标签页
            with gr.Tab("📥 下载视频"):
                with gr.Column():
                    links_input = gr.Textbox(
                        label="Instagram视频链接",
                        placeholder="粘贴Instagram视频链接，每行一个...",
                        lines=5
                    )
                    download_output_folder = gr.Textbox(
                        label="下载保存路径",
                        placeholder="视频保存的文件夹路径",
                        value="downloads"
                    )
                    download_btn = gr.Button("开始下载", variant="primary")
                    download_output = gr.Textbox(label="下载结果")
                    
                    download_btn.click(
                        fn=download_only,
                        inputs=[links_input, download_output_folder],
                        outputs=download_output
                    )
            
            # 合并标签页
            with gr.Tab("🔄 合并视频"):
                with gr.Column():
                    input_folder = gr.Textbox(
                        label="视频文件夹",
                        placeholder="包含要合并的视频的文件夹路径",
                        value="downloads"
                    )
                    
                    # 使用HTML组件实现拖拽排序
                    video_list = gr.State([])
                    video_list_ui = gr.HTML(
                        label="视频列表（拖拽调整顺序）",
                        value='<div id="video-list"><div class="sortable-list"></div><input type="hidden" id="video-list-state"></div>'
                    )
                    
                    refresh_btn = gr.Button("刷新视频列表")
                    output_path = gr.Textbox(
                        label="输出文件路径",
                        placeholder="合并后的视频保存路径（包含文件名）",
                        value="merged_video.mp4"
                    )
                    title = gr.Textbox(
                        label="视频标题",
                        placeholder="合并后的视频标题",
                        value="今日份快乐"
                    )
                    author = gr.Textbox(
                        label="作者",
                        placeholder="视频作者",
                        value="Cynvann"
                    )
                    merge_btn = gr.Button("开始合并", variant="primary")
                    merge_output = gr.Textbox(label="合并结果")
                    
                    # 刷新视频列表
                    def refresh_videos(folder):
                        if not os.path.exists(folder):
                            return [], "<div>文件夹不存在</div>"
                        videos = []
                        html_list = ['<div id="video-list" class="sortable-container">']
                        html_list.append('<ul class="sortable-list" style="list-style: none; padding: 0; margin: 0;">')
                        
                        for file in sorted(os.listdir(folder)):
                            if file.endswith(('.mp4', '.MP4', '.mov', '.MOV')):
                                videos.append(file)
                                html_list.append(f'<li class="video-item" data-file="{file}">{file}</li>')
                        
                        html_list.append('</ul>')  # close sortable-list
                        html_list.append(f'<input type="hidden" id="video-list-state" value=\'{json.dumps(videos)}\'>')
                        html_list.append('</div>')  # close video-list
                        return videos, ''.join(html_list)
                    
                    refresh_btn.click(
                        fn=refresh_videos,
                        inputs=[input_folder],
                        outputs=[video_list, video_list_ui]
                    )
                    
                    # 合并视频（使用自定义顺序）
                    def merge_with_order(folder, video_paths, output, title, author):
                        try:
                            if not video_paths:
                                return "请先刷新视频列表！"
                            
                            # 从完整路径中提取文件名
                            video_files = [os.path.join(folder, path) for path in video_paths]
                            return merge_videos(folder, output, title, author, video_files)
                        except Exception as e:
                            return f"处理过程中出错: {str(e)}"
                    
                    merge_btn.click(
                        fn=merge_with_order,
                        inputs=[input_folder, video_list, output_path, title, author],
                        outputs=merge_output
                    )
            
            # 一键下载合并标签页
            with gr.Tab("🚀 一键下载合并"):
                with gr.Column():
                    combined_links = gr.Textbox(
                        label="Instagram视频链接",
                        placeholder="粘贴Instagram视频链接，每行一个...",
                        lines=5
                    )
                    combined_download_folder = gr.Textbox(
                        label="下载保存路径",
                        placeholder="视频保存的文件夹路径",
                        value="downloads"
                    )
                    combined_output_path = gr.Textbox(
                        label="输出文件路径",
                        placeholder="合并后的视频保存路径（包含文件名）",
                        value="merged_video.mp4"
                    )
                    combined_title = gr.Textbox(
                        label="视频标题",
                        placeholder="合并后的视频标题",
                        value="今日份快乐"
                    )
                    combined_author = gr.Textbox(
                        label="作者",
                        placeholder="视频作者",
                        value="Cynvann"
                    )
                    combined_btn = gr.Button("开始处理", variant="primary")
                    combined_output = gr.Textbox(label="处理结果")
                    
                    combined_btn.click(
                        fn=download_and_merge,
                        inputs=[
                            combined_links,
                            combined_download_folder,
                            combined_output_path,
                            combined_title,
                            combined_author
                        ],
                        outputs=combined_output
                    )
        
        gr.Markdown("""
        ### 📝 使用说明
        1. 确保已经在项目目录下放置了有效的 cookies.txt 文件
        2. 在文本框中粘贴Instagram视频链接，每行一个
        3. 设置保存路径和其他选项
        4. 点击相应的按钮开始处理
        """)
    
    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="127.0.0.1",  # 本地服务器地址
        server_port=8080,         # 端口号
        share=False,              # 不生成公共链接
        inbrowser=True,           # 自动打开浏览器
        show_api=False,           # 关闭API界面
        auth=None,                # 不设置访问密码
        favicon_path=None,        # 默认网站图标
        quiet=True,               # 减少命令行输出
        # enable_queue=True,        # 启用队列处理请求
    )
