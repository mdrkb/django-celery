import json
from django.shortcuts import render
from celery.result import AsyncResult
from django.http import HttpResponse
from myapp.forms import GenerateRandomUserForm
from myapp.tasks import create_random_user_accounts


def generate_random_user(request):
    if request.method == 'POST':
        form = GenerateRandomUserForm(request.POST)
        if form.is_valid():
            total_user = form.cleaned_data.get('total_user')
            task = create_random_user_accounts.delay(total_user)
            return HttpResponse(json.dumps({'task_id': task.id}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'task_id': None}), content_type='application/json')
    else:
        form = GenerateRandomUserForm
    return render(request, 'myapp/index.html', {'form': form})


def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('No job id given.')
