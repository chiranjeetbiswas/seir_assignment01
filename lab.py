import requests
from bs4 import BeautifulSoup as bs
import sys


# -----------------------------
# Extract body, title and links
# -----------------------------
def get_body_title_link(response):
    soup = bs(response.text, "html.parser")

    # Extract body text
    body = soup.body.get_text() if soup.body else ""

    clean_body = ""
    for char in body:
        if char.isalnum():
            clean_body += char.lower()
        else:
            clean_body += " "

    # Extract title
    title = soup.title.string.strip() if soup.title else ""

    # Extract links
    links = []
    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href:
            links.append(href)

    return clean_body, title, links


# -----------------------------
# Word Frequency with Stopwords
# -----------------------------
def word_count(text):
    words = text.split()
    word_frequency = {}

    stopwords = [
        "the", "is", "am", "are", "not", "a", "very",
        "and", "or", "in", "on", "at", "of", "to", "for",
        "with", "as", "by", "that", "this", "it"
    ]

    for word in words:
        if word in stopwords:
            continue

        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1

    return word_frequency


# -----------------------------
# 64-bit Polynomial Rolling Hash
# -----------------------------
def Hash(word, p=53, m=2**64):
    hash_value = 0
    power = 1

    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % m
        power = (power * p) % m

    return hash_value


# -----------------------------
# Compute SimHash
# -----------------------------
def compute_simhash(word_frequency):
    vector = [0] * 64

    for word, freq in word_frequency.items():
        hash_value = Hash(word)

        for i in range(64):
            bit = (hash_value >> i) & 1

            if bit == 1:
                vector[i] += freq
            else:
                vector[i] -= freq

    # Convert vector to final 64-bit integer
    simhash_code = 0

    for i in range(64):
        if vector[i] > 0:
            simhash_code |= (1 << i)

    return simhash_code


# -----------------------------
# Compare Two Pages
# -----------------------------
def compare_two_page(url_1, url_2):

    response1 = requests.get(url_1)
    response2 = requests.get(url_2)

    body1, title1, links1 = get_body_title_link(response1)
    body2, title2, links2 = get_body_title_link(response2)

    word_freq1 = word_count(body1)
    word_freq2 = word_count(body2)

    simhash_code1 = compute_simhash(word_freq1)
    simhash_code2 = compute_simhash(word_freq2)

    # Hamming Distance using XOR
    xor_value = simhash_code1 ^ simhash_code2
    different_bits = bin(xor_value).count("1")
    common_bits = 64 - different_bits

    return common_bits


# -----------------------------
# Main Execution
# -----------------------------


if len(sys.argv) < 3:
    print("Usage: python file.py <url1> <url2>")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

result = compare_two_page(url1, url2)

print("Common Bits:", result)