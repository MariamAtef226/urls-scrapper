import requests
import bs4
import tkinter as tk


def get_urls(url, n):
    urls = []
    try:
        response = requests.get(url) # start request
        html = bs4.BeautifulSoup(response.content, 'html.parser') # get html content
        all_links = html.find_all('a', href=True) # extract the anchor tags only
        for link in all_links:
            url = link['href'] # extract the href attribute value
            if ('http' in url or 'www' in url) and url not in urls: # extract valid links and unique one for this depth
                urls.append(url)

        if n > 1: # base case
            temp = []
            for url in urls:
                more_urls = get_urls(url, n - 1) # dive into next depth
                temp.extend(more_urls)
            urls.extend(temp) # used extend not append to merge the 2 lists
    except:
        print("Failed to Access Page") # handle exceptions due to failing to access some links
        # due to connection timeout or unauthorised access
    finally:
        return urls


def main():
    # gui
    root = tk.Tk()
    root.title("URLs Scrapper")

    url_label = tk.Label(root, text="Enter the URL:")
    url_label.grid(row=0, column=0)

    url_entry = tk.Entry(root)
    url_entry.grid(row=0, column=1)

    depth_label = tk.Label(root, text="Enter the search depth:")
    depth_label.grid(row=1, column=0)

    depth_entry = tk.Entry(root)
    depth_entry.grid(row=1, column=1)

    start_button = tk.Button(root, text="Start", command= lambda: search(url_entry.get(), int(depth_entry.get())))
    start_button.grid(row=2, column=0)

    root.mainloop()


def search(url, n):
    result = tk.Tk()
    result.title("Results")
    urls_list = tk.Text(result, height=1000, width=1000)
    urls_list.grid(row=1, column=0, columnspan=2)

    urls = get_urls(url, n)

    for url in urls:
        urls_list.insert(tk.END, url + '\n')

    result.mainloop()


if __name__ == "__main__":
    main()
