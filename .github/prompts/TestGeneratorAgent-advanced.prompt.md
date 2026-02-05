# TestGeneratorAgent - Advanced Usage

## Prompt: Generate Complete Test Suite for Project

Please create a comprehensive test suite for the entire project:

1. **Analyze all source files** in `src/` directory
   - Identify all testable functions, classes, and methods
   - Map dependencies between modules

2. **Generate test files** for each source file:
   - Unit tests for individual functions
   - Integration tests for module interactions
   - Edge case tests for boundary conditions
   - Error handling tests

3. **Configure test framework**:
   - Set up test runner configuration
   - Configure coverage reporting
   - Add test scripts to package.json (if needed)

4. **Execute full test suite**:
   - Run all tests
   - Generate coverage report
   - Identify any failing tests

5. **Report findings**:
   - **Source code issues detected** (DO NOT FIX - report only)
   - Test coverage metrics
   - Recommendations for improving testability
   - List of tests awaiting user decisions on ambiguous behavior

6. **Handle detected issues**:
   - For each potential bug, ask for user decision:
     - Should the source code be fixed? (User must fix manually)
     - Is this intentional behavior? (Update tests to match)
     - Should this scenario be ignored? (Remove related tests)

---

**Expected Output:**
- Complete test suite in `tests/` directory
- Test execution results with coverage report
- Detailed analysis report of source code issues
- Recommendations for next steps
- Test files ready to maintain as code evolves
