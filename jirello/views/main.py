from django.shortcuts import render


def main(request):
    return render(request, 'jirello/main_page.html')
