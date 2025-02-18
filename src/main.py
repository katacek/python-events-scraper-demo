"""This module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

# Beautiful Soup - A library for pulling data out of HTML and XML files. Read more at:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc
from bs4 import BeautifulSoup

# HTTPX - A library for making asynchronous HTTP requests in Python. Read more at:
# https://www.python-httpx.org/
from httpx import AsyncClient

# Apify SDK - A toolkit for building Apify Actors. Read more at:
# https://docs.apify.com/sdk/python
from apify import Actor


async def main() -> None:
    """Main entry point for the Apify Actor.

    This coroutine is executed using `asyncio.run()`, so it must remain an asynchronous function for proper execution.
    Asynchronous execution is required for communication with Apify platform, and it also enhances performance in
    the field of web scraping significantly.
    """
    async with Actor:
        # Retrieve the input object for the Actor. The structure of input is defined in input_schema.json.
        actor_input = {'url': 'https://www.python.org/events/'}
        url = actor_input.get('url')

        # Create an asynchronous HTTPX client for making HTTP requests.
        async with AsyncClient() as client:
            # Fetch the HTML content of the page, following redirects if necessary.
            Actor.log.info(f'Sending a request to {url}')
            response = await client.get(url, follow_redirects=True)

        # Parse the HTML content using Beautiful Soup and lxml parser.
        soup = BeautifulSoup(response.content, 'lxml')

        def extract_event_data(html):
            soup = BeautifulSoup(html, 'html.parser')
            events = []
            baseUrl = 'https://www.python.org'
            
            for event in soup.select('.list-recent-events.menu li'):
                title_tag = event.select_one('.event-title a')
                date_tag = event.select_one('time')
                location_tag = event.select_one('.event-location')
                
                title = title_tag.get_text(strip=True) if title_tag else 'N/A'
                url = title_tag['href'] if title_tag and 'href' in title_tag.attrs else 'N/A'
                fullUrl = f"{baseUrl}{url}" if url else 'N/A'
                date = date_tag.get_text(separator=' ', strip=True) if date_tag else 'N/A'
                location = location_tag.get_text(strip=True) if location_tag else 'N/A'
                
                events.append({
                    'title': title,
                    'url': fullUrl,
                    'date': date,
                    'location': location
                })
            
            return events
 
        # Extract all events from the page including basic info
        events = extract_event_data(response.content)

        

        # Save the extracted headings to the dataset, which is a table-like storage.
        await Actor.push_data(events)