# Error Messages Improvement Design

## Executive Summary

This document designs improvements to error messages in IterableData to provide actionable guidance, helping users understand what went wrong and how to fix it. The improvements include specific troubleshooting steps, common solutions, and links to relevant documentation.

## Current State

### Existing Error Messages

1. **Exception Hierarchy** (`iterable/exceptions.py`)
   - Comprehensive exception hierarchy with error codes
   - Contextual information (filename, row_number, byte_offset, etc.)
   - Basic error messages

2. **Current Message Format**
   - Descriptive but not always actionable
   - Sometimes technical without user-friendly guidance
   - Missing troubleshooting steps
   - Missing common solutions

### Example Current Messages

**FormatNotSupportedError**:
```python
"Format 'parquet' is not supported: Required dependency 'pyarrow' is not installed"
```

**FormatDetectionError**:
```python
"Could not detect file format for file: data.unknown. File extension not recognized and content detection failed"
```

**FormatParseError**:
```python
"Failed to parse csv format at data.csv:123 (byte 4567): Expecting ',' delimiter: line 123 column 45"
```

### Limitations

1. **No Actionable Guidance**: Messages describe the problem but don't tell users how to fix it
2. **No Troubleshooting Steps**: Missing step-by-step guidance
3. **No Common Solutions**: Don't suggest common fixes
4. **No Documentation Links**: Missing links to relevant documentation
5. **Technical Jargon**: Sometimes too technical for end users

## Improvement Goals

### 1. Actionable Guidance

Error messages should tell users:
- **What went wrong**: Clear description of the problem
- **Why it happened**: Explanation of the root cause
- **How to fix it**: Specific steps to resolve the issue
- **What to check**: Things to verify

### 2. User-Friendly Language

- Avoid technical jargon when possible
- Use clear, concise language
- Provide examples where helpful
- Include relevant context

### 3. Progressive Detail

- **Brief message**: Quick summary for experienced users
- **Detailed guidance**: Expanded information for troubleshooting
- **Documentation links**: Links to relevant docs

## Design Approach

### Option 1: Enhanced Exception Messages (Recommended)

**Approach**: Enhance exception `__str__` methods to include actionable guidance.

**Pros**:
- No API changes
- Backward compatible
- Easy to implement
- Works with existing exception handling

**Cons**:
- May make messages longer
- Need to balance detail vs brevity

**Implementation**:
```python
class FormatNotSupportedError(FormatError):
    def __str__(self):
        base_msg = super().__str__()
        guidance = self._get_actionable_guidance()
        return f"{base_msg}\n\n{guidance}"
    
    def _get_actionable_guidance(self):
        """Return actionable guidance for this error."""
        if "dependency" in self.reason.lower():
            return (
                "To fix this issue:\n"
                "1. Install the required dependency: pip install pyarrow\n"
                "2. Verify installation: python -c 'import pyarrow'\n"
                "3. Retry the operation\n"
                "\n"
                "For more information, see: https://iterabledata.io/docs/formats/parquet"
            )
        # ... other guidance ...
```

### Option 2: Separate Guidance Attribute

**Approach**: Add `guidance` attribute to exceptions with actionable steps.

**Pros**:
- Separates message from guidance
- Can be accessed programmatically
- Flexible formatting

**Cons**:
- Requires API changes
- More complex implementation

**Implementation**:
```python
class FormatNotSupportedError(FormatError):
    def __init__(self, format_id: str, reason: str | None = None):
        # ... existing code ...
        self.guidance = self._generate_guidance()
    
    def _generate_guidance(self):
        """Generate actionable guidance."""
        # ... guidance generation ...
```

### Option 3: Helper Function for Guidance

**Approach**: Create helper function that generates guidance from exception.

**Pros**:
- No exception changes
- Can be used selectively
- Easy to extend

**Cons**:
- Requires separate function call
- Not automatic

**Recommendation**: Option 1 (Enhanced Exception Messages) - provides automatic guidance while maintaining backward compatibility.

## Implementation Design

### 1. Enhanced Exception Messages

#### FormatNotSupportedError

**Current**:
```python
"Format 'parquet' is not supported: Required dependency 'pyarrow' is not installed"
```

**Improved**:
```python
"""Format 'parquet' is not supported: Required dependency 'pyarrow' is not installed

To fix this issue:
1. Install the required dependency:
   pip install pyarrow

2. Verify the installation:
   python -c 'import pyarrow'

3. Retry your operation

If you continue to have issues:
- Check that you're using a compatible Python version
- Verify your pip installation is working correctly
- See documentation: https://iterabledata.io/docs/formats/parquet
"""
```

