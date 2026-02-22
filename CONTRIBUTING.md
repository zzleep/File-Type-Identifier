# Contributing

Thanks for your interest in contributing!

## How to Contribute

### Reporting Bugs

Open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your Python version and OS

### Adding File Signatures

To support new file types:

1. Find the magic number (file signature in hex)
2. Add to `src/filemagic/database.py`:
   ```python
   MagicNumber(
       signature=bytes.fromhex('YOUR_HEX'),
       offset=0,
       extension='ext',
       description='File Type',
       mime_type='type/subtype'
   )
   ```
3. Test with sample files
4. Submit a pull request

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Code Style

- Follow PEP 8
- Add docstrings for functions
- Use type hints where appropriate
- Keep functions focused and small

## Questions?

Feel free to open an issue for discussion.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
