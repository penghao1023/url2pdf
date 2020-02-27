import asyncio
from pathlib import Path
from pyppeteer import launcher

WIDTH = 1080
HEIGHT = 1920


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
    await page.pdf(path=path.joinpath(f'{title}.pdf)'))
    await page.close()


async def main():
    browser = await launcher.launch(args=[
        "--no-sandbox",
        '--disable-setuid-sandbox',
    ])
    path = Path('data')
    path.mkdir(parents=True, exist_ok=True)
    # urls = [each.strip() for each in ','.join(open('work1.csv').readlines()).split(',') if each[:4] == 'http']
    urls = ['https://mp.weixin.qq.com/s/YsyTsma8tGXRgBwhpnWAuA']
    try:
        await asyncio.gather(*(deal(browser, path, url) for url in urls))
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
