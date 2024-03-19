import requests
from bs4 import BeautifulSoup, NavigableString
from fake_useragent import UserAgent


def get_page_info(url):
    try:
        # Send a request to the URL
        # headers = {'User-Agent': UserAgent().random}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Set response encoding if needed (sometimes needed for correct character display)
        response.encoding = response.apparent_encoding

        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def extract_novel_info(li_elements):
    novel_info = []

    for element in li_elements:
        # Extract text and add to the list
        a_tag = element.find('a')

        # Check if a_tag is not None
        if a_tag:
            title = element.get_text(strip=True)
            href = a_tag['href']
            novel_info.append({"title": title, "href": href})

    return novel_info


def extract_content(novel_info):
    novel_content = []
    for info in novel_info:
        if info["title"] and info["href"]:
            novel_url = info["href"]
            title, soup = get_page_info(novel_url)

            text = ''
            for br in soup.find_all('br'):
                next_s = br.nextSibling
                if not (next_s and isinstance(next_s, NavigableString)):
                    continue
                next2_s = next_s.nextSibling
                if next2_s and next2_s.name == 'br':
                    text += next_s.strip()
            novel_content.append({"title": info["title"], "content": text})
    return novel_content


def generate_txt(filename, novel_content):
    with open(filename, "a", encoding='utf-8') as file:
        for i in novel_content:
            file.write(i["title"])
            file.write(i["content"])


def run_code(url, filename):
    soup = get_page_info(url)
    print("get page info successful")
    lists = soup.find_all("li")
    novel_infos = extract_novel_info(lists)
    print("get novel info successful")
    novel_contents = extract_content(novel_infos)
    print("get page content successful")
    generate_txt(filename, novel_contents)
    print("generate txt successful")


if __name__ == '__main__':
    run_code('https://www.69shu.pro/book/53686/', "只想让玩家省钱的我却被氪成首富")