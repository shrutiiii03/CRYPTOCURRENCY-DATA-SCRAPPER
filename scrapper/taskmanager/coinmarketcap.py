from bs4 import BeautifulSoup
import requests


class CoinMarketCap:
    def __init__(self, coin):
        self.coin = coin

    def make_request(self):
        url = f"https://coinmarketcap.com/currencies/{self.coin}"
        response = requests.get(url)
        return response.content

    def extract_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        data = {
            "coin": self.coin,
            "price": self.extract_price(soup),
            "price_change": self.extract_price_change(soup),
            "market_cap": self.extract_market_cap(soup),
            "market_cap_rank": self.extract_market_cap_rank(soup),
            "volume": self.extract_volume(soup),
            "volume_rank": self.extract_volume_rank(soup),
            "volume_change": self.extract_volume_change(soup),
            "circulating_supply": self.extract_circulating_supply(soup),
            "total_supply": self.extract_total_supply(soup),
            "diluted_market_cap": self.extract_diluted_market_cap(soup),
            "contracts":self.extract_contracts(soup),
            "official_links": self.extract_official_links(soup),
            "socials": self.extract_social_links(soup)
        }
        # formatted_output = "\n".join(f"{key}: {value}" for key, value in data.items() if value is not None)  
           # return formatted_output
        return data
        
    def clean_price_change(self, price_change):
        """ Remove $ part from the price change."""
        return price_change.split('$')[0]

    def clean_market_cap(self, market_cap):
        """Remove percentage part from market cap."""
        return market_cap.split('%')[-1].strip()
    
    def clean_volume(self, volume):
        """Remove percentage part from vol."""
        return volume.split('%')[-1].strip() 
    
    def extract_price(self, soup):
        price_element = soup.find('span', class_='sc-d1ede7e3-0 fsQm base-text')
        if price_element:
            price = price_element.text.strip().replace('$', '').replace(',', '')
            return price
        return None

    def extract_price_change(self, soup):
        price_change_tag = soup.find("dd", class_="sc-d1ede7e3-0 hPHvUM base-text")
        if price_change_tag:
            return self.clean_price_change(price_change_tag.text.strip())
        return None

    def extract_market_cap(self, soup):
     market_cap_tag = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')[0]  # Assuming market cap is the first
     if market_cap_tag:
        return self.clean_market_cap(market_cap_tag.text.strip())
     return None
    
    def extract_market_cap_rank(self, soup):
        market_cap_rank_tag = soup.find('span', class_='text slider-value rank-value')
        if market_cap_rank_tag:
            return market_cap_rank_tag.text.strip()
        return None

    def extract_volume(self, soup):
        volume_tag = soup.find_all("dd", class_="sc-d1ede7e3-0 hPHvUM base-text")[1]
        if volume_tag:
            return self.clean_volume(volume_tag.text.strip())
        return None

    def extract_volume_rank(self, soup):
    # Find all elements with the shared parent class
      rank_elements = soup.find_all("div", class_="sc-d1ede7e3-0 sc-c6f90d42-3 bwRagp kLKyoa BasePopover_base__tgkdS")
    
      if rank_elements and len(rank_elements) > 1:
        # The second occurrence is assumed to be the volume rank
        volume_rank_tag = rank_elements[1].find("span", class_="text slider-value rank-value")
        if volume_rank_tag:
            return volume_rank_tag.text.strip()
      return None

    def extract_volume_change(self, soup):
     volume_change_tag = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')[2]  # Assuming volume change is the third
     if volume_change_tag:
        return volume_change_tag.text.strip()
     return None

    def extract_circulating_supply(self, soup):
        circulating_supply_tag = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')[3]
        if circulating_supply_tag:
            return circulating_supply_tag.text.strip()
        return None

    def extract_total_supply(self, soup):
        total_supply_tag = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')[4]
        if total_supply_tag:
            return total_supply_tag.text.strip()
        return None

    def extract_diluted_market_cap(self, soup):
        diluted_market_cap_tag = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')[6]
        if diluted_market_cap_tag:
            return diluted_market_cap_tag.text.strip()
        return None
 
    def extract_contracts(self, soup):
        contracts = []
        contracts_header = soup.find("span", text="Contracts")
        if contracts_header:
            contracts_div = contracts_header.find_parent("div").find_next_sibling("div")
            if contracts_div:
                contracts_tags = contracts_div.find_all("a", rel="nofollow noopener")
                for tag in contracts_tags:
                    contracts.append({
                        "name": tag.text.strip(),
                        "link": tag['href']
                    })
        return contracts if contracts else None

    def extract_official_links(self, soup):
        official_links = []
        official_links_divs = soup.find_all("div", class_="sc-d1ede7e3-0 sc-7f0f401-2 bwRagp kXjUeJ")
        
        contracts = self.extract_contracts(soup)
        index = 1 if contracts else 0  # Adjust index based on contracts
        
        if len(official_links_divs) > index:
            official_links_div = official_links_divs[index]
            official_link_tags = official_links_div.find_all("a", rel="nofollow noopener")
            for tag in official_link_tags:
                official_links.append({
                    "name": tag.text.strip(),
                    "link": tag['href']
                })
        
        return official_links

    def extract_social_links(self, soup): 
        social_links = []
        social_links_divs = soup.find_all("div", class_="sc-d1ede7e3-0 sc-7f0f401-2 bwRagp kXjUeJ")
        
        contracts = self.extract_contracts(soup)
        index = 2 if contracts else 1  # Adjust index based on contracts
        
        if len(social_links_divs) > index:
            social_links_div = social_links_divs[index]
            social_media_tags = social_links_div.find_all("a", rel="nofollow noopener")
            for tag in social_media_tags:
                social_links.append({
                    "name": tag.text.strip(),
                    "url": tag['href']
                })
        
        return social_links
