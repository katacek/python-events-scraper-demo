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
    # start the Actor, ensures proper initialization and cleanup when the script runs inside Apify
    async with Actor:
        # Retrieve the input object for the Actor. The structure of input is defined in input_schema.json.
        actor_input = await Actor.get_input() or {'url': 'https://www.python.org/events/'}
        url = actor_input.get('url')

        # Create an asynchronous HTTPX client for making HTTP requests.
        async with AsyncClient() as client:
            # Fetch the HTML content of the page, following redirects if necessary.
            Actor.log.info(f'Sending a request to {url}')
            response = await client.get(url, follow_redirects=True)

        # Defines a function to extract event details from the HTML response.
        def extract_event_data(html):
            # Parses the HTML using BeautifulSoup.
            soup = BeautifulSoup(html, 'html.parser')
            # Initializes an empty events list and sets a baseUrl for constructing full URLs.
            events = []
            baseUrl = 'https://www.python.org'
            
            # Finds all <li> elements inside .list-recent-events.menu
            for event in soup.select('.list-recent-events.menu li'):
                # Extract the event title <a> element.
                title_tag = event.select_one('.event-title a')
                # Extract the event date inside a <time> tag.
                date_tag = event.select_one('time')
                # Extract the event location.
                location_tag = event.select_one('.event-location')
                
                # Extracts text values and ensures they have default values ('N/A' if missing).
                title = title_tag.get_text(strip=True) if title_tag else 'N/A'
                url = title_tag['href'] if title_tag and 'href' in title_tag.attrs else 'N/A'
                date = date_tag.get_text(separator=' ', strip=True) if date_tag else 'N/A'
                location = location_tag.get_text(strip=True) if location_tag else 'N/A'
                # Constructs the full event URL by appending the relative href to baseUrl.
                fullUrl = f"{baseUrl}{url}" if url else 'N/A'
                
                # Adds the extracted data into the events list.
                events.append({
                    'title': title,
                    'url': fullUrl,
                    'date': date,
                    'location': location
                })
            
            return events
 
        # Calls the extract_event_data() function with the page’s HTML content.
        events = extract_event_data(response.content)

        # Saves the extracted event data to Apify’s dataset storage (like a database for structured data).
        await Actor.push_data(events)
