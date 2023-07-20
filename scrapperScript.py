import bs4
import asyncio  # for asynchronous programming
import aiohttp  # instead of requests since request.get() is sync function that blocks the action


async def fetch_url(session, url):
    try:
        async with session.get(url) as response:  # the returned response object is assigned to variabl eresponse
            if response.status == 200:
                return await response.text()  # return text of response (html and other data)
    except:
        print(f"Failed to Access Page: {url}")  # handle exceptions due to failing to access some links
        # due to connection timeout or unauthorised access or unavailable pages ... etc.
    return None


async def get_urls(url, n, session):
    urls = []
    try:
        response = await fetch_url(session, url)  # start connection
        if not response:
            return urls
        html = bs4.BeautifulSoup(response, 'html.parser')  # get html content
        all_links = html.find_all('a', href=True) # extract the anchor tags only
        for link in all_links:
            url = link['href']  # extract the href attribute value
            if ('http' in url or 'www' in url) and url not in urls:  # extract valid links and unique one for this depth
                urls.append(url)

        if n > 1:  # base case for recursion
            tasks = [get_urls(url, n - 1, session) for url in urls]  # list of coroutine objects of get_urls func for each sublink
            innerURLs = await asyncio.gather(*tasks)  # concurrently wait for all the coroutines to complete to fetch urls in next depth in parallel.
            for url in innerURLs:
                urls.extend(url)
    except:
        print("Failed to Access Page")  # handle exceptions due to any reasons
    finally:
        return urls


async def scrapper():
    async with aiohttp.ClientSession() as session:
        url = input('Enter the URL: ')
        n = int(input('Enter search depth: '))
        urls = await get_urls(url, n, session)
        print(urls)
        print("Number of returned links: ", len(urls))


async def rest_of_the_system():
    while True:
        await asyncio.sleep(1)
        print("Other programs running ...")


async def main():
    await asyncio.gather(scrapper(), rest_of_the_system())  # runs them both concurrently


if __name__ == '__main__':
    asyncio.run(main())


# test data:

# http://www.wikipedia.org/
