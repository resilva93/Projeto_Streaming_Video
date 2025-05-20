import requests as rq

# Chave da API do YouTube
chaveAcessoYT = 'AIzaSyAZpDOyplCZuMaFHhWZEHdHi93LC5Vx6RI'
yt_consulta = 'https://www.googleapis.com/youtube/v3/search?'

def consultaVideosYT():
    st.title("Busca de Vídeos no YouTube 🎥")
    
    pesquisa = st.text_input('Digite um termo para pesquisar no YouTube')

    if pesquisa:
        # Parâmetros da requisição
        params = {
            'key': chaveAcessoYT,
            'q': pesquisa,
            'type': 'video',
            'part': 'snippet',
            'maxResults': 5
        }

        response = rq.get(yt_consulta, params=params)

        if response.status_code == 200:
            data = response.json()
            video_ids = []

            for item in data.get('items', []):
                video_id = item['id']['videoId']
                titulo = item['snippet']['title']
                descricao = item['snippet']['description']
                video_ids.append(video_id)

                # Exibe o título, descrição e o vídeo na tela
                st.subheader(titulo)
                #st.caption(descricao)
                st.video(f"https://www.youtube.com/watch?v={video_id}")

            # Salva os video_ids em um arquivo
            with open('video_ids.txt', 'w') as f:
                for vid in video_ids:
                    f.write(vid + '\n')

            st.success("IDs dos vídeos salvos em video_ids.txt.")
            return video_ids

        else:
            st.error("Erro ao acessar a API do YouTube.")
            return []

# Executa a função
consultaVideosYT()