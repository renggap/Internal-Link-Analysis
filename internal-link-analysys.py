import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re

# Function to fetch and parse a sitemap or sitemapindex
def get_sitemap_urls(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            urls = set()

            # Check if it's a sitemapindex
            if soup.find_all('sitemap'):
                for sitemap in soup.find_all('sitemap'):
                    # Recursively fetch URLs from nested sitemaps
                    nested_sitemap_url = sitemap.find('loc').text
                    urls.update(get_sitemap_urls(nested_sitemap_url))
            else:
                # Extract URLs from a regular sitemap
                for url_loc in soup.find_all('loc'):
                    url = url_loc.text
                    if not is_image(url) and not should_exclude_url(url):  # Avoid crawling images and excluded URLs
                        urls.add(url)

            return urls
        else:
            print(f"Failed to fetch sitemap: {sitemap_url}")
            return set()
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return set()

# Function to check if the URL is an image (avoid crawling images)
def is_image(url):
    return re.search(r'\.(jpg|jpeg|png|gif|bmp|svg|webp)$', url, re.IGNORECASE)

# Function to check if the URL should be excluded
def should_exclude_url(url):
    return re.search(r'/(tag|category|author)/', url, re.IGNORECASE)

# Function to fetch and parse a page
def get_links(url, base_domain):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all anchor tags with href attributes
            links = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Convert relative links to absolute
                full_url = urljoin(url, href)
                # Check if the link belongs to the same domain, is not an image, and should not be excluded
                if (base_domain in urlparse(full_url).netloc
                    and not is_image(full_url)
                    and not should_exclude_url(full_url)):
                    links.add(full_url)
            return links
        else:
            print(f"Failed to fetch {url}")
            return set()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

# Function to crawl the site based on sitemap URLs
def crawl_sitemap(sitemap_urls, base_domain):
    crawled = set()
    internal_links_map = {}

    for current_url in sitemap_urls:
        if current_url in crawled:
            continue

        print(f"Crawling: {current_url}")
        links = get_links(current_url, base_domain)
        internal_links_map[current_url] = links.intersection(sitemap_urls)  # Restrict to sitemap URLs only
        crawled.add(current_url)

    return internal_links_map

# Analyse the link structure
def analyse_links(internal_links_map):
    page_link_count = {page: len(links) for page, links in internal_links_map.items()}
    all_pages = set(internal_links_map.keys())
    linked_pages = {link for links in internal_links_map.values() for link in links}
    orphan_pages = all_pages - linked_pages  # Pages with no incoming links

    return page_link_count, orphan_pages

# Compute PageRank using networkx
def compute_pagerank(internal_links_map):
    G = nx.DiGraph()

    # Add edges (from -> to) to the graph
    for page, links in internal_links_map.items():
        for link in links:
            G.add_edge(page, link)

    # Compute PageRank
    pagerank = nx.pagerank(G, alpha=0.85)

    return pagerank

# Visualise the internal link structure
def visualise_internal_links(internal_links_map, pagerank):
    G = nx.DiGraph()

    # Add edges and nodes
    for page, links in internal_links_map.items():
        for link in links:
            G.add_edge(page, link)

    # Draw the graph
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)

    # Draw nodes, sized by PageRank
    node_size = [v * 10000 for v in pagerank.values()]  # Scale PageRank for visualisation
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="skyblue", alpha=0.8)

    # Draw edges
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10, edge_color="gray", alpha=0.7)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title("Internal Link Structure Visualised by PageRank")
    plt.show()

# Save report to CSV
def save_report(page_link_count, orphan_pages, pagerank, output_file="internal_link_report.csv"):
    df = pd.DataFrame(page_link_count.items(), columns=['Page', 'Internal Links Count'])
    df['PageRank'] = df['Page'].map(pagerank)
    df['Is Orphan'] = df['Page'].apply(lambda x: x in orphan_pages)
    df.sort_values(by='Internal Links Count', ascending=True, inplace=True)
    df.to_csv(output_file, index=False)
    print(f"Report saved to {output_file}")

# Main function
def main():
    # Sitemap URL
    sitemap_url = "https://psualatberat.com/sitemap_index.xml"  # Replace with your site's sitemap URL
    base_domain = urlparse(sitemap_url).netloc

    # Get URLs from sitemap (supports sitemapindex)
    sitemap_urls = get_sitemap_urls(sitemap_url)

    if not sitemap_urls:
        print("No URLs found in the sitemap.")
        return

    # Crawl the site based on the sitemap
    internal_links_map = crawl_sitemap(sitemap_urls, base_domain)

    # Analyse link structure
    page_link_count, orphan_pages = analyse_links(internal_links_map)

    # Compute PageRank
    pagerank = compute_pagerank(internal_links_map)

    # Visualise the internal link structure
    visualise_internal_links(internal_links_map, pagerank)

    # Save the results
    save_report(page_link_count, orphan_pages, pagerank)

if __name__ == "__main__":
    main()
