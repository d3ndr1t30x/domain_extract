import os
import requests
from urllib.parse import urlparse, parse_qs

# Function to extract the target URL from query parameters (e.g., 'u=' or 'url=')
def get_redirect_target(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Check for common redirect parameters like 'u', 'url', or 'redirect'
    redirect_url = None
    if 'u' in query_params:
        redirect_url = query_params['u'][0]
    elif 'url' in query_params:
        redirect_url = query_params['url'][0]
    elif 'redirect' in query_params:
        redirect_url = query_params['redirect'][0]
    
    return redirect_url

# Function to extract the domain name after following redirects
def extract_domain(url):
    try:
        # Follow the redirect and get the final URL
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        
        # If there's a query redirect (like in your case), follow it
        redirect_target = get_redirect_target(final_url)
        if redirect_target:
            print(f"Redirecting to: {redirect_target}")
            response = requests.get(redirect_target, allow_redirects=True)
            final_url = response.url
        
        # Parse the final URL to get the domain
        parsed_url = urlparse(final_url)
        domain = parsed_url.netloc
        return domain
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

# Main function to read URLs from a file and write domains to a new file
def process_urls(input_file, output_file):
    # Ensure input file exists
    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' does not exist.")
        return
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        urls = infile.readlines()
        for url in urls:
            url = url.strip()
            domain = extract_domain(url)
            if domain:
                outfile.write(domain + '\n')
                print(f"Extracted domain: {domain}")
            else:
                print(f"Failed to extract domain from: {url}")

# Prompt user for input and output filenames
input_file = input("Enter the input .txt filename (with path if needed): ")
output_file = input("Enter the output .txt filename (with path if needed): ")

# Process URLs
process_urls(input_file, output_file)
