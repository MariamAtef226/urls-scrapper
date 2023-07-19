import requests
import bs4

def get_urls(url, n):
    urls = []
    try:
        response = requests.get(url)
        html = bs4.BeautifulSoup(response.content, 'html.parser')
        all_links = html.find_all('a', href=True)
        for link in all_links:
            url = link['href']
            if ('http' in url or 'www' in url) and url not in urls:
                urls.append(url)

        if n > 1:
            temp = []
            for url in urls:
                more_urls = get_urls(url, n - 1)
                temp.extend(more_urls)
            urls.extend(temp)
    except:
        print("Failed to Access Page")
    finally:
        return urls


def main():
    url = input('Enter the URL: ')
    n = int(input('Enter search depth: '))
    print(url)
    print(n)
    urls = get_urls(url, n)
    print(urls)

if __name__ == '__main__':
    main()
