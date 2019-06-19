# Downloader for scrapy over socks proxy  

Install:    
pip install git+https://github.com/igoral5/txsocksx.git  
pip install git+https://github.com/igoral5/scrapy-socks-downloader.git  

Usage:  
In settings.py (settings scrapy project)
  
```
DOWNLOAD_HANDLERS = {  
    'http': 'socks_downloader.downloader.SocksDownloadHandler',  
    'https': 'socks_downloader.downloader.SocksDownloadHandler',  
}
```




