import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

matplotlib.rcParams['toolbar'] = 'None'

def equalize_color_hsv(color_img):
    hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def apply_clahe_color(color_img, clahe_obj):
    hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = clahe_obj.apply(hsv[:, :, 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def equalize_color_bgr(color_img):
    bgr_eq_result = np.zeros_like(color_img)
    for i in range(3):
        bgr_eq_result[:, :, i] = cv2.equalizeHist(color_img[:, :, i])
    return bgr_eq_result

try:
    color_image = cv2.imread("dex.jpg")
    if color_image is None:
        raise FileNotFoundError
except FileNotFoundError:
    print("⚠️ Erro: 'dex.jpg' não encontrado. Verifique o caminho!")
    exit()

# --- (0,5 ponto): A partir de uma imagem colorida, crie as seguintes imagens base ---
gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
darker_image = cv2.convertScaleAbs(color_image, alpha=0.7, beta=0)
brighter_image = cv2.convertScaleAbs(color_image, alpha=1.3, beta=30)
kernel_nitidez = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpened_image = cv2.filter2D(color_image, -1, kernel_nitidez)
gaussian_noise = np.random.normal(0, 30, gray_image.shape).astype(np.uint8)
noisy_image = cv2.add(gray_image, gaussian_noise)

base_images_to_process = [
    ("Original", color_image, None),
    ("Escura", darker_image, None),
    ("Clara", brighter_image, None),
    ("Grayscale", gray_image, "gray"),
    ("Com Ruído", noisy_image, "gray"),
    ("Com Detalhes Finos", sharpened_image, None)
]

image_gallery = []
clahe1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
clahe2 = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(16,16))

# --- (1,0 ponto): Apresente os resultados de se utilizar a equalização básica e o CLAHE ---

for title, base_img, cmap in base_images_to_process:
    image_gallery.append((f"{title}", base_img, cmap))
    if base_img.ndim == 3:
        image_gallery.append((f"{title} - Equalização Básica", equalize_color_hsv(base_img), cmap))
        image_gallery.append((f"{title} - CLAHE (2.0, 8x8)", apply_clahe_color(base_img, clahe1), cmap))
        image_gallery.append((f"{title} - CLAHE (4.0, 16x16)", apply_clahe_color(base_img, clahe2), cmap))
    else:
        image_gallery.append((f"{title} - Equalização Básica", cv2.equalizeHist(base_img), cmap))
        image_gallery.append((f"{title} - CLAHE (2.0, 8x8)", clahe1.apply(base_img), cmap))
        image_gallery.append((f"{title} - CLAHE (4.0, 16x16)", clahe2.apply(base_img), cmap))

# --- (0,5 ponto): Comparação de equalização em espaço de cores HSV x BGR ---
image_gallery.append(("Original (Ref. HSV vs BGR)", color_image, None))
image_gallery.append(("Equalização em HSV (Correto)", equalize_color_hsv(color_image), None))
image_gallery.append(("Equalização em BGR (Incorreto)", equalize_color_bgr(color_image), None))

current_index = 0
total_images = len(image_gallery)
histogram_visible = False

fig = plt.figure(figsize=(10, 7))
ax_image = fig.add_subplot(1, 1, 1)
ax_histogram = fig.add_subplot(1, 2, 2)

manager = plt.get_current_fig_manager()
manager.set_window_title("Dexter - Cores (Processamento Digital de Imagens)")

pos_img_full = [0.1, 0.2, 0.8, 0.7]
pos_img_split = [0.07, 0.2, 0.45, 0.7]
pos_hist_split = [0.58, 0.2, 0.35, 0.7]

def plot_histogram(ax, image):
    ax.clear()
    if image.ndim == 3:
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            ax.plot(hist, color=color)
        ax.legend(['Canal Azul', 'Canal Verde', 'Canal Vermelho'])
    else:
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        ax.plot(hist, color='gray')
    ax.set_title("Histograma")
    ax.set_xlabel("Intensidade")
    ax.set_ylabel("Qtde. de Pixels")
    ax.set_xlim([0, 256])

def update_display():
    if histogram_visible:
        ax_image.set_position(pos_img_split)
        ax_histogram.set_position(pos_hist_split)
        ax_histogram.set_visible(True)
        btn_hist_toggle.label.set_text('Ocultar Histograma')
    else:
        ax_image.set_position(pos_img_full)
        ax_histogram.set_visible(False)
        btn_hist_toggle.label.set_text('Mostrar Histograma')
    
    title, image, cmap = image_gallery[current_index]
    ax_image.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if cmap is None else image, cmap=cmap)
    ax_image.set_title(f"{title}\n({current_index + 1}/{total_images})")
    ax_image.axis("off")
    
    if histogram_visible:
        plot_histogram(ax_histogram, image)
    fig.canvas.draw_idle()

def next_image(event):
    global current_index
    if current_index < total_images - 1:
        current_index += 1
        update_display()
        update_navigation_buttons()

def prev_image(event):
    global current_index
    if current_index > 0:
        current_index -= 1
        update_display()
        update_navigation_buttons()

def toggle_histogram(event):
    global histogram_visible
    histogram_visible = not histogram_visible
    update_display()

ax_prev = plt.axes([0.24, 0.05, 0.15, 0.075])
ax_hist_toggle = plt.axes([0.425, 0.05, 0.15, 0.075])
ax_next = plt.axes([0.61, 0.05, 0.15, 0.075])

btn_prev = Button(ax_prev, 'Anterior')
btn_hist_toggle = Button(ax_hist_toggle, 'Mostrar Histograma')
btn_next = Button(ax_next, 'Próximo')

DISABLED_COLOR = 'lightgray'
DEFAULT_COLOR = btn_prev.color
DEFAULT_HOVER_COLOR = btn_prev.hovercolor

def update_button_style(button, text, is_active):
    face_color = DEFAULT_COLOR if is_active else DISABLED_COLOR
    hover_color = DEFAULT_HOVER_COLOR if is_active else DISABLED_COLOR
    button.label.set_text(text)
    button.ax.set_facecolor(face_color)
    button.hovercolor = hover_color

def update_navigation_buttons():
    is_first = (current_index == 0)
    update_button_style(btn_prev, 'Início' if is_first else 'Anterior', not is_first)
    is_last = (current_index == total_images - 1)
    update_button_style(btn_next, 'Fim' if is_last else 'Próximo', not is_last)
    fig.canvas.draw_idle()

btn_prev.on_clicked(prev_image)
btn_hist_toggle.on_clicked(toggle_histogram)
btn_next.on_clicked(next_image)

update_display()
update_navigation_buttons()

plt.show()