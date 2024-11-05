#!/usr/bin/env python3
import requests, csv
from selectolax.parser import HTMLParser


def get_html_from(base_url):
    print(f"[+] Navigating to {base_url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}
    res = requests.get(url=base_url, headers=headers)
    print("[+] Navigation done!")
    return res.text


def extract_data_from(given_html):
    print("[+] Starting data extraction.")
    tree = HTMLParser(html=given_html)
    products = tree.css("li.type-product")
    data = []
    for product in products:
        item = {"name": product.css_first("a h2").text(strip=True),
                "price": product.css_first("li.type-product span.amount").text(),
                "sku": product.css_first("li.type-product a.button").attributes["data-product_sku"]}
        data.append(item)
    print("[+] Extracting data done!")
    return data


def save_data_to(csv_file, data):
    print(f"[+] Saving data to {csv_file}...")
    header = data[0].keys()
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

    print("[+] Saving data done!")


if __name__ == "__main__":
    total = []
    for i in range(15):
        url = f"https://gopher1.extrkt.com/?paged={i + 1}"
        html = get_html_from(base_url=url)
        d = extract_data_from(given_html=html)
        total += d
    print(total)
    save_data_to(csv_file="result.csv", data=total)
