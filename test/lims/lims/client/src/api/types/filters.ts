export interface PaginationParams {
  page: number;
  limit: number;
}

export interface ProductFilters extends PaginationParams {
  status?: string[];
  search?: string;
  created_from?: string;
  created_to?: string;
}
