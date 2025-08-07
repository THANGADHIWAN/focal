/**
 * Utility functions for transforming data between frontend and backend formats
 */

/**
 * Transforms snake_case keys to camelCase
 */
export function snakeToCamel<T = any>(obj: any): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => snakeToCamel(item)) as any;
  }

  return Object.keys(obj).reduce((acc, key) => {
    const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
    acc[camelKey] = snakeToCamel(obj[key]);
    return acc;
  }, {} as Record<string, any>) as T;
}

/**
 * Transforms camelCase keys to snake_case
 */
export function camelToSnake<T = any>(obj: any): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => camelToSnake(item)) as any;
  }

  return Object.keys(obj).reduce((acc, key) => {
    const snakeKey = key.replace(/([A-Z])/g, "_$1").toLowerCase();
    acc[snakeKey] = camelToSnake(obj[key]);
    return acc;
  }, {} as Record<string, any>) as T;
}

/**
 * Transforms enum values to uppercase with underscores
 */
export function normalizeEnumValue(value: string): string {
  return value.toUpperCase().replace(/ /g, '_');
}

/**
 * Transforms uppercase enum values to display format
 */
export function formatEnumValue(value: string): string {
  return value
    .toLowerCase()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
}
