"""WhatsApp command parser for paid users"""

import logging
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    """Result of parsing a command"""
    command_type: str  # "alerta", "listar", "pausar", "deletar", "status", "ajuda", "unknown"
    params: dict = None
    error_message: str = None
    
    def is_valid(self) -> bool:
        """Check if command parsed successfully"""
        return self.error_message is None


def parse_command(text: str) -> CommandResult:
    """
    Parse a WhatsApp message command for paid users.
    
    Supported commands:
    - /alerta GRU MIA 2026-08-01 2026-08-15 1500
    - /alerta GRU qualquer 2026-07-01 2026-07-31 800
    - /listar
    - /pausar 3
    - /deletar 3
    - /status
    - /ajuda
    
    Args:
        text: The message text from the user
    
    Returns:
        CommandResult with parsed command or error
    """
    text = text.strip()
    
    if not text.startswith("/"):
        return CommandResult(
            command_type="unknown",
            error_message="Use /ajuda for available commands"
        )
    
    parts = text.split()
    command = parts[0].lower().replace("/", "")
    
    # /ajuda command
    if command == "ajuda":
        return CommandResult(command_type="ajuda", params={})
    
    # /status command
    if command == "status":
        return CommandResult(command_type="status", params={})
    
    # /listar command
    if command == "listar":
        return CommandResult(command_type="listar", params={})
    
    # /pausar command
    if command == "pausar":
        if len(parts) < 2:
            return CommandResult(
                command_type="pausar",
                error_message="Uso: /pausar <id>"
            )
        try:
            alert_id = parts[1]
            return CommandResult(
                command_type="pausar",
                params={"alert_id": alert_id}
            )
        except Exception as e:
            return CommandResult(
                command_type="pausar",
                error_message=f"Erro ao processar ID: {str(e)}"
            )
    
    # /deletar command
    if command == "deletar":
        if len(parts) < 2:
            return CommandResult(
                command_type="deletar",
                error_message="Uso: /deletar <id>"
            )
        try:
            alert_id = parts[1]
            return CommandResult(
                command_type="deletar",
                params={"alert_id": alert_id}
            )
        except Exception as e:
            return CommandResult(
                command_type="deletar",
                error_message=f"Erro ao processar ID: {str(e)}"
            )
    
    # /alerta command
    if command == "alerta":
        if len(parts) < 6:
            return CommandResult(
                command_type="alerta",
                error_message="Uso: /alerta ORIGEM DESTINO DATA_INICIAL DATA_FINAL PRECO_MAXIMO"
            )
        
        try:
            origin = parts[1].upper()
            destination = parts[2].upper()
            date_from_str = parts[3]
            date_to_str = parts[4]
            max_price_str = parts[5]
            
            # Validate IATA codes
            if origin != "QUALQUER" and len(origin) != 3:
                return CommandResult(
                    command_type="alerta",
                    error_message="Origem deve ser código IATA (3 letras) ou 'qualquer'"
                )
            
            if destination != "QUALQUER" and len(destination) != 3:
                return CommandResult(
                    command_type="alerta",
                    error_message="Destino deve ser código IATA (3 letras) ou 'qualquer'"
                )
            
            # Parse dates
            try:
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
                date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
            except ValueError:
                return CommandResult(
                    command_type="alerta",
                    error_message="Datas devem estar no formato YYYY-MM-DD"
                )
            
            # Validate date range
            if date_from > date_to:
                return CommandResult(
                    command_type="alerta",
                    error_message="Data inicial deve ser anterior à data final"
                )
            
            # Parse price
            try:
                max_price = float(max_price_str)
                if max_price <= 0:
                    raise ValueError("Price must be positive")
            except ValueError:
                return CommandResult(
                    command_type="alerta",
                    error_message="Preço máximo deve ser um número positivo"
                )
            
            # Convert "qualquer" to None for wildcards
            origin = None if origin == "QUALQUER" else origin
            destination = None if destination == "QUALQUER" else destination
            
            return CommandResult(
                command_type="alerta",
                params={
                    "origin_iata": origin,
                    "destination_iata": destination,
                    "date_from": date_from,
                    "date_to": date_to,
                    "max_price": max_price,
                }
            )
        
        except Exception as e:
            logger.error(f"Error parsing /alerta command: {e}")
            return CommandResult(
                command_type="alerta",
                error_message=f"Erro ao processar comando: {str(e)}"
            )
    
    # Unknown command
    return CommandResult(
        command_type="unknown",
        error_message=f"Comando desconhecido: {command}. Use /ajuda para ver os comandos disponíveis"
    )
