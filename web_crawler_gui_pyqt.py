import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel

# Fungsi untuk mengambil semua link dari halaman web
def get_all_links(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        links.append(full_url)
    
    return links

# Fungsi untuk mengambil URL dari sitemap
def get_sitemap_links(sitemap_url):
    response = requests.get(sitemap_url)
    
    if response.status_code != 200:
        return []
    
    # Gunakan 'lxml-xml' untuk parsing XML
    soup = BeautifulSoup(response.content, 'lxml-xml')
    
    urls = []
    for url_tag in soup.find_all('loc'):
        urls.append(url_tag.text)
    
    return urls

class WebCrawlerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Web Crawler')
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.url_label = QLabel('Start URL:')
        self.layout.addWidget(self.url_label)
        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)
        
        self.sitemap_label = QLabel('Sitemap URL:')
        self.layout.addWidget(self.sitemap_label)
        self.sitemap_input = QLineEdit()
        self.layout.addWidget(self.sitemap_input)
        
        self.start_button = QPushButton('Start Crawling')
        self.start_button.clicked.connect(self.start_crawling)
        self.layout.addWidget(self.start_button)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.layout.addWidget(self.output_area)
    
    def log_output(self, text):
        self.output_area.append(text)
    
    def start_crawling(self):
        self.output_area.clear()
        url = self.url_input.text()
        sitemap = self.sitemap_input.text()
        
        if url or sitemap:
            self.crawl_website(start_url=url, sitemap_url=sitemap, max_pages=10)
        else:
            self.log_output("Please enter a URL or Sitemap")
    
    def crawl_website(self, start_url=None, sitemap_url=None, max_pages=5):
        visited = set()
        to_visit = []

        if sitemap_url:
            self.log_output(f"Fetching sitemap from: {sitemap_url}")
            to_visit = get_sitemap_links(sitemap_url)
        else:
            to_visit.append(start_url)

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue
            
            self.log_output(f"Crawling: {url}")
            visited.add(url)
            
            links = get_all_links(url)
            self.log_output(f"Found {len(links)} links on {url}")
            
            for link in links:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

        self.log_output("Crawling finished")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebCrawlerApp()
    window.show()
    sys.exit(app.exec_())
