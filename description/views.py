from django.shortcuts import render
import os
# Create your views here.
def description(request):
	absolute_path = os.path.abspath(os.path.dirname('data.csv'))
	args = {'asbs': absolute_path}	
	return render(request, 'description.html', args)	
