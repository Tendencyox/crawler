import requests
from lxml import etree



class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.base_url = 'https://github.com'
        self.session = requests.Session()
    
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')
        return token
    
    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            self.exact1(response.text)

    
    def exact1(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "js-repos-container")]//ul[contains(@class,"list-style-none")]//li')
        i = 0
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//a/@href')).strip()
            i = i +1
            if i == 8:
                break;
            print(i)
            url = self.base_url + dynamic + "/pulls"
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                self.exact2(response.text)

    def exact2(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "js-navigation-container js-active-navigation-container")]//div[contains(@class, "float-left col-8 lh-condensed p-2")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//a[contains(@class,"link-gray-dark v-align-middle no-underline h4 js-navigation-open")]/@href')).strip()
            url = self.base_url + dynamic
            print(url)
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                self.exact3(response.text)

    def exact3(self, html):
        selector = etree.HTML(html)
        list = selector.xpath('//div[contains(@class, "edit-comment-hide js-edit-comment-hide")]//code//text()')
        print(list)


if __name__ == "__main__":
    login = Login()
    login.login(email='', password='')