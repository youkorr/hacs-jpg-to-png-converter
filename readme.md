<p align="center">
  <img src="https://raw.githubusercontent.com/youkorr/hacs-jpg-to-png-converter/main/custom_components/jpg_to_png_converter/images/logo.png" alt="JPG/WebP to PNG Converter" width="400"/>
</p>

# JPG to PNG Converter - Guide ESPHome

Cette intégration HACS convertit vos images JPG/JPEG/WebP en PNG optimisées pour ESPHome, avec gestion de l'endianness pour les écrans RGB565.

## 🎯 Cas d'usage ESPHome

### Problème résolu
Les écrans ESPHome (comme les écrans TFT) utilisent souvent le format RGB565 avec un ordre d'octets spécifique :
- **Big-endian** : Ordre naturel des octets
- **Little-endian** : Octets inversés (courant sur ESP32)

### Solution
Cette intégration permet de préparer vos images avec le bon ordre d'octets avant de les utiliser dans ESPHome.

## 📋 Configuration ESPHome

### Configuration type dans ESPHome :
```yaml
# config.yaml ESPHome
image:
  - file: 'source/images/back72.png'
    id: back
    type: RGB565
    byte_order: little_endian  # ou big_endian
```

### Configuration correspondante dans Home Assistant :
```yaml
# Automation Home Assistant
service: jpg_to_png_converter.convert
data:
  local_input_path: "/config/esphome/source/images/back72.jpg"
  output_path: "/config/esphome/source/images/back72.png"
  resolution: "320x240"
  optimize_mode: "esp32"
  byte_order: "swap"  # Pour little_endian ESPHome
```

## 🔧 Correspondance des paramètres

| ESPHome | Home Assistant | Description |
|---------|---------------|-------------|
| `byte_order: big_endian` | `byte_order: "default"` | Ordre naturel |
| `byte_order: little_endian` | `byte_order: "swap"` | Octets inversés |
| `type: RGB565` | `optimize_mode: "esp32"` | Optimisation ESP32 |

## 🚀 Workflow recommandé

1. **Préparez vos images** avec cette intégration
2. **Testez** avec `byte_order: "default"` d'abord
3. **Si les couleurs sont incorrectes**, utilisez `byte_order: "swap"`
4. **Copiez** le PNG généré dans votre dossier ESPHome
5. **Compilez** votre projet ESPHome

## 💡 Conseils

### Détection automatique
Si vous ne savez pas quel ordre utiliser :
1. Créez une image test avec `byte_order: "default"`
2. Flashez sur votre ESP32
3. Si les couleurs Rouge/Bleu sont inversées → utilisez `byte_order: "swap"`

### Optimisation ESP32
```yaml
service: jpg_to_png_converter.convert
data:
  optimize_mode: "esp32"  # Limite à 256 couleurs
  resolution: "320x240"   # Résolution écran
  byte_order: "swap"      # Pour little_endian
```

### Automation complète
```yaml
# Automation pour traiter plusieurs images
automation:
  - alias: "Convert Images for ESPHome"
    trigger:
      platform: homeassistant
      event: start
    action:
      - repeat:
          for_each:
            - "background.jpg"
            - "icon1.webp"
            - "icon2.jpeg"
          sequence:
            - service: jpg_to_png_converter.convert
              data:
                local_input_path: "/config/www/original/{{ repeat.item }}"
                output_path: "/config/esphome/images/{{ repeat.item | regex_replace('\\.(jpg|jpeg|webp)$', '.png') }}"
                resolution: "320x240"
                optimize_mode: "esp32"
                byte_order: "swap"
```

## 🎨 Exemples pratiques

### Image pour écran 320x240 little-endian :
```yaml
service: jpg_to_png_converter.convert
data:
  url_input_path: "https://example.com/image.jpg"
  output_path: "/config/esphome/images/converted.png"
  resolution: "320x240"
  optimize_mode: "esp32"
  byte_order: "swap"
```

### Image haute résolution conservée :
```yaml
service: jpg_to_png_converter.convert
data:
  local_input_path: "/config/www/hires.jpg"
  output_path: "/config/esphome/images/hires.png"
  resolution: "original"
  optimize_mode: "none"
  byte_order: "default"
```

## 🔍 Dépannage

### Couleurs inversées Rouge/Bleu ?
→ Changez `byte_order` de "default" à "swap" ou vice-versa

### Image trop lourde pour ESP32 ?
→ Utilisez `optimize_mode: "esp32"` et une résolution adaptée

### Erreur de compilation ESPHome ?
→ Vérifiez que le fichier PNG est dans le bon dossier et accessible

---

*Cette intégration simplifie la préparation d'images pour ESPHome en gérant automatiquement l'endianness et l'optimisation.*

