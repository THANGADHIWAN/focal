import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, FlaskRound } from 'lucide-react';
import { useProducts } from '../../context/ProductContext';
import App from '../../App';

export default function ProductDetails() {
  const { productId } = useParams();
  const navigate = useNavigate();
  const { products, getProductById, loading } = useProducts();
  const [product, setProduct] = React.useState(null);
  const [productLoading, setProductLoading] = React.useState(true);

  // Load specific product
  React.useEffect(() => {
    const loadProduct = async () => {
      if (!productId) return;
      
      setProductLoading(true);
      
      // First try to find in existing products
      const existingProduct = products.find(p => p.id.toString() === productId);
      if (existingProduct) {
        setProduct(existingProduct);
        setProductLoading(false);
        return;
      }
      
      // If not found, fetch from API
      try {
        const fetchedProduct = await getProductById(productId);
        setProduct(fetchedProduct);
      } catch (error) {
        console.error('Failed to load product:', error);
        setProduct(null);
      } finally {
        setProductLoading(false);
      }
    };

    loadProduct();
  }, [productId, products, getProductById]);
  
  // Show loading state while product is being fetched
  if (productLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  // Show error if product not found after loading
  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Product Not Found</h2>
          <p className="text-gray-600 mb-4">The product you're looking for doesn't exist.</p>
          <button
            onClick={() => navigate('/products')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Products
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-30 px-4">
        <div className="h-full flex items-center justify-between">
          <div className="flex items-center">
          <button
            onClick={() => navigate('/products')}
            className="mr-4 text-gray-500 hover:text-gray-700"
          >
            <ArrowLeft className="w-6 h-6" />
          </button>
            <div>
              <h1 className="text-xl font-semibold text-gray-800">{product.name}</h1>
              <p className="text-sm text-gray-500">{product.id}</p>
            </div>
          </div>
          <div className="flex items-center">
            <div className="flex items-center mr-8">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white mr-2">
                <FlaskRound className="w-5 h-5" />
              </div>
              <span className="text-lg font-semibold text-gray-900">LabFlow</span>
            </div>
            <img
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?fit=facearea&facepad=2&w=256&h=256&q=80"
              alt="Profile"
              className="w-8 h-8 rounded-full"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div>
        <App productId={productId} />
      </div>
    </div>
  );
}