import requests
from bs4 import BeautifulSoup


def search_flipkart(product_name):
    base_url = "https://www.flipkart.com"
    search_url = f"{base_url}/search?q={product_name}"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract product information from the search results
    # Customize this part based on the actual structure of the website
    product_links = soup.find_all('a', {'class': '_1fQZEK'})

    if product_links:
        first_product_url = base_url + product_links[0]['href']
        product_info_flipkart = scrape_product_info_flipkart(first_product_url)
        return product_info_flipkart
    else:
        return None


def scrape_product_info_flipkart(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract relevant product information from the product page
    # Customize this part based on the actual structure of the website
    product_title_element = soup.find('span', {'class': 'B_NuCI'})
    product_price_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})

    # Extracting reviews
    reviews = []
    review_elements = soup.find_all('div', {'class': '_1AtVbE'})
    for review_element in review_elements:
        review_text = review_element.find('div', {'class': 't-ZTKy'})
        if review_text:
            reviews.append(review_text.get_text().strip())
        else:
            reviews.append("N/A")

    # Extracting additional details
    product_rating_element = soup.find('div', {'class': '_3LWZlK'})
    product_specifications_element = soup.find('div', {'class': '_1UhVsV'})

    product_title = product_title_element.get_text().strip() if product_title_element else "N/A"
    product_price = product_price_element.get_text().strip() if product_price_element else "N/A"
    product_rating = product_rating_element.get_text().strip() if product_rating_element else "N/A"
    product_specifications = product_specifications_element.get_text().strip() if product_specifications_element else "N/A"

    # Extract seller information
    seller_info_element = soup.find('div', {'class': '_3HGjxn'})
    seller_info = seller_info_element.get_text().strip() if seller_info_element else "N/A"

    print("\nFlipkart Product Information:")
    print(f"Title: {product_title}")
    print(f"Price: {product_price}")
    print(f"Rating: {product_rating}")
    print(f"Specifications: {product_specifications}")
    print(f"Seller Information: {seller_info}")
    print(f"URL: {product_url}")

    print("\nReviews:")
    for i, review in enumerate(reviews, 1):
        print(f"Review {i}: {review}")

    # Return the information as a dictionary if needed
    product_info = {
        'title': product_title,
        'price': product_price,
        'rating': product_rating,
        'specifications': product_specifications,
        'seller_info': seller_info,
        'url': product_url,
        'reviews': reviews
        # Add more fields as needed
    }

    return product_info


# Example usage
product_name = "poco x4"
flipkart_result = search_flipkart(product_name)

if flipkart_result:
    print("\nComplete Flipkart Product Information:")
    print(flipkart_result)
