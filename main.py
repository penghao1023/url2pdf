import asyncio
from pathlib import Path
from pyppeteer import launcher
from tqdm import tqdm
from json import load

WIDTH = 1080
HEIGHT = 4000


def patch_pyppeteer():
    """
    This function is copied from https://github.com/miyakogi/pyppeteer/pull/160#issuecomment-448886155
    This is a bug about chromium, and here is a simple method to temporarily fix it
    """
    import pyppeteer.connection
    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method


async def deal(path, url):
    browser = await launcher.launch(args=[
        "--no-sandbox",
        '--disable-setuid-sandbox',
    ])
    page = await browser.newPage()
    await page.setViewport({
        "width": WIDTH,
        "height": HEIGHT
    })
    await page.goto(url)
    element = await page.querySelector('#activity-name')
    title = await page.evaluate('(e) => e.textContent', element)
    title = title.strip()
    await page.waitFor(1400)
    height = await page.evaluate("()=> document.body.scrollHeight")
    for i in range(2 * height // HEIGHT + 1):
        await page.evaluate("(height)=>{window.scrollBy(0, height);}", HEIGHT >> 1)
        await page.waitFor(300)
    await page.pdf(path=path.joinpath(f'{title}__{url.split("/")[-1]}.pdf'))
    await page.close()
    await browser.close()


async def main():
    parent = Path('data')
    data = [(name, url) for name, urls in load(open('source.json')).items() for url in urls ]
    for name, url in tqdm(data):
        path = parent.joinpath(name)
        path.mkdir(parents=True, exist_ok=True)
        try:
            task = asyncio.create_task(deal(path, url))
            await task
        except:
            print('[ERROR] Failed to deal', url)


if __name__ == '__main__':
    patch_pyppeteer()
    asyncio.run(main())
