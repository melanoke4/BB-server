from rest_framework.decorators import api_view
from rest_framework.response import Response

from bottomlessboxapi.models.user import User


@api_view(['POST'])
def check_user(request):
    '''
    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'uid': user.uid,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)