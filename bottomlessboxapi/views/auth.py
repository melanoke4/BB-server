from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from bottomlessboxapi.models.user import User

@api_view(['POST'])
def check_user(request):
    '''
    Check if a user exists based on the provided UID.
    '''
    uid = request.data.get('uid')
    
    if not uid:
        return Response({'error': 'UID is required'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(uid=uid).first()

    if user:
        data = {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'uid': user.uid,
            'valid': True
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)