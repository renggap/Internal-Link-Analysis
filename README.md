# SEO Internal Linking Analysis Script

I recently came across an interesting SEO tool called "Internal Linking Analysis," originally created by **Warren Hance** and shared on [LinkedIn](https://www.linkedin.com/posts/warren-hance-86869b122_new-python-script-for-seo-internal-link-activity-7242452206229057537-JGTv?utm_source=share&utm_medium=member_desktop).

Inspired by his work, I decided to fork the script and enhance it with some new functionalities. With the help of AI, I've expanded its capabilities to provide even more insights into website structure and internal linking strategies.

This Python script can be a valuable asset for SEO professionals looking to optimize their site's architecture and improve user navigation.

## Purpose:

1. **Crawl the Website:** It starts from a given URL, and recursively fetches internal links up to a defined depth (default is 3 levels).
2. **Analyze Link Structure:** It analyzes the relationships between pages, identifies "orphan" pages (those with no incoming links), and calculates the number of links per page.
3. **Compute PageRank:** Using the networkx library, it computes the PageRank of each page, which is a measure of the importance of the page based on the link structure (similar to how Google ranks pages).
4. **Visualize the Structure:** It visualizes the internal link structure using a directed graph where nodes represent pages and arrows represent links between them, with node size determined by their PageRank.
5. **Generate a Report:** It saves the analysis, including PageRank scores, link counts, and orphan pages, into a CSV report.

## Added Features:

**[0.2]**
*   Use sitemap URL instead of root domain to prevent crawling unnecessary URLS, eg: pagination, fragment URLs, etc
*   Prevent crawling of images
* Prevent crawling of slugs that contain: /tag/, /category/, and /author/


---

Regards,

Rengga Putra (rengga@neodigital.co.id / hey@rengga.my.id)
