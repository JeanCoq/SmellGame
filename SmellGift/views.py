#-*- coding: utf-8 -*-

################################################################
#######################    LIBRARIES    ########################
################################################################
# Django libs:
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render

# Local import:
from forms import SampleGiverForm
from SmellGift.models import SampleGiver, Food
from SmellGuess.models import Sample

################################################################
#########################    VIEWS    ##########################
################################################################

def giftView(request):
	form = SampleGiverForm()
	form.fields["foodRecentlyEaten"].queryset = Food.objects.all()
	return render(request, 'SmellGiftTemplate/gift.html', {'form': form})

def thanksView(request) :
	if request.method == 'POST':
		formGiver = SampleGiverForm(request.POST)
		if formGiver.is_valid() :
			giver = formGiver.save()
			sample = Sample(sampleGiver=giver)
			sample.save()
			sample.name = "PT"+str(sample.id)
			sample.save()
	return render(request, 'SmellGiftTemplate/thanks.html')