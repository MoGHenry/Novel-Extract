import requests
import unicodedata
from bs4 import BeautifulSoup, NavigableString
from fake_useragent import UserAgent
import time
import random


def convert_fullwidth_to_halfwidth(text):
    return unicodedata.normalize('NFKC', text)


def get_page_info(url):
    try:
        # Send a request to the URL
        headers = {'User-Agent': UserAgent().random}
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
        # Chrome/122.0.0.0 Safari/537.36'}
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
            if title and href and href != "#":
                novel_info.append({"title": convert_fullwidth_to_halfwidth(title), "href": href})

    return novel_info


def cleanup(html_content):
    if html_content is None:
        return ""
    # Extract text and remove unnecessary whitespace
    return html_content.get_text(separator='\n').strip()


def remove_before_second_occurrence(text, substring):
    # Find the first occurrence of the substring
    first_occurrence = text.find(substring)
    if first_occurrence == -1:
        return text

    second_occurrence = text.find(substring, first_occurrence + 1)
    if second_occurrence == -1:
        return text[first_occurrence:]

    # Return the text from the second occurrence onwards
    return text[second_occurrence:]


def extract_content(novel_info):
    novel_content = []
    i = 0
    for info in novel_info[30:31]:
        novel_url = info["href"]
        soup = get_page_info(novel_url)

        text = soup.find(class_="txtnav")
        text = cleanup(text)
        print(text)
        text = remove_before_second_occurrence(text, "\u2003\u2003")
        text = text.replace("\u2003\u2003", "")
        text = text.replace("\n\n", "\n")
        print(text)

        novel_content.append({"title": info["title"], "content": text})
        i = i+1
        print(info["title"], f"--- ({i}/{len(novel_info)})finished")
        sleep_time = random.uniform(0.5, 1.5)
        time.sleep(sleep_time)
    return novel_content


def generate_txt(filename, novel_content):
    with open(filename+".txt", "a", encoding='utf-8') as file:
        for i in novel_content:
            file.write(i["title"]+"\n")
            file.write(i["content"]+"\n")


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
    # run_code('https://www.69shu.pro/book/53686/', "只想让玩家省钱的我却被氪成首富")
    run_code('https://www.otcwuxi.com/chapter/57212741111/', "我全点了掉宝率2")
