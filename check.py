from pathlib import Path
from json import load


if __name__ == '__main__':
    data = load(open('source.json'))
    for name, urls in data.items():
        if urls and len(urls) != len(set(urls)) and urls[0]:
            print(name)
        try:
            total = ' '.join(map(str, Path('data/' + name).iterdir()))
        except:
            continue
        for url in urls:
            if url.split('/')[-1] not in total:
                print(url)