#### FormatDetectionError

**Current**:
```python
"Could not detect file format for file: data.unknown. File extension not recognized and content detection failed"
```

**Improved**:
```python
"""Could not detect file format for file: data.unknown

The file format could not be determined because:
- File extension '.unknown' is not recognized
- Content-based detection failed (no matching magic numbers or patterns)

To fix this issue:
1. Specify the format explicitly:
   open_iterable('data.unknown', iterableargs={'format': 'csv'})

2. Rename the file with a recognized extension:
   mv data.unknown data.csv

3. Check the file content:
   - Verify the file is not corrupted
   - Ensure the file contains valid data
   - Check file encoding (use encoding parameter if needed)

For a list of supported formats, see: https://iterabledata.io/docs/formats/
"""
```

#### FormatParseError

**Current**:
```python
"Failed to parse csv format at data.csv:123 (byte 4567): Expecting ',' delimiter: line 123 column 45"
```

**Improved**:
```python
"""Failed to parse CSV format at data.csv:123 (byte 4567)

Error: Expecting ',' delimiter: line 123 column 45

This usually means:
- The CSV file has inconsistent delimiters
- There's an unescaped quote or special character
- The file encoding is incorrect

To fix this issue:
1. Check the problematic line:
   - Open the file and examine line 123
   - Look for unescaped quotes, commas, or special characters
   - Verify the delimiter matches your expectations

2. Specify the correct delimiter:
   open_iterable('data.csv', iterableargs={'delimiter': ';'})

3. Handle encoding issues:
   open_iterable('data.csv', iterableargs={'encoding': 'utf-8'})

4. Use error handling to skip problematic rows:
   open_iterable('data.csv', iterableargs={'on_error': 'skip'})

For more help, see: https://iterabledata.io/docs/formats/csv#error-handling
"""
```

#### CodecNotSupportedError

**Current**:
```python
"Codec 'zstd' is not supported: Required dependency 'zstandard' is not installed"
```

**Improved**:
```python
"""Codec 'zstd' is not supported: Required dependency 'zstandard' is not installed

To fix this issue:
1. Install the required dependency:
   pip install zstandard

2. Verify the installation:
   python -c 'import zstandard'

3. Retry your operation

Alternative: Use a different compression format that's already installed:
- GZip (.gz): Usually pre-installed
- BZip2 (.bz2): Usually pre-installed
- XZ (.xz): Requires lzma (usually pre-installed)

For more information, see: https://iterabledata.io/docs/compression
"""
```

#### ReadError

**Current**:
```python
"Cannot reset: stream is not seekable (e.g., stdin, network stream)"
```

**Improved**:
```python
"""Cannot reset: stream is not seekable

The stream you're trying to reset doesn't support seeking. This typically happens with:
- Standard input (stdin)
- Network streams (HTTP, FTP)
- Pipes and other non-seekable streams

To fix this issue:
1. If reading from a file, ensure the file is opened in a seekable mode
2. If reading from stdin, consider reading the data into memory first
3. If reading from a network stream, download the file first, then process it
4. Avoid calling reset() on non-seekable streams

Alternative: Read the stream once and process it without resetting

For more information, see: https://iterabledata.io/docs/getting-started/troubleshooting#reset-operation-issues
"""
```

### 2. Guidance Generation System

#### Base Guidance Generator

