import os
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from PIL import Image
import io

# Clarifai API Key
CLARIFAI_API_KEY = "1ec87780113f4f449622334d89dca747"

# Food model ID - using the general model which can detect various objects including food items
CLARIFAI_MODEL_ID = "general-image-recognition"
CLARIFAI_MODEL_VERSION_ID = "aa7f35c01e0642fda5cf400f543e7c40"  # General model version

def get_clarifai_stub():
    """Create a gRPC stub for the Clarifai API."""
    channel = ClarifaiChannel.get_grpc_channel()
    return service_pb2_grpc.V2Stub(channel)

def analyze_image(image_file):
    """
    Analyze an image using Clarifai API to detect ingredients.
    
    Args:
        image_file: PIL Image object or file-like object containing the image
    
    Returns:
        list: List of detected ingredients/food items
    """
    # Convert PIL Image to bytes if needed
    if isinstance(image_file, Image.Image):
        img_byte_arr = io.BytesIO()
        image_file.save(img_byte_arr, format='JPEG')
        file_bytes = img_byte_arr.getvalue()
    else:
        # Assume it's already a file-like object
        file_bytes = image_file.read()
        
    # Get the gRPC stub
    stub = get_clarifai_stub()
    
    # Construct the request
    request = service_pb2.PostModelOutputsRequest(
        model_id=CLARIFAI_MODEL_ID,
        version_id=CLARIFAI_MODEL_VERSION_ID,
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ]
    )
    
    # Set metadata with API key
    metadata = (('authorization', f'Key {CLARIFAI_API_KEY}'),)
    
    # Make the request
    try:
        response = stub.PostModelOutputs(request, metadata=metadata)
        
        # Check if the request was successful
        if response.status.code != status_code_pb2.SUCCESS:
            print(f"Error: {response.status.description}")
            return []
        
        # Process the response
        ingredients = []
        food_related_concepts = [
            'food', 'vegetable', 'fruit', 'meat', 'dairy', 'grain', 'herb', 'spice',
            'ingredient', 'dish', 'meal', 'breakfast', 'lunch', 'dinner', 'snack',
            'appetizer', 'dessert', 'beverage', 'drink'
        ]
        
        # Extract concepts with confidence above 0.7 that might be food-related
        for concept in response.outputs[0].data.concepts:
            # Filter for likely food items with good confidence
            if concept.value >= 0.7:
                # Check if it's a food item or if it contains food-related words
                if any(food_term in concept.name.lower() for food_term in food_related_concepts) or \
                   concept.name.lower() in food_related_concepts:
                    ingredients.append(concept.name)
        
        # If we have too many ingredients, limit to the top 10 by confidence
        if len(ingredients) > 10:
            ingredients = ingredients[:10]
            
        return ingredients
    
    except Exception as e:
        print(f"Error calling Clarifai API: {e}")
        return []

def filter_food_items(concepts):
    """
    Filter detected concepts to only include likely food items.
    This is a simple heuristic and might need refinement.
    """
    # Common non-food items that might be detected
    non_food = ['plate', 'bowl', 'table', 'fork', 'knife', 'spoon', 'cup', 'glass', 
                'napkin', 'person', 'hand', 'container', 'package']
    
    # Filter out non-food items
    food_items = [item for item in concepts if item.lower() not in [nf.lower() for nf in non_food]]
    
    return food_items
