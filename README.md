# Trabalho de Processamento Digital de Imagens

Este repositório contém o código-fonte de um visualizador interativo de imagens desenvolvido para o trabalho da disciplina de Processamento Digital de Imagens. A aplicação permite explorar diversas técnicas de manipulação, com foco em filtros, equalização de histograma (Padrão e CLAHE) e a importância dos espaços de cores no processamento.

### Integrantes do Grupo

GABRIEL AUGUSTO COSTEIRA DA SILVA GONÇALVES G766857
GUSTAVO DIAS DE OLIVEIRA - G7862G6 
KAIKY SOUZA PROENCA DE ANDRADE - N088575 
LUCAS PEDRO AMÉRICO DA SILVA  – T881HA3 

## Funcionalidades da Aplicação

O projeto consiste em um único script Python que gera uma galeria com 30 imagens processadas e as exibe em uma interface interativa, onde o usuário pode:
* Navegar entre as imagens com os botões "Anterior" e "Próximo".
* Ativar ou desativar a visualização do histograma correspondente a cada imagem.
* Analisar o histograma de imagens em tons de cinza ou de cada canal de cor (RGB).

## Tecnologias Utilizadas
* **Python 3**
* **OpenCV (`cv2`):** Para todas as operações de processamento de imagem.
* **NumPy:** Para manipulação de arrays e operações matemáticas.
* **Matplotlib:** Para a criação da interface gráfica, exibição das imagens e plotagem dos histogramas.
