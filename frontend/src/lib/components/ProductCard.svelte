<script lang="ts">
  export let product: Product;
</script>

<a href={`/products/${product.id}`} class="product-card" rel="prefetch">
  <div class="product-image-wrapper">
    <img class="product-image" src={product.image_url} alt={product.name} />
  </div>
  <div class="product-details">
    <h2>{product.name}</h2>
    <p class="description">
      {product.description.length > 120 ? `${product.description.substring(0, 117)}...` : product.description}
    </p>
    <p class="price">¥ {product.price.toLocaleString()}</p>
    <p class="author">Author: {product.author}</p>
    <slot />
  </div>
</a>

<style>
  .product-card {
    height: 330px;
    display: flex;
    border: none;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 16px;
    border-radius: 8px;
    width: 100%;
    transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
    text-decoration: none; /* アンダーラインを除去 */
    color: inherit; /* テキストの色を維持 */
  }

  .product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
    background-color: rgba(155, 77, 202, 0.1);
  }

  h2 {
    font-size: 1.5em;
    color: #9b4dca;
  }

  .product-image-wrapper {
    flex: 0 0 20%;
    overflow: hidden;
    position: relative;
  }

  .product-image {
    width: 100%;
    object-fit: contain;
    object-position: center;
    vertical-align: bottom;
  }

  .product-details {
    flex: 1;
    padding-left: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .description {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .price {
    font-weight: bold;
    margin-top: 8px;
  }

  .author {
    color: #888;
    margin-top: 8px;
  }
</style>
