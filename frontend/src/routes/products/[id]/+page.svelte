<script lang="ts">
  import Api from '$lib/api/index.js';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { getCartTotalQuantity } from '$lib/stores/cartStatus';
  import Modal from '$lib/components/Modal.svelte';
  import logger from '$lib/logger';

  // Variables
  let productId: string;
  let product: Product;
  let isModalVisible: boolean = false;
  let itemsToShow = 4;
  let currentIndex = 0;
  let quantity = 1;
  let recommendedProducts: Product[] = [];
  let displayedProducts: Product[] = [];

  // Fetch product and recommendations when the page parameter changes
  $: if ($page.params.id !== productId) {
    productId = $page.params.id;
    fetchProductAndRecommendations();
  }

  // Fetch the product and its recommendations
  const fetchProductAndRecommendations = async () => {
    await fetchProduct();
    await fetchRecommendedProducts();
  };

  // Fetch single product
  const fetchProduct = async () => {
    try {
      const resp = await Api.get<Product>(`/products/${productId}`);
      product = resp.data;
    } catch (e) {
      logger.error(e, 'Failed to fetchProduct');
    }
  };

  // Fetch recommended products
  const fetchRecommendedProducts = async () => {
    try {
      const params = { query: product.name };
      const resp = await Api.get<Product[]>('/products', { params });
      recommendedProducts = resp.data;
      updateDisplayedProducts();
    } catch (e) {
      logger.error(e, 'Failed to getRecommendedProducts');
    }
  };

  // Handle cart actions
  const handleCart = async () => {
    const data = { product_id: productId, quantity: quantity };
    try {
      await Api.post('/cart', data);
      await getCartTotalQuantity();
      isModalVisible = true;
    } catch (e) {
      if (Api.verifyAxiosError(e) && e.response?.status === 401) {
        goto('/login');
      } else {
        logger.error(e, 'Failed to handleCart');
        alert('エラーが発生しました。ページをリロードしてもう一度お試しください。');
      }
    }
  };

  // Update displayed products
  const updateDisplayedProducts = () => {
    displayedProducts = recommendedProducts.slice(currentIndex, currentIndex + itemsToShow);
  };

  // Navigate to next products
  const nextProducts = () => {
    if (currentIndex + itemsToShow < recommendedProducts.length) {
      currentIndex += itemsToShow;
      updateDisplayedProducts();
    }
  };

  // Navigate to previous products
  const prevProducts = () => {
    if (currentIndex - itemsToShow >= 0) {
      currentIndex -= itemsToShow;
      updateDisplayedProducts();
    }
  };
</script>

<div class="product-detail">
  {#if product}
    <img src={product.image_url} alt={product.name} class="product-image" />
    <div class="product-info">
      <h2>{product.name}</h2>
      <p class="author">Author: {product.author}</p>
      <div class="price-and-cart">
        <p class="price">￥{product.price.toLocaleString()}</p>

        <select class="selector" bind:value={quantity}>
          {#each Array(9).fill(null) as _, i}
            <option value={i + 1}>数量: {i + 1}</option>
          {/each}
        </select>

        <button class="add-to-cart" on:click={handleCart}>
          <i class="fa-solid fa-cart-shopping" /> Add To Cart
        </button>
      </div>
      <p class="description">{product.description}</p>
    </div>
  {:else}
    <p>Loading product...</p>
  {/if}
</div>

{#if isModalVisible}
  <Modal closeModal={() => (isModalVisible = false)}>
    <h3>Product Added to Cart!</h3>
  </Modal>
{/if}

{#if recommendedProducts.length > 0}
  <h3>おすすめの商品</h3>
  <div class="carousel">
    <button class="arrow" on:click={prevProducts} disabled={currentIndex === 0}>◀︎</button>
    <div class="slider-content">
      {#each displayedProducts as product}
        <div
          class="recommended-product-card"
          on:click={() => goto(`/products/${product.id}`)}
          on:keydown={(e) => e.key === 'Enter' && goto(`/products/${product.id}`)}
          role="link"
          tabindex="0"
          aria-label={`View details of ${product.name}`}
        >
          <img src={product.image_url} alt={product.name} />
          <div class="recommended-product-info">
            <p style="font-size: 13px;">{product.name}</p>
          </div>
        </div>
      {/each}
    </div>
    <button class="arrow" on:click={nextProducts} disabled={currentIndex + itemsToShow >= recommendedProducts.length}
      >▶︎</button
    >
  </div>
{/if}

<style>
  /* Product Detail */
  .product-detail {
    display: flex;
    gap: 24px;
    align-items: flex-start;
    height: 80vh;
    justify-content: center;
    margin-top: 5vh;
  }

  .product-image {
    flex: 1;
    object-fit: contain;
    border-radius: 8px;
    height: 600px;
  }

  .product-info {
    flex: 2;
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-height: 70vh;
    overflow-y: auto;
  }

  /* Price and Cart */
  .price-and-cart {
    display: flex;
    align-items: center;
    gap: 30px;
  }

  .price {
    font-weight: bold;
    font-size: 25px;
    color: #ff0084;
    margin: 0;
  }

  .add-to-cart {
    margin: 0;
  }

  .selector {
    width: 100px;
    margin: 0;
  }

  /* Carousel */
  .carousel {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
    margin-bottom: 80px;
  }

  .arrow {
    width: 40px;
    height: 40px;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: transparent;
    border: none;
    color: grey;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .arrow:disabled {
    color: lightgrey;
    box-shadow: none;
  }

  /* Slider Content */
  .slider-content {
    display: flex; /* カードを横並びに */
    gap: 20px; /* カードの間隔 */
  }

  /* Recommended Product Card */
  .recommended-product-card {
    width: 200px;
    height: 280px; /* カードの高さを固定 */
    display: flex;
    flex-direction: column; /* 子要素を縦方向に並べる */
    align-items: center; /* 子要素を中央に配置 */
    border: none;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s ease-in-out;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    margin: 0 10px;
  }

  .recommended-product-card img {
    width: 60%;
    height: auto;
    max-height: 200px; /* 画像の最大高さを設定 */
    object-fit: cover; /* 画像をカバーするように設定 */
    transition: transform 0.3s ease-in-out;
  }

  .recommended-product-info {
    padding: 10px;
    background-color: #fff;
    text-align: center;
    width: 100%; /* テキストエリアの幅を最大に */
    flex-grow: 1; /* 残りの空間を埋める */
    display: flex;
    flex-direction: column;
    justify-content: center; /* テキストを中央に配置 */
  }

  .recommended-product-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  }
</style>
