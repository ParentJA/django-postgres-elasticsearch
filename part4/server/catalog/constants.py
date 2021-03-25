ES_INDEX = 'wine'

ES_MAPPING = {
    'dynamic': 'strict',
    'properties': {
        'variety': {
            'type': 'text',
            'analyzer': 'english',
            'copy_to': 'all_text',
        },
        'country': {
            'type': 'keyword',
        },
        'price': {
            'type': 'keyword',
        },
        'winery': {
            'type': 'text',
            'analyzer': 'english',
            'copy_to': 'all_text',
        },
        'description': {
            'type': 'text',
            'analyzer': 'english',
            'copy_to': 'all_text',
        },
        'points': {
            'type': 'float',
        },
        'all_text': {
            'type': 'text',
        },
    }
}
