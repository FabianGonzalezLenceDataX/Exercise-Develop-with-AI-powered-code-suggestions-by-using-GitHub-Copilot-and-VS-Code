# TestGeneratorAgent - Basic Usage

## Prompt: Generate Tests for Single File

Please generate a comprehensive test suite for `src/app.py`.

Requirements:
1. **Analyze the source code** (read-only, do not modify)
2. **Create test file** at `tests/test_app.py`
3. **Include tests for**:
   - All public functions and methods
   - Happy path scenarios
   - Edge cases (empty inputs, boundary values)
   - Error handling
   - Common use cases

4. **Run the tests** to verify they work
5. **Report any issues** found in the source code

Remember: If you find potential bugs in the source code, report them to me but **do not modify the source code**.

---

**Expected Output:**
- New test file: `tests/test_app.py`
- Test execution results
- Code coverage report (if available)
- Any potential source code issues detected
