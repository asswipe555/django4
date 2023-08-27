from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.shortcuts import render
import requests

TRELLO_API_KEY = 'b0e246adc54e1dd1c6ea7ce292441746'
TRELLO_TOKEN = 'ATTAcde8a1ecf53c48f00a9756a062dc5f368bb924ff0837223f4c429cf2c33f78ca68FBD0AC'
TRELLO_WORKSPACE_ID = 'text183'  # ワークスペースIDをここに設定
    
class AboutView(TemplateView):
    template_name ="about.html"

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    
def trello_view(request):
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        
        # Step 1: Get boards in the workspace
        boards_url = f'https://api.trello.com/1/organizations/{TRELLO_WORKSPACE_ID}/boards'
        boards_params = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
        }
        boards_response = requests.get(boards_url, params=boards_params)
        boards_data = boards_response.json()

        members_counts = {}  # Dictionary to store member card counts

        # Step 2: Iterate through boards and fetch cards and members
        for board in boards_data:
            board_id = board['id']

            cards_url = f'https://api.trello.com/1/boards/{board_id}/cards'
            cards_params = {
                'key': TRELLO_API_KEY,
                'token': TRELLO_TOKEN,
            }
            cards_response = requests.get(cards_url, params=cards_params)
            cards_data = cards_response.json()

            for card in cards_data:
                card_id = card['id']
                card_members_url = f'https://api.trello.com/1/cards/{card_id}/members'
                card_members_params = {
                    'key': TRELLO_API_KEY,
                    'token': TRELLO_TOKEN,
                }
                card_members_response = requests.get(card_members_url, params=card_members_params)
                card_members_data = card_members_response.json()

                for member in card_members_data:
                    member_id = member['id']
                    member_name = member['fullName']
                    if member_id not in members_counts:
                        members_counts[member_id] = {'name': member_name, 'count': 0}
                    members_counts[member_id]['count'] += 1

        for member_id, member_data in members_counts.items():
            member_name = member_data['name']
            card_count = member_data['count']

        if search_text == "/card":
            text_data = 'メンバー別トレロカード数一覧' + '\n'
            text_data += f'メンバー: {member_name}: カード: {card_count}'
            trello_data = text_data  # APIから取得したデータ
            return render(request, 'index.html', {'trello_data': trello_data})
    return render(request, 'index.html')
 

