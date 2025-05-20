import os
from sqlalchemy.orm import Session
from app.core.conexaoBD import get_db
from app.models.videos import Videos


def import_videos():
    pasta_videos = 'app/static/videos'
    arquivos = os.listdir(pasta_videos)

    db: Session = next(get_db())

    for arquivo in arquivos:
        if arquivo.endswith('.mpeg'):
            video_existente = db.query(Videos).filter(
                Videos.url == f"/static/videos/{arquivo}").first()
            if video_existente:
                print(f"O video já está cadastrado! Arquivo: {arquivo}")
                continue

            novo_video = Videos(
                nome=os.path.splitext(arquivo)[0],
                artista="Artista Desconhecido",
                descricao="Descrição não fornecida",
                duracao=0, 
                genero="Gênero Desconhecido",
                album="Álbum Desconhecido",
                url=f"/static/videos/{arquivo}"
            )
            db.add(novo_video)
            print(f"O video foi adicionado com êxito! Arquivo: {arquivo}")

    db.commit()
    print("\n🎵 Banco de dados atualizado com os videos da pasta!")


if __name__ == "__main__":
    import_videos()
