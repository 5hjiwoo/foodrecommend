from openai import OpenAI
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Meal, MealItem, FoodImage
from .serializers import MealSerializer, FoodImageSerializer

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Configure OpenAI API
client = OpenAI(api_key=settings.OPENAI_API_KEY)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    """
    Upload an image and return its URL.
    """
    if 'image' not in request.FILES:
        return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    image = request.FILES['image']
    file_name = default_storage.save(image.name, ContentFile(image.read()))
    file_url = default_storage.url(file_name)

    return Response({"image_url": file_url}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meal_list(request):
    """
    List all meals for the authenticated user based on their email.
    """
    email = request.query_params.get('email')
    if not email:
        return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = request.user.__class__.objects.get(email=email)
    except request.user.__class__.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    meals = Meal.objects.filter(user=user)
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_similar_foods(request):
    """
    Generate similar foods based on the uploaded image.
    """
    serializer = FoodImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        image = serializer.validated_data['image']

        # Call OpenAI API to generate similar food images
        response = client.images.generate(prompt=f"Generate images of Indonesian and Korean foods similar to the uploaded image.",
        n=2,
        size="1024x1024",
        image=image.read())  # Read image file as binary)

        similar_foods = response.data
        # Assume 'similar_foods' contains image URLs and related information
        return Response(similar_foods, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def extract_and_save_meal_info(request):
    """
    Extract meal information from the uploaded image and save it.
    """
    image = request.FILES.get('image')
    if not image:
        return Response({'detail': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Call OpenAI API to extract meal information
    response = client.images.generate(prompt=f"Extract the food name, meal time, and nutrition information from this image.",
    n=1,
    size="1024x1024",
    image=image.read())  # Read image file as binary)

    extracted_info = response.data[0]
    food_name = extracted_info.get('food_name')
    meal_type = extracted_info.get('meal_type')  # breakfast, lunch, or dinner
    calories = extracted_info.get('calories')
    carbs = extracted_info.get('carbs')
    protein = extracted_info.get('protein')
    fat = extracted_info.get('fat')

    # Save meal information
    meal = Meal.objects.create(
        meal_type=meal_type,
        date=request.data.get('date'),
        user=request.user
    )

    MealItem.objects.create(
        meal=meal,
        food_name=food_name,
        calories=calories,
        carbs=carbs,
        protein=protein,
        fat=fat
    )

    return Response({
        'food_name': food_name,
        'meal_type': meal_type,
        'calories': calories,
        'carbs': carbs,
        'protein': protein,
        'fat': fat
    }, status=status.HTTP_201_CREATED)
