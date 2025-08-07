import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Plus, 
  Search, 
  Filter, 
  FlaskRound as Flask, 
  Beaker, 
  TestTube2,
  AlertCircle, 
  Loader2, 
  X, 
  ChevronLeft, 
  ChevronRight 
} from 'lucide-react';
import { useProducts, ProductStatus } from '../../context/ProductContext';
import type { ProductFilters } from '../../api/types/filters';
import type { Product } from '../../api/types';
import toast, { Toaster } from 'react-hot-toast';
import EditProductModal from './modals/EditProductModal';
import NewProductModal from './modals/NewProductModal';
import CardDropdownMenu from '../ui/CardDropdownMenu';
import { debounce } from 'lodash';

interface FilterState {
  status: ProductStatus[];
  search: string;
  created_from?: string;
  created_to?: string;
  page?: number;
  limit?: number;
}

export default function ProductList() {
  const navigate = useNavigate();
  const { products, loading, error, pagination, refreshProducts, deleteProduct } = useProducts();
  const [showNewModal, setShowNewModal] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterState>({
    status: [],
    search: '',
    created_from: undefined,
    created_to: undefined
  });
  

  // Load products on component mount
  useEffect(() => {
    refreshProducts();
  }, [refreshProducts]);

  // Debounced search handler
  const debouncedSearch = useCallback(
    debounce((searchTerm: string) => {
      handleFilterChange(1, { ...filters, search: searchTerm });
    }, 300),
    [filters]
  );

  const handleDeleteProduct = async (productId: string) => {
    setDeleting(productId);
    try {
      const success = await deleteProduct(productId);
      if (success) {
        toast.success('Product deleted successfully');
        // Product removed from state automatically
      }
    } catch (error) {
      console.error('Failed to delete product:', error);
    } finally {
      setDeleting(null);
    }
  };

  const handleFilterChange = (page = 1, overrideFilters?: Partial<FilterState>) => {
    // Apply filters by calling refreshProducts with filter parameters
    const filterParams = {
      ...filters,
      ...overrideFilters,
      status: overrideFilters?.status || (filters.status.length > 0 ? filters.status : undefined),
      search: overrideFilters?.search || filters.search || undefined,
      created_from: overrideFilters?.created_from || filters.created_from,
      created_to: overrideFilters?.created_to || filters.created_to,
      page,
      limit: 10
    };
    refreshProducts(filterParams);
  };

  const getStatusColor = (status: ProductStatus) => {
    switch (status) {
      case 'NOT_STARTED':
        return 'bg-gray-100 text-gray-800';
      case 'IN_PROGRESS':
        return 'bg-blue-100 text-blue-800';
      case 'COMPLETED':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-6">
      <Toaster position="top-right" />

      {/* Edit Product Modal */}
      {showEditModal && selectedProduct && (
        <EditProductModal
          isOpen={showEditModal}
          onClose={() => {
            setShowEditModal(false);
            setSelectedProduct(null);
          }}
          product={selectedProduct}
        />
      )}

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Products</h1>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowFilters(true)}
            className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            <Filter className="w-4 h-4 mr-2" />
            Filters
            {filters.status.length > 0 && (
              <span className="ml-2 px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full text-xs">
                {filters.status.length}
              </span>
            )}
          </button>
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={filters.search}
              onChange={(e) => {
                const value = e.target.value;
                setFilters(prev => ({ ...prev, search: value }));
                debouncedSearch(value);
              }}
              placeholder="Search products..."
              className="pl-9 pr-4 py-2 w-[300px] text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={() => setShowNewModal(true)}
            className="flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Product
          </button>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
            <p className="text-red-600">{error}</p>
            <button
              onClick={() => refreshProducts()}
              className="ml-auto text-red-600 hover:text-red-700 text-sm font-medium"
            >
              Try Again
            </button>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && products.length === 0 && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-blue-600 animate-spin mr-3" />
          <p className="text-gray-600">Loading products...</p>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && products.length === 0 && (
        <div className="text-center py-12">
          <Flask className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No products found</h3>
          <p className="text-gray-500 mb-4">You haven't created any products yet. Get started by creating your first product.</p>
          <button
            onClick={() => setShowNewModal(true)}
            className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create Product
          </button>
        </div>
      )}

      {/* Product Grid with Pagination */}
      {!loading && !error && products.length > 0 && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
            <div
              key={product.id}
              className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer relative"
              onClick={() => navigate(`/products/${product.id}`)}
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <h2 className="text-lg font-bold text-gray-800">{product.product_name.toUpperCase()}</h2>
                        <p className="text-xs text-gray-400 mt-1">{product.description || 'No description'}</p>
                      </div>
                      <div className="flex items-center space-x-2 shrink-0">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(product.status)}`}>
                          {product.status.replace('_', ' ').toLowerCase()}
                        </span>
                        <CardDropdownMenu
                          onDelete={() => handleDeleteProduct(product.id.toString())}
                          onEdit={() => {
                            setSelectedProduct(product);
                            setShowEditModal(true);
                          }}
                          itemName={product.name}
                          isDeleting={deleting === product.id.toString()}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="flex flex-col items-center p-3 bg-gray-50 rounded-lg">
                    <TestTube2 className="w-5 h-5 text-blue-600 mb-1" />
                    <span className="text-sm font-medium text-gray-900">{product.sample_count || 0}</span>
                    <span className="text-xs text-gray-500">Samples</span>
                  </div>
                  <div className="flex flex-col items-center p-3 bg-gray-50 rounded-lg">
                    <Beaker className="w-5 h-5 text-blue-600 mb-1" />
                    <span className="text-sm font-medium text-gray-900">{product.test_count || 0}</span>
                    <span className="text-xs text-gray-500">Tests</span>
                  </div>
                  <div className="flex flex-col items-center p-3 bg-gray-50 rounded-lg">
                    <Flask className="w-5 h-5 text-blue-600 mb-1" />
                    <span className="text-sm font-medium text-gray-900">0</span>
                    <span className="text-xs text-gray-500">Completed</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>Created {new Date(product.created_at).toLocaleDateString()}</span>
                    <span>Updated {new Date(product.updated_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
          </div>
          
          {/* Pagination Controls */}
          {pagination && pagination.pages > 1 && (
            <div className="flex items-center justify-center space-x-2">
              <button
                onClick={() => handleFilterChange(pagination.page - 1)}
                disabled={pagination.page === 1}
                className="p-2 rounded-lg border border-gray-300 disabled:opacity-50"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <div className="text-sm text-gray-700">
                Page {pagination.page} of {pagination.pages}
              </div>
              <button
                onClick={() => handleFilterChange(pagination.page + 1)}
                disabled={pagination.page === pagination.pages}
                className="p-2 rounded-lg border border-gray-300 disabled:opacity-50"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          )}
        </div>
      )}

      {/* No Results */}
      {!loading && !error && products.length === 0 && (
        <div className="text-center py-12">
          <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No products found</h3>
          <p className="text-gray-500 mb-4">Try adjusting your search or filter criteria.</p>
          <button
            onClick={() => {
              setFilters({ status: [], search: '' });
              refreshProducts();
            }}
            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            Clear filters
          </button>
        </div>
      )}

      {/* New Product Modal */}
      <NewProductModal
        isOpen={showNewModal}
        onClose={() => setShowNewModal(false)}
      />

      {/* Filters Modal */}
      {showFilters && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-20 z-50">
          <div className="bg-white rounded-lg shadow-xl w-[400px]">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Filter Products</h2>
              <button
                onClick={() => setShowFilters(false)}
                className="text-gray-400 hover:text-gray-500"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6">
              <h3 className="text-sm font-medium text-gray-900 mb-4">Status</h3>
              <div className="space-y-3">
                {(['NOT_STARTED', 'IN_PROGRESS', 'COMPLETED'] as ProductStatus[]).map(status => (
                  <label key={status} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={filters.status.includes(status)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setFilters(prev => ({
                            ...prev,
                            status: [...prev.status, status]
                          }));
                        } else {
                          setFilters(prev => ({
                            ...prev,
                            status: prev.status.filter(s => s !== status)
                          }));
                        }
                      }}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="ml-2 text-sm text-gray-600">
                      {status.replace('_', ' ')}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            <div className="flex justify-end px-6 py-4 bg-gray-50 border-t border-gray-200">
              <button
                onClick={() => {
                  setFilters({ status: [], search: '' });
                  setShowFilters(false);
                  refreshProducts({ page: 1, limit: 10 });
                  toast.success('Filters reset successfully');
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-500 mr-3"
              >
                Reset
              </button>
              <button
                onClick={() => {
                  handleFilterChange(1);
                  setShowFilters(false);
                }}
                className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}