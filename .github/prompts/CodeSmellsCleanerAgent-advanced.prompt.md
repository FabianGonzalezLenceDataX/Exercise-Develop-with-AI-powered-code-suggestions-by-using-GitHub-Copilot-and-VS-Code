# CodeSmellsCleanerAgent - Advanced Usage

## Prompt: Clean All Code Smells in Project

Please perform a comprehensive code quality review and refactoring:

1. **Analyze all files** in `src/` directory
   - Identify all code smells
   - Prioritize by severity and impact

2. **Run tests before changes**
   - Execute existing test suite
   - Document current test status

3. **Apply refactorings systematically**:
   - Start with low-risk changes (dead code, naming)
   - Move to medium-risk (extract methods, simplify conditionals)
   - Apply high-risk changes only with explicit confirmation
   
4. **Verify after each major change**:
   - Run tests after each refactoring
   - Ensure no functionality is broken

5. **Generate final report**:
   - Summary of all changes made
   - Before/after metrics
   - Test results
   - Any remaining issues

---

**Expected Output:**
- Refactored source files
- Test execution results
- Comprehensive refactoring report
- Improved code quality metrics
