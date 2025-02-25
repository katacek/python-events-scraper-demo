## Readme overview
1. [Find upcoming Python events all around the world!](#introduction)
2. [Creating Actor](#createActor)
3. [Publishing Actor to Store](#publishing)
4. [Monetizing Actor](#monetizing)
5. [Creating Actor using CLI (command line interface)](#actorCLI)
6. [What next (useful links)](#next)

## Prerequisities
- [ ] Account on [Apify console](https://console.apify.com/): for creating Actor through web interface: 
- [ ] Node.js version 18 or higher with NPM installed: for using [Apify CLI](https://docs.apify.com/cli/docs/installation)
- [ ] Billing details and payment method set up: for Actor monetization

## Find upcoming Python events all around the world! <a name="introduction"></a>

We will try to find upcoming Python events all around the world, and the best website to find those is Python's official website.

Visit Python's official website events section: https://www.python.org/events/

<img width="1231" alt="Screenshot 2025-02-18 at 1 13 43 AM" src="https://github.com/user-attachments/assets/3fc38cb5-0e2d-4d3f-9210-1036e687cfe3" />

As you can see there are a lot of upcoming events there. We will try to scrape all the upcoming events with their dates and locations and make an Actor out of it, and, in the end, publish it to Apify Store so that anybody from the community can use it.

## Creating Actor <a name="createActor"></a>

1. Visit the page to be scraped and inspect it using browser developers tools (aka devTools)

- page: https://www.python.org/events/
- devTools: press **F12** or `Right-click` a page and select `Inspect`
- in the `Elements tab`, look for the [`selector`](https://docs.apify.com/academy/concepts/css-selectors) for the content we want to scrape
    - (In Firefox it's called the **Inspector**). You can use this tab to inspect the page's HTML on the left hand side, and its CSS on the right. The items in the HTML view are called [**elements**](https://docs.apify.com/academy/concepts/html-elements).
    - All elements are wrapped in the html tag such as <p> </p> for paragraph, <a /> for link, …
    - using the selector tool, find the selector: `.list-recent-events.menu li`for our case

<img width="1708" alt="Screenshot 2025-02-13 at 15 41 51" src="https://github.com/user-attachments/assets/7e9bb163-aab5-4909-92dd-bd2891b540a2" />

- you can test the selector the devtools directly, just put the `document.querySelector('.list-recent-events.menu li');` to the `Console tab` and see the result (it prints the first result)
- if you do `document.querySelectorAll()`, it shows all the given elements
- for filtering the happening ones, just do `document.querySelectorAll('.list-recent-events.menu li:not(.most-recent-events)');`
    - good selectors: **simple**, **human-readable**, **unique** and **semantically connected** to the data.

<img width="671" alt="Screenshot 2025-02-13 at 15 48 39" src="https://github.com/user-attachments/assets/bf664c29-299d-48fb-9980-228b19de655a" />

2. Create Actor from Apify templates
   
- Visit https://console.apify.com/actors/development/my-actors and click `Develop new` on the top right corner
- Under Python section, select `Start with Python` template
- Check the basic structure, information about the template, … and click `Use this template`
    - there are also links to various resources / tutorial videos
- name the actor 😁

3. Source code adjustments
   
- in the `main.py` , we are going to replace this part using the selectors we have found earlier
- first, change line 31 as well

```python
actor_input = await Actor.get_input() or {'url': 'https://www.python.org/events/'}
```

and the original

```python

# Parse the HTML content using Beautiful Soup and lxml parser.
soup = BeautifulSoup(response.content, 'lxml')


# Extract all headings from the page (tag name and text).
headings = []
for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
    heading_object = {'level': heading.name, 'text': heading.text}
    Actor.log.info(f'Extracted heading: {heading_object}')
    headings.append(heading_object)

# Save the extracted headings to the dataset, which is a table-like storage.
await Actor.push_data(headings)
```

by those

```python
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
```

- now, just hit the button `Save, Build & Start`
- the Actor starts and take you to the `Log` tab
- results are in the `Output tab`
    - can be exported in various formats
    - can be also seen in datasets

## Publishing Actor to Store <a name="publishing"></a>

- Go to [Apify Console](https://console.apify.com/) to Actor detail page
    - go to the `Publication tab`
    - fill in all the details
    - press `Publish to store`
    - check it out by clicking on `Store` (main menu on the left) -> search for the name of your Actor
- docs [here](https://docs.apify.com/platform/actors/publishing/publish)

<img width="1231" alt="Screenshot 2025-02-19 at 9 13 34" src="https://github.com/user-attachments/assets/67587ad1-176b-429d-b58d-292662a24a29" />


## Monetizing Actor <a name="monetizing"></a>

- at the `Actor detail` -> `Publication tab` open the `Monetization` card, follow the set up guide
- basic info [here](https://docs.apify.com/platform/actors/publishing/monetize)
- detailed info about pricing models [here](https://docs.apify.com/academy/get-most-of-actors/monetizing-your-actor)

## Creating Actor through CLI <a name="actorCLI"></a>

- general docs [here](https://docs.apify.com/platform/actors/development/quick-start/locally)

```python
brew install apify-cli // npm -g install apify-cli

apify create
```

- select name, Python and `Start with Python` template

<img width="930" alt="Screenshot 2025-02-13 at 17 08 09" src="https://github.com/user-attachments/assets/c745bb1b-7806-4471-b823-3222eb190267" />

```python
cd your-actor-name
```

- navigate to [main.py](http://main.py) and the same part of the code to be replaced
    - also the Actor.get_input() needs to be deleted

<img width="1526" alt="Screenshot 2025-02-13 at 17 19 04" src="https://github.com/user-attachments/assets/b152f80f-fd2e-443e-a99a-069382548985" />

- run `apify-run`  and see the results in `storage/dataset/default` folder 🚀

<img width="1046" alt="Screenshot 2025-02-13 at 17 29 37" src="https://github.com/user-attachments/assets/96020e54-b134-4058-a4ee-52603344f8a2" />


- push to apify platform

```python
apify login
apify push
```

<img width="722" alt="Screenshot 2025-02-13 at 17 35 32" src="https://github.com/user-attachments/assets/35f0315e-7fb7-4396-a0ce-5c6785ad8f76" />

Get you to the browser and see, it is there!

<img width="1720" alt="Screenshot 2025-02-13 at 17 36 31" src="https://github.com/user-attachments/assets/14303513-09ef-43dc-b861-99ab87cf4de6" />

## What next (useful links) <a name="next"></a>
Did you enjoy scraping and want to learn more? Just check out one of the following links
- [Apify web scraping academy](https://docs.apify.com/academy) and for python [here](https://docs.apify.com/academy/python)
- Step by step guide to extract data [here](https://docs.apify.com/academy/web-scraping-for-beginners/data-extraction/browser-devtools)
- Looking for some inspiration what to build? Check the [ideas page](https://apify.com/ideas)
- [Actor whitepaper](https://whitepaper.actor/)
- [Apify open source fair share program](https://apify.com/partners/open-source-fair-share)
- Create Actor from template [video](https://www.youtube.com/watch?v=u-i-Korzf8w&ab_channel=Apify)
- How to build and monetize Actors on Apify Store - Earn passive income from your scrapers [video](https://www.youtube.com/watch?v=4nxStxC1BJM&t=709s&ab_channel=Apify)
- Apify Discord [channel](https://discord.gg/jyEM2PRvMU)
- Apify Actors developers [page](https://apify.com/partners/actor-developers}

