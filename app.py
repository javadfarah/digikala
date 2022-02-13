import asyncio
from playwright.async_api import async_playwright
import re
from lxml import html
import datetime
from model import Database
import logging
import os

#change the database uri 
mydb = Database(f'mongodb://{os.environ["MONGODB_USERNAME"]}:{os.environ["MONGODB_PASSWORD"]}@{os.environ["MONGODB_HOSTNAME"]}:27017/')

async def worker(context, url: str):
    page = await context.new_page()
    page.set_default_timeout(180000)
    page.set_default_navigation_timeout(180000)
    await page.goto(url, timeout=0)
    await page.locator('//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]/div/h1').wait_for()
    product_star = page.locator('//div[@class="d-none d-block-lg ml-12 left-0 pos-sticky"]/div[@class="d-flex ai-center"]/p[1]')
    product_qualities = await page.query_selector_all('//div[@class="d-flex ai-center bg-color-neutral-600 mr-auto"]/p[@class="text-body-2"]')
    quality_construction = await product_qualities[0].text_content()
    purchase_value = await product_qualities[1].text_content()
    innovation = await product_qualities[2].text_content()
    features = await product_qualities[3].text_content()
    ease_of_use = await product_qualities[4].text_content()
    design = await product_qualities[5].text_content()
    product_star = await product_star.all_text_contents()
    product_star = product_star[0]
    query = dict(time=datetime.datetime.now(), link=url, quality_construction=quality_construction, purchase_value=purchase_value, innovation=innovation,
                 features=features, ease_of_use=ease_of_use, design=design, product_star=product_star)
    # save post details
    mydb.insert_query(query=query, db_name='digikala', col_name='product_detail')

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        host = "https://www.digikala.com"
        product_pre = "https://www.digikala.com/product"

        context = await browser.new_context()
        # Open new page
        page = await context.new_page()
        # set 90 seconds timeout for poor connections
        page.set_default_timeout(90000)
        page.set_default_navigation_timeout(90000)
        # Go to https://www.digikala.com/search/category-mobile-phone/
        await page.goto("https://www.digikala.com/search/category-mobile-phone/", timeout=90000)
        await page.locator(
            "//html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div/section[1]/div[2]/div[1]/div/div[1]/article").wait_for()
        result = html.fromstring(await page.content())

        products = result.xpath("//article/a")
        product_links = []
        for product in products:
            image = product.xpath(".//img[not(contains(@data-src, '.svg'))][1]")
            if image:
                image = image[0].get("data-src")
            try:
                title = product.xpath(".//h2//text()")[0]
                link = product.get("href")
                link = re.search("\/product\/(dkp-\d*)\/", link).group(1)
            except AttributeError as error:
                # some times this xpath catch non-product objects its not problem we will pass
                logging.error(error)
                continue
            except IndexError as error:
                logging.error(error)
                continue
            url = f"{product_pre}/{link}"
            query = {"link": url, "image": image, "title": title}
            res = mydb.search_query(query={"link": url}, db_name='digikala', col_name='products')
            # check for duplicate data
            if not res:
                mydb.insert_query(query=query, db_name='digikala', col_name='products')
            product_links.append(url)

        await asyncio.wait(
            [asyncio.create_task(worker(context, url)) for url in product_links],
            return_when=asyncio.ALL_COMPLETED,
        )
        await browser.close()


asyncio.run(main())
