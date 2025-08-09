"""The JPG to PNG Converter integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .services import async_setup_services

# Variable globale pour éviter l'enregistrement multiple des services
_SERVICES_REGISTERED = False

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the JPG to PNG Converter component."""
    global _SERVICES_REGISTERED
    
    # Enregistrer les services une seule fois au démarrage
    if not _SERVICES_REGISTERED:
        await async_setup_services(hass)
        _SERVICES_REGISTERED = True
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JPG to PNG Converter from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # Les services sont enregistrés dans async_setup
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        
        # Si plus d'entrées, supprimer les services
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)
            global _SERVICES_REGISTERED
            if _SERVICES_REGISTERED:
                hass.services.async_remove(DOMAIN, "convert")
                _SERVICES_REGISTERED = False
    
    return True


