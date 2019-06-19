# -*- coding: utf-8 -*-
'''
Created on 19 июн. 2019 г.
Downloader for scrapy over socks proxy
@author: ilalimov
'''
from base64 import b64decode
from twisted.internet.endpoints import TCP4ClientEndpoint
from scrapy.core.downloader.handlers.http11 import HTTP11DownloadHandler, ScrapyAgent
from scrapy.core.downloader.webclient import _parse
from scrapy.utils.python import to_bytes, to_unicode
from txsocksx.http import SOCKS4Agent, SOCKS5Agent 
from twisted.internet import reactor

class SocksDownloadHandler(HTTP11DownloadHandler):
   
    def download_request(self, request, spider):
        """Return a deferred for the HTTP download"""
        agent = ScrapySocksAgent(contextFactory=self._contextFactory, pool=self._pool,
            maxsize=getattr(spider, 'download_maxsize', self._default_maxsize),
            warnsize=getattr(spider, 'download_warnsize', self._default_warnsize),
            fail_on_dataloss=self._fail_on_dataloss)
        return agent.download_request(request)


class ScrapySocksAgent(ScrapyAgent):
    
    def _get_agent(self, request, timeout):
        bindaddress = request.meta.get('bindaddress') or self._bindAddress
        proxy = request.meta.get('proxy')
        if proxy:
            proxyScheme, _, proxyHost, proxyPort, proxyParams = _parse(proxy)
            if proxyScheme.startswith(b'http'):
                scheme = _parse(request.url)[0]
                proxyHost = to_unicode(proxyHost)
                omitConnectTunnel = b'noconnect' in proxyParams
                if  scheme == b'https' and not omitConnectTunnel:
                    proxyConf = (proxyHost, proxyPort,
                                 request.headers.get(b'Proxy-Authorization', None))
                    return self._TunnelingAgent(reactor, proxyConf,
                        contextFactory=self._contextFactory, connectTimeout=timeout,
                        bindAddress=bindaddress, pool=self._pool)
                else:
                    return self._ProxyAgent(reactor, proxyURI=to_bytes(proxy, encoding='ascii'),
                        connectTimeout=timeout, bindAddress=bindaddress, pool=self._pool)
            elif proxyScheme == b'socks4':
                proxyEndPoint = TCP4ClientEndpoint(reactor, proxyHost, proxyPort, 
                                                   timeout=timeout, bindAddress=bindaddress)
                agent = SOCKS4Agent(reactor, proxyEndPoint=proxyEndPoint, 
                        contextFactory=self._contextFactory,
                        connectTimeout=timeout, bindAddress=bindaddress, pool=self._pool)
                return agent
            elif proxyScheme == b'socks5':
                proxyEndPoint = TCP4ClientEndpoint(reactor, proxyHost, proxyPort,
                        timeout=timeout, bindAddress=bindaddress)
                
                proxyAuth = request.headers.get(b'Proxy-Authorization', None)
                if proxyAuth:
                    proxyUser, proxyPassword = b64decode(proxyAuth.split()[-1]).split(b':')
                    agent = SOCKS5Agent(reactor, proxyEndpoint=proxyEndPoint, 
                            endpointArgs=dict(methods={'login': (proxyUser, proxyPassword)}), 
                            contextFactory=self._contextFactory, connectTimeout=timeout, 
                            bindAddress=bindaddress, pool=self._pool)
                else:
                    agent = SOCKS5Agent(reactor, proxyEndpoint=proxyEndPoint, 
                            contextFactory=self._contextFactory,
                            connectTimeout=timeout, bindAddress=bindaddress, 
                            pool=self._pool)
                return agent

        return self._Agent(reactor, contextFactory=self._contextFactory,
            connectTimeout=timeout, bindAddress=bindaddress, pool=self._pool)
