from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import ProducSerializer, ReviewSerializer
from api.models import Product, Review

# Create your views here.



def home(request):
    return render(request,'home.html')

@api_view(['GET'])
def getProducts(request):
    print(request.user)
    products = Product.objects.all()
    serializer = ProducSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getProduct(request,pk=None):
    products = Product.objects.all()
    product = get_object_or_404(products, pk=pk)
    serializer = ProducSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def getReview(request):
    if request.method == 'POST':
        data = request.data
        data['user'] = request.user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
