import csv
import os
import requests
import re
import datetime
from pprint import pprint
from operator import itemgetter
from textblob import TextBlob
import nltk
from collections import Counter
from pymongo import MongoClient, TEXT
from PIL import Image
from io import BytesIO
import time
from bs4 import BeautifulSoup

from credentials import MONGO_URL

try:
    STOPWORDS = nltk.corpus.stopwords.words('english')
except LookupError:
    pass


def write_series_csv():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    with open(os.path.join('csv', 'tribune_series.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['call_number', 'series_number', 'part_number', 'level', 'title', 'object_number', 'priref', 'date_string', 'date_start', 'date_end', 'quantity', 'url', 'collection_url', 'number_children', 'subjects', 'people'])
        for record in db.series.find().sort([('series_number', 1), ('part_number', 1)]):
            writer.writerow([
                record['call_number'],
                record['series_number'],
                record['part_number'],
                record['level'],
                record['title'],
                record['object_number'],
                record['priref'],
                record['date_string'],
                record['date_start'],
                record['date_end'],
                record['quantity'],
                record['url'],
                record['parent_url'],
                record['number_children'],
                '|'.join(record['subjects']),
                '|'.join(record['people'])
            ])


def write_items_csv(series_number='01'):
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    for part in db.series.find({'series_number': series_number}):
        part_number = part['part_number']
        with open(os.path.join('csv', 'series-{}-part-{}-items.csv'.format(series_number, part_number)), 'wb') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['series_number', 'part_number', 'item_number', 'level', 'title', 'call_number', 'object_number', 'priref', 'intellectual_entity', 'date_string', 'date_start', 'date_end', 'quantity', 'url', 'parent_url', 'number_images', 'images', 'description', 'subjects', 'topics', 'people', 'places'])
            for item in db.items.find({'parent_number': series_number, 'parent_part': part_number}):
                print item['title']
                writer.writerow([
                    series_number,
                    part_number,
                    item['item_number'],
                    item['level'],
                    item['title'].encode('utf-8'),
                    item['call_number'],
                    item['object_number'],
                    item['priref'],
                    item['intellectual_entity'],
                    item['date_string'],
                    item['date_start'],
                    item['date_end'],
                    item['quantity'],
                    item['url'],
                    item['parent_url'],
                    item['number_images'],
                    '|'.join(item['images']),
                    '|'.join(item['description']).encode('utf-8'),
                    '|'.join(item['subjects']).encode('utf-8'),
                    '|'.join(item['topics']).encode('utf-8'),
                    '|'.join(item['people']).encode('utf-8'),
                    '|'.join(item['places']).encode('utf-8')
                ])


def write_all_items_csv():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    with open(os.path.join('csv', 'all_items.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['series_number', 'part_number', 'item_number', 'level', 'title', 'call_number', 'object_number', 'priref', 'intellectual_entity', 'date_string', 'date_start', 'date_end', 'quantity', 'url', 'parent_url', 'number_images', 'images', 'description', 'subjects', 'topics', 'people', 'places'])
        for series_number in ['01', '02', '03', '04']:
            for part in db.series.find({'series_number': series_number}).sort('part_number', 1):
                part_number = part['part_number']
                for item in db.items.find({'parent_number': series_number, 'parent_part': part_number}).sort('item_number', 1):
                    print item['title']
                    writer.writerow([
                        series_number,
                        part_number,
                        item['item_number'],
                        item['level'],
                        item['title'].encode('utf-8'),
                        item['call_number'],
                        item['object_number'],
                        item['priref'],
                        item['intellectual_entity'],
                        item['date_string'],
                        item['date_start'],
                        item['date_end'],
                        item['quantity'],
                        item['url'],
                        item['parent_url'],
                        item['number_images'],
                        '|'.join(item['images']),
                        '|'.join(item['description']).encode('utf-8'),
                        '|'.join(item['subjects']).encode('utf-8'),
                        '|'.join(item['topics']).encode('utf-8'),
                        '|'.join(item['people']).encode('utf-8'),
                        '|'.join(item['places']).encode('utf-8')
                    ])


def write_titles_as_text():
    with open(os.path.join('csv', 'all_titles.txt'), 'wb') as text_file:
        with open(os.path.join('csv', 'all-items.csv'), 'rb') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[4] != 'title':
                    title = re.sub(r'Item \d+[a-zA-Z]*\: Tribune negatives including ', '', row[4])
                    title = title[:title.find(',')]  # Kuldgey way of getting rid of places and dates also cuts some events
                    text_file.write('{}\n'.format(title))


def stopwords_check(ngram):
    ''' Check if all words in ngrams are stopwords '''
    keep = False
    for word in ngram:
        if word not in STOPWORDS:
            keep = True
            break
    return keep


def analyse_titles(titles_file='all_titles.txt'):
    with open(os.path.join('csv', titles_file), 'rb') as text_file:
        text = text_file.read().decode('ascii', errors="replace")
    blob = TextBlob(text)
    word_counts = [[word, count] for word, count in blob.lower().word_counts.items() if word not in STOPWORDS and count > 1]
    bigrams = [' '.join(bigram).lower() for bigram in blob.lower().ngrams(2) if stopwords_check(bigram)]
    bigram_counts = [[word, count] for word, count in Counter(bigrams).items() if count > 1]
    trigrams = [' '.join(trigram).lower() for trigram in blob.lower().ngrams(3) if stopwords_check(trigram)]
    trigram_counts = [[word, count] for word, count in Counter(trigrams).items() if count > 1]
    word_counts = sorted(word_counts, key=itemgetter(1), reverse=True)[:20]
    bigram_counts = sorted(bigram_counts, key=itemgetter(1), reverse=True)[:20]
    trigram_counts = sorted(trigram_counts, key=itemgetter(1), reverse=True)[:20]
    np_counts = [[word, count] for word, count in blob.lower().np_counts.items() if count > 1]
    np_counts = sorted(np_counts, key=itemgetter(1), reverse=True)[:20]
    print '## Most frequent words\n'
    for term in word_counts:
        print '* {} ({})'.format(term[0], term[1])
    print '\n\n## Most frequent bigrams\n'
    for term in bigram_counts:
        print '* {} ({})'.format(term[0], term[1])
    print '\n\n## Most frequent trigrams\n'
    for term in trigram_counts:
        print '* {} ({})'.format(term[0], term[1])
    print '\n\n## Most frequent noun phrases\n'
    for term in np_counts:
        print '* {} ({})'.format(term[0], term[1])


def aggregate_subjects():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    pipeline = [
        {'$unwind': '$subjects'},
        {'$group': {'_id': '$subjects', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    results = db.items.aggregate(pipeline)
    # print len(list(results))
    # pprint(list(results))
    # for result in results:
    #   print '| {} | {} |'.format(result['_id'], result['count'])
    return list(results)


def aggregate_topics():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    pipeline = [
        {'$unwind': '$topics'},
        {'$group': {'_id': '$topics', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    results = db.items.aggregate(pipeline)
    # print len(list(results))
    # pprint(list(results))
    for result in results:
        print '| {} | {} |'.format(result['_id'], result['count'])


def list_descriptions():
    ignore = ['Includes:', 'May include:', 'Original negative sleeve annotated:', 'Image descriptions provided by cataloguer.']
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    with open(os.path.join('csv', 'all_descriptions.txt'), 'wb') as descriptions:
        for item in db.items.find().sort('date_start', 1):
            for desc in item['description']:
                if desc and desc not in ignore:
                    descriptions.write('{}\n'.format(desc.encode('utf-8')))


def aggregate_descriptions():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    pipeline = [
        {'$unwind': '$description'},
        {'$group': {'_id': '$description', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    results = db.items.aggregate(pipeline)
    # print len(list(results))
    # pprint(list(results))
    for result in results:
        print '| {} | {} |'.format(result['_id'], result['count'])


def aggregate_people():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    pipeline = [
        {'$unwind': '$people'},
        {'$group': {'_id': '$people', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    results = db.items.aggregate(pipeline)
    # print len(list(results))
    # pprint(list(results))
    for result in results:
        print '| {} | {} |'.format(result['_id'].encode('utf-8'), result['count'])


def list_places():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    act = []
    nsw = []
    subjects = aggregate_subjects()
    for subject in subjects:
        # print subject
        if 'N.S.W.' in subject['_id']:
            nsw.append(subject['_id'])
        elif 'A.C.T.' in subject['_id']:
            act.append(subject['_id'])
    with open(os.path.join('csv', 'items-by-place.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['place', 'call_number', 'item_number', 'level', 'title', 'object_number', 'priref', 'date_string', 'date_start', 'date_end', 'quantity', 'url', 'parent_url', 'number_images', 'images', 'subjects', 'topics', 'people'])
        for place in sorted(nsw):
            items = db.items.find({'subjects': place}).sort([('parent_number', 1), ('part_number', 1), ('item_number', 1)])
            print '\n### {}\n'.format(place)
            for item in items:
                print '* [{}]({})'.format(item['title'].encode('utf-8'), item['url'])
                writer.writerow([
                    place,
                    item['call_number'],
                    item['item_number'],
                    item['level'],
                    item['title'].encode('utf-8'),
                    item['object_number'],
                    item['priref'],
                    item['date_string'],
                    item['date_start'],
                    item['date_end'],
                    item['quantity'],
                    item['url'],
                    item['parent_url'],
                    item['number_images'],
                    '|'.join(item['images']),
                    '|'.join(item['subjects']).encode('utf-8'),
                    '|'.join(item['topics']).encode('utf-8'),
                    '|'.join(item['people']).encode('utf-8')
                ])


def write_places():
    act = []
    nsw = []
    subjects = aggregate_subjects()
    for subject in subjects:
        # print subject
        if 'N.S.W.' in subject['_id']:
            nsw.append(subject['_id'])
        elif 'A.C.T.' in subject['_id']:
            act.append(subject['_id'])
    with open(os.path.join('csv', 'nsw_places.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['place', 'latitiude', 'longitude'])
        for place in sorted(nsw):
            writer.writerow([place, '', ''])
    with open(os.path.join('csv', 'act_places.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['place', 'latitiude', 'longitude'])
        for place in sorted(act):
            writer.writerow([place, '', ''])


def count_images():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    pipeline = [
        {'$group': {'_id': '', 'total': {'$sum': '$number_images'}}}
    ]
    results = db.items.aggregate(pipeline)
    print list(results)


def list_items_with_images():
    dbclient = MongoClient(MONGO_URL)
    db = dbclient.get_default_database()
    items = db.items.find({'images': {'$not': {'$size': 0}}}).sort([('date_start', 1)])
    for item in items:
        print '| [{}]({}) | {} |'.format(item['title'], item['url'], item['number_images'])
