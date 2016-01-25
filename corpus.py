# -*- coding: utf-8 -*-
import nltk
import nltk.data
from nltk.corpus import stopwords
from nltk.util import ngrams
import os
import pprint
from wikipedia import Wikipedia
from wiki2plain import Wiki2Plain
from google import GoogleGraph
from google import GoogleSearch

class Corpus:
    def __init__( self, string):
        '''
            Recibe la cadena "Telcel no da el servicio de 3g en la facultad de ingenieria"
            Busca documentos en wikipedia, y Google y los guarda en self.documents.
            '''
        self.documents = []
        #Pruebas
        self.documents = self.documents + GoogleSearch(string).documents
        for word in string.split():
            self.wikipediaSearch(word)
    
    def wikipediaSearch( self, word = "iOS", lang = 'simple', maximumNumberOfResults = 1, save = False ):
        '''
            (get) Wikipedia (corpus (documents) ) (by) Search
            Recibe una palabra: 'word', busca 'word' en Wikipedia y guarda los articulos en 'self.corpus'
            '''
        wiki = Wikipedia(lang)
        
        resultadosdebusqueda = wiki.search(word , 1, maximumNumberOfResults)
        
        numerodearticulos = len(resultadosdebusqueda)
        
        for resultado in resultadosdebusqueda:
            try:
                raw = wiki.article(resultado['title'])
            except:
                raw = None
            if raw:
                wiki2plain = Wiki2Plain(raw)
                content = wiki2plain.text
                if save:
                    f = open( resultado['title'] + '.txt', 'w+')
                    f.write(content)
                    f.close()
                self.documents.append(content)
            #os.system('clear')
            
            #Imprime avance del metodo.
            '''
                percentage = str( ((resultadosdebusqueda.index(resultado) + 1.0)/numerodearticulos) * 100 ) + "%" + "\t"
                try:
                percentage = percentage + resultado['title']
                except:
                percentage = percentage + "Title not available"
                print(percentage)
                '''

class nGramDictionary:
    def __init__(self):
        self.dictionary = {}
    def add_string(self, string):
        for (a,b,c) in ngrams(string.split(), 3):
            try:
                self.dictionary[a][b][c] = self.dictionary[a][b][c] + 1
            except:
                try:
                    self.dictionary[a][b] = { c :  1 }
                except:
                    try:
                        self.dictionary[a] = { b : { c : 1 } }
                    except:
                        print('exception')