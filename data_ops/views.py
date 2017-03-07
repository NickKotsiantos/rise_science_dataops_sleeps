from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .helper_functions import query_airtable_data_by_name


# Create your views here.
@login_required
def home(request):
	if request.method == 'POST':
		if request.POST.get('first_name') and request.POST.get('last_name'):
			player_data = query_airtable_data_by_name(request.POST['first_name'].lower(), 
													  request.POST['last_name'].lower())
			if player_data == 0:
				return render(request, 'data_ops/home.html', {'message':'ERROR: Failed to grab data.'})
			if len(player_data) == 0:
				return render(request, 'data_ops/home.html', {'message':'ERROR: Player not found'})
			else:
				return render(request, 'data_ops/home.html', {'data':player_data})
		else:
			return render(request, 'data_ops/home.html', 
						{'message':'ERROR: Enter player\'s first and last name'})
	else:
		return render(request, 'data_ops/home.html')




	
