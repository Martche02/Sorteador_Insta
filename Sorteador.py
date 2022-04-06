from instagram_private_api import Client
from tkinter import *
import random
import re
import json

def pegar_vencedor():
    with open("credenciais.json", encoding='utf-8') as credenciais:
        data = json.load(credenciais)
        usuario = data['usuario']
        senha = data['senha']

    api = Client(usuario, senha)

    UUID = api.generate_uuid() # Necessário para a API
    followers = api.user_followers(api.authenticated_user_id, rank_token=UUID)['users'] # Lista de usuários que seguem o perfil do Neps.
    followers = [follower['pk'] for follower in followers] # Mas queremos uma lista apenas com o ID dos usuários

    POST_CODE =  "CbxTsrEOSrY"
    post_id = None

    feed = api.self_feed() # Primeiro pegamos todas as postagens no nosso feed.
    for item in feed['items']: # Iteramos em cada postagem.
        if item['code'] == POST_CODE: # Se a postagem tem code igual a POST_CODE
            post_id = item['id'] # Salvamos o ID dessa postagem na variável post_id
            break

    users_valid_comments = []

    comments = api.media_n_comments(post_id, n=3604) # Vamos pegar os 3604 primeiros comentários do nosso post
    for comment in comments:	    
        match = re.findall(r"(@\w*)", comment['text']) # Checar se o usuário marcou uma pessoa usando regex
        if(len(match) >= 1 and comment['user_id'] in followers): # Se o usuário realmente marcou uma pessoa e segue o perfil do Neps, adicionamos ele nos comentários válidos
            users_valid_comments.append(comment['user_id']) # Vamos armazenar o id do usuário, note que o mesmo usuário pode aparecer várias vezes se tiver postado múltiplos comentários válidos.		
    # print(users_valid_comments)
    random.shuffle(users_valid_comments)
    # print(users_valid_comments)
    # winners = set()
    winner_id = users_valid_comments[0]

    winner = api.user_info(winner_id)['user'] # Use a API para pegar informações detalhadas dessa pessoa
    print(f"{winner['full_name']} ({winner['username']})") # Imprima nome completo e nome de usuário no Instagram.
    #Uptade Janela text with the winner
    texto["text"] = f"{winner['full_name']} ({winner['username']})"


janela = Tk()
janela.title("VENCEDOR - Sorteador de Comentários")
texto = Label(janela, text="Clique no botão para sortear um vencedor!")
texto.grid(column=0, row=0, padx=10, pady=10)

botao = Button(janela, text="Sortear Vencedor", command=pegar_vencedor)
botao.grid(column=0, row=1, padx=10, pady=10)

texto_resposta = Label(janela, text="")
texto_resposta.grid(column=0, row=2, padx=10, pady=10)


janela.mainloop()