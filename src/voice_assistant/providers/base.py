class ProviderError(RuntimeError):
    """Error base para fallos de proveedor."""

    def __init__(self, provider: str, message: str) -> None:
        super().__init__(f"[{provider}] {message}")
        self.provider = provider
        self.message = message
