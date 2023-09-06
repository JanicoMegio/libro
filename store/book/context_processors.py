from book.models import CartItems
from django.http import JsonResponse

def cart_count(request):
	user = request.user
	cart_count = CartItems.objects.filter(user_name=user).count()
	return {'cart_count': cart_count}
