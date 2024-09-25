import pdfkit
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# Define a function to scrape all links on a given webpage
def get_internal_links(url, domain):
    internal_links = set()  # To avoid duplicates
    try:
        # Send a request to the URL
        response = requests.get(url)
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract all anchor tags with href attributes
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            
            # Filter to include only internal links
            if href.startswith("/") or domain in href:
                # Convert relative URLs to absolute URLs
                full_url = urllib.parse.urljoin(url, href)
                internal_links.add(full_url)
    except Exception as e:
        print(f"Failed to get links from {url}: {e}")
    
    return internal_links

# Define a function to save each page as a PDF
def save_page_as_pdf(url, download_folder="pdfs", config_path='/usr/local/bin/wkhtmltopdf'):
    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    try:
        # Parse the domain name from the URL to avoid saving external links
        domain = urllib.parse.urlparse(url).netloc

        # Get all internal links from the main page
        internal_links = get_internal_links(url, domain)
        print(f"Found {len(internal_links)} internal links on {url}")

        for link in internal_links:
            # Clean up the title to make it filename-safe
            pdf_filename = link.split("/")[-1] or "index"
            pdf_filename = pdf_filename.replace(" ", "_").replace("/", "-") + ".pdf"
            pdf_path = os.path.join(download_folder, pdf_filename)

            # Print which page is being saved
            print(f"Saving {link} as {pdf_filename}...")

            # Save the page as a PDF using pdfkit
            config = pdfkit.configuration(wkhtmltopdf=config_path)
            pdfkit.from_url(link, pdf_path, configuration=config)

            print(f"Saved: {pdf_path}")
    except Exception as e:
        print(f"Failed to save the page: {e}")



# Example usage
# website_url = "https://software4kmu-gw7raga7xq-uc.a.run.app/"  # Replace with the actual website URL
# save_page_as_pdf(website_url)
