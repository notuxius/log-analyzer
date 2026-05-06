class LogAnalyzerError(Exception):
    """Base exception for log analyzer errors."""


class LogFileNotFoundError(LogAnalyzerError):
    """Raised when the log file does not exist."""


class EmptyLogFileError(LogAnalyzerError):
    """Raised when the log file has no usable content."""


class InvalidLogLevelError(LogAnalyzerError):
    """Raised when a log entry contains an unsupported level."""


class UnsupportedFormatError(LogAnalyzerError):
    """Raised when an unsupported report format is requested."""


class EmptyReportError(LogAnalyzerError):
    """Raised when trying to save an empty report."""
