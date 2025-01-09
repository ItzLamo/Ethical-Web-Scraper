import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Frame
from urllib.parse import urlparse, urljoin
import re
from datetime import datetime
import threading

class WebScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethical Web Scraper")
        self.root.geometry("950x800")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL Frame
        url_frame = ttk.LabelFrame(main_frame, text="URL Configuration", padding="5")
        url_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_entry = ttk.Entry(url_frame, width=80)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.url_entry.insert(0, "https://example.com")
        
        # Control Frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(control_frame, text="Scrape", command=self.start_scraping).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.clear_results).grid(row=0, column=1, padx=5)
        
        # Statistics Frame
        self.stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="5")
        self.stats_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_text = tk.Text(self.stats_frame, height=4, width=90)
        self.stats_text.grid(row=0, column=0, pady=5)
        
        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Scraped Data", padding="5")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, width=110, height=30)
        self.results_text.grid(row=0, column=0, pady=5)
        self.results_text.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))
        self.results_text.tag_configure("subheading", font=("TkDefaultFont", 9, "bold"))
        self.results_text.tag_configure("url", foreground="blue", underline=1)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))

    def start_scraping(self):
        threading.Thread(target=self.scrape, daemon=True).start()

    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.status_var.set("Ready")

    def scrape(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        try:
            self.status_var.set("Scraping...")
            self.root.update()
            
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                html = response.read()
                
            soup = BeautifulSoup(html, 'html.parser')
            data = self.extract_data(soup, url)
            
            self.display_results(data, url)
            self.save_results(data, url)
            
            self.status_var.set(f"Successfully scraped {url}")
            
        except urllib.error.URLError as e:
            messagebox.showerror("Error", f"Error accessing the URL: {e}")
            self.status_var.set("Error occurred")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_var.set("Error occurred")

    def extract_data(self, soup, base_url):
        data = {
            'meta': self.extract_meta_data(soup),
            'headings': self.extract_headings(soup),
            'links': self.extract_links(soup, base_url),
            'images': self.extract_images(soup, base_url),
            'text_content': self.extract_text_content(soup),
            'forms': self.extract_forms(soup)
        }
        return data

    def extract_meta_data(self, soup):
        meta_data = {
            'title': soup.title.string if soup.title else None,
            'meta_description': None,
            'meta_keywords': None,
            'charset': None
        }
        
        for meta in soup.find_all('meta'):
            if meta.get('name') == 'description':
                meta_data['meta_description'] = meta.get('content')
            elif meta.get('name') == 'keywords':
                meta_data['meta_keywords'] = meta.get('content')
            elif meta.get('charset'):
                meta_data['charset'] = meta.get('charset')
        
        return meta_data

    def extract_headings(self, soup):
        headings = []
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(tag):
                headings.append({
                    'level': tag,
                    'text': heading.get_text(strip=True),
                    'id': heading.get('id', ''),
                    'classes': heading.get('class', [])
                })
        return headings

    def extract_links(self, soup, base_url):
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                links.append({
                    'text': link.get_text(strip=True),
                    'url': absolute_url,
                    'title': link.get('title', ''),
                    'rel': link.get('rel', []),
                    'classes': link.get('class', [])
                })
        return links

    def extract_images(self, soup, base_url):
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                absolute_url = urljoin(base_url, src)
                images.append({
                    'src': absolute_url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', '')
                })
        return images

    def extract_text_content(self, soup):
        text_content = []
        for element in soup.find_all(['p', 'div', 'span', 'article', 'section']):
            text = element.get_text(strip=True)
            if text:
                text_content.append({
                    'tag': element.name,
                    'text': text,
                    'classes': element.get('class', []),
                    'id': element.get('id', '')
                })
        return text_content

    def extract_forms(self, soup):
        forms = []
        for form in soup.find_all('form'):
            fields = []
            for field in form.find_all(['input', 'textarea', 'select']):
                fields.append({
                    'type': field.get('type', 'text'),
                    'name': field.get('name', ''),
                    'id': field.get('id', ''),
                    'required': field.get('required') is not None
                })
            forms.append({
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'fields': fields
            })
        return forms

    def display_results(self, data, url):
        self.clear_results()
        
        # Display statistics
        stats = self.calculate_statistics(data)
        self.display_statistics(stats)
        
        # Display detailed results
        self.results_text.insert(tk.END, f"Scraping Results for {url}\n", "heading")
        self.results_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # Meta Data
        self.results_text.insert(tk.END, "META INFORMATION\n", "subheading")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        meta = data['meta']
        self.results_text.insert(tk.END, f"Title: {meta['title']}\n")
        self.results_text.insert(tk.END, f"Description: {meta['meta_description']}\n")
        self.results_text.insert(tk.END, f"Keywords: {meta['meta_keywords']}\n")
        self.results_text.insert(tk.END, f"Charset: {meta['charset']}\n\n")
        
        # Headings
        self.results_text.insert(tk.END, "HEADINGS\n", "subheading")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        for heading in data['headings']:
            self.results_text.insert(tk.END, f"{heading['level']}: {heading['text']}\n")
        self.results_text.insert(tk.END, "\n")
        
        # Links
        self.results_text.insert(tk.END, "LINKS\n", "subheading")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        for link in data['links']:
            self.results_text.insert(tk.END, f"Text: {link['text']}\n")
            self.results_text.insert(tk.END, f"URL: {link['url']}\n", "url")
            if link['title']:
                self.results_text.insert(tk.END, f"Title: {link['title']}\n")
            self.results_text.insert(tk.END, "-" * 20 + "\n")
        self.results_text.insert(tk.END, "\n")
        
        # Images
        self.results_text.insert(tk.END, "IMAGES\n", "subheading")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        for img in data['images']:
            self.results_text.insert(tk.END, f"Source: {img['src']}\n", "url")
            self.results_text.insert(tk.END, f"Alt Text: {img['alt']}\n")
            if img['title']:
                self.results_text.insert(tk.END, f"Title: {img['title']}\n")
            self.results_text.insert(tk.END, "-" * 20 + "\n")
        
        # Forms
        if data['forms']:
            self.results_text.insert(tk.END, "\nFORMS\n", "subheading")
            self.results_text.insert(tk.END, "-" * 40 + "\n")
            for i, form in enumerate(data['forms'], 1):
                self.results_text.insert(tk.END, f"Form {i}:\n")
                self.results_text.insert(tk.END, f"Action: {form['action']}\n")
                self.results_text.insert(tk.END, f"Method: {form['method']}\n")
                self.results_text.insert(tk.END, "Fields:\n")
                for field in form['fields']:
                    self.results_text.insert(tk.END, f"  - {field['type']}: {field['name']}"
                                          f"{' (required)' if field['required'] else ''}\n")
                self.results_text.insert(tk.END, "-" * 20 + "\n")

    def calculate_statistics(self, data):
        return {
            'total_headings': len(data['headings']),
            'total_links': len(data['links']),
            'total_images': len(data['images']),
            'total_forms': len(data['forms']),
            'total_text_blocks': len(data['text_content'])
        }

    def display_statistics(self, stats):
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "Page Statistics:\n")
        self.stats_text.insert(tk.END, f"Total Headings: {stats['total_headings']}\n")
        self.stats_text.insert(tk.END, f"Total Links: {stats['total_links']}\n")
        self.stats_text.insert(tk.END, f"Total Images: {stats['total_images']}\n")
        self.stats_text.insert(tk.END, f"Total Forms: {stats['total_forms']}\n")
        self.stats_text.insert(tk.END, f"Total Text Blocks: {stats['total_text_blocks']}\n")

    def save_results(self, data, url):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = re.sub(r'[^\w\-_]', '_', urlparse(url).netloc)
        filename = f'scraped_data_{domain}_{timestamp}.json'
        
        results = {
            'url': url,
            'timestamp': timestamp,
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)

def main():
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()