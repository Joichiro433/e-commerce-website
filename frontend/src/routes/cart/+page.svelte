<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Api from '$lib/api/index.js';
  import { getCartTotalQuantity } from '$lib/stores/cartStatus';
  import ProductCard from '$lib/components/ProductCard.svelte';
  import Modal from '$lib/components/Modal.svelte';
  import logger from '$lib/logger';

  let cartItems: CartProducts = {};
  let products: Product[] = [];
  let totalAmount = 0;
  let isModalVisible: boolean = false;

  const fetchCartProducts = async (): Promise<void> => {
    try {
      const response = await Api.get<CartProducts>('/cart');
      cartItems = response.data;
      products = await Promise.all(
        Object.keys(cartItems).map(async (id) => (await Api.get<Product>(`/products/${id}`)).data)
      );
      totalAmount = products.reduce((total, product) => total + product.price * cartItems[product.id], 0);
    } catch (e) {
      logger.error('Failed to fetchCartProducts:', e);
    }
  };

  const handleQuantityChange = async (productId: string, event: Event): Promise<void> => {
    const selectElement = event.target as HTMLSelectElement;
    const quantity = parseInt(selectElement.value, 10);
    try {
      await Api.put('/cart', { product_id: productId, quantity });
      getCartTotalQuantity();
      fetchCartProducts();
    } catch (e) {
      logger.error('Failed to handleQuantityChange:', e);
      alert('エラーが発生しました。ページをリロードしてもう一度お試しください。');
    }
  };

  const placeOrder = async (): Promise<void> => {
    const orderData = Object.keys(cartItems).map((id) => ({ product_id: id, quantity: cartItems[id] }));
    try {
      await Api.post('/orders', orderData);
      await Api.delete('/cart');
      getCartTotalQuantity();
      isModalVisible = true;
    } catch (e) {
      logger.error('Failed to placeOrder:', e);
      alert('エラーが発生しました。ページをリロードしてもう一度お試しください。');
    }
  };

  const closeModal = (): void => {
    isModalVisible = false;
    goto('/');
  };

  onMount(fetchCartProducts);
</script>

<div>
  <h1>Your Shopping Cart</h1>
  {#if !products.length}
    <p>Your cart is empty.</p>
  {:else}
    {#if isModalVisible}
      <Modal {closeModal}>
        <h3>注文を確定しました！</h3>
      </Modal>
    {/if}

    <div class="products">
      {#each products as product (product.id)}
        <ProductCard {product}>
          <select
            style="width: 100px;"
            bind:value={cartItems[product.id]}
            on:change={(event) => handleQuantityChange(product.id, event)}
            on:click|preventDefault
          >
            {#each Array(10).fill(null) as _, i}
              <option value={i}>{i === 0 ? `数量: 0 (削除)` : `数量: ${i}`}</option>
            {/each}
          </select>
        </ProductCard>
      {/each}
    </div>
    <div class="checkout">
      <p class="total-amount">合計: ¥ {totalAmount.toLocaleString()}</p>
      <button on:click|preventDefault={placeOrder}>注文を確定する</button>
    </div>
  {/if}
</div>

<style>
  .products {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .checkout {
    position: fixed;
    right: 24px;
    bottom: 24px;
    background-color: white;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    z-index: 1000;
  }

  .total-amount {
    font-size: 1.2em;
    margin-bottom: 12px;
  }
</style>