```python
# In iterable/exceptions.py or iterable/helpers/guidance.py

class ErrorGuidance:
    """Helper class for generating actionable error guidance."""
    
    @staticmethod
    def format_not_supported(format_id: str, reason: str | None) -> str:
        """Generate guidance for FormatNotSupportedError."""
        guidance = []
        
        # Check if it's a dependency issue
        if reason and "dependency" in reason.lower():
            dep_name = _extract_dependency_name(reason)
            if dep_name:
                guidance.append("To fix this issue:")
                guidance.append(f"1. Install the required dependency:")
                guidance.append(f"   pip install {dep_name}")
                guidance.append("")
                guidance.append("2. Verify the installation:")
                guidance.append(f"   python -c 'import {dep_name}'")
                guidance.append("")
                guidance.append("3. Retry your operation")
                guidance.append("")
                guidance.append("If you continue to have issues:")
                guidance.append("- Check that you're using a compatible Python version")
                guidance.append("- Verify your pip installation is working correctly")
                guidance.append(f"- See documentation: https://iterabledata.io/docs/formats/{format_id}")
        
        # Check if format is not implemented
        elif reason and "not implemented" in reason.lower():
            guidance.append("This format is not yet implemented.")
            guidance.append("")
            guidance.append("Options:")
            guidance.append("1. Use a different format that's supported")
            guidance.append("2. Check if there's a plugin available")
            guidance.append("3. Request this format in the issue tracker")
        
        return "\n".join(guidance) if guidance else ""
    
    @staticmethod
    def format_detection_failed(filename: str | None, reason: str | None) -> str:
        """Generate guidance for FormatDetectionError."""
        guidance = []
        guidance.append("The file format could not be determined.")
        guidance.append("")
        
        if filename:
            ext = os.path.splitext(filename)[1]
            if ext:
                guidance.append(f"File extension '{ext}' is not recognized.")
            else:
                guidance.append("File has no extension.")
        
        guidance.append("")
        guidance.append("To fix this issue:")
        guidance.append("1. Specify the format explicitly:")
        guidance.append("   open_iterable('file', iterableargs={'format': 'csv'})")
        guidance.append("")
        guidance.append("2. Rename the file with a recognized extension:")
        guidance.append("   mv file file.csv")
        guidance.append("")
        guidance.append("3. Check the file content:")
        guidance.append("   - Verify the file is not corrupted")
        guidance.append("   - Ensure the file contains valid data")
        guidance.append("   - Check file encoding (use encoding parameter if needed)")
        guidance.append("")
        guidance.append("For a list of supported formats, see: https://iterabledata.io/docs/formats/")
        
        return "\n".join(guidance)
    
    @staticmethod
    def format_parse_error(format_id: str, message: str, filename: str | None, 
                          row_number: int | None, byte_offset: int | None,
                          original_line: str | None) -> str:
        """Generate guidance for FormatParseError."""
        guidance = []
        guidance.append("This usually means:")
        
        # Analyze error message to provide specific guidance
        if "delimiter" in message.lower():
            guidance.append("- The file has inconsistent delimiters")
            guidance.append("- There's an unescaped quote or special character")
            guidance.append("- The file encoding is incorrect")
            guidance.append("")
            guidance.append("To fix this issue:")
            guidance.append("1. Check the problematic line:")
            if row_number:
                guidance.append(f"   - Open the file and examine line {row_number}")
            guidance.append("   - Look for unescaped quotes, commas, or special characters")
            guidance.append("   - Verify the delimiter matches your expectations")
            guidance.append("")
            guidance.append("2. Specify the correct delimiter:")
            guidance.append("   open_iterable('file.csv', iterableargs={'delimiter': ';'})")
            guidance.append("")
            guidance.append("3. Handle encoding issues:")
            guidance.append("   open_iterable('file.csv', iterableargs={'encoding': 'utf-8'})")
            guidance.append("")
            guidance.append("4. Use error handling to skip problematic rows:")
            guidance.append("   open_iterable('file.csv', iterableargs={'on_error': 'skip'})")
        
        elif "json" in message.lower() or "parse" in message.lower():
            guidance.append("- The JSON structure is invalid")
            guidance.append("- There's a syntax error in the JSON")
            guidance.append("- The file encoding is incorrect")
            guidance.append("")
            guidance.append("To fix this issue:")
            guidance.append("1. Validate the JSON:")
            guidance.append("   python -m json.tool file.json")
            guidance.append("")
            guidance.append("2. Check the problematic line:")
            if row_number:
                guidance.append(f"   - Examine line {row_number} in the file")
            if original_line:
                guidance.append(f"   - Problematic line: {original_line[:100]}")
            guidance.append("")
            guidance.append("3. Use error handling to skip problematic rows:")
            guidance.append("   open_iterable('file.jsonl', iterableargs={'on_error': 'skip'})")
        
        guidance.append("")
        guidance.append(f"For more help, see: https://iterabledata.io/docs/formats/{format_id}#error-handling")
        
        return "\n".join(guidance)
```

### 3. Exception Message Enhancement

#### Enhanced Exception Classes

```python
class FormatNotSupportedError(FormatError):
    def __init__(self, format_id: str, reason: str | None = None):
        message = f"Format '{format_id}' is not supported"
        if reason:
            message += f": {reason}"
        super().__init__(message, format_id=format_id, error_code="FORMAT_NOT_SUPPORTED")
        self.reason = reason
    
    def __str__(self):
        """Return enhanced error message with actionable guidance."""
        base_message = super().__str__()
        guidance = ErrorGuidance.format_not_supported(self.format_id, self.reason)
        
        if guidance:
            return f"{base_message}\n\n{guidance}"
        return base_message


class FormatDetectionError(FormatError):
    def __str__(self):
        """Return enhanced error message with actionable guidance."""
        base_message = super().__str__()
        guidance = ErrorGuidance.format_detection_failed(self.filename, self.reason)
        
        if guidance:
            return f"{base_message}\n\n{guidance}"
        return base_message


class FormatParseError(FormatError):
    def __str__(self):
        """Return enhanced error message with actionable guidance."""
        base_message = super().__str__()
        guidance = ErrorGuidance.format_parse_error(
            self.format_id,
            self.message,
            self.filename,
            self.row_number,
            self.byte_offset,
            self.original_line
        )
        
        if guidance:
            return f"{base_message}\n\n{guidance}"
        return base_message
```

