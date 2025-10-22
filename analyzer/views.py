from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import AnalyzerSerializer
from .models import Analyzer
from rest_framework.parsers import JSONParser
import hashlib
import logging
from .utils import parse_natural_language_query
import re
# Create your views here.

logging.basicConfig(level=logging.INFO)

def is_palindrome(str):
    rev = str[::-1]
    if str == rev:
        return True
    else:
        return False

def count_unique_characters(str):
    start = str[0]
    count = 0
    for i in range(0, len(str)-1):
        for j in range(0, len(str)-1):
            if start == str[j]:
                pass
            else:
                count+=1
    return count

def word_count(str):
    data = str.split()
    print(len(data))
    return len(data)      
    
def getHash(str):
    hash_object = hashlib.sha256(str.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex    

def character_frequency_map(str):
    freq = {}
    for char in str:
        freq[char] = freq.get(char,0) + 1
    return freq     
    
    
class SaveAnalyzerView(APIView):
    def post(self,request):
        value = request.data.get('value')
        id = getHash(value)
        word_count(value)
        properties = {
                "length": len(value),
                "is_palindrome": is_palindrome(value),
                "unique_characters": count_unique_characters(value),
                "word_count": word_count(value),
                "sha256_hash":getHash(value),
                "character_frequency_map": character_frequency_map(value)
            }
        analyzer = Analyzer(id=id,value=value,properties=properties)
        analyzer.save()
        return Response({"id":id,"value": value, "properties":properties},status=200)
    
    def get(self,request):
        try:
            queryset = Analyzer.objects.all()
            print("Data:",queryset)
            filters_applied = {}

            # Extract query parameters
            is_palindrome = request.GET.get('is_palindrome')
            min_length = request.GET.get('min_length')
            max_length = request.GET.get('max_length')
            word_count = request.GET.get('word_count')
            contains_character = request.GET.get('contains_character')

            # Filter by is_palindrome
            if is_palindrome is not None:
                if is_palindrome.lower() == 'true':
                    queryset = queryset.filter(properties__is_palindrome=True)
                    filters_applied['is_palindrome'] = True
                elif is_palindrome.lower() == 'false':
                    queryset = queryset.filter(properties__is_palindrome=False)
                    filters_applied['is_palindrome'] = False
                else:
                    return Response({'error': 'Invalid value for is_palindrome'}, status=400)

            # Filter by min_length
            if min_length is not None:
                try:
                    min_len = int(min_length)
                    queryset = queryset.filter(properties__length__gte=min_len)
                    filters_applied['min_length'] = min_len
                except ValueError:
                    return Response({'error': 'min_length must be an integer'}, status=400)

            # Filter by max_length
            if max_length is not None:
                try:
                    max_len = int(max_length)
                    queryset = queryset.filter(properties__length__lte=max_len)
                    filters_applied['max_length'] = max_len
                except ValueError:
                    return Response({'error': 'max_length must be an integer'}, status=400)

            # Filter by word_count
            if word_count is not None:
                try:
                    wc = int(word_count)
                    queryset = queryset.filter(properties__word_count=wc)
                    filters_applied['word_count'] = wc
                except ValueError:
                    return Response({'error': 'word_count must be an integer'}, status=400)

            # Filter by contains_character
            if contains_character is not None:
                if len(contains_character) != 1:
                    return Response({'error': 'contains_character must be a single character'}, status=400)
                queryset = queryset.filter(properties__character_frequency_map__has_key=contains_character)
                filters_applied['contains_character'] = contains_character

            # Serialize results
            data = [
                {
                    'id': obj.id,
                    'value': obj.value,
                    'properties': obj.properties,
                    'created_at': obj.created_at
                } for obj in queryset
            ]

            return Response({
                'data': data,
                'count': len(data),
                'filters_applied': filters_applied
            }, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
class FetchAnalyzerView(APIView):
    def get(self,request,id):
        print(id)
        analyzer = Analyzer.objects.filter(value=id).first()
        print(analyzer)
        analyzerSerializer = AnalyzerSerializer(analyzer)
        return Response(analyzerSerializer.data, status=200)
    def delete(self,request,id):
        print(id)
        analyzer = Analyzer.objects.filter(value=id).first()
        analyzer.delete()
        return Response({},status=204)
    
    

class NaturalLanguageFilterAPIView(APIView):
    """
    GET /strings/filter-by-natural-language?query=<your query>
    Example: /strings/filter-by-natural-language?query=all single word palindromic strings
    """
    def get(self, request):
        query = request.GET.get('query', '').strip()
        if not query:
            return Response({'error': 'Query parameter is required'}, status=400)

        try:
            queryset = Analyzer.objects.all()
            parsed_filters = {}

            # --- NLP heuristics ---
            # 1️⃣ Palindromic strings
            if re.search(r'\bpalindromic|\bpalindrome', query, re.IGNORECASE):
                parsed_filters['is_palindrome'] = True
                queryset = queryset.filter(properties__is_palindrome=True)

            # 2️⃣ Single or multiple words
            match_word_count = re.search(r'(\b\d+\b|\bsingle\b|\bmultiple\b)\s+word', query, re.IGNORECASE)
            if match_word_count:
                word_count_str = match_word_count.group(1).lower()
                if word_count_str == 'single':
                    parsed_filters['word_count'] = 1
                    queryset = queryset.filter(properties__word_count=1)
                elif word_count_str == 'multiple':
                    parsed_filters['word_count'] = '>=2'
                    queryset = queryset.filter(properties__word_count__gte=2)
                else:
                    try:
                        wc = int(word_count_str)
                        parsed_filters['word_count'] = wc
                        queryset = queryset.filter(properties__word_count=wc)
                    except ValueError:
                        pass

            # 3️⃣ Longer than N characters
            match_min_length = re.search(r'longer than (\d+)\s*characters?', query, re.IGNORECASE)
            if match_min_length:
                min_len = int(match_min_length.group(1)) + 1
                parsed_filters['min_length'] = min_len
                queryset = queryset.filter(properties__length__gte=min_len)

            # 4️⃣ Shorter than N characters
            match_max_length = re.search(r'shorter than (\d+)\s*characters?', query, re.IGNORECASE)
            if match_max_length:
                max_len = int(match_max_length.group(1)) - 1
                parsed_filters['max_length'] = max_len
                queryset = queryset.filter(properties__length__lte=max_len)

            # 5️⃣ Containing a specific letter
            match_char = re.search(r'contain(?:ing)?(?: the)? letter (\w)', query, re.IGNORECASE)
            if match_char:
                char = match_char.group(1).lower()
                parsed_filters['contains_character'] = char

                # Safe fallback if DB doesn’t support __has_key
                try:
                    queryset = queryset.filter(properties__character_frequency_map__has_key=char)
                except Exception:
                    # Fallback: filter in Python
                    queryset = [obj for obj in queryset if char in obj.properties.get('character_frequency_map', {})]

            # Serialize
            if not queryset:
                return Response({
                    'data': [],
                    'count': 0,
                    'interpreted_query': {
                        'original': query,
                        'parsed_filters': parsed_filters
                    },
                    'message': 'No matches found for this query'
                }, status=200)

            # If queryset is a list (fallback case)
            if isinstance(queryset, list):
                data = [
                    {
                        'id': obj.id,
                        'value': obj.value,
                        'properties': obj.properties,
                        'created_at': obj.created_at
                    } for obj in queryset
                ]
            else:
                data = [
                    {
                        'id': obj.id,
                        'value': obj.value,
                        'properties': obj.properties,
                        'created_at': obj.created_at
                    } for obj in queryset
                ]

            return Response({
                'data': data,
                'count': len(data),
                'interpreted_query': {
                    'original': query,
                    'parsed_filters': parsed_filters
                }
            }, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
