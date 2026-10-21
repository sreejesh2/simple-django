import socket

from django.shortcuts import render

from .models import Photo

WORKSHOP = {
    'department': 'Department of Computer Applications',
    'type': 'Faculty Development Workshop',
    'title': 'Exploring Web Development with Python & Django',
    'date': '22 October 2026',
    'time': '10:00 AM',
    'venue': 'BCA Lab 3',
    'speakers': [
        {'name': 'Sajay N J', 'role': 'Senior Faculty & HOD - Full Stack', 'org': 'Luminar Technolab'},
        {'name': 'Sreejesh V S', 'role': 'CTO', 'org': 'Anvitha Infotech'},
    ],
    'organisers': [
        {'name': 'Dr. Solomon K Peter', 'role': 'Principal'},
        {'name': 'Dr. Shaju Varughese', 'role': 'Dean'},
        {'name': 'Ms. Nimmy N Abraham', 'role': 'HOD'},
        {'name': 'Vandana V, Reshmi K P', 'role': 'Faculty Coordinators'},
    ],
    'contacts': ['9496096650', '6282057846'],
}

COLLEGE = {
    'name': 'Marian Academy of Management Studies',
    'short_name': 'MAMS',
    'partner': 'Yeldo Mar Baselios College',
    'affiliation': 'Affiliated to Mahatma Gandhi University, Kottayam',
    'phone': '9446 676 125',
    'address': 'Marian Village, Puthuppady, Kothamangalam, Ernakulam Dist, Kerala - 686673',
    'website': 'https://www.mams.ac.in',
    'website_label': 'www.mams.ac.in',
    'instagram': 'https://www.instagram.com/mams_official_/',
    'instagram_label': '@mams_official_',
}


def classroom_context(request, page_title, heading):
    port = request.META.get('SERVER_PORT', '8000')
    return {
        'page_title': page_title,
        'heading': heading,
        'class_url': f'http://{lan_ip()}:{port}',
        'workshop': WORKSHOP,
        'college': COLLEGE,
    }


def lan_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        return sock.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        sock.close()


def home(request):
    context = classroom_context(request, 'Django Workshop · MAMS', WORKSHOP['title'])
    try:
        context['photos'] = list(Photo.objects.all())
    except Exception:
        context['photos'] = []
    return render(request, 'pages/home.html', context)


def cloudinary_guide(request):
    return render(
        request,
        'pages/cloudinary.html',
        classroom_context(request, 'Cloudinary', 'Cloudinary — store images'),
    )


def supabase_guide(request):
    return render(
        request,
        'pages/supabase.html',
        classroom_context(request, 'Supabase', 'Supabase — Postgres database'),
    )


def render_guide(request):
    return render(
        request,
        'pages/render.html',
        classroom_context(request, 'Render', 'Render — put the site online'),
    )
