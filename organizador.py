import os
import shutil

pasta_origem = "arquivos"
tipos_arquivos = {
    "imagens": [".jpg", ".jpeg", ".png", ".gif"],
    "Documentos": [".pdf", ".txt", ".docx"],
    "Panilhas": [".xlsx", ".csv"]
}

for pasta in tipos_arquivos:
    caminho_pasta = os.path.join(pasta_origem, pasta)

    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

        for arquivo in os.listdir(pasta_origem):
            caminho_arquivo = os.path.join(pasta_origem, arquivo)

            if os.path.isfile(caminho_arquivo):
                nome, extensao = os.path.splitext(arquivo)

                for pasta, extensoes in tipos_arquivos.items():
                    if extensao.lower() in extensoes:
                        destino = os.path.join(pasta_origem, pasta, arquivo)
                        shutil.move(caminho_arquivo, destino)