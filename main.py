import asyncio
from pathlib import Path
from pyppeteer import launcher
from tqdm import tqdm

WIDTH = 1080
HEIGHT = 1920


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


async def deal(browser, path, url):
    page = await browser.newPage()
    await page.setViewport({
        "width": WIDTH,
        "height": HEIGHT
    })
    await page.goto(url)
    element = await page.querySelector('#activity-name')
    title = await page.evaluate('(e) => e.textContent', element)
    title = title.strip()
    await page.waitFor(2000)
    height = await page.evaluate("()=> document.body.scrollHeight")
    for i in range(height // HEIGHT + 1):
        await page.evaluate("(height)=>{window.scrollBy(0, height);}", HEIGHT)
        await page.waitFor(500)
    await page.pdf(path=path.joinpath(f'{title}.pdf'))
    await page.close()


async def main():
    browser = await launcher.launch(args=[
        "--no-sandbox",
        '--disable-setuid-sandbox',
    ])
    path = Path('data')
    path.mkdir(parents=True, exist_ok=True)
    urls = [each.strip() for each in ','.join(open('work1.csv').readlines()).split(',') if each[:4] == 'http']
    # urls = ['https://mp.weixin.qq.com/s/YsyTsma8tGXRgBwhpnWAuA',
    #         'https://mp.weixin.qq.com/s/7OFhT0H2PckaxNMriOUp6g']
    # await asyncio.gather(*(deal(browser, path, url) for url in urls))
    try:
        for url in tqdm(urls):
            try:
                task = asyncio.create_task(deal(browser, path, url))
                await task
            except:
                print('[ERROR] Failed to deal', url)
    finally:
        await browser.close()


if __name__ == '__main__':
    patch_pyppeteer()
    asyncio.run(main())
