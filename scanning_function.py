import re
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox
import tkinter as tk
import logging
import socket
import threading
from subprocess import Popen, PIPE

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class ScanningFunction:
    def __init__(self, txt):
        self.txt = txt
    def get_domain_from_url(self, url):
        url_parts = url.split("//")[-1].split("/")
        return url_parts[0]

    def reverse_dns_lookup(ip_address):
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except socket.herror:
            return None

    def validate_input(self, input_str):
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        url_pattern = r"^(?:http[s]?:\/\/)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,3}){1,2}$"
        ip_valid = re.match(ip_pattern, input_str)
        url_valid = re.match(url_pattern, input_str)
        return ip_valid or url_valid

    def is_ip(self, input_str):
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        ip_valid = re.match(ip_pattern, input_str)
        return bool(ip_valid)

    def prepend_http(self, input_str):
        if not input_str.startswith("http://") and not input_str.startswith("https://"):
            input_str = "http://" + input_str
        return input_str

    def get_domain_from_url(self, url):
        url_parts = url.split("//")[-1].split("/")
        return url_parts[0]

    def perform_web_scraping(self, target):
        try:
            if self.is_ip(target):
                target = f"http://{target}"
            else:
                target = self.prepend_http(target)

            threading.Thread(target=self.get_webpage_content, args=(target,)).start()

        except Exception as e:
            self.txt.insert(tk.END, "Error occurred while performing web scraping: " + str(e) + "\n")
            messagebox.showerror("Error", "Error occurred while performing web scraping: " + str(e))

    def get_webpage_content(self, target):
        try:
            r = requests.get(target, timeout=3)
            htmlcontent = r.content

            soup = BeautifulSoup(htmlcontent, 'html.parser')

            separator = "-" * 80 + "\n\n"

            title = soup.find('title').string
            self.txt.configure(state='normal')
            self.txt.delete('1.0', tk.END)  # Clear the text widget
            self.txt.insert(tk.END, "Title: " + title + "\n" + separator)

            head = soup.head
            self.txt.insert(tk.END, "Head:\n" + head.prettify() + "\n" + separator)

            body = soup.body
            self.txt.insert(tk.END, "Body:\n" + body.prettify() + "\n" + separator)

            links = soup.find_all('a')
            self.txt.insert(tk.END, "Links:\n")
            for link in links:
                self.txt.insert(tk.END, "Link: " + str(link.get('href')) + "\n")
            self.txt.insert(tk.END, separator)

            headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            self.txt.insert(tk.END, "Headers:\n")
            for header in headers:
                self.txt.insert(tk.END, str(header.name) + ": " + str(header.text.strip()) + "\n")
            self.txt.insert(tk.END, separator)

            images = soup.find_all('img')
            self.txt.insert(tk.END, "Images:\n")
            for image in images:
                self.txt.insert(tk.END, "Image: " + str(image.get('src')) + "\n")
            self.txt.insert(tk.END, separator)

            paragraphs = soup.find_all('p')
            self.txt.insert(tk.END, "Paragraphs:\n")
            for paragraph in paragraphs:
                self.txt.insert(tk.END, "Paragraph: " + str(paragraph.text.strip()) + "\n")
            self.txt.insert(tk.END, separator)

            self.txt.configure(state='disabled')

        except Exception as e:
            self.txt.insert(tk.END, "Error occurred while performing web scraping: " + str(e) + "\n")
            messagebox.showerror("Error", "Error occurred while performing web scraping: " + str(e))


    def perform_subdomain_enumeration(self, target):
        try:
            if self.is_ip(target):
                target = self.reverse_dns_lookup(target)
            else:
                target = self.get_domain_from_url(target)

            threading.Thread(target=self.enumerate_subdomains, args=(target,)).start()

        except Exception as e:
            self.txt.insert(tk.END, "Error occurred while performing subdomain enumeration: " + str(e) + "\n")
            messagebox.showerror("Error", "Error occurred while performing subdomain enumeration: " + str(e))

    def enumerate_subdomains(self, target):
        try:
            subdomains = [
                'www', 'blog', 'shop', 'mail', 'ftp', 'webmail', 'admin', 'forum', 'api', 'cdn',
                'staging', 'dev', 'login', 'auth', 'support', 'help'
            ]
            subdomain_results = []

            for subdomain in subdomains:
                full_url = f"http://{subdomain}.{target}"
                try:
                    response = requests.get(full_url, timeout=3)
                    if response.status_code == 200:
                        subdomain_results.append(full_url)
                except requests.exceptions.RequestException:
                    pass

            self.txt.configure(state='normal')
            self.txt.delete('1.0', tk.END)
            self.txt.insert(tk.END, "Subdomain Enumeration Results:\n\n")

            if len(subdomain_results) > 0:
                for subdomain in subdomain_results:
                    self.txt.insert(tk.END, subdomain + "\n")
            else:
                self.txt.insert(tk.END, "No subdomain matches found.\n")

            self.txt.configure(state='disabled')

        except Exception as e:
            self.txt.insert(tk.END, "Error occurred while performing subdomain enumeration: " + str(e) + "\n")
            messagebox.showerror("Error", "Error occurred while performing subdomain enumeration: " + str(e))


    def run_nikto(self, target, options):
        try:
            if self.is_ip(target):
                target = f"http://{target}"
            else:
                target = self.prepend_http(target)

            threading.Thread(target=self.execute_nikto, args=(target, options)).start()

        except FileNotFoundError:
            self.txt.insert(tk.END, "Nikto not found. Please install Nikto and try again.\n")
            logging.error("Nikto not found. Please install Nikto and try again.")

        except Exception as e:
            self.txt.insert(tk.END, "Error occurred while running Nikto: " + str(e) + "\n")
            logging.error(f"Error occurred while running Nikto: {str(e)}")

    def execute_nikto(self, target, options):
        try:
            cmd = ["nikto", "-host", target] + options
            process = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(f"Nikto exited with code {process.returncode}: {stderr.decode('utf-8')}")

            output = stdout.decode('utf-8').replace("Enumeration Scanning Report will appear here...", "")
            
            self.txt.configure(state='normal')
            self.txt.delete('1.0', tk.END)  # Clear the text widget
            self.txt.insert(tk.END, output)
            self.txt.configure(state='disabled')

        except Exception as e:
            self.txt.insert(tk.END, "Error occurred while running Nikto: " + str(e) + "\n")
            logging.error(f"Error occurred while running Nikto: {str(e)}")
