# -*- coding: utf-8 -*-

# Google Search

import urllib
import urllib2
import lxml.html
import re

class GoogleSearch:
    def __init__(self, search_term, pages = 1 ):
        self.links = self.search(search_term, pages)
        self.documents = self.getText(self.links)

    def search(self, search_term, pages = 1):
        '''
            Busca el término en google y añade a self.links los links encontrados
            
            Argumentos:
                search_term : Término buscado (puede ser cualquier cadena)
                
        '''
        links = []
        for page in range(pages):
            try:
                search_term = search_term.replace(" ","%20")
                url = 'https://www.google.com/search?q="' + search_term + '"' + '&start=' + str((page - 1) * 10)
                headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:24.0)"}
                req = urllib2.Request(url, headers=headers)
                page = urllib2.urlopen(req)
                doc = lxml.html.document_fromstring(page.read())
                for t in doc.xpath("//h3[@class='r']/a"):
                    link = t.get("href").replace("/url?q=","")
                    link = link.partition("&sa")[0]
                    if not link.find("http:") == -1:
                        links.append(link)
            except:
                print('Google: HTTP Error 503 The service is unavailable')
        return links

    def getText(self, links):
        documents = []
        for link in links:
            try:
                url = link
                headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:24.0)"}
                req = urllib2.Request(url, headers=headers)
                page = urllib2.urlopen(req)
                htmlStr = page.read()
                doc = lxml.html.document_fromstring(htmlStr)
                text = doc.text_content()
                text = text.encode('utf-8')
                text = self.cleanText(text)
                documents.append(text)
            except:
                print(link + ': HTTP Error 503 The service is unavailable')
        return documents

    def cleanText(self, text):
        text = re.sub(r'(?i)&nbsp;', ' ', text)
        text = re.sub(r'(?i)<br[ \\]*?>', '\n', text)
        text = re.sub(r'(?m)<!--.*?--\s*>', '', text)
        text = re.sub(r'(?i)<ref[^>]*>[^>]*<\/ ?ref>', '', text)
        text = re.sub(r'(?m)<.*?>', '', text)
        text = re.sub(r'(?i)&amp;', '&', text)
        text = re.sub(r'(?i)\{\{IPA(\-[^\|\{\}]+)*?\|([^\|\{\}]+)(\|[^\{\}]+)*?\}\}', lambda m: m.group(2), text)
        text = re.sub(r'(?i)\{\{Lang(\-[^\|\{\}]+)*?\|([^\|\{\}]+)(\|[^\{\}]+)*?\}\}', lambda m: m.group(2), text)
        text = re.sub(r'\{\{[^\{\}]+\}\}', '', text)
        text = re.sub(r'(?m)\{\{[^\{\}]+\}\}', '', text)
        text = re.sub(r'(?m)\{\|[^\{\}]*?\|\}', '', text)
        text = re.sub(r'(?i)\[\[Category:[^\[\]]*?\]\]', '', text)
        text = re.sub(r'(?i)\[\[Image:[^\[\]]*?\]\]', '', text)
        text = re.sub(r'(?i)\[\[File:[^\[\]]*?\]\]', '', text)
        text = re.sub(r'\[\[[^\[\]]*?\|([^\[\]]*?)\]\]', lambda m: m.group(1), text)
        text = re.sub(r'\[\[([^\[\]]+?)\]\]', lambda m: m.group(1), text)
        text = re.sub(r'\[\[([^\[\]]+?)\]\]', '', text)
        text = re.sub(r'(?i)File:[^\[\]]*?', '', text)
        text = re.sub(r'\[[^\[\]]*? ([^\[\]]*?)\]', lambda m: m.group(1), text)
        text = re.sub(r"''+", '', text)
        text = re.sub(r'(?m)^\*$', '', text)
        text = re.sub(r'\r\n|\n|\r', '\n', text)
        text = re.sub(r'\n\n+', '\n\n', text)
        parts = text.split('\n\n')
        partsParsed = []
        for part in parts:
            part = part.strip()
            if len(part) == 0:
                continue
            partsParsed.append(part)
        return '\n\n'.join(partsParsed)


# Google Graph

from nltk.corpus import stopwords

class GoogleGraph:
    
    def __init__(self, language = 'english', string = ""):
        '''
            Graph
            Recibe el lenguaje del grafo y una cadena con la que se construye el grafo.
        '''
        self.graph = {}
        self.language = language
        wordlist = string.split()
        #Inicializa Variables
        self.graph[('S')] = []
        for i in range( len(wordlist)):
            word = wordlist[i]
            self.graph[word, i] = []
        #Realiza Grafo
        for i in range(len(wordlist)):
            word = wordlist[i]
            if i == 0:
                self.graph[('S')].append((word, i))
            if i < len(wordlist) - 1:
                nextWord = wordlist[ i + 1 ]
                self.graph[word, i].append((nextWord, i + 1))
            if i == len(wordlist) - 1:
                self.graph[word, i].append('E')
    
    def add_string(self, string):
        '''
            Add String
            Recibe una cadena que se agrega al grafo.
        '''
        wordlist = string.split()
        wordlist.reverse()
        wordlistlength = len(wordlist)
        lastNode = 'E'
        for i in range(wordlistlength):
            word = wordlist[i]
            key = (word, wordlistlength - i - 1)
            candidates = self.find_candidates_for_key(key)
            if len(candidates) > 0:
                bestcandidate = candidates[0]
                self.graph[bestcandidate].append(lastNode)
                lastNode = bestcandidate
            else:
                if key not in self.graph:
                    self.graph[key] = []
                self.graph[key].append(lastNode)
                lastNode = key
        self.graph['S'].append(lastNode)
        return
    
    def find_candidates_for_key(self, key):
        '''
            Find Candidates for Key
            Recibe una llave cualquiera y regresa los candidatos para esta llave ordenados por preferencia decendente.
        '''
        candidates = []
        for _key in self.graph:
            if _key[0] == key[0] and _key != key and key[0] not in stopwords.words(self.language):
                candidates.append(_key)
        return candidates
    
    def find_all_paths(self, start, end, path=[]):
        '''
            Find all paths
            Recibe el nodo inicial y el nodo final y regresa todas las posibles rutas.
        '''
        graph = self.graph
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                try:
                    newpaths = self.find_all_paths(node, end, path)
                except:
                    #newpaths = end
                    return [path]
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    
    def find_shortest_path(self, start, end, path=[]):
        '''
            Find Shortest Path
            Recibe el nodo inicial y el nodo final y regresa la ruta mas corta.
        '''
        graph = self.graph
        path = path + [start]
        
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def search(self, search_term):
        for key in self.graph:
            if key[0] == search_term:
                try:
                    return (key[0],key[1])
                except:
                    print('Search exception raised')
                    return None
        print('Search Term ' + search_term + ' not found in Google Graph')
        return None
# Main

def main(*args):
    googleSearch = GoogleSearch("Telcel", 1)
    #pprint.pprint(googleSearch.links)
    print(googleSearch.links)

if __name__ == "__main__":
    main()
    
