import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../stores/cartStore';
import { useAuthStore } from '../stores/authStore';
import ErrorMessage from '../components/ErrorMessage';

export default function CheckoutPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const { cart, checkout, isLoading, error } = useCartStore();
  const [checkoutError, setCheckoutError] = useState<string | null>(null);
  const [checkoutSuccess, setCheckoutSuccess] = useState(false);

  if (!isAuthenticated) {
    navigate('/login');
    return null;
  }

  if (!cart || cart.items.length === 0) {
    navigate('/cart');
    return null;
  }

  const handleCheckout = async () => {
    setCheckoutError(null);
    try {
      await checkout();
      setCheckoutSuccess(true);
      setTimeout(() => {
        navigate('/');
      }, 3000);
    } catch (err: any) {
      setCheckoutError(err.error || err.errors?.join(', ') || 'Checkout failed');
    }
  };

  if (checkoutSuccess) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto text-center">
          <div className="bg-green-50 border border-green-200 text-green-700 px-6 py-8 rounded-lg">
            <div className="text-6xl mb-4">✓</div>
            <h2 className="text-2xl font-bold mb-2">Order Placed Successfully!</h2>
            <p className="mb-4">Thank you for your purchase. Redirecting to homepage...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Checkout</h1>

      {(error || checkoutError) && (
        <ErrorMessage message={checkoutError || error || ''} />
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Order Items</h2>
            <div className="space-y-4">
              {cart.items.map((item) => (
                <div key={item.id} className="flex justify-between items-center border-b pb-4">
                  <div>
                    <h3 className="font-semibold">{item.book.title}</h3>
                    <p className="text-sm text-gray-600">Quantity: {item.quantity}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">${parseFloat(item.subtotal).toFixed(2)}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
            <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
            <div className="space-y-2 mb-4">
              <div className="flex justify-between">
                <span>Subtotal</span>
                <span>${parseFloat(cart.total).toFixed(2)}</span>
              </div>
            </div>
            <div className="border-t pt-4 mb-4">
              <div className="flex justify-between text-xl font-bold">
                <span>Total</span>
                <span>${parseFloat(cart.total).toFixed(2)}</span>
              </div>
            </div>
            <button
              onClick={handleCheckout}
              disabled={isLoading}
              className="btn-primary w-full"
            >
              {isLoading ? 'Processing...' : 'Complete Purchase'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

