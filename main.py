import requests
from bs4 import BeautifulSoup

url = "https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd?cena_d_from=400&cena_d_to=600&cena_d_unit=4&oglasivac_nekretnine_id_l=387237&nacin_placanja_id_l=387273"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# <h3 class="product-title"><a href="/nekretnine/izdavanje-stanova/stan-u-zemunu/5425642473977?kid=4&amp;sid=1667673896783">Stan u Zemunu</a></h3>

links = soup.find_all("h3", class_="product-title")
print(len(links))

result = []

for link in links:
    result.append({"url": f"www.halooglasi.com{link.find('a').attrs['href']}"})

for i in result:
    print(i)