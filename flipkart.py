import requests
from bs4 import BeautifulSoup

def scrape_flipkart():
    url = "https://www.flipkart.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    unrealistic_products = []  # List to store unrealistic products

    while not unrealistic_products:  # Continue loop until at least one unrealistic product is found
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("div", {"class": "_1AtVbE"})
            for product in products:
                title = product.find("a", {"class": "IRpwTa"}).text.strip()
                price = product.find("div", {"class": "_30jeq3"}).text.strip()
                discounted_price = product.find("div", {"class": "_3I9_wc"}).text.strip()
                discount_percent = product.find("div", {"class": "_3Ay6Sb"}).text.strip()
                product_url = "https://www.flipkart.com" + product.find("a", {"class": "IRpwTa"})["href"]

                print("Title:", title)
                print("Price:", price)
                print("Discounted Price:", discounted_price)
                print("Discount Percent:", discount_percent)
                print("Product URL:", product_url)
                print()

                # Check for unrealistic offer - If discount percent is greater than 80%
                if float(discount_percent[:-1]) > 80:
                    print("Unrealistic offer detected!")
                    unrealistic_products.append({
                        "title": title,
                        "discount_percent": discount_percent,
                        "product_url": product_url
                    })

            if not unrealistic_products:  # If no unrealistic products found, print message and retry
                print("No unrealistic products found. Retrying...")
        else:
            print("Failed to retrieve data from Flipkart. Retrying...")

    return unrealistic_products

if __name__ == "__main__":
    unrealistic_products = scrape_flipkart()
    print("Scraping completed.")

    # Printing unrealistic products
    print("\nUnrealistic Products:")
    for product in unrealistic_products:
        print(f"Product: {product['title']}, Discount Percent: {product['discount_percent']}, Product URL: {product['product_url']}")
