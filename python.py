#!/usr/bin/python3.3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json
import time
import random
import urllib
import datetime
import os
import pprint
from google import GoogleGraph
from corpus import Corpus
from random import choice

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "4FqG4YZih6jOiulqlIVCwg"
CONSUMER_SECRET = "gfv7PeOjjQeSWCTZBT8gbzuF16oUaneeE52cjJd64"

OAUTH_TOKEN = "9114432-OEItiikD2TnfsFsHBXG0C95knWWJ33Yb0xcqbg3h8"
OAUTH_TOKEN_SECRET = "1eg29eLhtyqdSXSYnynChVwi4XsWNkrxtWwX2PlMWI"

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    
    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]
    
    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url
    
    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)
                   
    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]
                   
    return token, secret

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=OAUTH_TOKEN,
                   resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def tweet(status):
    if OAUTH_TOKEN:
        oauth = get_oauth()
        status = urllib.quote(status, '')
        r = requests.post(url="https://api.twitter.com/1.1/statuses/update.json?status=" + status, auth=oauth )
    #print r.json()
    else:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print

def main(*args):
    
    #   Bajar Corpus
    print("Bajando Corpus")
#    corpus = Corpus("Spongebob")

    #   Crear un GoogleGraph a partir de las oraciones de los documentos del corpus.
    print("Creando Google Graph")
    googleGraph = GoogleGraph()
    
#    for document in corpus.documents:
#        for sentence in document.split('.'):
#            #googleGraph.add_string(sentence)
#            print sentence

    
    documento = '''
        
      When the last anchovy gets his Krabby Patty, Mr Krabs is delighted. He immediately hires SpongeBob, by welcoming him to the Krusty Krew and giving him a nametag. Then, Mr. Krabs calls for three cheers for SpongeBob (in which Squidward unenthusiastically replies "Hooray" all three times). Even though Squidward is upset, Mr Krabs doesn't listen to him because he wants to go and count the "booty" he had just made in his office.
        
        At the end, Patrick walks in and asks for a Krabby Patty. SpongeBob then flies into the kitchen and makes a huge stream of Krabby Patties, which hit Patrick and sends him flying out of the restaurant, making him make his traditional scream of protest and pain. Squidward, in a sarcastic and sing-song tone, tells Mr Krabs to come see his new employee.
        
    '''
    
    print("Anadiendo oraciones al Google Graph")
    for sentence in documento.split('.'):
        googleGraph.add_string(sentence)
    
    #   Establecer inicio y fin de la busqueda.
    print("Realizando busqueda en el Google Graph")
    paths = googleGraph.find_all_paths( 'S' , 'E' )

    print("Guardando tweets y oraciones")
    sentences = []
    tweets = []
    for path in paths:
        path.remove('S')
        path.remove('E')
        string = ''
        for set in path:
            string = string + ' ' + set[0]
        string = string + '.'
        sentences.append(string)
        if len(string) <= 140:
            tweets.append(string)
    
    #   Twitter
    print("Tweets:")
    pprint.pprint(tweets)

    #   Tweet
    for i in range(len(tweets)):
        print("Tweet #"+ str(i) + " at " + str(datetime.datetime.now().time()) )
        #os.system('clear')
        wait1 = random.randint(0, 60)
        wait2 = random.randint(60, 120)
        wait = wait1 + wait2
        tweet(tweets[i])
        time.sleep(wait)

    #   Wikipedia
    print("Articulo de Wikipedia")
    article = ""
    for i in range(len(sentences)):
        randomsentence = choice(sentences)
        sentences.remove(randomsentence)
        article = article + randomsentence
    print article

    print('fin')

if __name__ == "__main__":
    main()