### 4. Context-Aware Guidance

#### Smart Guidance Based on Context

```python
def _extract_dependency_name(reason: str) -> str | None:
    """Extract dependency name from error reason."""
    # Patterns: "Required dependency 'pyarrow'", "missing 'pandas'", etc.
    import re
    patterns = [
        r"dependency ['\"]([\w-]+)['\"]",
        r"missing ['\"]([\w-]+)['\"]",
        r"requires ['\"]([\w-]+)['\"]",
    ]
    for pattern in patterns:
        match = re.search(pattern, reason, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def _suggest_alternatives(format_id: str) -> list[str]:
    """Suggest alternative formats."""
    alternatives = {
        'parquet': ['csv', 'jsonl', 'arrow'],
        'arrow': ['parquet', 'csv', 'jsonl'],
        'orc': ['parquet', 'arrow'],
    }
    return alternatives.get(format_id, [])
```

## Usage Examples

### Enhanced Error Messages

```python
# FormatNotSupportedError with dependency issue
try:
    with open_iterable('data.parquet') as source:
        pass
except FormatNotSupportedError as e:
    print(e)
    # Output:
    # Format 'parquet' is not supported: Required dependency 'pyarrow' is not installed
    #
    # To fix this issue:
    # 1. Install the required dependency:
    #    pip install pyarrow
    #
    # 2. Verify the installation:
    #    python -c 'import pyarrow'
    #
    # 3. Retry your operation
    #
    # If you continue to have issues:
    # - Check that you're using a compatible Python version
    # - Verify your pip installation is working correctly
    # - See documentation: https://iterabledata.io/docs/formats/parquet
```

### Programmatic Access

```python
# Access guidance separately if needed
try:
    with open_iterable('data.parquet') as source:
        pass
except FormatNotSupportedError as e:
    print(f"Error: {e.message}")
    print(f"Error code: {e.error_code}")
    print(f"Format: {e.format_id}")
    print(f"Reason: {e.reason}")
    # Full message with guidance is in str(e)
```

## Testing Strategy

### Unit Tests

1. **Guidance Generation Tests**
   - Test guidance for each exception type
   - Test context-aware guidance
   - Test edge cases

2. **Message Format Tests**
   - Test message formatting
   - Test guidance inclusion
   - Test backward compatibility

### Integration Tests

1. **End-to-End Error Tests**
   - Test error messages in real scenarios
   - Verify guidance is helpful
   - Test user experience

## Migration Path

### Backward Compatibility

- **No Breaking Changes**: Enhanced messages are additive
- **Existing Code Works**: Exception handling continues to work
- **Optional Guidance**: Can be disabled if needed (future enhancement)

### Gradual Rollout

1. **Phase 1**: Add guidance to common exceptions
2. **Phase 2**: Add guidance to all exceptions
3. **Phase 3**: Refine and optimize guidance
4. **Phase 4**: Add user feedback mechanism

## Recommendations

### Immediate Implementation (Phase 1)

1. **Add guidance to common exceptions**
   - FormatNotSupportedError
   - FormatDetectionError
   - FormatParseError
   - CodecNotSupportedError

2. **Create guidance generation system**
   - ErrorGuidance helper class
   - Context-aware guidance
   - Documentation links

3. **Test thoroughly**
   - Verify guidance is helpful
   - Test backward compatibility
   - Gather user feedback

### Future Enhancements (Phase 2+)

1. **Expand guidance coverage**
   - All exception types
   - More specific guidance
   - More context-aware suggestions

2. **Add interactive help**
   - Command-line help for errors
   - Interactive troubleshooting
   - Error reporting system

3. **User feedback integration**
   - Collect feedback on guidance usefulness
   - Improve guidance based on feedback
   - A/B test different guidance formats

## Conclusion

Improving error messages with actionable guidance significantly enhances the developer experience by helping users understand and fix issues quickly. The recommended approach is to enhance exception `__str__` methods with actionable guidance while maintaining backward compatibility.

All improvements are additive and maintain existing exception handling behavior. The system provides progressive detail - brief messages for experienced users and detailed guidance for troubleshooting.
