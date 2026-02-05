/**
 * Jest test setup file
 * Configures testing environment for DOM-based tests
 */

// Import jest-dom matchers for better assertions
require('@testing-library/jest-dom');

// Mock fetch globally for all tests
global.fetch = jest.fn();

// Mock console.error to avoid cluttering test output with expected errors
const originalError = console.error;
beforeAll(() => {
  console.error = jest.fn();
});

afterAll(() => {
  console.error = originalError;
});

// Reset all mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});
