from rest_framework.decorators import api_view
from rest_framework.response import Response

# @api_view(['GET', 'PUT', 'POST'])
@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
    ]
    return Response(routes)
