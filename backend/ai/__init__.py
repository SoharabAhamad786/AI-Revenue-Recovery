"""AI service abstraction for RecoverAI."""
from .base import AIService
from .mock_provider import MockAIProvider

__all__ = ['AIService', 'MockAIProvider']
