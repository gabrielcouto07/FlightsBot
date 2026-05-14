"""WhatsApp message formatting utilities"""

from datetime import datetime


def format_free_alert(flight: dict) -> str:
    """
    Format a flight deal message for free group alerts.
    
    Args:
        flight: Normalized flight dictionary from scraper
    
    Returns:
        Formatted WhatsApp message string with emoji
    """
    origin = flight.get("origin", "??")
    destination = flight.get("destination", "??")
    price = flight.get("price", 0)
    airline = flight.get("airline", "Unknown")
    departure_at = flight.get("departure_at", "")
    duration = flight.get("duration_minutes", 0)
    booking_url = flight.get("deep_link", "")
    
    # Parse departure date
    try:
        dep_datetime = datetime.fromisoformat(departure_at.replace("Z", "+00:00"))
        dep_date = dep_datetime.strftime("%d/%m/%Y")
    except:
        dep_date = "TBA"
    
    # Format duration
    hours = duration // 60
    minutes = duration % 60
    duration_str = f"{hours}h {minutes}min" if hours > 0 else f"{minutes}min"
    
    # Format price
    price_formatted = f"R$ {price:,.0f}".replace(",", ".")
    
    message = f"""✈️ *PROMOÇÃO DE PASSAGEM!*
━━━━━━━━━━━━━━━━━━━━
🛫 *{origin} → {destination}*
📅 *Ida:* {dep_date}
💰 *A partir de:* {price_formatted}
🏢 *Companhia:* {airline}
⏱️ *Duração:* {duration_str}
━━━━━━━━━━━━━━━━━━━━
🔗 Reservar agora: {booking_url}

_Preço capturado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}_
_⚠️ Preços podem mudar. Confira antes de comprar._"""
    
    return message


def format_paid_alert(user_name: str, flight: dict) -> str:
    """
    Format a personalized flight deal message for paid users.
    
    Args:
        user_name: User's name for personalization
        flight: Normalized flight dictionary from scraper
    
    Returns:
        Formatted WhatsApp message string with emoji
    """
    origin = flight.get("origin", "??")
    destination = flight.get("destination", "??")
    price = flight.get("price", 0)
    airline = flight.get("airline", "Unknown")
    departure_at = flight.get("departure_at", "")
    duration = flight.get("duration_minutes", 0)
    booking_url = flight.get("deep_link", "")
    
    # Parse departure date
    try:
        dep_datetime = datetime.fromisoformat(departure_at.replace("Z", "+00:00"))
        dep_date = dep_datetime.strftime("%d/%m/%Y")
    except:
        dep_date = "TBA"
    
    # Format duration
    hours = duration // 60
    minutes = duration % 60
    duration_str = f"{hours}h {minutes}min" if hours > 0 else f"{minutes}min"
    
    # Format price
    price_formatted = f"R$ {price:,.0f}".replace(",", ".")
    
    greeting = f"Oi {user_name}! " if user_name else "Olá! "
    
    message = f"""{greeting}Encontrei uma oferta para você 👇

✈️ *PROMOÇÃO DE PASSAGEM!*
━━━━━━━━━━━━━━━━━━━━
🛫 *{origin} → {destination}*
📅 *Ida:* {dep_date}
💰 *A partir de:* {price_formatted}
🏢 *Companhia:* {airline}
⏱️ *Duração:* {duration_str}
━━━━━━━━━━━━━━━━━━━━
🔗 Reservar agora: {booking_url}

_Preço capturado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}_
_⚠️ Preços podem mudar. Confira antes de comprar._"""
    
    return message


def format_help_message() -> str:
    """
    Format a help message with available commands.
    
    Returns:
        Formatted help message
    """
    return """📚 *COMANDOS DISPONÍVEIS*

/alerta GRU MIA 2026-08-01 2026-08-15 1500
_Cria um alerta para essa rota com preço máximo de R$1500_

/alerta GRU qualquer 2026-07-01 2026-07-31 800
_Qualquer destino de um local até uma data com preço máximo_

/listar
_Lista todos os seus alertas ativos_

/pausar 3
_Pausa o alerta número 3_

/deletar 3
_Deleta o alerta número 3_

/status
_Mostra o status da sua conta_

/ajuda
_Mostra esta mensagem_

━━━━━━━━━━━━━━━━━━━
Dúvidas? Entre em contato com nosso suporte! 🤝"""


def format_status_message(user_name: str, plan: str, alert_count: int) -> str:
    """
    Format an account status message.
    
    Args:
        user_name: User's name
        plan: User's plan (free or paid)
        alert_count: Number of active alerts
    
    Returns:
        Formatted status message
    """
    plan_emoji = "🆓" if plan == "free" else "⭐"
    plan_label = "Gratuito" if plan == "free" else "Premium"
    
    return f"""👤 *SEUS DADOS*

Nome: {user_name}
Plano: {plan_emoji} {plan_label}
Alertas Ativos: {alert_count}

Obrigado por usar o Flight Bot! ✈️"""
