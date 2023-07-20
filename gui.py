import bs4
import asyncio
import aiohttp
import tkinter as tk


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
        all_links = html.find_all('a', href=True)  # extract the anchor tags only
        for link in all_links:
            url = link['href']  # extract the href attribute value
            if ('http' in url or 'www' in url) and url not in urls:  # extract valid links and unique one for this depth
                urls.append(url)

        if n > 1:  # base case for recursion
            tasks = [get_urls(url, n - 1, session) for url in
                     urls]  # list of coroutine objects of get_urls func for each sublink
            innerURLs = await asyncio.gather(
                *tasks)  # concurrently wait for all the coroutines to complete to fetch urls in next depth in parallel.
            for url in innerURLs:
                urls.extend(url)
    except:
        print("Failed to Access Page")  # handle exceptions due to any reasons
    finally:
        return urls


async def scrapper(url_entry, depth_entry):
    async with aiohttp.ClientSession() as session:
        result = tk.Tk()
        result.title("Results")
        urls_list = tk.Text(result, height=1000, width=1000)
        urls_list.grid(row=1, column=0, columnspan=2)
        url = url_entry.get()
        n = int(depth_entry.get())
        urls = await get_urls(url, n, session)
        urls_list.insert(tk.END, f"Number of returned links: {len(urls)}\n")
        for url in urls:
            urls_list.insert(tk.END, url + '\n')
        result.mainloop()


async def rest_of_the_system():
    while True:
        await asyncio.sleep(1)
        print("Other programs running ...")


async def main(url_entry, depth_entry):
    await asyncio.gather(scrapper(url_entry, depth_entry), rest_of_the_system())

def create_gui():
    root = tk.Tk()
    root.title("URL Scrapper")

    url_label = tk.Label(root, text="Enter the URL:")
    url_label.pack()
    url_entry = tk.Entry(root)
    url_entry.pack()

    depth_label = tk.Label(root, text="Enter search depth:")
    depth_label.pack()
    depth_entry = tk.Entry(root)
    depth_entry.pack()

    start_button = tk.Button(root, text="Start", command=lambda: asyncio.run(main(url_entry, depth_entry)))
    start_button.pack()

    root.mainloop()

if __name__ == '__main__':
    create_gui()


# # test data:
#
# # http://www.wikipedia.org/