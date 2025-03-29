
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import ShortURL
from .serializers import ShortURLSerializer

@api_view(['POST'])
def create_short_url(request):
    """
    Create a new short URL
    """
    serializer = ShortURLSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            url_obj = serializer.save()
            return Response({
                'id': url_obj.id,
                'url': url_obj.original_url,
                'short_code': url_obj.short_code,
                'created_at': url_obj.created_at,
                'updated_at': url_obj.updated_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': 'Could not create short URL',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import ShortURL

@api_view(['GET'])
def retrieve_original_url(request, short_code):
    """
    Retrieve original URL details
    """
    try:
        url_obj = ShortURL.objects.get(short_code=short_code)
        url_obj.access_count += 1
        url_obj.save()

        response_data = {
            "id": str(url_obj.id),
            "url": url_obj.original_url,
            "shortCode": url_obj.short_code,
            "createdAt": url_obj.created_at.isoformat(),
            "updatedAt": url_obj.updated_at.isoformat(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({"error": "Short URL not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_short_url(request, short_code):
    """
    Update an existing short URL
    """
    try:
        url_obj = ShortURL.objects.get(short_code=short_code)
        serializer = ShortURLSerializer(url_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_url = serializer.save()
            return Response({
                'id': updated_url.id,
                'url': updated_url.original_url,
                'short_code': url_obj.short_code,
                'updated_at': updated_url.updated_at
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except ObjectDoesNotExist:
        return Response({
            'error': 'Short URL not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_short_url(request, short_code):
    """
    Delete an existing short URL
    """
    try:
        url_obj = ShortURL.objects.get(short_code=short_code)
        url_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({
            'error': 'Short URL not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_url_statistics(request, short_code):
    """
    Get statistics for a short URL
    """
    try:
        url_obj = ShortURL.objects.get(short_code=short_code)
        return Response({
            'id': url_obj.id,
            'url': url_obj.original_url,
            'short_code': url_obj.short_code,
            'created_at': url_obj.created_at,
            'updated_at': url_obj.updated_at,
            'access_count': url_obj.access_count
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'error': 'Short URL not found'
        }, status=status.HTTP_404_NOT_FOUND)
