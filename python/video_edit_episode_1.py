from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os 

# --- Configurações ---
# MUDA ESTES CAMINHOS para apontar para os teus ficheiros
FICHEIRO_AUDIO = 'python/podcast/episode_1_san _francisco.wav'
FICHEIRO_IMAGEM = 'python/podcast/episode_1_san _francisco.png'
FICHEIRO_VIDEO_OUTPUT = 'python/podcast/episode_1_san _francisco.mp4' # Nome do ficheiro de vídeo que será criado

# --- Verifica se os ficheiros de entrada existem ---
if not os.path.exists(FICHEIRO_AUDIO):
    print(f"Erro: O ficheiro de áudio '{FICHEIRO_AUDIO}' não foi encontrado.")
    exit() # Termina o script se o áudio não existe

if not os.path.exists(FICHEIRO_IMAGEM):
    print(f"Erro: O ficheiro de imagem '{FICHEIRO_IMAGEM}' não foi encontrado.")
    exit() # Termina o script se a imagem não existe

# --- Lógica de Criação do Vídeo ---
try:
    print(f"A carregar o áudio: {FICHEIRO_AUDIO}")
    audio_clip = AudioFileClip(FICHEIRO_AUDIO)
    audio_duration = audio_clip.duration # Guarda a duração do áudio em segundos

    if not audio_duration or audio_duration <= 0:
         print("Erro: O áudio parece não ter duração válida.")
         audio_clip.close() # Fecha o clipe de áudio
         exit()

    print(f"Duração do áudio: {audio_duration:.2f} segundos")

    print(f"A carregar a imagem: {FICHEIRO_IMAGEM}")
    image_clip = ImageClip(FICHEIRO_IMAGEM)
    image_clip.duration = audio_duration 
    
    print("A duração da imagem foi ajustada...")
    
    # Cria um vídeo composto usando a imagem
    print("A criar clip de vídeo...")
    video_clip = CompositeVideoClip([image_clip])
    video_clip.duration = audio_duration  # Define a duração explicitamente para o clip composto
    
    # Define o áudio do clipe de vídeo
    print("A adicionar áudio ao vídeo...")
    video_clip.audio = audio_clip
    # Define os frames por segundo (FPS). 1 FPS é suficiente para uma imagem estática
    # e ajuda a manter o tamanho do ficheiro mais baixo.
    video_clip.fps = 1

    # Escreve o resultado final no ficheiro de vídeo
    print(f"A escrever o ficheiro de vídeo final: {FICHEIRO_VIDEO_OUTPUT}")
    video_clip.write_videofile(
        FICHEIRO_VIDEO_OUTPUT,
        codec='libx264',
        audio_codec='aac'
        # Sem parâmetros adicionais
    )

    print("\nProcesso concluído com sucesso!")
    print(f"O vídeo foi guardado como: {FICHEIRO_VIDEO_OUTPUT}")

except Exception as e:
    print(f"\nOcorreu um erro durante o processo:")
    print(e)
    print("Verifica se os nomes dos ficheiros estão corretos e se o FFmpeg está instalado.")

finally:
    # É uma boa prática fechar os clipes para libertar recursos,
    # embora write_videofile geralmente faça isso.
    if 'audio_clip' in locals() and audio_clip:
        audio_clip.close()
    if 'image_clip' in locals() and image_clip:
        image_clip.close()
    if 'video_clip' in locals() and video_clip:
        video_clip.close()
    print("Recursos libertados.")