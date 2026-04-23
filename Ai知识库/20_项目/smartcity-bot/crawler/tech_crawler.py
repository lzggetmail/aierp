"""
技术资料爬虫框架
================

自动抓取IT技术文档、白皮书、研究报告
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup
import hashlib


@dataclass
class TechDocument:
    """技术文档数据结构"""
    title: str
    url: str
    source: str
    doc_type: str  # report, whitepaper, policy, standard, tutorial, paper
    category: str
    publish_date: Optional[str]
    download_url: Optional[str]
    content_summary: str
    keywords: List[str]
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    created_at: str = datetime.now().isoformat()


class TechDataCrawler:
    """技术资料爬虫"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "config/tech_sources_simple.json"
        self.config = self._load_config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 存储目录
        self.storage_dir = Path("tech_documents")
        self.storage_dir.mkdir(exist_ok=True)
        
        # 子目录
        (self.storage_dir / "reports").mkdir(exist_ok=True)
        (self.storage_dir / "whitepapers").mkdir(exist_ok=True)
        (self.storage_dir / "policies").mkdir(exist_ok=True)
        (self.storage_dir / "standards").mkdir(exist_ok=True)
        (self.storage_dir / "tutorials").mkdir(exist_ok=True)
        (self.storage_dir / "papers").mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def crawl_consulting_reports(self) -> List[TechDocument]:
        """抓取咨询公司报告"""
        documents = []
        
        # 德勤
        print("\n📊 抓取德勤报告...")
        deloitte_docs = self._crawl_deloitte()
        documents.extend(deloitte_docs)
        print(f"  找到 {len(deloitte_docs)} 份报告")
        
        # 麦肯锡
        print("\n📊 抓取麦肯锡报告...")
        mckinsey_docs = self._crawl_mckinsey()
        documents.extend(mckinsey_docs)
        print(f"  找到 {len(mckinsey_docs)} 份报告")
        
        return documents
    
    def _crawl_deloitte(self) -> List[TechDocument]:
        """抓取德勤报告"""
        documents = []
        
        try:
            # 德勤中国洞察页面
            url = "https://www2.deloitte.com/cn/zh/insights.html"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找报告链接
                report_links = soup.find_all('a', href=re.compile(r'/cn/zh/insights/.*\.html'))
                
                for link in report_links[:10]:  # 限制前10个
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if title and href:
                        doc = TechDocument(
                            title=title,
                            url=f"https://www2.deloitte.com{href}" if href.startswith('/') else href,
                            source="德勤",
                            doc_type="report",
                            category="咨询报告",
                            publish_date=None,
                            download_url=None,
                            content_summary=title,
                            keywords=["德勤", "Deloitte", "咨询报告"]
                        )
                        documents.append(doc)
                
                time.sleep(1)  # 礼貌爬取
        
        except Exception as e:
            print(f"  ✗ 德勤抓取失败: {e}")
        
        return documents
    
    def _crawl_mckinsey(self) -> List[TechDocument]:
        """抓取麦肯锡报告"""
        documents = []
        
        try:
            url = "https://www.mckinsey.com.cn/insights/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找文章链接
                articles = soup.find_all('article') or soup.find_all('div', class_='article')
                
                for article in articles[:10]:
                    title_elem = article.find('h2') or article.find('h3') or article.find('a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a') if title_elem.name != 'a' else title_elem
                        href = link.get('href', '') if link else ''
                        
                        if title and href:
                            doc = TechDocument(
                                title=title,
                                url=href if href.startswith('http') else f"https://www.mckinsey.com.cn{href}",
                                source="麦肯锡",
                                doc_type="report",
                                category="咨询报告",
                                publish_date=None,
                                download_url=None,
                                content_summary=title,
                                keywords=["麦肯锡", "McKinsey", "咨询报告"]
                            )
                            documents.append(doc)
                
                time.sleep(1)
        
        except Exception as e:
            print(f"  ✗ 麦肯锡抓取失败: {e}")
        
        return documents
    
    def crawl_gov_policies(self) -> List[TechDocument]:
        """抓取政府政策文件"""
        documents = []
        
        print("\n🏛️  抓取政府政策...")
        
        # 国务院
        gov_docs = self._crawl_gov_cn()
        documents.extend(gov_docs)
        print(f"  找到 {len(gov_docs)} 份政策文件")
        
        return documents
    
    def _crawl_gov_cn(self) -> List[TechDocument]:
        """抓取国务院政策"""
        documents = []
        
        try:
            url = "http://www.gov.cn/zhengce/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找政策链接
                policy_links = soup.find_all('a', href=re.compile(r'/zhengce/content/.*\.htm'))
                
                for link in policy_links[:20]:
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if title and href and ('智慧城市' in title or '数字化' in title or '新型基础设施' in title):
                        doc = TechDocument(
                            title=title,
                            url=f"http://www.gov.cn{href}" if href.startswith('/') else href,
                            source="国务院",
                            doc_type="policy",
                            category="政府政策",
                            publish_date=None,
                            download_url=None,
                            content_summary=title,
                            keywords=["国务院", "政策", "智慧城市", "数字化"]
                        )
                        documents.append(doc)
                
                time.sleep(1)
        
        except Exception as e:
            print(f"  ✗ 国务院抓取失败: {e}")
        
        return documents
    
    def crawl_tech_docs(self) -> List[TechDocument]:
        """抓取技术文档"""
        documents = []
        
        # 华为技术支持
        print("\n🔧 抓取华为技术文档...")
        huawei_docs = self._crawl_huawei_docs()
        documents.extend(huawei_docs)
        print(f"  找到 {len(huawei_docs)} 份文档")
        
        # 阿里云文档
        print("\n🔧 抓取阿里云技术文档...")
        aliyun_docs = self._crawl_aliyun_docs()
        documents.extend(aliyun_docs)
        print(f"  找到 {len(aliyun_docs)} 份文档")
        
        return documents
    
    def _crawl_huawei_docs(self) -> List[TechDocument]:
        """抓取华为技术文档"""
        documents = []
        
        try:
            # 华为技术支持网站
            url = "https://e.huawei.com/cn/material/technology"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找文档链接
                doc_links = soup.find_all('a', href=re.compile(r'/cn/material/.*'))
                
                for link in doc_links[:15]:
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if title and href and len(title) > 5:
                        doc = TechDocument(
                            title=title,
                            url=f"https://e.huawei.com{href}" if href.startswith('/') else href,
                            source="华为",
                            doc_type="whitepaper",
                            category="技术白皮书",
                            publish_date=None,
                            download_url=None,
                            content_summary=title,
                            keywords=["华为", "Huawei", "技术文档"]
                        )
                        documents.append(doc)
                
                time.sleep(1)
        
        except Exception as e:
            print(f"  ✗ 华为抓取失败: {e}")
        
        return documents
    
    def _crawl_aliyun_docs(self) -> List[TechDocument]:
        """抓取阿里云技术文档"""
        documents = []
        
        try:
            url = "https://developer.aliyun.com/article"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找文章链接
                articles = soup.find_all('div', class_='article-item') or soup.find_all('article')
                
                for article in articles[:15]:
                    title_elem = article.find('h2') or article.find('h3') or article.find('a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a') if title_elem.name != 'a' else title_elem
                        href = link.get('href', '') if link else ''
                        
                        if title and href:
                            doc = TechDocument(
                                title=title,
                                url=href if href.startswith('http') else f"https://developer.aliyun.com{href}",
                                source="阿里云",
                                doc_type="whitepaper",
                                category="技术文档",
                                publish_date=None,
                                download_url=None,
                                content_summary=title,
                                keywords=["阿里云", "Alibaba Cloud", "技术文档"]
                            )
                            documents.append(doc)
                
                time.sleep(1)
        
        except Exception as e:
            print(f"  ✗ 阿里云抓取失败: {e}")
        
        return documents
    
    def crawl_all(self) -> List[TechDocument]:
        """抓取所有数据源"""
        all_documents = []
        
        print("=" * 60)
        print("开始抓取技术资料...")
        print("=" * 60)
        
        # 咨询报告
        reports = self.crawl_consulting_reports()
        all_documents.extend(reports)
        
        # 政府政策
        policies = self.crawl_gov_policies()
        all_documents.extend(policies)
        
        # 技术文档
        tech_docs = self.crawl_tech_docs()
        all_documents.extend(tech_docs)
        
        print("\n" + "=" * 60)
        print(f"✓ 抓取完成，共 {len(all_documents)} 份文档")
        print("=" * 60)
        
        # 保存结果
        self._save_documents(all_documents)
        
        return all_documents
    
    def _save_documents(self, documents: List[TechDocument]):
        """保存文档列表"""
        output = []
        
        for doc in documents:
            output.append({
                "title": doc.title,
                "url": doc.url,
                "source": doc.source,
                "doc_type": doc.doc_type,
                "category": doc.category,
                "publish_date": doc.publish_date,
                "download_url": doc.download_url,
                "content_summary": doc.content_summary,
                "keywords": doc.keywords,
                "created_at": doc.created_at
            })
        
        # 保存JSON
        output_file = self.storage_dir / f"documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 已保存到: {output_file}")
    
    def download_document(self, doc: TechDocument, download_url: str = None) -> Optional[str]:
        """
        下载文档
        
        Args:
            doc: 文档对象
            download_url: 下载链接
        
        Returns:
            下载文件路径
        """
        if not download_url:
            return None
        
        try:
            print(f"  下载: {doc.title}")
            
            response = self.session.get(download_url, stream=True, timeout=30)
            
            if response.status_code == 200:
                # 确定文件类型
                content_type = response.headers.get('content-type', '')
                
                if 'pdf' in content_type:
                    ext = '.pdf'
                elif 'doc' in content_type:
                    ext = '.docx'
                elif 'xls' in content_type:
                    ext = '.xlsx'
                else:
                    ext = '.pdf'  # 默认PDF
                
                # 生成文件名
                safe_title = re.sub(r'[^\w\s-]', '', doc.title)[:50]
                filename = f"{safe_title}{ext}"
                
                # 保存路径
                category_dir = self.storage_dir / f"{doc.doc_type}s"
                filepath = category_dir / filename
                
                # 写入文件
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                print(f"  ✓ 已保存: {filepath}")
                
                return str(filepath)
            
        except Exception as e:
            print(f"  ✗ 下载失败: {e}")
        
        return None


def main():
    """主函数"""
    crawler = TechDataCrawler()
    
    # 抓取所有数据源
    documents = crawler.crawl_all()
    
    # 显示统计
    print("\n📊 统计信息:")
    print(f"  总文档数: {len(documents)}")
    
    # 按来源统计
    sources = {}
    for doc in documents:
        sources[doc.source] = sources.get(doc.source, 0) + 1
    
    print("\n按来源统计:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} 份")
    
    # 按类型统计
    types = {}
    for doc in documents:
        types[doc.doc_type] = types.get(doc.doc_type, 0) + 1
    
    print("\n按类型统计:")
    for doc_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {doc_type}: {count} 份")


if __name__ == "__main__":
    main()
