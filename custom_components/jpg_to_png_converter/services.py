async def convert_jpg_to_png(call: ServiceCall) -> None:
    """Handle the service call."""
    input_paths = call.data.get("input_path")
    
    # Assurez-vous que input_paths est une liste
    if not isinstance(input_paths, list):
        input_paths = [input_paths]
    
    for input_path in input_paths:
        # Vérifiez que le fichier existe et a une extension valide
        if not (input_path.lower().endswith(('.jpg', '.jpeg')) and os.path.exists(input_path)):
            _LOGGER.error(f"Invalid or non-existent file: {input_path}")
            continue

        output_path = call.data.get("output_path", None)
        resolution = call.data.get("resolution", "320x240")
        optimize_mode = call.data.get("optimize_mode", "none")
        
        # Si aucun chemin de sortie n'est spécifié, générez un nom de fichier unique
        if not output_path:
            base_name = os.path.splitext(os.path.basename(input_path))[0]  # Nom du fichier sans extension
            extension = "_jpeg.png" if input_path.lower().endswith('.jpeg') else "_jpg.png"
            output_path = os.path.join(os.path.dirname(input_path), base_name + extension)
        
        try:
            _LOGGER.debug(f"Opening image from {input_path}")
            img = Image.open(input_path)
            
            # Appliquer la résolution si nécessaire
            if resolution != "original":
                img = img.resize(RESOLUTIONS[resolution])
            
            # Enregistrer l'image au format PNG
            img.save(output_path, "PNG", optimize=(optimize_mode == "optimize"))
            _LOGGER.info(f"Image successfully converted and saved to {output_path}")
        
        except Exception as e:
            _LOGGER.error(f"Failed to convert image: {e}")
