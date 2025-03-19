import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Plancksches Strahlungsgesetz (vereinfachte Darstellung der Spitzenfrequenz)
def peak_wavelength(T):
    # Wiensches Verschiebungsgesetz: lambda_max = b / T
    # b = 2.89777 × 10^-3 m·K (Wiensche Verschiebungskonstante)
    b = 2.89777e-3  # in m*K
    return b / T  # Wellenlänge in Metern

def wavelength_to_rgb(wavelength):
    """Wandelt eine Wellenlänge in den sichtbaren Bereich in eine RGB-Farbe um"""
    gamma = 0.8
    intensity_max = 255
    factor = 0.0
    R = G = B = 0
    
    if 380 <= wavelength < 440:
        R = -(wavelength - 440) / (440 - 380)
        B = 1.0
    elif 440 <= wavelength < 490:
        G = (wavelength - 440) / (490 - 440)
        B = 1.0
    elif 490 <= wavelength < 510:
        G = 1.0
        B = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        R = (wavelength - 510) / (580 - 510)
        G = 1.0
    elif 580 <= wavelength < 645:
        R = 1.0
        G = -(wavelength - 645) / (645 - 580)
    elif 645 <= wavelength <= 780:
        R = 1.0
    
    # Intensität anpassen
    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength < 645:
        factor = 1.0
    elif 645 < wavelength <= 780:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 645)
    
    R = int(intensity_max * (R * factor) ** gamma)
    G = int(intensity_max * (G * factor) ** gamma)
    B = int(intensity_max * (B * factor) ** gamma)
    
    return (R / 255, G / 255, B / 255)

# Initiale Temperatur
temp_init = 3000  # in Kelvin

# Erstellen der Figur und Achsen
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Erstellen der x-Achse (sichtbares Licht: 380 nm - 780 nm)
wavelengths = np.linspace(380, 780, 100)
frequencies = 3e8 / (wavelengths * 1e-9)  # c = f * lambda => f = c / lambda

# Linienplot
line, = ax.plot([peak_wavelength(temp_init) * 1e9], [3e8 / peak_wavelength(temp_init)], 'ro', markersize=8, label='Peak-Frequenz')
ax.set_xlabel("Wellenlänge (nm)")
ax.set_ylabel("Frequenz (Hz)")
ax.set_title("Spektrum der Schwarzkörperstrahlung")
ax.set_xlim(380, 780)
ax.set_ylim(3e14, 8e14)
ax.legend()

# Farbverlauf unter der Kurve
for i, wl in enumerate(wavelengths):
    ax.axvspan(wl, wl + (780 - 380) / 100, color=wavelength_to_rgb(wl), alpha=0.5)

# Slider für Temperatur
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
temp_slider = Slider(ax_slider, 'Temperatur (K)', 1000, 10000, valinit=temp_init)

# Update-Funktion
def update(val):
    T = temp_slider.val
    peak_wl = peak_wavelength(T) * 1e9  # in nm
    peak_freq = 3e8 / (peak_wavelength(T))  # c = f * lambda
    line.set_xdata([peak_wl])
    line.set_ydata([peak_freq])
    fig.canvas.draw_idle()

temp_slider.on_changed(update)

plt.show()
