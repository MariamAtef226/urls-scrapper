import requests
import bs4

def get_urls(url, n):
    urls = []
    try:
        response = requests.get(url) # start connection
        html = bs4.BeautifulSoup(response.content, 'html.parser')  # get html content
        all_links = html.find_all('a', href=True) # extract the anchor tags only
        for link in all_links:
            url = link['href'] # extract the href attribute value
            if ('http' in url or 'www' in url) and url not in urls: # extract valid links and unique one for this depth
                urls.append(url)

        if n > 1:
            temp = []
            for url in urls:
                more_urls = get_urls(url, n - 1)  # dive into next depth
                temp.extend(more_urls)
            urls.extend(temp) # used extend not append to merge the 2 lists
    except:
        print("Failed to Access Page") # handle exceptions due to failing to access some links
        # due to connection timeout or unauthorised access
    finally:
        return urls


def main():
    url = input('Enter the URL: ')
    n = int(input('Enter search depth: '))
    urls = get_urls(url, n)
    print(urls)

if __name__ == '__main__':
    main()
