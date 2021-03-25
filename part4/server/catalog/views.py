from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, Term
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import constants
from .models import Wine, WineSearchWord
from .serializers import WineSerializer, WineSearchWordSerializer
from .filters import WineFilterSet, WineSearchWordFilterSet


class WinesView(ListAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    filterset_class = WineFilterSet

    def filter_queryset(self, request):
        return super().filter_queryset(request)[:100]


class WineSearchWordsView(ListAPIView):
    queryset = WineSearchWord.objects.all()
    serializer_class = WineSearchWordSerializer
    filterset_class = WineSearchWordFilterSet


class ESWinesView(APIView):
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('query')
        country = self.request.query_params.get('country')
        points = self.request.query_params.get('points')

        # Build Elasticsearch query.
        search = Search(index=constants.ES_INDEX)
        q = {'should': [], 'filter': []}

        # Build should clause.
        if query:
            q['should'] = [
                Match(variety={'query': query, 'boost': 3.0}),
                Match(winery={'query': query, 'boost': 2.0}),
                Match(description={'query': query, 'boost': 1.0})
            ]
            q['minimum_should_match'] = 1

            # Build highlighting.
            search = search.highlight_options(
                number_of_fragments=0,
                pre_tags=['<mark>'],
                post_tags=['</mark>']
            )
            search = search.highlight('variety', 'winery', 'description')

        # Build filter clause.
        if country:
            q['filter'].append(Term(country=country))
        if points:
            q['filter'].append(Term(points=points))

        response = search.query('bool', **q).params(size=100).execute()

        if response.hits.total.value > 0:
            return Response(data=[{
                'id': hit.meta.id,
                'country': hit.country,
                'description': (
                    hit.meta.highlight.description[0]
                    if 'highlight' in hit.meta and 'description' in hit.meta.highlight
                    else hit.description
                ),
                'points': hit.points,
                'price': hit.price,
                'variety': (
                    hit.meta.highlight.variety[0]
                    if 'highlight' in hit.meta and 'variety' in hit.meta.highlight
                    else hit.variety
                ),
                'winery': (
                    hit.meta.highlight.winery[0]
                    if 'highlight' in hit.meta and 'winery' in hit.meta.highlight
                    else hit.winery
                ),
            } for hit in response])
        else:
            return Response(data=[])


class ESWineSearchWordsView(APIView):
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('query')

        # Build Elasticsearch query.
        search = Search().suggest('result', query, term={
            'field': 'all_text'
        })

        response = search.execute()

        # Extract words.
        options = response.suggest.result[0]['options']
        words = [{'word': option['text']} for option in options]

        return Response(data=words)
