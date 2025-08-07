import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import API from '../api';
import { 
  Product, 
  ProductCreateRequest, 
  ProductUpdateRequest, 
  ProductStatus 
} from '../api/types/product';

interface ProductContextType {
  products: Product[];
  loading: boolean;
  error: string | null;
  pagination: PaginationInfo;
  addProduct: (product: ProductCreateRequest) => Promise<Product>;
  updateProduct: (id: string, updates: ProductUpdateRequest) => Promise<Product | null>;
  deleteProduct: (id: string) => Promise<boolean>;
  refreshProducts: (filters?: ProductFilters) => Promise<void>;
  getProductById: (id: string) => Promise<Product | null>;
}

interface ProductFilters {
  status?: string[];
  search?: string;
  created_from?: string;
  created_to?: string;
  page?: number;
  limit?: number;
}

interface PaginationInfo {
  total: number;
  page: number;
  size: number;
  pages: number;
}

const ProductContext = createContext<ProductContextType | undefined>(undefined);

export function ProductProvider({ children }: { children: ReactNode }) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState<PaginationInfo>({
    total: 0,
    page: 1,
    size: 10,
    pages: 0
  });

  const refreshProducts = useCallback(async (filters?: ProductFilters) => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('[ProductContext] Refreshing products with filters:', filters);
      const page = filters?.page || 1;
      const limit = filters?.limit || 10;
      
      const response = await API.products.getAllProducts(page, limit, filters);
      console.log('[ProductContext] Products loaded:', response);
      
      setProducts(response.items || []);
      setPagination({
        total: response.total,
        page: response.page,
        size: response.size,
        pages: response.pages
      });
    } catch (err: any) {
      console.error('[ProductContext] Failed to fetch products:', err);
      
      // Distinguish between connection errors and other errors
      if (err.code === 'ECONNREFUSED' || err.code === 'ENOTFOUND' || err.message?.includes('Network Error')) {
        setError('Unable to connect to the API server. Please check if the server is running.');
      } else if (err.response?.status >= 400 && err.response?.status < 500) {
        // Client errors (400-499) - usually validation or auth issues
        setError(err.response?.data?.detail || 'Invalid request. Please check your input.');
      } else {
        // For other errors, show a generic message
        setError('Failed to load products. Please try again later.');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const addProduct = async (productData: ProductCreateRequest): Promise<Product> => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('[ProductContext] Creating product:', productData);
      const newProduct = await API.products.createProduct(productData);
      
      // Add the new product to the local state
      setProducts(prev => [newProduct, ...prev]);
      
      console.log('[ProductContext] Product created:', newProduct);
      return newProduct;
    } catch (err: any) {
      console.error('[ProductContext] Failed to create product:', err);
      
      let errorMessage = 'Failed to create product. Please try again.';
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const updateProduct = async (id: string, updates: ProductUpdateRequest): Promise<Product | null> => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('[ProductContext] Updating product:', id, updates);
      const updatedProduct = await API.products.updateProduct(id, updates);
      
      // Update the product in local state
      setProducts(prev => prev.map(product => 
        product.id.toString() === id ? updatedProduct : product
      ));
      
      console.log('[ProductContext] Product updated:', updatedProduct);
      return updatedProduct;
    } catch (err) {
      console.error('[ProductContext] Failed to update product:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to update product. Please try again.';
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const deleteProduct = async (id: string): Promise<boolean> => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('[ProductContext] Deleting product:', id);
      const success = await API.products.deleteProduct(id);
      
      if (success) {
        // Remove the product from local state
        setProducts(prev => prev.filter(product => product.id.toString() !== id));
        console.log('[ProductContext] Product deleted:', id);
      }
      
      return success;
    } catch (err) {
      console.error('[ProductContext] Failed to delete product:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete product. Please try again.';
      setError(errorMessage);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const getProductById = async (id: string): Promise<Product | null> => {
    try {
      // First check if we have it in local state
      const localProduct = products.find(p => p.id.toString() === id);
      if (localProduct) {
        return localProduct;
      }
      
      // If not found locally, fetch from API
      console.log('[ProductContext] Fetching product by ID:', id);
      const product = await API.products.getProductById(id);
      console.log('[ProductContext] Product fetched:', product);
      
      return product;
    } catch (err) {
      console.error('[ProductContext] Failed to fetch product by ID:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch product.');
      return null;
    }
  };

  return (
    <ProductContext.Provider value={{
      products,
      loading,
      error,
      pagination,
      addProduct,
      updateProduct,
      deleteProduct,
      refreshProducts,
      getProductById
    }}>
      {children}
    </ProductContext.Provider>
  );
}

export function useProducts() {
  const context = useContext(ProductContext);
  if (context === undefined) {
    throw new Error('useProducts must be used within a ProductProvider');
  }
  return context;
}

// Export types for convenience
export type { Product, ProductStatus, ProductCreateRequest, ProductUpdateRequest, ProductFilters };