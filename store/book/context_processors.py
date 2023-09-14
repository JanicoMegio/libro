# from book.models import CartItems
# from django.contrib.auth.decorators import login_required

# @login_required(login_url='login')
# def cart_count(request):
# 	user = request.user
# 	cart_count = CartItems.objects.filter(user_name=user).count()
# 	return {'cart_count': cart_count}
