"""
PDF 完整内容抓取器
=================

下载 PDF 文件并提取完整文本内容
"""

import os
import re
import requests
import tempfile
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class PDFContent:
    """PDF 内容"""
    title: str
    url: str
    content: str
    page_count: int
    source: str


class PDFFetcher:
    """PDF 抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 60
        self.max_pages = 50  # 最多提取50页
    
    def fetch_pdf(self, url: str, title: str = "") -> Optional[PDFContent]:
        """
        下载 PDF 并提取完整文本
        
        Args:
            url: PDF 链接
            title: 标题
        
        Returns:
            PDF 内容
        """
        try:
            print(f"  📥 下载 PDF: {url[:60]}...")
            
            # 下载 PDF
            response = self.session.get(url, timeout=self.timeout, stream=True)
            
            if response.status_code != 200:
                print(f"  ❌ 下载失败: HTTP {response.status_code}")
                return None
            
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                temp_path = f.name
            
            # 提取文本
            content = self._extract_text(temp_path)
            
            # 删除临时文件
            os.unlink(temp_path)
            
            if not content:
                print(f"  ❌ 文本提取失败")
                return None
            
            # 统计页数
            page_count = self._count_pages(temp_path) if os.path.exists(temp_path) else 0
            
            # 来源
            source = url.split('/')[2] if '/' in url else "未知"
            
            print(f"  ✅ 提取成功: {len(content)} 字符")
            
            return PDFContent(
                title=title or self._extract_title(content) or "未命名文档",
                url=url,
                content=content[:50000],  # 限制50000字符
                page_count=page_count,
                source=source
            )
            
        except Exception as e:
            print(f"  ❌ 处理失败: {e}")
            return None
    
    def _extract_text(self, pdf_path: str) -> Optional[str]:
        """提取 PDF 文本"""
        try:
            # 尝试使用 pdfplumber（效果更好）
            import pdfplumber
            
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages[:self.max_pages]):
                    page_text = page.extract_text()
                    if page_text:
                        # 清理文本
                        page_text = self._clean_text(page_text)
                        if page_text.strip():
                            text_parts.append(f"--- 第 {i+1} 页 ---\n{page_text}")
            
            return "\n\n".join(text_parts)
            
        except ImportError:
            # 回退到 PyPDF2
            try:
                from PyPDF2 import PdfReader
                
                reader = PdfReader(pdf_path)
                text_parts = []
                
                for i, page in enumerate(reader.pages[:self.max_pages]):
                    page_text = page.extract_text()
                    if page_text:
                        page_text = self._clean_text(page_text)
                        if page_text.strip():
                            text_parts.append(f"--- 第 {i+1} 页 ---\n{page_text}")
                
                return "\n\n".join(text_parts)
                
            except Exception as e:
                print(f"  PyPDF2 提取失败: {e}")
                return None
                
        except Exception as e:
            print(f"  pdfplumber 提取失败: {e}")
            return None
    
    def _count_pages(self, pdf_path: str) -> int:
        """统计页数"""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            return len(reader.pages)
        except:
            return 0
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
        return text.strip()
    
    def _extract_title(self, content: str) -> Optional[str]:
        """从内容中提取标题"""
        lines = content.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 5 and len(line) < 100:
                return line
        return None


# 测试
if __name__ == "__main__":
    fetcher = PDFFetcher()
    
    # 测试 PDF 下载
    test_urls = [
        ("https://www.gz.gov.cn/attachment/7/7511/7511635/9341271.pdf", "广州智慧城市基础设施技术指引"),
    ]
    
    for url, title in test_urls:
        print(f"\n{'='*60}")
        result = fetcher.fetch_pdf(url, title)
        
        if result:
            print(f"\n标题: {result.title}")
            print(f"页数: {result.page_count}")
            print(f"内容长度: {len(result.content)} 字符")
            print(f"\n内容预览:\n{result.content[:1500]}...")
