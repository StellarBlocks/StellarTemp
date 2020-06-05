# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:26:35 2020

@author: jido
"""

#not work very well
import trafilatura
downloaded = trafilatura.fetch_url('http://finance.jrj.com.cn/2020/04/24012529362098.shtml')
#string = trafilatura.extract(downloaded, include_comments=False, include_tables=False)

from boilerpipe.extract import Extractor
extractor = Extractor(extractor='ArticleExtractor', html=downloaded)
title = extractor.getTitle()
content = extractor.getText()
