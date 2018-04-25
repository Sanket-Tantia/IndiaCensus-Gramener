from django.shortcuts import render

# Create your views here.
def description(request):
	return render(request, 'description.html')	
